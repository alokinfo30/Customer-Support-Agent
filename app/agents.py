from crewai import Agent
import os
import logging
from app.model_manager import model_manager
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

class SupportAgents:
    """
    Define all support agents with OpenRouter support
    Six key elements:
    1. Role Playing - Each agent has a distinct role
    2. Focus - Clear goals and backstories
    3. Tools - Agents can use tools for research
    4. Cooperation - Agents work together
    5. Guardrails - Clear boundaries and expectations
    6. Memory - Agents remember past interactions
    """
    
    def __init__(self):
        self.model_manager = model_manager
    
    def _create_llm(self, config: dict):
        """Pass native string to bypass Pydantic validation mismatches"""
        model = config['model']
        
        # Ensures the model string starts with 'openrouter/' so CrewAI routes it correctly
        if not model.startswith("openrouter/"):
            return f"openrouter/{model}"
            
        return model
    
    def create_support_agent(self, tools: list = None):
        """
        Create the Senior Support Representative Agent
        Role: Support Specialist
        Focus: Friendly and helpful support
        Tools: Can use search and scrape tools
        """
        config = self.model_manager.get_model_config('support')
        llm = self._create_llm(config)
        
        return Agent(
            role="Senior Support Representative",
            goal="Be the most friendly and helpful support representative in your team",
            backstory=(
                "You work at crewAI (https://crewai.com) and are now working on providing "
                "support to {customer}, a super important customer for your company.\n\n"
                "Your responsibilities include:\n"
                "- Providing friendly and helpful support\n"
                "- Making sure to provide full complete answers\n"
                "- Making no assumptions\n"
                "- Using all available tools to find accurate information\n"
                "- Maintaining a professional yet friendly tone"
            ),
            allow_delegation=False,
            verbose=True,
            llm=llm,
            tools=tools or []
        )
    
    def create_qa_agent(self):
        """
        Create the Support Quality Assurance Specialist Agent
        Role: Quality Assurance
        Focus: Ensuring support quality
        Cooperation: Can review and improve responses
        """
        config = self.model_manager.get_model_config('qa')
        llm = self._create_llm(config)
        
        return Agent(
            role="Support Quality Assurance Specialist",
            goal="Get recognition for providing the best support quality assurance in your team",
            backstory=(
                "You work at crewAI (https://crewai.com) and are now working with your team "
                "on a request from {customer} ensuring that the support representative is "
                "providing the best support possible.\n\n"
                "Your responsibilities include:\n"
                "- Reviewing support responses for quality\n"
                "- Ensuring complete and accurate answers\n"
                "- Checking for proper references and sources\n"
                "- Maintaining a helpful and friendly tone\n"
                "- Flagging any gaps or assumptions"
            ),
            allow_delegation=True,  # Can delegate back to support agent
            verbose=True,
            llm=llm
        )
    
    def create_escalation_agent(self):
        """
        Create the Escalation Specialist Agent
        Role: Escalation Handler
        Focus: Handling complex issues
        Guardrails: Knows when to escalate
        """
        config = self.model_manager.get_model_config('escalation')
        llm = self._create_llm(config)
        
        return Agent(
            role="Escalation Specialist",
            goal="Handle complex customer issues that require advanced expertise",
            backstory=(
                "You work at crewAI (https://crewai.com) and are the escalation point "
                "for complex technical issues.\n\n"
                "Your responsibilities include:\n"
                "- Handling complex technical inquiries\n"
                "- Coordinating with engineering teams\n"
                "- Providing advanced solutions\n"
                "- Ensuring customer satisfaction"
            ),
            allow_delegation=True,
            verbose=True,
            llm=llm
        )
    
    def create_analytics_agent(self):
        """
        Create the Analytics Agent
        Role: Data Analyst
        Focus: Analyzing support patterns
        Memory: Learns from past interactions
        """
        config = self.model_manager.get_model_config('analytics')
        llm = self._create_llm(config)
        
        return Agent(
            role="Support Analytics Specialist",
            goal="Analyze support interactions to improve customer experience",
            backstory=(
                "You work at crewAI (https://crewai.com) and analyze support patterns "
                "to continuously improve the customer experience.\n\n"
                "Your responsibilities include:\n"
                "- Analyzing support interactions\n"
                "- Identifying common issues\n"
                "- Suggesting improvements\n"
                "- Tracking customer satisfaction"
            ),
            allow_delegation=False,
            verbose=True,
            llm=llm
        )