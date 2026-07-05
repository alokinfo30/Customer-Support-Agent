from crewai import Crew
import os
import logging
from typing import List, Dict, Optional
from app.model_manager import model_manager

logger = logging.getLogger(__name__)

class SupportCrew:
    """
    Orchestrate the customer support process
    Features:
    1. Memory - Remembers past interactions
    2. Cooperation - Agents work together
    3. Guardrails - Clear boundaries
    4. Role Playing - Each agent has a role
    5. Focus - Clear goals
    6. Tools - Agents have access to tools
    """
    
    def __init__(self):
        try:
            from app.agents import SupportAgents
            from app.tasks import SupportTasks
            from app.tools import support_tools
            
            self.agents = SupportAgents()
            self.tasks = SupportTasks()
            self.tools = support_tools
            
            self.verbose = os.getenv('DEBUG', 'False').lower() == 'true'
            self.model_manager = model_manager
            
            # Enable memory for learning from interactions
            self.memory_enabled = os.getenv('MEMORY_ENABLED', 'False').lower() == 'false'
            
            logger.info("SupportCrew initialized with memory: {}".format(self.memory_enabled))
            
            # Test models
            self._test_models()
            
        except Exception as e:
            logger.error(f"Failed to initialize SupportCrew: {str(e)}")
            raise
    
    def _test_models(self):
        """Test all configured models"""
        logger.info("Testing all configured models...")
        results = self.model_manager.test_providers()
        
        available_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        logger.info(f"Models available: {available_count}/{total_count}")
        
        if available_count == 0:
            logger.warning("WARNING: No models are available! Check your OpenRouter API key.")
        else:
            logger.info(f"Available models: {[m for m, v in results.items() if v]}")
    
    def process_inquiry(self, customer: str, person: str, inquiry: str, use_tools: bool = True) -> Dict:
        """
        Process a customer inquiry through the support pipeline
        """
        try:
            logger.info("=" * 60)
            logger.info(f"Processing inquiry from {customer} ({person})")
            logger.info(f"Inquiry: {inquiry[:100]}...")
            logger.info("=" * 60)
            
            # Prepare tools if needed
            tools = []
            if use_tools:
                if self.tools.get_docs_scrape_tool():
                    tools.append(self.tools.get_docs_scrape_tool())
                if self.tools.get_search_tool():
                    tools.append(self.tools.get_search_tool())
                if self.tools.get_scrape_tool():
                    tools.append(self.tools.get_scrape_tool())
            
            # Step 1: Create support agent with tools
            support_agent = self.agents.create_support_agent(tools)
            
            # Step 2: Create QA agent
            qa_agent = self.agents.create_qa_agent()
            
            # Step 3: Create tasks
            inquiry_task = self.tasks.create_inquiry_resolution_task(support_agent, tools)
            qa_task = self.tasks.create_qa_review_task(qa_agent)
            
            # Step 4: Create crew with memory enabled
            crew = Crew(
                agents=[support_agent, qa_agent],
                tasks=[inquiry_task, qa_task],
                verbose=self.verbose,
                memory=self.memory_enabled,
                embedder={
                        "provider": "openrouter",
                        "config": {
                            "model": "google/text-embedding-004", # Or any embedding model supported by OpenRouter
                            "api_key": os.getenv("OPENROUTER_API_KEY")
                        }
                    },
                cache=True  # Cache results for efficiency
            )
            
            # Step 5: Execute the crew
            logger.info("Starting support crew execution...")
            result = crew.kickoff(
                inputs={
                    "customer": customer,
                    "person": person,
                    "inquiry": inquiry
                }
            )
            
            logger.info("Support crew execution completed")
            
            if not result:
                raise Exception("Crew execution returned no result. This might be due to an internal error in the crew.")

            return {
                "status": "success",
                "customer": customer,
                "person": person,
                "inquiry": inquiry,
                # The result from a sequential crew is the output of the last task.
                # It's usually a string, so str() is okay, but we check for None first.
                "response": result,
                "memory_enabled": self.memory_enabled
            }
            
        except Exception as e:
            logger.error(f"Support processing failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e),
                "customer": customer,
                "person": person,
                "inquiry": inquiry
            }
    
    def process_with_escalation(self, customer: str, person: str, inquiry: str, complexity: str = "high") -> Dict:
        """
        Process a complex inquiry with escalation handling
        """
        try:
            logger.info("=" * 60)
            logger.info(f"Processing complex inquiry from {customer} with escalation")
            logger.info("=" * 60)
            
            # Create all agents
            support_agent = self.agents.create_support_agent([])
            qa_agent = self.agents.create_qa_agent()
            escalation_agent = self.agents.create_escalation_agent()
            
            # Create tasks
            inquiry_task = self.tasks.create_inquiry_resolution_task(support_agent, [])
            escalation_task = self.tasks.create_escalation_task(escalation_agent)
            
            # Create crew with all agents
            crew = Crew(
                agents=[support_agent, escalation_agent, qa_agent],
                tasks=[inquiry_task, escalation_task],
                verbose=self.verbose,
                memory=self.memory_enabled,
                  embedder={
                        "provider": "openrouter",
                        "config": {
                            "model": "google/text-embedding-004", # Or any embedding model supported by OpenRouter
                            "api_key": os.getenv("OPENROUTER_API_KEY")
                        }
                    }
            )
            
            result = crew.kickoff(
                inputs={
                    "customer": customer,
                    "person": person,
                    "inquiry": inquiry,
                    "complexity": complexity
                }
            )
            
            return {
                "status": "success",
                "customer": customer,
                "person": person,
                "inquiry": inquiry,
                "response": str(result),
                "escalation_handled": True
            }
            
        except Exception as e:
            logger.error(f"Escalation processing failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e),
                "customer": customer,
                "person": person,
                "inquiry": inquiry
            }
    
    def analyze_support_patterns(self, conversations: List[Dict]) -> Dict:
        """
        Analyze support patterns for improvement
        """
        try:
            logger.info("Analyzing support patterns...")
            
            analytics_agent = self.agents.create_analytics_agent()
            analytics_task = self.tasks.create_analytics_task(analytics_agent)
            
            crew = Crew(
                agents=[analytics_agent],
                tasks=[analytics_task],
                verbose=self.verbose,
                memory=self.memory_enabled,
                  embedder={
                        "provider": "openrouter",
                        "config": {
                            "model": "google/text-embedding-004", # Or any embedding model supported by OpenRouter
                            "api_key": os.getenv("OPENROUTER_API_KEY")
                        }
                    },
            )
            
            result = crew.kickoff(
                inputs={
                    "conversations": conversations
                }
            )
            
            return {
                "status": "success",
                "analysis": str(result)
            }
            
        except Exception as e:
            logger.error(f"Analytics failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e)
            }