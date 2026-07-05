import os
import logging
from typing import List, Dict, Optional, Any
from enum import Enum
import time
from openai import OpenAI

logger = logging.getLogger(__name__)

class FallbackStrategy(Enum):
    SEQUENTIAL = "sequential"
    RANDOM = "random"
    ROUND_ROBIN = "round_robin"

class OpenRouterManager:
    """
    Manages OpenRouter API with intelligent model routing and fallback
    No daily limits - pay-as-you-go with free tier support
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables!")
        
        self.base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self.app_url = os.getenv('OPENROUTER_APP_URL', 'http://localhost:5000')
        self.app_name = os.getenv('OPENROUTER_APP_NAME', 'Customer Support Agent')
        
        # Production environment check for app_url
        is_production = os.getenv('FLASK_ENV') == 'production'
        if is_production and 'localhost' in self.app_url:
            logger.warning("⚠️ WARNING: Running in production, but OPENROUTER_APP_URL is not set or is localhost.")
            logger.warning("   Set OPENROUTER_APP_URL to your public app URL in your production environment.")

        # Initialize OpenAI client with OpenRouter base URL
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": self.app_url,
                "X-Title": self.app_name
            }
        )
        
        # Model configuration
        self.primary_model = os.getenv('OPENROUTER_PRIMARY_MODEL', 'openai/gpt-4o-mini')
        self.fallback_models = self._get_fallback_models()
        
        # Agent-specific models
        self.agent_models = {
            'support': os.getenv('SUPPORT_AGENT_MODEL', self.primary_model),
            'qa': os.getenv('QA_AGENT_MODEL', self.primary_model),
            'escalation': os.getenv('ESCALATION_AGENT_MODEL', self.primary_model),
            'analytics': os.getenv('ANALYTICS_AGENT_MODEL', self.primary_model)
        }
        
        # Strategy
        strategy_name = os.getenv('MODEL_FALLBACK_STRATEGY', 'sequential')
        try:
            self.strategy = FallbackStrategy(strategy_name.lower())
        except ValueError:
            self.strategy = FallbackStrategy.SEQUENTIAL
        
        self._round_robin_counter = 0
        self._model_cache = {}
        self._last_test_time = 0
        self._cache_duration = 300  # 5 minutes
        
        logger.info("🚀 OpenRouter Manager initialized")
        logger.info(f"  Primary Model: {self.primary_model}")
        logger.info(f"  Fallback Models: {self.fallback_models}")
        
        # Test connection
        self._test_connection()
    
    def _get_fallback_models(self) -> List[str]:
        """Get fallback models from env or use defaults"""
        fallbacks = os.getenv('OPENROUTER_FALLBACK_MODELS', '')
        if fallbacks:
            return [m.strip() for m in fallbacks.split(',')]
        
        # Default fallbacks
        return [
            "mistralai/mixtral-8x22b-instruct",
            "meta-llama/llama-3.1-8b-instruct",
            "deepseek/deepseek-chat"
        ]
    
    def _test_connection(self):
        """Test OpenRouter connection"""
        try:
            response = self.client.chat.completions.create(
                model=self.primary_model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            logger.info("✅ OpenRouter connection successful")
        except Exception as e:
            logger.warning(f"⚠️ OpenRouter connection test failed: {str(e)}")
            logger.info("  Trying fallback models...")
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        current_time = time.time()
        
        if current_time - self._last_test_time < self._cache_duration:
            if self._model_cache:
                return self._model_cache
        
        all_models = [self.primary_model] + self.fallback_models
        available = []
        
        for model in all_models:
            if self._test_model(model):
                available.append(model)
        
        self._model_cache = available
        self._last_test_time = current_time
        
        return available
    
    def _test_model(self, model: str) -> bool:
        """Test if a model is available"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5,
                timeout=10
            )
            return True
        except Exception as e:
            logger.debug(f"Model {model} unavailable: {str(e)}")
            return False
    
    def get_next_model(self, preferred: Optional[str] = None) -> str:
        """Get the next available model based on strategy"""
        available = self.get_available_models()
        
        if not available:
            logger.warning("No available models, using primary model")
            return self.primary_model
        
        if preferred and preferred in available:
            return preferred
        
        if self.strategy == FallbackStrategy.SEQUENTIAL:
            return available[0]
        elif self.strategy == FallbackStrategy.RANDOM:
            import random
            return random.choice(available)
        elif self.strategy == FallbackStrategy.ROUND_ROBIN:
            model = available[self._round_robin_counter % len(available)]
            self._round_robin_counter += 1
            return model
        else:
            return available[0]
    
    def get_model_config(self, agent_type: str) -> Dict[str, Any]:
        """Get model configuration for an agent"""
        preferred = self.agent_models.get(agent_type, self.primary_model)
        chosen_model = self.get_next_model(preferred)
        
        logger.info(f"Agent {agent_type} using model: {chosen_model}")
        
        return {
            'model': chosen_model,
            'temperature': self._get_agent_temperature(agent_type),
            'client': self.client,
            'base_url': self.base_url
        }
    
    def _get_agent_temperature(self, agent_type: str) -> float:
        temperatures = {
            'support': 0.3,
            'qa': 0.2,
            'escalation': 0.4,
            'analytics': 0.5
        }
        return temperatures.get(agent_type.lower(), 0.3)
    
    def test_providers(self) -> Dict[str, bool]:
        """Test all configured models"""
        results = {}
        all_models = [self.primary_model] + self.fallback_models
        
        for model in all_models:
            try:
                logger.info(f"Testing {model}...")
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say OK"}],
                    max_tokens=10
                )
                results[model] = True
                logger.info(f"✅ {model} is available")
            except Exception as e:
                results[model] = False
                logger.warning(f"❌ {model} unavailable: {str(e)}")
        
        return results

# Singleton instance
model_manager = OpenRouterManager()