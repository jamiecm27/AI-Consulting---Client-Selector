# AI Client Selection Engine
### AI-Assisted Decision Support for Student Consulting

**Python | SQLite | OpenAI API | Responsible AI | Decision Support**

## About Me

I am an Economics and Philosophy student at the University of St Andrews and a member of the St Andrews University Consulting Society.

I am particularly interested in management consulting, private equity and the opportunities artificial intelligence creates for improving business decision-making.

I developed this prototype to explore how AI could help consulting organisations make more consistent, transparent and evidence-based decisions while retaining human oversight.

## 1. The Business Problem

Student consulting societies have limited resources. They must decide which businesses to support, balancing competing objectives such as client impact, project feasibility, student development and the needs of applicants.

The St Andrews University Consulting Society receives more requests for consulting support than it can accommodate.

This creates a resource-allocation problem: **how can a consulting organisation select the projects that create the greatest overall value while ensuring decisions are fair and explainable?**

## 2. My Solution

The AI Client Selection Engine is a working prototype that supports the evaluation and prioritisation of prospective consulting projects.

It combines structured quantitative scoring with AI-generated qualitative analysis and human committee judgement.

The application enables users to:

- Register new business applications.
- Score businesses against four criteria.
- Adjust the relative importance of those criteria.
- Automatically calculate weighted rankings.
- Generate AI-assisted assessments of applications.
- Identify missing evidence and questions requiring further investigation.
- Record committee decisions and the reasons behind them.
- Maintain an auditable decision history.
- Export rankings and decisions to CSV files.

The application stores its records locally, allowing decisions and assessments to remain available between sessions.

## 3. Evaluation Framework

Each application is evaluated against four criteria.

| Criterion | Assessment focus |
|---|---|
| Impact | Potential benefits of the consulting project |
| Feasibility | Whether students can realistically deliver the work |
| Student Learning | Opportunities to develop practical consulting skills |
| Business Need | The applicant's need for external consulting support |

Each criterion is scored from 1 to 10.

Users can adjust the percentage weighting assigned to each criterion, provided the total equals 100%.

The final weighted score is calculated as:

**Weighted Score = Σ (Criterion Score × Criterion Weight / 100)**

This makes the prioritisation methodology explicit and allows decision-makers to explore how different organisational priorities affect the rankings.

## 4. AI-Assisted Assessment

The application integrates with the OpenAI API to analyse application descriptions.

The AI can generate:

- A concise application summary.
- Suggested scores for the four evaluation criteria.
- Explanations supporting those scores.
- Evidence gaps and uncertainties.
- Follow-up questions for applicants.
- Caveats requiring human consideration.

AI-generated scores remain separate from human-entered scores.

**The AI does not automatically change rankings or make committee decisions.**

This distinction is deliberate: the system is designed to improve human judgement rather than replace it.

## 5. Responsible AI and Governance

Responsible AI is a central design consideration.

The prototype incorporates several safeguards:

**Human oversight:** Committee members retain responsibility for selection decisions.

**Transparency:** Scores are supported by explicit evaluation criteria and explanations.

**Accountability:** Decisions, reasons and changes are recorded in an audit history.

**Uncertainty:** AI assessments identify missing information rather than treating incomplete applications as conclusive evidence.

**Data protection:** Users are instructed to submit only fictional, anonymised or explicitly authorised information to the external AI service.

**Separation of roles:** AI recommendations do not overwrite human assessments.

The prototype does not eliminate the possibility of bias or incorrect AI outputs. Assessments require human verification.

## 6. Technical Architecture

The application is designed to be lightweight and straightforward to run locally.

| Component | Technology |
|---|---|
| Backend | Python 3.13 |
| User interface | HTML, CSS and JavaScript |
| Local database | SQLite |
| AI integration | OpenAI API |
| Data exports | CSV |
| Hosting | Local computer |

The application uses Python's standard library for its core functionality, avoiding complex external dependencies.

It has been tested on Windows 11 ARM64.

### Project structure

```text
ai-client-selection-engine/
├── app.py
├── index.html
└── README.md
```

The SQLite database is created locally when the application runs and should not be committed to GitHub.

## 7. Running the Application

Install Python 3.13 or another compatible version of Python 3.

Download or clone this repository, open a terminal in the project folder and run:

```bash
python app.py
```

The application should open in a web browser.

The main dashboard works without an OpenAI API key.

To use the optional AI assessment feature, enter a valid OpenAI API key in the application. API usage may incur separate charges.

Never commit API keys or confidential client information to the repository.

## 8. Connection to Economics and Philosophy

My degree has influenced both the problem I chose and the design of the solution.

### Economics

The selection of consulting projects is a resource-allocation problem.

The society must allocate limited student time and expertise among competing opportunities.

Weighted scoring provides a practical framework for examining trade-offs, opportunity costs and different definitions of value.

It also raises questions about how organisations should measure outcomes that are not easily expressed financially.

### Philosophy

The project raises important questions about fairness, accountability and the appropriate role of AI in human decision-making.

For example:

- What makes a selection process fair?
- How should competing interests be balanced?
- Can quantitative scores adequately represent ethical considerations?
- Who should be accountable when AI recommendations influence decisions?
- How can organisations avoid treating apparently objective scores as unquestionable facts?

These questions informed the decision to keep AI recommendations separate from committee decisions.

## 9. Relevance to AI Advisory and Consulting

This project demonstrates how a relatively small AI implementation can address a genuine organisational challenge.

The underlying approach could also be adapted to commercial consulting environments, including opportunity screening, portfolio prioritisation, investment evaluation and operational decision support.

I am particularly interested in how private equity firms and their portfolio companies might apply similar techniques to improve decision-making across multiple businesses.

The project has given me practical experience in translating a business problem into an AI-supported workflow, designing evaluation criteria, considering governance risks and testing a working application.

## 10. Limitations and Future Development

This is a functional prototype, not a production-ready enterprise application.

Potential future improvements include:

- A separate application portal for businesses.
- User authentication and role-based permissions.
- More systematic evaluation of AI accuracy and bias.
- Comparison of human and AI assessments across larger datasets.
- Secure multi-user deployment.
- Improved reporting and visual analytics.

The current implementation is intended for demonstration and learning, using fictional or appropriately authorised data.

## 11. Project Status

**Working prototype — functional testing completed.**

Core features tested include persistent application records, weighted rankings, AI assessments, committee decisions, decision history and CSV exports.

The project has not been formally adopted by the St Andrews University Consulting Society.

---

**Developed as a personal AI consulting project inspired by my experience as a member of the St Andrews University Consulting Society.**
