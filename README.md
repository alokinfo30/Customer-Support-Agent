# Customer-Support-Agent
Multi-Agent Customer Support Automation system using CrewAI and OpenRouter



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




Quick Start Commands
powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate secret key
python generate_secret.py

# 3. Get OpenRouter API key from: https://openrouter.ai/keys
# 4. Update .env with your OpenRouter API key

# 5. Test OpenRouter
python test_openrouter.py

# 6. Run the application
python -m app.main

# 7. Open browser: http://localhost:5000

python -m venv .venv
.\.venv\Scripts\Activate.ps1
.venv\Scripts\activate

python -m pip install --upgrade pip setuptools wheel
 pip install "numpy>=2.0.0"  
pip install crewai langchain-openai

pip install -r requirements.txt



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