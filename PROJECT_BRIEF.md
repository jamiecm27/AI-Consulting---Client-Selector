# Client Selector project brief

## Scope agreed on 22 October 2026
Finish the existing local Mac application. Preserve its existing SQLite records, scores, decisions, history and AI drafts. Invitation-only accounts and remote committee access remain outside this release.

## Users and purpose
Jamie administers the application and records committee reviews. The society compares potential consulting projects and records explainable human selection decisions.

## Journey
1. Save application details without scores.
2. Review evidence and missing information.
3. Optionally obtain AI draft advice; this can be skipped.
4. Enter and save human scores independently.
5. Compare weighted rankings.
6. Record a decision with a reason and history.
7. Export rankings or decisions; administer backups separately.

## Acceptance criteria
- An application can be saved without entering scores or calling AI.
- Unscored applications have no numeric human scores or rank in the interface and exports.
- AI appears before human scoring and never populates it automatically.
- Four valid human scores are required before ranking.
- Request information is available before scoring; Shortlist and Decline require saved human scores.
- Existing data survives upgrade and restart.
- Weights total 100%; invalid values do not change saved settings.
- Users receive save feedback and a warning before leaving unsaved changes.
- The installer preserves the existing database and a verified backup precedes upgrade.

## Evidence limits
Original automated checks ran on Linux. The owner subsequently confirmed the main local Mac workflow; see ACCEPTANCE_RECORD.md. Extended accessibility, backup restore, live AI, remote access and sign-in/reboot startup remain outstanding.
