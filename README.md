# Jamie's AI Client Selection Engine — ARM64, version 2

Runs on Windows 11 ARM64 with Python 3.13 using only built-in Python modules. No pip, Streamlit, Pandas or Visual Studio required.

## Start
1. Extract the ZIP to a new folder. Keep the folder somewhere private.
2. Open PowerShell in the folder containing `app.py`.
3. Run:
   ```powershell
   & "C:\Users\sion_\AppData\Local\Programs\Python\Python313-arm64\python.exe" app.py
   ```
4. Your browser should open `http://127.0.0.1:8501`.
5. To stop, press Ctrl+C in PowerShell.

If port 8501 is occupied by the old version, stop the old PowerShell server first.

## What's new
- SQLite database `jamie_data.sqlite3` is created automatically on first launch. Applications, decisions, weights and AI assessments survive refresh and restart.
- Weights must total 100% before saving.
- Date applied and date of decision included in dashboard and CSV exports.
- Committee decision history is retained, including previous decisions.
- AI assessments attach to the selected business, with concise summary and expandable detail. AI scores never replace human scores.
- Ranking CSV label and filename are consistent.

## Security and backup
- API key is typed into the browser and sent only to the local server for the OpenAI request; it is never written to the SQLite database or saved in project files.
- Do not put a real API key in source files or upload it to GitHub.
- The SQLite database may contain business-sensitive information. Keep it private and backed up; it is excluded from Git by `.gitignore`.
- Back up `jamie_data.sqlite3` **after stopping the server** by copying it to a secure location. Do not delete this file when updating the app.
- The local server has no login or access controls. It binds to 127.0.0.1 and is **not** suitable for public deployment or shared computers.
- All four sample businesses are fictional. Their applied dates are demonstration dates set when the database is first created.
- AI processing requires an OpenAI API key and incurs separate API usage charges. Only send fictional, anonymised or explicitly authorised information.

## Important
This new version starts with four fictional sample businesses in a new database. The earlier prototype saved nothing persistently, so it cannot recover any records lost after browser refresh.
