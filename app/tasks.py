from crewai import Task
import logging

logger = logging.getLogger(__name__)

class SupportTasks:
    """
    Define all support tasks with clear objectives
    Tasks include:
    - Inquiry Resolution
    - Quality Assurance Review
    - Escalation Handling
    - Analytics Processing
    """
    
    def create_inquiry_resolution_task(self, agent, tools: list = None):
        """
        Create the primary inquiry resolution task
        Focus: Resolving customer inquiry
        Tools: Search and scrape tools
        Guardrails: Complete, accurate responses
        """
        return Task(
            description=(
                "{customer} just reached out with a super important ask:\n"
                "{inquiry}\n\n"
                "{person} from {customer} is the one that reached out. "
                "Make sure to use everything you know to provide the best support possible.\n\n"
                "Requirements:\n"
                "1. Provide a complete and accurate response\n"
                "2. Address all aspects of the question\n"
                "3. Include references to external data or solutions\n"
                "4. Leave no questions unanswered\n"
                "5. Maintain a helpful and friendly tone throughout"
            ),
            expected_output=(
                "A detailed, informative response to the customer's inquiry that addresses "
                "all aspects of their question.\n\n"
                "The response should include:\n"
                "- A clear and direct answer to the question\n"
                "- Step-by-step guidance if applicable\n"
                "- References to documentation or resources\n"
                "- A friendly and professional tone\n"
                "- Follow-up questions if clarification is needed"
            ),
            tools=tools or [],
            agent=agent
        )
    
    def create_qa_review_task(self, agent):
        """
        Create the quality assurance review task
        Focus: Ensuring response quality
        Guardrails: Verify completeness and accuracy
        """
        return Task(
            description=(
                "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
                "Ensure that the answer is comprehensive, accurate, and adheres to the "
                "high-quality standards expected for customer support.\n\n"
                "Review Checklist:\n"
                "1. Is the response complete and thorough?\n"
                "2. Are all parts of the inquiry addressed?\n"
                "3. Is the tone helpful and friendly?\n"
                "4. Are references and sources properly cited?\n"
                "5. Are there any assumptions made?\n"
                "6. Is the response well-supported with information?\n"
                "7. Does it leave any questions unanswered?"
            ),
            expected_output=(
                "A final, detailed, and informative response ready to be sent to the customer.\n\n"
                "The response should:\n"
                "- Fully address all aspects of the inquiry\n"
                "- Incorporate all relevant feedback\n"
                "- Maintain a professional yet friendly tone\n"
                "- Be concise and clear\n"
                "- Include all necessary details"
            ),
            agent=agent
        )
    
    def create_escalation_task(self, agent):
        """
        Create the escalation handling task
        Role: Complex issue resolution
        Guardrails: Know when to escalate
        """
        return Task(
            description=(
                "Handle escalated support issues that require advanced expertise.\n\n"
                "Requirements:\n"
                "1. Analyze the complexity of the issue\n"
                "2. Determine if escalation is needed\n"
                "3. Coordinate with appropriate teams\n"
                "4. Provide advanced solutions\n"
                "5. Ensure customer satisfaction"
            ),
            expected_output=(
                "A comprehensive resolution for complex support issues including:\n"
                "- Issue analysis and classification\n"
                "- Detailed solution or escalation path\n"
                "- Communication plan with customer\n"
                "- Timeline for resolution"
            ),
            agent=agent
        )
    
    def create_analytics_task(self, agent):
        """
        Create the analytics processing task
        Focus: Learning from interactions
        Memory: Patterns and improvements
        """
        return Task(
            description=(
                "Analyze support interactions and identify patterns for improvement.\n\n"
                "Analysis Areas:\n"
                "1. Common customer issues\n"
                "2. Response quality metrics\n"
                "3. Customer satisfaction indicators\n"
                "4. Knowledge base gaps\n"
                "5. Process improvement opportunities"
            ),
            expected_output=(
                "An analytical report containing:\n"
                "- Key insights from interactions\n"
                "- Pattern identification\n"
                "- Improvement recommendations\n"
                "- Customer satisfaction trends\n"
                "- Knowledge base updates needed"
            ),
            agent=agent
        )