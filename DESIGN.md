# Client Selector design — Mac edition 2

## User experience
Three main areas: Applications, Assessment, Rankings & decisions. Settings holds scoring weights and an administration link. The existing header administration shortcut remains available.

Applications lists projects and their assessment status. A short form saves business name, description and application date. Scores are not requested during entry.

Assessment presents evidence first, then optional AI advice, then human scoring. AI generation controls are expandable and a Skip AI button moves focus to the human assessment. New score selectors start blank. Criteria include plain-language definitions and general scoring bands.

Rankings includes assessed applications in descending weighted score order with business-name tie-breaking. Unassessed applications follow without a numeric rank or score. Decision controls use the same selected application. Missing evidence can be requested before assessment; shortlist and decline require saved scores.

Navigation uses native buttons and labelled selectors. Tables use headers; business names are keyboard-accessible buttons. Status regions announce saves/errors. Visible keyboard focus and responsive single-column scoring are included. Wide tables scroll. Human testing and measured accessibility checks remain pending.

Unsaved application, score, decision, weight or assessment-text changes trigger a confirmation before switching application or area. Leaving the page uses the browser's unsaved-work prompt. API saves disable their button; selection changes are blocked while a request is running. AI failure leaves manual scoring available.

## Technical design
Python standard-library HTTP server with the existing local security and backup manager. SQLite remains beside app.py. The application binds to localhost port 8510.

The additive migration adds applications.assessed with default 1, retaining existing scores as assessed. New applications store assessed=0 and zero placeholders in the retained NOT NULL score columns. These placeholders are exposed as null through the API and excluded from weighted scoring, ranking and numeric CSV output. Saving all four valid scores changes assessed to 1. Migration is idempotent and runs after the managed launcher's verified backup.

POST /api/applications saves evidence only and returns application_id. POST /api/scores validates and saves independent human scores. POST /api/decisions enforces assessment for Shortlist/Decline while allowing information requests. Existing weights, AI and history endpoints remain.

AI results remain advisory records and do not update human score columns. No cloud fallback or automatic AI request is introduced. Secrets and the current API key are not saved by the application.

## Deferred work
Application-detail editing, multiple reviewer identities, selection rounds, hosting and remote access require separate design. This release supports revising human scores, but does not add a score-change audit history. Decision history is retained.
