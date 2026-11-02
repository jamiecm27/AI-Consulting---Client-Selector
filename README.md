# Client Selector — Mac source release

**v2.1 / Mac edition 2 · Source code and guides only**

Local tool for comparing consulting-society project applications. Its sequence is application entry → evidence → optional AI advice → human scores → rankings → committee decision. Python standard library, SQLite and a browser; no pip dependencies.

## Read first

- Open `USER_GUIDE.html` for everyday operation.
- Open `ADMIN_GUIDE.html` for installation, backups, recovery, GitHub updates and limits.
- Read `ACCEPTANCE_RECORD.md` for the guided Mac checks confirmed by the owner.
- Read `TEST_REPORT.md` for the original developer checks and their limits.

This source package deliberately includes **no SQLite database, saved applications, API keys, exports, backups or runtime state**. It is a source release, not a backup of the working Mac.

## Already installed on the Mac?

Keep using Client Selector.app. No runtime-code change is required for these manuals. If you later use this folder as an update, `00 INSTALL ON MAC.command` can retain the valid database already in `~/Applications/JamieClientSelector`. Back up first and use the same Mac account as the authoritative installation.

## New developer checking out the repository

1. Use a separate development folder, not the live installation.
2. Install standard Python 3.11 or newer if necessary. Original developer checks used Python 3.13.
3. In Terminal, change to this folder and run:

```sh
python3 self_test.py
```

The self-test creates and removes disposable synthetic data on a spare localhost port. It does not open the live database, call AI or install a Mac startup entry.

### Optional local demonstration

Only use a separate development copy. If the working Selector is already using port 8510, stop it deliberately first or postpone the demo; this source does not use a second port automatically.

```sh
python3 client_selector_manager.py start
```

For an uninstalled source checkout with no database, first launch creates `jamie_data.sqlite3` with four fictional demonstration applications. That file remains local and is ignored by Git. This is an explicit source-demo route; the installed launcher instead refuses to replace a missing working database with samples.

To stop the source demo:

```sh
python3 client_selector_manager.py stop
```

The managed server uses localhost port 8510. Runtime logs/backups use the current Mac user’s Application Support folder. Do not mistake the source demo for the authoritative installed application.

For a fresh Finder/Dock installation, the migration installer requires a source database. This public source package does not supply one. After intentionally creating a separate fictional demo database as above and stopping it, the normal Mac installer can install that demo. To migrate existing records, use the private migration package or a controlled backup procedure instead. Never download and publish another person’s database.

## Working with GitHub

Target repository: https://github.com/jamiecm27/AI-Consulting---Client-Selector

The administrator guide provides a clone → branch → review → test → commit → push → pull request workflow using GitHub Desktop. No repository update has been performed as part of preparing this source package. Copy the contents of this folder to the intended branch after reviewing existing repository files; do not replace its `.git` directory or automatically delete legacy files.

## Data and access limits

- Saved human scores determine rankings. AI advice does not populate them.
- Unscored applications are not ranked. Shortlist/Decline require saved scores.
- The four weighting percentages must total 100.
- Decision history exists; score-change history does not.
- There are no app-level committee logins, user roles or named-reviewer audit records.
- The app is local-only. Remote access and independent application accounts need separate implementation/configuration and acceptance tests.
- The installed app starts optionally at that Mac user’s sign-in, not before login.
- Live AI calls and backup restoration remain untested in the owner’s acceptance sequence.

Keep credentials, databases, exports, backups and logs out of GitHub. `.gitignore` does not remove already tracked private files. The included `SOURCE_MANIFEST.json` describes files in this clean source release and hashes the unchanged runtime files; it includes no database fingerprint or application records.
