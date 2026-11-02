# Client Selector completion tasks

## Completed for Mac edition 2
- [x] Define evidence-first workflow and local scope.
- [x] Separate application entry, optional AI advice and human scoring.
- [x] Mark unscored applications Awaiting assessment; omit their rank and numeric scores.
- [x] Preserve existing scores and records through an additive upgrade.
- [x] Add score explanations, keyboard-accessible application selection and unsaved-work prompts.
- [x] Test HTTP workflow, validation, persistence and backups with disposable records.
- [x] Verify original database preservation and repeat migration.
- [x] Update setup, workflow and design documentation.

## Owner-confirmed Mac acceptance checks
- [x] Application entry and the evidence-first workflow open correctly.
- [x] Manual scoring, ranking and saved decisions/history work.
- [x] Refresh and stop/reopen retain data.
- [x] Both CSV exports contain the expected information.
- [x] Backup creation reports success.
- [x] Unscored records have no rank; decision restrictions work.
- [x] Cancel/discard protects unsaved work as expected.
- [x] Invalid weights are rejected; valid weights recalculate correctly.
- [x] Separate user/admin guides and a clean source package prepared.

See ACCEPTANCE_RECORD.md for the evidence basis and the clarified numeric-weight check.

## Outstanding
- [ ] Live AI call, quality and independence of human scores during a live call.
- [ ] Backup restoration rehearsal.
- [ ] Jamie remote access acceptance.
- [ ] Mac sign-in/reboot startup and sleep behaviour.
- [ ] Extended keyboard/zoom/accessibility testing.
- [ ] Review application-detail editing/deletion and score-change audit needs.
- [ ] Review and publish a source-only GitHub branch; no push has been performed.
