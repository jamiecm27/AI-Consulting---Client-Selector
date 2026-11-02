# Client Selector — Administrator Guide

**For Jamie or the person managing the Mac mini · v2.1 / Mac edition 2**

This guide covers operating the tested local application, protecting its records, updating its code and preparing changes for GitHub. It does not set up hosting or committee accounts. The source package accompanying this guide contains no database or saved application records.

## 1. Know which copy you are using

Three different locations have different jobs:

| Location | Purpose |
| --- | --- |
| Downloads / extracted ZIP | The installation or update payload. Keep it separate from daily working data. |
| `~/Applications/JamieClientSelector` | Installed application code and its working SQLite database. |
| A separate GitHub clone under your Development folder | Source editing, version control and review. It is not the live installation. |

`~` means the home folder of the currently logged-in Mac user. If you install under two accounts, you can create two independent databases. Pick one authoritative running installation. Mac user accounts do not automatically share or synchronise their application data.

The local address is **http://127.0.0.1:8510**. The port number is deliberately separate from other tools using 8501.

## 2. Start, stop and check the service

### Daily startup

Open **Client Selector.app** from `~/Applications` or the Dock. A repeated launch reuses the running service for that installation. If app creation was unavailable, use **START Client Selector.command** in the installed folder instead.

Closing the browser leaves the service running. A saved bookmark opens the address but does not itself start the service.

### System administration

Open **Settings → Open system administration & backups**, or the administration shortcut at the top of the dashboard. Check application count, latest backup, backup count, data path, log path and startup status.

Use **Stop Client Selector** for a deliberate shutdown. Use **CHECK Client Selector Status.command** from the installed folder if the website is unavailable. Do not stop all Python processes; other projects may use them.

### Startup at sign-in

**Enable automatic startup** creates a per-user startup entry. It starts the application after that Mac user signs in. It does not start the application before login, unlock FileVault, keep the Mac awake or complete remote access. This sign-in-startup behaviour has not yet been confirmed on the actual Mac in this acceptance sequence.

## 3. Back up the database

1. Open system administration.
2. Click **Create backup now**.
3. Wait for the verified-backup success message.
4. Confirm the latest backup and count update.
5. Keep a secure off-device copy of verified backups at an agreed interval and before major updates.

A backup snapshot uses SQLite’s backup API, checks database integrity and expected tables, closes database handles and then finalises the file. If the safety backup fails, the managed launcher stops rather than continuing. The app also takes a backup before a new managed server start when a database already exists.

Default backup location:

`~/Library/Application Support/JamieClientSelector/Backups`

To open it in Finder, choose **Go → Go to Folder**, paste the path and press Return. The administration page’s actual paths take precedence if a later installation has been configured differently.

Suggested operating routine: back up before each committee session and before updates; keep a separate secure copy after important decisions. Do not store backups in a public repository. CSV exports omit parts of the database and cannot replace this process.

## 4. Update an existing installation

1. Create a verified backup and record its location.
2. Keep a copy of the current release code for rollback.
3. Download and extract the intended update outside the installed folder.
4. Double-click **00 INSTALL ON MAC.command** in the extracted update.
5. The installer stops the recognised existing installation, backs it up and replaces code while retaining its database.
6. Reopen Client Selector and reload an old browser tab.
7. Check original applications, scores, decisions and history before continuing work.

The update can run without a database in its source payload when the destination already has its valid database. For a fresh installation, the installer needs a source database; the clean GitHub source package deliberately omits it. Use the existing private installation package for migration, or use the isolated demonstration method described in the source README.

Edition 2 adds an `assessed` status to the existing applications table on startup after backup. Existing scores remain assessed. New unscored applications are excluded from numeric rankings. Repeating the migration was checked using a temporary database copy.

## 5. Recover from a backup — rehearsal still required

**Backup creation passed; restoration into the live Mac installation has not been tested.** First rehearse on a separate copy with someone comfortable managing SQLite. A successful backup message is not proof of a successful recovery.

Recovery sequence for the responsible administrator:

1. Stop Client Selector. Confirm the managed service is stopped before touching database files. If another database program is open, close it too.
2. Record the installed folder and chosen verified backup. Keep a safe copy of the current application folder and release code before changing anything.
3. Preserve the current `jamie_data.sqlite3` and any matching `-wal`, `-shm` or `-journal` files together in a separate recovery folder. Do not mix old journal files with a restored database. If you cannot confirm the database is closed, pause and get help.
4. Copy the chosen verified backup into the installed folder as exactly `jamie_data.sqlite3`. Retain the backup itself in its original backup location.
5. Reopen the application and check expected counts, a known application, scores, decisions and history.
6. Record the backup restored, time, checks and any work lost since that snapshot. A restore does not merge later records automatically.

If the backup belongs to an older schema, matching release code may be needed. Do not assume old code can read a newer database. Keep the installed marker and launcher files intact; do not delete the installation to force a fresh database.

## 6. Keep development separate from working records

Use separate working copies for you and Jamie, and exchange code through GitHub. Keep the live installed database out of both Git working copies. Do not change the running application in place while a committee session is underway.

The **user** and **administrator** labels in these manuals describe responsibilities. They are not enforced app permissions: this version has no invitation-only accounts, per-user roles or named-reviewer audit trail. A trusted person able to reach this app can use its settings and administration controls.

A Mac account’s file permissions and a private connection are separate controls. Remote user access must be configured and tested independently. Do not change the server to listen on all interfaces or expose it publicly as a shortcut. Jamie’s remote Selector access remains unverified in this acceptance record.

## 7. Prepare the existing GitHub repository

