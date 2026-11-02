# Client Selector — Guided Mac Acceptance Record

## Basis of this record

Application: v2.1, Mac edition 2, local Client Selector. The owner performed guided steps on the Mac and confirmed the outcomes in this conversation. These are reported observations, not direct automated observation by the assistant. They supplement the original developer report; they do not replace independent testing or establish production security.

| Check | Reported outcome |
| --- | --- |
| Save Test Bakery without scores and open Assessment | Passed |
| Evidence and optional AI before human scoring; blank new score fields | Passed |
| Skip AI, enter human scores and show numeric ranking | Passed |
| Record Shortlist, reason, date and decision history | Passed |
| Refresh browser; decision and history retained | Passed |
| Export rankings and latest-decision CSV; check content | Passed |
| Create verified backup and see success message | Passed |
| Stop and reopen the app; saved data retained | Passed — application restart only |
| New Test Pending application has no score or rank | Passed |
| Shortlist/Decline unavailable before scoring; Request information remains available | Passed |
| Cancel switching business with unsaved reason; retain draft | Passed |
| Confirm discard; original saved reason retained | Passed |
| Reject 101% weights and retain saved settings | Passed |
| Valid weights change weighted results; restore original settings | Owner clarified the result was correct after initially reporting 7.6; accepted as a functional confirmation, not an independently captured numeric result |

## Outstanding

- Live AI request, draft quality and unchanged human scores during a live call.
- Restore from a backup, including a recovery rehearsal.
- Jamie’s remote application access and its permissions.
- Actual Mac sign-in startup, reboot recovery, FileVault/network behaviour and sleep.
- Extended keyboard, zoom, responsive layout and assistive-technology assessment.
- Named-reviewer attribution, application accounts and score-change audit: not implemented.

The user’s current weights and full database were not retrieved. The package does not contain the new test records, exports or backups from the user’s Mac.
