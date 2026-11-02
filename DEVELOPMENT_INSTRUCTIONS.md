# Development instructions — Ankura internship

Use this repeatable process for every new application and substantial update in this project. Keep the level of documentation and testing proportionate to the change.

## Context

- I am a beginner. Explain instructions in plain English.
- Use the existing project brief, code and documentation.
- Preserve existing user data and working functionality.
- Ask only questions that materially affect the solution. Make reasonable assumptions for routine choices and record them.

## 1. Define

Before substantial coding, establish:

- The problem and intended users.
- The main user journeys.
- Inputs, outputs and where data is stored.
- What is included and excluded from this version.
- Observable acceptance criteria: how we know it works.

Create or update PROJECT_BRIEF.md. Agree what working means before writing substantial code.

## 2. Design

Create or update DESIGN.md with both user experience design and technical design. For an existing application, review its current screens and preserve useful, familiar behaviour before proposing changes.

### 2a. User experience and interface design

- Identify each user type, their main tasks, their technical confidence and the devices they use.
- Map the journey from opening the application to completing each important task. Include first use and returning use.
- Define the screens, their purpose, navigation and the main action on each screen.
- Sketch simple screen layouts or wireframes before substantial interface changes. Show representative content and review the proposed experience with the user before major changes.
- Use plain language, descriptive labels, clear instructions and consistent controls. Explain unfamiliar scoring terms where they are used.
- Specify visual hierarchy, spacing, typography, colours and consistent feedback so the next action is easy to find.
- Design forms with sensible defaults, clear required fields, validation beside the relevant field and preservation of entered values after errors.
- Include empty, loading, saving, success and error states. Make save status and recovery steps clear.
- Address accessibility: keyboard operation, visible focus, labelled controls, readable contrast, text resizing and information that does not depend on colour alone.
- Check layout on the supported screen sizes; use scrolling intentionally for wide tables and keep important actions reachable.
- Make rankings and scores understandable. Distinguish AI suggestions from recorded human decisions and show the relevant evidence or explanation.
- Keep administration tasks easy to locate for the administrator and everyday tasks clear for ordinary users.
- Define usability acceptance criteria, such as completing the main task without developer help, understanding whether a record saved and recovering from an invalid entry.
- Check key journeys with a representative user when available. Record what was observed, what remains untested and the changes needed.

### 2b. Technical design

- Main components and their responsibilities.
- Data structure and persistence.
- Where the application runs and its supported devices.
- Access permissions, where relevant.
- Error handling, backups and recovery.
- Any AI models, evidence sources and limitations.

Keep the design proportionate to the application.

## 3. Plan

- Maintain a prioritised TASKS.md.
- Divide work into small features, each with a clear completion check.
- Distinguish the current release from future enhancements.

## 4. Build

- Build in small, reviewable steps, one feature at a time.
- Save working changes in Git when working in a Git repository.
- Reuse existing functionality where appropriate.
- Keep configuration and secrets separate from code.
- Avoid unnecessary dependencies and complexity.
- Update documentation alongside implementation.

## 5. Verify

- Check each acceptance criterion.
- Use automated tests for important calculations, validation and data operations where appropriate.
- Check the main user journeys manually.
- Check usability as well as correctness: navigation, labels, form feedback, save status and recovery from mistakes.
- Check keyboard access, focus, contrast and the supported screen sizes for changed interfaces.
- Record representative-user feedback when available; do not describe a developer walkthrough as user testing.
- Check invalid inputs, missing data and meaningful failure cases.
- For saved data, verify refresh and restart behaviour.
- For upgrades, verify that existing data is preserved.
- Never claim a check passed unless it was actually run.
- State clearly what remains untested.

Example acceptance criterion: A committee member records a decision, closes the application, reopens it and sees the same decision and its date.

## 6. Document

- Keep README.md accurate.
- Provide beginner-friendly installation and startup instructions.
- Add separate user and administrator guidance where needed.
- Document data locations, configuration and dependencies.
- Explain backup, update and recovery procedures.
- Include GitHub update instructions where GitHub is used.

## 7. Release and maintain

- Package a tested, numbered version.
- Record the version and changes in CHANGELOG.md.
- Keep a recovery route to the previous working version.
- Report what changed, what was tested and any remaining issues.

## Standard requirements

- Persistence: records survive refreshes, closing the browser and restarting the computer.
- Simple startup: provide a clear launcher or website address.
- Safe updates: preserve existing databases and imported files; back up before database changes.
- Clear errors: explain what happened and what the user should do next.
- Separate code and data: keep passwords, private documents and live databases out of GitHub.
- Transparent AI: distinguish source evidence, calculations and AI suggestions; flag missing evidence.
- Reproducible setup: record required software and dependencies so another computer can run it.

## Suggested starter structure

```text
project-name/
  README.md                 # What it does and how to run it
  PROJECT_BRIEF.md          # Problem, users, scope and success criteria
  DESIGN.md                 # Screens, data, components and decisions
  TASKS.md                  # Planned work and progress
  CHANGELOG.md              # Changes in each release
  .gitignore               # Files Git must exclude
  requirements.txt         # Python dependencies
  src/                     # Application code
  tests/                   # Checks for important behaviour
  docs/                    # User and administrator guides
  sample_data/             # Safe demonstration data
```

Live data and backups should have a separate, documented location. Small applications can start with fewer files and add structure as needed.

To reuse this approach across repositories, create a GitHub template repository containing the starter structure and these instructions. Keep each application's specific requirements in its own PROJECT_BRIEF.md.