Repository:

[AI-Consulting---Client-Selector](https://github.com/jamiecm27/AI-Consulting---Client-Selector)

Use the accompanying **Client_Selector_GitHub_Source.zip**, not a migration ZIP or the live installed folder. Its top-level source files are intended for review in the existing repository; it contains no saved database. No upload, commit, push or merge has been performed for you.

### Beginner route: GitHub Desktop

1. Install GitHub Desktop from its official site and sign into an account with write access to the repository. Never share GitHub passwords.
2. Choose **File → Clone Repository**, select the repository above (or its URL), and choose a dedicated Development folder. Do not clone over the installed application.
3. Fetch and pull the latest changes before starting. If GitHub Desktop reports local changes or a conflict, resolve those before copying the release files.
4. Create a branch, for example **mac-edition-2-docs**.
5. Extract the clean source ZIP. Copy the contents of its **Client_Selector_GitHub_Source** folder into the cloned repository root. Preserve the clone’s `.git` folder. Finder’s **Command + Shift + .** shows hidden files, including `.gitignore`.
6. If the repository already has ignore rules, combine the supplied exclusions with its existing rules rather than removing useful exclusions.
7. Review every changed file in GitHub Desktop. Confirm the payload is code/documentation only. Review any older Windows files separately; the package does not determine which legacy files should be deleted.
8. Run the source’s isolated self-test as described below. Do not use the live database to test a branch.
9. Enter a concise commit summary such as **Document tested Mac workflow and administration**, then commit to the branch.
10. Click **Publish branch** or **Push origin**, as appropriate. Open a pull request for review before merging into the default branch.
11. After review and merge, keep a release copy and record its version. A GitHub push does not update the installed Mac application; installation is a separate step.

GitHub Desktop’s clone, branch, commit and push workflow is described in GitHub’s official documentation. See the references at the end.

### What must stay out of GitHub

- Databases: `.sqlite3`, `.sqlite`, `.db`, and matching journal/WAL files.
- Backups, exports, logs and temporary files.
- API keys, passwords, `.env` files and credential files.
- Runtime metadata such as `.python-path`, `.install-marker.json` and managed-server state.
- Downloaded migration ZIPs and compiled Mac app bundles.

The supplied `.gitignore` helps with Git staging. It does not remove a file already tracked and does not protect manual uploads through the GitHub website. If private data is already in the repository, do not merely add an ignore rule: stop publishing and arrange appropriate removal, history review and credential rotation where needed.

## 8. Run the isolated developer check

From Terminal in the clean source folder, run:

```sh
python3 self_test.py
```

If you need to select the folder: type `cd ` with a trailing space, drag that source folder from Finder into Terminal, press Return, then run the command above. Use standard Python 3.11 or newer; the original developer checks used Python 3.13.

The test uses disposable synthetic data, a private temporary home folder and an available local port. It does not open the live database, call OpenAI or install Mac startup entries. Passing it does not replace actual Mac launcher, Safari, remote-connection or live-AI tests.

## 9. Operational troubleshooting

| Symptom | Action |
| --- | --- |
| Could not verify installer | For the expected downloaded installer, use macOS Privacy & Security → Open Anyway after reviewing the specific file. A malware/damage warning needs separate investigation. Do not disable Mac security globally. |
| Python missing | Follow the installer’s official Python link and certificate instructions. Do not install unrelated frameworks. |
| Safety backup failed | Stop. Check the reported path, disk space and permissions. Preserve the working database; do not bypass the backup check. |
| Port 8510 occupied | Determine which app owns it. The launcher refuses to stop an unrelated listener. |
| Wrong or missing records | Check the active Mac account and the administration page’s database path. Avoid creating another installation as a fix. |
| AI error | Check authorised key, model access, billing and certificate/network errors. Manual selection remains available. Do not include keys in screenshots or logs shared for help. |
| Cannot connect after sign-out/restart | Application startup and private networking each need checking. A local app restart test is not a machine-reboot or remote-access test. |

Server log default:

`~/Library/Application Support/JamieClientSelector/server.log`

A service log may include error details. Review it before sharing. The app does not provide an automatic monitoring or update service.

## 10. Test status and known limitations

Owner-reported Mac checks passed: application creation without scores; skip-AI/manual scoring; ranked output; decision save/history; persistence after refresh; both CSV exports; verified backup creation; stop/reopen persistence; unscored-state restrictions; cancel/discard unsaved-work behaviour; rejection of 101% weights; and correct valid-weight recalculation with original settings restored. These are guided user confirmations, not independent observation or a security audit.

Still outstanding: live AI call and quality; restoring a backup; remote Selector access; sign-in/reboot startup; extended keyboard, zoom and assistive-technology checks. Original records from the owner’s Mac have not been copied back into this source package.

Additional limits: no app-level user accounts, separate reviewer scoring, named decision authors, selection-round management, application-detail editing/deletion, score-change history or full history CSV export. Test Bakery/Test Pending may remain in the owner’s working database; the current UI cannot delete them. Agree a safe clean-up approach before real selection sessions rather than editing SQLite by hand during use.

## References

- [GitHub Desktop: cloning repositories](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop)
- [GitHub Desktop: getting started](https://docs.github.com/en/desktop/overview/getting-started-with-github-desktop)
- [GitHub Desktop: branches](https://docs.github.com/en/desktop/making-changes-in-a-branch/managing-branches-in-github-desktop)
- [Python macOS downloads](https://www.python.org/downloads/macos/)
- [Apple: opening a downloaded app](https://support.apple.com/guide/mac-help/open-an-app-by-overriding-security-settings-mh40617/mac)
