# Mac edition 2 verification report

Prepared 22 October 2026. Runtime: Python 3.13 on Linux; JavaScript syntax: Node.js 24. These are developer checks, not Mac or representative-user testing.

## Passed
- Synthetic startup, weight validation/save and existing local security-token/consent checks.
- Application saved without scores; API returns assessed=false and null score values.
- Existing synthetic applications retain assessed=true.
- Shortlist rejected before scoring; Request information accepted.
- Invalid and unknown-application human scores rejected; four valid scores saved independently.
- Application-entry endpoint rejects score payloads to enforce separate scoring.
- Decision and decision history saved after assessment.
- Verified backups pass SQLite quick_check.
- Restart preserves application, scores, assessment status, weights, decisions and history.
- Repeated start reuses the running service.
- Additive migration applied twice to a disposable copy of the original database.
- Every original application value retained; all decision, history, settings and AI-assessment rows retained.
- Original packaged database was checked unchanged during the edition-2 developer checks. No database is included in this source release.
- JavaScript syntax parses; static IDs are unique; AI section precedes human scoring; entry form contains no scores.

## Not yet checked
The revised interface has not been rendered or exercised in a browser here: no browser binary was available. Navigation, unsaved prompts, downloads, responsive layout and assistive-technology behaviour need actual browser checks. Prior-edition browser results do not establish these behaviours for the new interface.

Actual Mac installer execution, Finder/Dock launching, Safari, login startup and sleep behaviour remain Mac acceptance checks. No live AI request was made. The existing installer and manager safety logic were retained; the installer was not re-executed on an actual Mac for this release.

Run python3 self_test.py for reproducible isolated workflow checks. It uses temporary synthetic storage and does not open the live database or call AI.

## Subsequent owner-guided Mac acceptance

The owner has since confirmed the main local workflow, CSV downloads, backup creation, app restart persistence, unscored restrictions, unsaved-change prompts and weight validation/recalculation. See ACCEPTANCE_RECORD.md. These are reported user checks, not a new automated browser run. Live AI, backup restore, remote access and machine reboot/sign-in startup remain untested in that record. No runtime code was changed while preparing these guides. Earlier runtime checks were not rerun solely for these documentation changes.
