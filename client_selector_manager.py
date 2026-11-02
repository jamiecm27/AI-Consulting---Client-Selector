"""Client Selector v2.0 - Mac edition 1, standard-library local launcher.

No public listening address, background updater, package downloads or telemetry.
The optional assessment in app.py is the only application cloud feature.
"""
from __future__ import annotations

from contextlib import closing, contextmanager
from datetime import datetime
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import fcntl
import hmac
import importlib.util
import json
import os
import platform
import plistlib
import secrets
import signal
import socket
import sqlite3
import subprocess
import sys
import threading
import time
import webbrowser

ROOT = Path(__file__).resolve().parent
APP = ROOT / 'app.py'
HTML = ROOT / 'index.html'
ADMIN_HTML = ROOT / 'admin_console.html'
DB = ROOT / 'jamie_data.sqlite3'
HOST, PORT = '127.0.0.1', 8510
URL = f'http://{HOST}:{PORT}'
SERVICE_ID = 'jamie-client-selector-mac-1'
DATA_DIR = Path.home() / 'Library' / 'Application Support' / 'JamieClientSelector'
BACKUP_DIR = DATA_DIR / 'Backups'
STATE_FILE = DATA_DIR / 'managed_server.json'
LOG_FILE = DATA_DIR / 'server.log'
LABEL = 'uk.jamie.clientselector'
STARTUP_FILE = Path.home() / 'Library' / 'LaunchAgents' / (LABEL + '.plist')
CONTROL = '/__client_selector_control/shutdown'
ALLOWED_HOSTS = {f'127.0.0.1:{PORT}', f'localhost:{PORT}'}
ALLOWED_ORIGINS = {'http://' + host for host in ALLOWED_HOSTS}


def ensure_files() -> None:
    missing = [p.name for p in (APP, HTML, ADMIN_HTML) if not p.is_file()]
    if (ROOT / '.install-marker.json').exists() and not DB.is_file():
        raise RuntimeError('The installed database is missing. Restore a backup; no demonstration database was created.')
    if missing:
        raise RuntimeError('Missing files: ' + ', '.join(missing) + '. Re-run the Mac installer; keep the database.')


def make_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    DATA_DIR.chmod(0o700)


@contextmanager
def launch_lock():
    """Serialize launch/stop actions; an exited process releases its lock."""
    make_data_dir()
    with (DATA_DIR / 'launch.lock').open('a') as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def load_state() -> dict:
    try:
        value = json.loads(STATE_FILE.read_text(encoding='utf-8'))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def save_state(value: dict) -> None:
    make_data_dir()
    temporary = STATE_FILE.with_name('.managed_server.' + secrets.token_hex(6) + '.tmp')
    try:
        with temporary.open('x', encoding='utf-8') as handle:
            temporary.chmod(0o600)
            json.dump(value, handle, indent=2)
        temporary.replace(STATE_FILE)
    finally:
        temporary.unlink(missing_ok=True)


def request_identity() -> dict | None:
    try:
        req = Request(URL + '/api/manager/identity', headers={'Accept': 'application/json'})
        with urlopen(req, timeout=1.5) as response:
            value = json.load(response)
        if isinstance(value, dict) and value.get('service_id') == SERVICE_ID and value.get('root') == str(ROOT):
            return value
    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        pass
    return None


def port_taken() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex((HOST, PORT)) == 0


