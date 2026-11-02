# Client Selector — User Guide

**For Jamie and committee reviewers · v2.1 / Mac edition 2**

This guide covers using the existing local application. It follows the Mac workflow checked by the owner in this conversation. Remote access and individual committee accounts are not part of this completed local setup.

## 1. Open the application

1. On the Mac mini, open **Client Selector.app**. If it is not in the Dock, use Finder → Go → Go to Folder and enter `~/Applications`, then open the app there.
2. Safari opens the application at **http://127.0.0.1:8510**.
3. If you already have a browser tab open, reload it after starting the app.

The address refers to the computer running the browser. Entering it on Jamie’s separate Mac does not connect to the Mac mini. Ask the administrator to complete his private remote connection first.

Closing Safari does not stop the application. Saved information remains in its database.

## 2. Understand the workflow

| Area | What you do |
| --- | --- |
| Applications | Enter project details and see which applications await assessment. |
| Assessment | Review evidence, optionally obtain AI advice, then enter human scores. |
| Rankings & decisions | Compare weighted scores and record the committee’s decision. |
| Settings | Set scoring weights. The administrator also accesses backups here. |

Save each completed task using its **Save** or **Record** button. This application does not automatically save every keystroke.

## 3. Add an application

1. Open **Applications**.
2. Enter **Business name**, **Project description** and **Date applied**.
3. Click **Save application & review**.
4. Check the save message and the business name on the Assessment screen.

No human scores are required at entry. The application remains **Awaiting assessment** until all four scores are saved. Business names must be unique, including differences in capital letters.

**Limits:** this version does not have an application-detail edit or delete button. Check names, dates and descriptions before saving. Ask the administrator about corrections; do not create a duplicate to work around a mistake.

## 4. Review the evidence

Read the project description under **1. Review the evidence**. Consider what the project would achieve, whether students can deliver it and what information is missing.

AI advice is optional. You can click **Skip AI and enter human scores** and complete the whole selection process without using AI.

### If you choose AI advice

1. Expand **Generate an AI draft**.
2. Enter an authorised OpenAI API key. It is not saved by the application.
3. Review **Text to assess**. Use only fictional, anonymised or explicitly authorised text.
4. Tick the confirmation for external AI processing.
5. Click **Generate draft AI assessment** and wait for the result.
6. Read the summary, full reasoning, evidence gaps, follow-up questions and caveats.

The request sends the approved text to OpenAI and may incur API charges. AI scores never automatically become human scores or determine the committee decision. If AI fails, continue with evidence-based human assessment. Live AI behaviour and assessment quality have not yet been accepted on the Mac.

## 5. Enter human scores

Under **3. Human assessment**, choose a whole-number score from 1 to 10 for every criterion:

| Criterion | Meaning |
| --- | --- |
| Impact | Benefit to the client or community. |
| Feasibility | Achievable student scope over roughly six weeks. |
| Learning | Opportunity for students to develop useful skills. |
| Need | Value the organisation would gain from pro bono assistance. |

Guidance bands are 1–3 weak, 4–6 mixed, 7–8 strong and 9–10 exceptional. Use evidence and committee judgement; the bands are guidance rather than a calibrated assessment standard.

Click **Save human scores & compare**. The application opens Rankings & decisions and includes the project in the ranking. Saved scores can be revised in Assessment. This version does not provide a separate score-change history.

## 6. Compare applications

Only applications with saved human scores have a numeric rank and weighted score. Unscored applications appear below them as **Awaiting assessment**, without a numeric score or rank.

The calculation is:

`Weighted score = (Impact × its weight + Feasibility × its weight + Learning × its weight + Need × its weight) ÷ 100`

For example, human scores 8, 7, 9 and 6 with weights 35%, 25%, 25% and 15% give **7.70/10**. These are an example, not a claim about your current saved weights. Tied scores are ordered by business name, not by an additional suitability judgement.

## 7. Record a committee decision

1. In **Rankings & decisions**, choose the business under **Committee decision**.
2. Check that the displayed business and score are the intended ones.
3. Select the decision.
4. Enter a clear reason. A reason is required unless the decision is Pending.
5. Click **Record decision** and check the success message.
6. Expand **Decision history** to see the recorded date, decision and reason.

| Decision | When it is available |
| --- | --- |
| Pending | While review is incomplete. |
| Request information | Before or after human scoring. |
| Shortlist | After human scores have been saved. |
| Decline | After human scores have been saved. |

Updating a decision adds a history record. Dates in the decision log/history use UTC. The system records decisions and reasons, but does not identify which committee member made them.

### Unsaved work

If you try to change business or area with unsaved changes, the application warns you. Choose **Cancel** to keep editing; choose the confirmation to discard the changes. The saved record is retained. Browsers may use different wording for their confirmation buttons.

## 8. Export the results

- **Download rankings CSV** creates `business_rankings.csv` with application details, assessment status, scores, current decision and dates. Unassessed records have blank rank and score fields.
- **Download decision log CSV** creates `committee_decisions.csv` with the latest recorded decision, reason and dates for applications with saved decisions. It is not the full decision-history export.
- **Download AI draft JSON** saves the displayed AI draft when one is available.

Open downloads in Numbers or Excel and check the intended records are present. Treat exports as records that may contain private information. A CSV is a report, not a complete database backup.

## 9. Change weights only by agreement

In **Settings**, the four weights must be whole numbers between 0 and 100 and total exactly 100%. Click **Save weights**. Changing valid weights recalculates all scored applications; it does not change their individual human scores. Invalid totals leave the saved settings unchanged.

The current app does not enforce user versus administrator roles. Agree who can change the weights and use the system controls.

## 10. Get help

| Problem | First action |
| --- | --- |
| Safari cannot connect | Open Client Selector.app on the Mac mini first. |
| Application is unranked | Save all four human scores in Assessment. |
| Shortlist is unavailable | Confirm human scores have been saved for that business. |
| Decision will not save | Enter a reason and check the selected business. |
| Weights will not save | Make all four whole numbers total 100%. |
| AI request fails | Continue manually; send the error text, never the API key, to the administrator. |
| Data seems missing | Stop making changes and ask the administrator to check the running installation. Do not reinstall into another user account as a fix. |

Core local workflow checks passed through the owner’s guided Mac testing. Live AI, recovery from backup, remote access and a full accessibility assessment remain outstanding. Do not assume that different Mac accounts or two separate installations synchronise automatically.
