"""User-local Mac installer. Never replace an existing SQLite database.

The payload is copied to ~/Applications/JamieClientSelector, outside iCloud
Desktop/Documents. A small app launcher is compiled locally with osacompile.
"""
from __future__ import annotations
from contextlib import closing
from pathlib import Path
from datetime import datetime
import json
import os
import shlex
import shutil
import sqlite3
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
DEST = Path.home() / 'Applications' / 'JamieClientSelector'
LAUNCHER = Path.home() / 'Applications' / 'Client Selector.app'
MARKER_NAME = '.install-marker.json'
OWNER = 'jamie-client-selector-mac-1'
TABLES = ('applications', 'settings', 'decisions', 'decision_history', 'assessments')


def validate_database(path: Path) -> dict:
    with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as connection:
        if connection.execute('PRAGMA quick_check').fetchone() != ('ok',):
            raise RuntimeError('Database integrity check failed: ' + str(path))
        if connection.execute('PRAGMA foreign_key_check').fetchone() is not None:
            raise RuntimeError('Database contains an invalid linked record: ' + str(path))
        return {table: connection.execute('SELECT COUNT(*) FROM ' + table).fetchone()[0] for table in TABLES}


def read_marker(dest: Path) -> dict:
    try:
        obj = json.loads((dest / MARKER_NAME).read_text(encoding='utf-8'))
        return obj if isinstance(obj, dict) else {}
    except (OSError, ValueError):
        return {}


