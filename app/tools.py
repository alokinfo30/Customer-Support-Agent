import os
import logging
# Replace the broad import with specific module targets:
from crewai_tools import SerperDevTool
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import WebsiteSearchTool
from typing import Optional

logger = logging.getLogger(__name__)

class SupportTools:
    """Centralized tool configuration for support agents"""
    
    def __init__(self):
        self.search_tool = None
        self.scrape_tool = None
        self.docs_scrape_tool = None
        
        # Initialize tools if API keys are available
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize tools with available API keys"""
        try:
            # Search tool (requires Serper API key)
            serper_key = os.getenv('SERPER_API_KEY')
            if serper_key:
                self.search_tool = SerperDevTool(api_key=serper_key)
                logger.info("✅ Search tool initialized")
            else:
                logger.warning("⚠️ Search tool not initialized (SERPER_API_KEY missing)")
            
            # Scrape tool - no API key required
            self.scrape_tool = ScrapeWebsiteTool()
            logger.info("✅ Scrape tool initialized")
            
            # Documentation scrape tool
            self.docs_scrape_tool = ScrapeWebsiteTool(
                website_url="https://docs.crewai.com/en/enterprise/guides/kickoff-crew"
            )
            logger.info("✅ Documentation scrape tool initialized")
            
        except Exception as e:
            logger.error(f"Error initializing tools: {str(e)}")
    
    def get_search_tool(self):
        """Get search tool"""
        return self.search_tool
    
    def get_scrape_tool(self):
        """Get scrape tool"""
        return self.scrape_tool
    
    def get_docs_scrape_tool(self):
        """Get documentation scrape tool"""
        return self.docs_scrape_tool

# Singleton instance
support_tools = SupportTools()