# Customer-Support-Agent
Multi-Agent Customer Support Automation system using CrewAI and OpenRouter handle asynchronous task



CustomerSupportAgent/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── agents.py
│   ├── tasks.py
│   ├── crew.py
│   ├── model_manager.py
│   ├── tools.py
│   └── utils.py
├── templates/
│   └── dashboard.html
├── static/
│   ├── style.css
│   └── script.js
├── data/
│   ├── knowledge_base/
│   └── conversations/
├── logs/
├── .env
├── .gitignore
├── requirements.txt
├── test_openrouter.py
├── generate_secret.py
├── run_support.py
└── README.md




## Quick Start

Follow these steps to set up and run the project on Windows (using PowerShell).

1.  **Clone the repository and navigate into the project directory.**



# Deactivate if you're inside the (.venv)
deactivate

# Remove the old virtual environment directory
Remove-Item -Recurse -Force .venv


2.  **Create and activate a virtual environment:**
    ```powershell
    # Use the Python launcher 'py' on Windows for reliability
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Install the required dependencies:**
    ```powershell
    # Upgrade pip and install packages from requirements.txt
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    -   Rename the `.env.example` file (if you have one) to `.env`.
    -   Get an API key from OpenRouter.
    -   Add your `OPENROUTER_API_KEY` to the `.env` file.
    -   Generate a secret key for Flask:
        ```powershell
        python generate_secret.py
        ```
        This will also add the `SECRET_KEY` to your `.env` file.

5.  **Test the OpenRouter configuration:**
    ```powershell
    python test_openrouter.py
    ```

6.  **Run the web application:**
    ```powershell
    python -m app.main
    ```

7.  **Open your browser** and navigate to `http://localhost:5000`.

📊 Model Configuration Summary
Agent	Model	Purpose
Support Agent	openai/gpt-4o-mini	Primary support response
QA Agent	mistralai/mixtral-8x22b-instruct	Quality assurance review
Escalation Agent	meta-llama/llama-3.1-8b-instruct	Complex issue handling
Analytics Agent	deepseek/deepseek-chat	Pattern analysis
✅ Six Key Elements Implemented
Role Playing ✅ - Each agent has a distinct role, goal, and backstory

Focus ✅ - Clear objectives and scope for each agent

Tools ✅ - Search, scrape, and documentation tools

Cooperation ✅ - Agents can delegate and work together

Guardrails ✅ - Clear boundaries and quality checks

Memory ✅ - Agents remember past interactions




.gitignore file ensures that:

No sensitive data is committed (API keys, passwords)

No compiled files are committed (pycache, pyc)

No database files are committed (sqlite, etc.)

No IDE files are committed (vscode, idea)

No OS files are committed (.DS_Store, Thumbs.db)

No logs are committed

No large data files are committed

Directory structure is preserved with .gitkeep files