def install_files(source: Path, dest: Path) -> tuple[dict, dict]:
    """Install code safely; testable separately from Mac-only launcher actions."""
    source, dest = source.resolve(), dest.absolute()
    if dest.is_symlink():
        raise RuntimeError('Install destination is a symbolic link. No files were changed.')
    marker = read_marker(dest)
    if dest.exists() and any(dest.iterdir()) and marker.get('owner') != OWNER:
        raise RuntimeError('The install folder already contains unrelated files. Nothing was overwritten: ' + str(dest))
    for name in ('app.py', 'client_selector_manager.py', 'index.html', 'admin_console.html', '_mac_run.sh'):
        if not (source / name).is_file():
            raise RuntimeError('Incomplete installer; missing ' + name)
    for name in ('app.py', 'client_selector_manager.py', 'install_mac.py'):
        compile((source / name).read_text(encoding='utf-8'), name, 'exec')
    db = dest / 'jamie_data.sqlite3'
    source_db = source / 'jamie_data.sqlite3'
    # Validate before stopping or copying anything. No reset/reseed on error.
    if db.exists():
        counts = validate_database(db)
    elif source_db.exists():
        counts = validate_database(source_db)
    else:
        raise RuntimeError('Migration database is missing. This installer will not substitute demonstration data.')
    if dest != source and (dest / 'client_selector_manager.py').is_file():
        subprocess.run([sys.executable, str(dest / 'client_selector_manager.py'), 'stop'], check=True)
        subprocess.run([sys.executable, str(dest / 'client_selector_manager.py'), 'backup'], check=True)
    dest.mkdir(parents=True, exist_ok=True, mode=0o700)
    dest.chmod(0o700)
    # Runtime code and documentation only. Never copy virtualenvs, credentials,
    # Git metadata, exports, bytecode, backups, or runtime state.
    skipped = {MARKER_NAME, '.python-path', 'jamie_data.sqlite3', '.env', '.git', '__pycache__', '.venv', 'venv'}
    if dest != source:
        for path in source.iterdir():
            if path.name in skipped or not path.is_file():
                continue
            if path.suffix not in ('.py', '.html', '.sh', '.command', '.md', '.json') and path.name != '.gitignore':
                continue
            temporary = dest / ('.' + path.name + '.installtmp')
            try:
                shutil.copyfile(path, temporary)
                temporary.chmod(0o700 if path.suffix in ('.command', '.sh') else 0o600)
                temporary.replace(dest / path.name)
            finally:
                temporary.unlink(missing_ok=True)
    if not db.exists():
        # O_EXCL refuses even a concurrently created destination. The existing
        # Mac database is NEVER replaced by the bundled Windows snapshot.
        descriptor = os.open(db, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(descriptor, 'wb') as target, source_db.open('rb') as incoming:
                shutil.copyfileobj(incoming, target)
            validate_database(db)
        except Exception:
            db.unlink(missing_ok=True)
            raise
        print('Copied the supplied Windows database. No schema change was made.')
    else:
        print('Kept the existing Mac database; did not replace it with the bundled snapshot.')
    (dest / '.python-path').write_text(sys.executable + '\n', encoding='utf-8')
    (dest / '.python-path').chmod(0o600)
    new_marker = {'owner': OWNER, 'installed_at': datetime.now().isoformat(), 'launcher_created': marker.get('launcher_created', False)}
    (dest / MARKER_NAME).write_text(json.dumps(new_marker, indent=2) + '\n', encoding='utf-8')
    return validate_database(db), marker


def applescript_literal(text: str) -> str:
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'


def create_launcher(dest: Path, app: Path, allow_replace: bool) -> None:
    if app.exists() and not allow_replace:
        raise RuntimeError('An app already exists at ' + str(app) + '. It was not overwritten.')
    command = shlex.join(['/bin/bash', str(dest / '_mac_run.sh'), 'start'])
    script = '''on run
    try
        do shell script COMMAND
    on error errorMessage number errorNumber
        display dialog ("Client Selector could not start.\\n\\n" & errorMessage) with title "Client Selector" buttons {"OK"} default button "OK" with icon caution
    end try
end run
'''.replace('COMMAND', applescript_literal(command))
    app.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.client-selector-launcher-', dir=app.parent) as temporary:
        compiled = Path(temporary) / 'Client Selector.app'
        # Compile locally instead of shipping an unsigned prebuilt binary.
        result = subprocess.run(['/usr/bin/osacompile', '-o', str(compiled), '-'], input=script, text=True, capture_output=True, timeout=60)
        if result.returncode:
            raise RuntimeError('Could not create the optional app icon: ' + result.stderr.strip())
        previous = Path(temporary) / 'previous.app'
        if app.exists():
            app.rename(previous)
        try:
            compiled.rename(app)
        except Exception:
            if previous.exists():
                previous.rename(app)
            raise
    marker = read_marker(dest)
    marker['launcher_created'] = True
    (dest / MARKER_NAME).write_text(json.dumps(marker, indent=2) + '\n', encoding='utf-8')


def main() -> None:
    if sys.platform != 'darwin':
        raise RuntimeError('Run this installer on the Mac mini, not the Windows laptop.')
    if sys.version_info < (3, 11):
        raise RuntimeError('Python 3.11 or newer is required; Python 3.13 is the tested series.')
    print('\nCLIENT SELECTOR - MAC SETUP\n')
    counts, old_marker = install_files(ROOT, DEST)
    print('Installed code:', DEST)
    print('Saved applications:', counts['applications'])
    print('Current decisions:', counts['decisions'])
    launcher_ok = False
    try:
        create_launcher(DEST, LAUNCHER, bool(old_marker.get('launcher_created')))
        launcher_ok = True
        print('App launcher:', LAUNCHER)
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print('NOTE:', exc)
        print('Use START Client Selector.command in the installed folder instead.')
    subprocess.run([sys.executable, str(DEST / 'client_selector_manager.py'), 'start'], check=True)
    reveal = LAUNCHER if launcher_ok else DEST / 'START Client Selector.command'
    subprocess.run(['/usr/bin/open', '-R', str(reveal)], check=False)
    print('\nREADY: http://127.0.0.1:8510')
    print('For daily use, double-click Client Selector.app; drag it into the Dock for easy access.')
    print('Backups and optional start-at-sign-in are on the website Administration page.')
    print('You may close this Terminal window. Keep the Windows copy until you have checked the Mac data.')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, sqlite3.Error, subprocess.SubprocessError) as exc:
        print('\nSETUP DID NOT COMPLETE:', exc, file=sys.stderr)
        print('The supplied Windows ZIP has not been changed. Keep it as your backup.', file=sys.stderr)
        raise SystemExit(1)