def backup_database() -> Path | None:
    """Take a verified online snapshot, closing both SQLite handles before rename."""
    if not DB.is_file():
        print('No existing database; first launch will create demonstration records.')
        return None
    make_data_dir()
    BACKUP_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    dest = BACKUP_DIR / f'jamie_data_{stamp}.sqlite3'
    temp = BACKUP_DIR / f'.jamie_data_{stamp}.partial'
    try:
        with closing(sqlite3.connect(DB.as_uri() + '?mode=ro', uri=True, timeout=20)) as source:
            with closing(sqlite3.connect(temp, timeout=20)) as target:
                temp.chmod(0o600)
                source.backup(target, pages=50, sleep=0.05)
                if target.execute('PRAGMA quick_check').fetchone() != ('ok',):
                    raise RuntimeError('SQLite backup validation failed.')
                names = {row[0] for row in target.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                if not {'applications', 'settings', 'decisions', 'decision_history', 'assessments'} <= names:
                    raise RuntimeError('Database does not contain the expected Client Selector tables.')
        temp.replace(dest)
    except Exception:
        temp.unlink(missing_ok=True)
        raise
    print('Verified backup:', dest, flush=True)
    return dest


def startup_owned() -> bool:
    if not STARTUP_FILE.is_file():
        return False
    try:
        value = plistlib.loads(STARTUP_FILE.read_bytes())
        return isinstance(value, dict) and value.get('Label') == LABEL and value.get('ProgramArguments', [])[1:] == [str(ROOT / 'client_selector_manager.py'), 'login-serve']
    except (OSError, ValueError, TypeError, plistlib.InvalidFileException):
        return False


def autostart_install() -> None:
    if sys.platform != 'darwin':
        raise RuntimeError('Automatic sign-in startup is available on macOS only.')
    ensure_files()
    make_data_dir()
    if STARTUP_FILE.exists() and not startup_owned():
        raise RuntimeError('A different Client Selector startup entry exists. It has not been overwritten.')
    STARTUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    # The launch agent remains in the foreground, as required by launchd.
    # Do not bootstrap it here: the manually launched server is already running.
    # It takes effect after the next user sign-in, without opening a browser.
    config = {
        'Label': LABEL,
        'ProgramArguments': [sys.executable, str(ROOT / 'client_selector_manager.py'), 'login-serve'],
        'WorkingDirectory': str(ROOT),
        'RunAtLoad': True,
        'KeepAlive': False,
        'ProcessType': 'Background',
        'StandardOutPath': str(LOG_FILE),
        'StandardErrorPath': str(LOG_FILE),
    }
    temporary = STARTUP_FILE.with_suffix('.tmp')
    temporary.write_bytes(plistlib.dumps(config))
    temporary.chmod(0o644)
    temporary.replace(STARTUP_FILE)
    print('Automatic startup enabled for the next Mac sign-in. It does not keep the Mac awake.')


def autostart_remove() -> None:
    if not STARTUP_FILE.exists():
        print('Automatic startup was already disabled.')
        return
    if not startup_owned():
        raise RuntimeError('Startup entry belongs to a different copy. No file was removed.')
    STARTUP_FILE.unlink()
    # A loaded job has KeepAlive=false. Removing its plist prevents next-login
    # launch; the current server keeps running until the user stops it.
    print('Automatic startup disabled for future sign-ins. Current server is unchanged.')


def build_server(token: str) -> ThreadingHTTPServer:
    ensure_files()
    spec = importlib.util.spec_from_file_location('client_selector_original', APP)
    if spec is None or spec.loader is None:
        raise RuntimeError('Could not load app.py.')
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    if (original.HOST, original.PORT) != (HOST, PORT) or original.DB != DB:
        raise RuntimeError('Unexpected application host, port or database; refusing to start.')

    class ManagedHandler(original.Handler):
        def setup(self):
            super().setup()
            self.connection.settimeout(60)

        def end_headers(self):
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            super().end_headers()

        def local_request(self) -> bool:
            if self.headers.get('Host', '') not in ALLOWED_HOSTS:
                self.send(403, {'error': 'Only the local Client Selector address is accepted.'})
                return False
            origin = self.headers.get('Origin')
            if (origin is not None and origin not in ALLOWED_ORIGINS) or self.headers.get('Sec-Fetch-Site') == 'cross-site':
                self.send(403, {'error': 'Requests from other websites are not allowed.'})
                return False
            return True

        def do_GET(self):
            if not self.local_request():
                return
            if self.path == '/api/manager/identity':
                return self.send(200, {'service_id': SERVICE_ID, 'root': str(ROOT)})
            if self.path == '/':
                page = HTML.read_text(encoding='utf-8')
                nav = '<nav style="margin-top:12px"><a href="/admin" style="color:white;font-weight:600">System administration &amp; backups</a> <span style="font-size:12px"> | Mac edition</span></nav>'
                return self.send(200, page.replace('</header>', nav + '</header>', 1), 'text/html')
            if self.path == '/admin':
                page = ADMIN_HTML.read_text(encoding='utf-8').replace('__CONTROL_TOKEN__', json.dumps(token))
                return self.send(200, page, 'text/html')
            if self.path == '/api/manager/status':
                backups = sorted(BACKUP_DIR.glob('jamie_data_*.sqlite3'))
                with closing(sqlite3.connect(DB, timeout=10)) as connection:
                    count = connection.execute('SELECT COUNT(*) FROM applications').fetchone()[0]
                return self.send(200, {
                    'running': True, 'applications': count, 'database': str(DB),
                    'backup_folder': str(BACKUP_DIR), 'log_file': str(LOG_FILE),
                    'backup_count': len(backups), 'latest_backup': backups[-1].name if backups else None,
                    'autostart': startup_owned(), 'python': platform.python_version(),
                    'architecture': platform.machine(), 'url': URL,
                })
            return super().do_GET()

        def do_POST(self):
            if not self.local_request():
                return
            if self.headers.get_content_type() != 'application/json':
                return self.send(415, {'error': 'Content-Type must be application/json.'})
            manager_routes = {CONTROL, '/api/manager/backup', '/api/manager/startup-on', '/api/manager/startup-off'}
            if self.path not in manager_routes:
                return super().do_POST()
            if not hmac.compare_digest(token.encode('utf-8'), self.headers.get('X-Client-Selector-Token', '').encode('utf-8')):
                return self.send(403, {'error': 'This administration page is out of date. Reload it and try again.'})
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 1 <= length <= 35000:
                    raise ValueError('Request too large or empty.')
                if not isinstance(json.loads(self.rfile.read(length)), dict):
                    raise ValueError('Request must be a JSON object.')
                if self.path == CONTROL:
                    self.send(200, {'ok': True})
                    threading.Thread(target=self.server.shutdown, daemon=True).start()
                    return
                if self.path == '/api/manager/backup':
                    location = backup_database()
                    message = f'Verified backup created: {location}' if location else 'No database found.'
                elif self.path == '/api/manager/startup-on':
                    autostart_install()
                    message = 'Enabled for the next Mac sign-in. No browser opens automatically.'
                else:
                    autostart_remove()
                    message = 'Disabled for future sign-ins. The current server is still running.'
                return self.send(200, {'ok': True, 'message': message})
            except (RuntimeError, OSError, sqlite3.Error, ValueError, TypeError) as exc:
                return self.send(400, {'error': str(exc)})

    # Bind first, so a port conflict cannot change the database.
    server = ThreadingHTTPServer((HOST, PORT), ManagedHandler)
    try:
        original.init_db()
        DB.chmod(0o600)
        save_state({'pid': os.getpid(), 'token': token, 'root': str(ROOT), 'started': datetime.now().isoformat()})
    except Exception:
        server.server_close()
        raise
    return server


def run_server(server: ThreadingHTTPServer, token: str) -> None:
    def signal_stop(signum, frame):
        threading.Thread(target=server.shutdown, daemon=True).start()
    signal.signal(signal.SIGTERM, signal_stop)
    signal.signal(signal.SIGINT, signal_stop)
    print('Client Selector running at', URL, flush=True)
    try:
        server.serve_forever(poll_interval=0.2)
    finally:
        server.server_close()
        if hmac.compare_digest(str(load_state().get('token', '')), token):
            STATE_FILE.unlink(missing_ok=True)
        print('Client Selector stopped cleanly.', flush=True)


def serve() -> None:
    token = os.environ.pop('CLIENT_SELECTOR_CONTROL_TOKEN', '')
    if len(token) < 32:
        raise RuntimeError('Use Client Selector.app or START Client Selector.command to start.')
    run_server(build_server(token), token)


def login_serve() -> None:
    with launch_lock():
        if request_identity() is not None:
            print('This Client Selector is already running.')
            return
        if port_taken():
            raise RuntimeError(f'Port {PORT} is occupied. No other application was stopped.')
        backup_database()
        token = secrets.token_urlsafe(36)
        server = build_server(token)
    run_server(server, token)


def start(open_browser: bool = True) -> None:
    ensure_files()
    with launch_lock():
        if request_identity() is not None:
            print('Client Selector is already running.')
        else:
            if port_taken():
                raise RuntimeError(f'Port {PORT} belongs to another program or Client Selector copy. Close it first. No program was stopped.')
            try:
                backup_database()
            except (RuntimeError, OSError, sqlite3.Error) as exc:
                raise RuntimeError('Safety backup failed, so the app was not started: ' + str(exc)) from exc
            token = secrets.token_urlsafe(36)
            environment = os.environ.copy()
            environment['CLIENT_SELECTOR_CONTROL_TOKEN'] = token
            with LOG_FILE.open('a', encoding='utf-8') as log:
                LOG_FILE.chmod(0o600)
                process = subprocess.Popen(
                    [sys.executable, '-u', str(ROOT / 'client_selector_manager.py'), 'serve'],
                    cwd=ROOT, env=environment, stdin=subprocess.DEVNULL,
                    stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
                )
            for _ in range(60):
                if request_identity() is not None:
                    print('Client Selector started. Records:', DB)
                    break
                if process.poll() is not None:
                    raise RuntimeError(f'Server exited ({process.returncode}). See {LOG_FILE}')
                time.sleep(0.2)
            else:
                # This exact child belongs to this launch; never kill by port/PID search.
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
                raise RuntimeError(f'Server did not become ready. See {LOG_FILE}')
    if open_browser:
        webbrowser.open(URL)


def stop() -> None:
    with launch_lock():
        if request_identity() is None:
            if port_taken():
                raise RuntimeError(f'Another program or copy is using port {PORT}. It has not been stopped.')
            print('Client Selector is not running. Database is unchanged.')
            return
        state = load_state()
        if state.get('root') != str(ROOT) or not isinstance(state.get('token'), str):
            raise RuntimeError('Secure control information is missing. No process was terminated.')
        req = Request(URL + CONTROL, data=b'{}', method='POST', headers={
            'Content-Type': 'application/json', 'X-Client-Selector-Token': state['token'],
        })
        with urlopen(req, timeout=5) as response:
            if not json.load(response).get('ok'):
                raise RuntimeError('Shutdown was not acknowledged.')
        for _ in range(40):
            if not port_taken():
                print('Client Selector stopped. All saved records remain intact.')
                return
            time.sleep(0.2)
        raise RuntimeError('Server is still closing. Check the log before retrying.')


def status() -> None:
    info = request_identity()
    print('Running at ' + URL if info else 'Not running at ' + URL)
    print('Code folder:', ROOT)
    print('Database:', DB)
    print('Backups:', BACKUP_DIR)
    print('Log:', LOG_FILE)
    print('Start at next sign-in:', 'enabled' if startup_owned() else 'disabled')
    print('Python:', platform.python_version(), '| Architecture:', platform.machine())
    if info is None and port_taken():
        print(f'WARNING: Port {PORT} is occupied by another program or copy.')


def main() -> None:
    commands = {
        'start': start, 'start-quiet': lambda: start(False), 'stop': stop,
        'backup': backup_database, 'status': status, 'serve': serve,
        'login-serve': login_serve, 'autostart-install': autostart_install,
        'autostart-remove': autostart_remove,
    }
    action = sys.argv[1].lower() if len(sys.argv) > 1 else 'start'
    try:
        if action not in commands:
            raise RuntimeError('Unknown action. Choose: ' + ', '.join(commands))
        commands[action]()
    except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
        print('ERROR:', exc, file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
