"""Standard-library smoke test using synthetic records in an isolated temp folder.

Run: python3 self_test.py
No live database is opened or copied; no AI request is made. A spare localhost
port and private temporary HOME are used, so a running real app is left alone.
"""
from __future__ import annotations
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import importlib.util
import json
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile


def main() -> None:
    root = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix='client-selector-self-test-') as temporary:
        temp = Path(temporary)
        fixture = temp / 'app'
        fixture.mkdir()
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        for name in ('app.py', 'client_selector_manager.py', 'index.html', 'admin_console.html'):
            # Replace only within disposable copies, not the user's source.
            (fixture / name).write_text((root / name).read_text(encoding='utf-8').replace('8510', str(port)), encoding='utf-8')
        spec = importlib.util.spec_from_file_location('fixture_app', fixture / 'app.py')
        assert spec and spec.loader
        app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app)
        app.init_db()  # Creates four demonstration records ONLY in the temp folder.
        env = {**os.environ, 'HOME': str(temp / 'home'), 'PYTHONDONTWRITEBYTECODE': '1'}
        command = [sys.executable, str(fixture / 'client_selector_manager.py')]
        url = f'http://127.0.0.1:{port}'

        def call(path, data=None):
            request = Request(url + path, data=json.dumps(data).encode() if data is not None else None,
                              headers={'Content-Type': 'application/json'})
            try:
                response = urlopen(request, timeout=10)
            except HTTPError as error:
                response = error
            with response:
                return response.status, json.load(response)

        def run(action):
            result = subprocess.run(command + [action], env=env, text=True, capture_output=True, timeout=30)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            return result

        started = False
        try:
            run('start-quiet')
            started = True
            assert len(call('/api/state')[1]['applications']) == 4
            print('PASS: synthetic application starts')
            bad = {'Impact': 40, 'Feasibility': 30, 'Learning': 30, 'Need': 20}
            assert call('/api/weights', {'weights': bad})[0] == 400
            good = {'Impact': 40, 'Feasibility': 20, 'Learning': 25, 'Need': 15}
            assert call('/api/weights', {'weights': good})[0] == 200
            print('PASS: weight validation and save')
            application = {'business': 'Synthetic migration test', 'description': 'Test only', 'applied_date': '2026-10-21'}
            assert call('/api/applications', application)[0] == 200
            state = call('/api/state')[1]
            app_id = next(item['id'] for item in state['applications'] if item['Business'] == application['business'])
            new_app = next(item for item in state['applications'] if item['id'] == app_id)
            assert new_app['Assessed'] is False and all(new_app[k] is None for k in good)
            assert all(item['Assessed'] for item in state['applications'] if item['id'] != app_id)
            assert call('/api/decisions', {'application_id': app_id, 'decision': 'Shortlist', 'reason': 'Too early'})[0] == 400
            assert call('/api/decisions', {'application_id': app_id, 'decision': 'Request information', 'reason': 'Need evidence'})[0] == 200
            scores = {'Impact': 8, 'Feasibility': 7, 'Learning': 9, 'Need': 6}
            assert call('/api/scores', {'application_id': app_id, **scores, 'Need': 0})[0] == 400
            assert call('/api/scores', {'application_id': app_id, **scores})[0] == 200
            assert call('/api/scores', {'application_id': 999999, **scores})[0] == 400
            assert call('/api/applications', {**application, **scores})[0] == 400
            scored = next(item for item in call('/api/state')[1]['applications'] if item['id'] == app_id)
            assert scored['Assessed'] is True and all(scored[k] == v for k,v in scores.items())
            print('PASS: evidence-first workflow, unscored state and human scoring validation')
            assert call('/api/decisions', {'application_id': app_id, 'decision': 'Shortlist', 'reason': 'Synthetic evidence'})[0] == 200
            assert call('/api/manager/backup', {})[0] == 403
            assert call('/api/assess', {'application_id': app_id, 'consent': False})[0] == 400
            print('PASS: application, decision, control token and AI consent checks')
            run('backup')
            status = call('/api/manager/status')[1]
            backups = list(Path(status['backup_folder']).glob('*.sqlite3'))
            assert backups
            for path in backups:
                connection = sqlite3.connect(path)
                try:
                    assert connection.execute('PRAGMA quick_check').fetchone() == ('ok',)
                finally:
                    connection.close()
            print('PASS: verified backups')
            run('stop')
            started = False
            run('start-quiet')
            started = True
            state = call('/api/state')[1]
            assert len(state['applications']) == 5 and state['weights'] == good
            assert state['decisions'][str(app_id)]['reason'] == 'Synthetic evidence'
            assert len(state['decision_history']) == 2
            assert next(item for item in state['applications'] if item['id'] == app_id)['Assessed'] is True
            print('PASS: data survives restart')
            assert 'already running' in run('start-quiet').stdout
            print('PASS: repeated start does not launch a second server')
        finally:
            if started:
                run('stop')
    print('All self-tests passed. Live data was not accessed. Mac app/login and live AI remain separate checks.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('SELF-TEST FAILED:', exc, file=sys.stderr)
        raise SystemExit(1)
