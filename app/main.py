import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import secrets
import bleach
from datetime import datetime
import traceback

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
    template_folder='../templates',
    static_folder='../static'
)

app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    app.secret_key = secrets.token_urlsafe(32)
    logger.warning(f"Generated temporary SECRET_KEY")

app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
app.config['SESSION_COOKIE_HTTPONLY'] = os.getenv('SESSION_COOKIE_HTTPONLY', 'True').lower() == 'true'
app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')

CORS(app, resources={r"/api/*": {"origins": "*"}})

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[os.getenv('RATELIMIT_DEFAULT', '1000/day')],
    enabled=os.getenv('RATELIMIT_ENABLED', 'False').lower() == 'true'
)

def validate_openrouter():
    """Validate OpenRouter configuration"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        logger.error("OPENROUTER_API_KEY not found")
        return False
    if not api_key.startswith('sk-or-'):
        logger.error("Invalid OpenRouter API key format")
        return False
    logger.info("✅ OpenRouter API key validated")
    return True

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('dashboard.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        from app.model_manager import model_manager
        
        model_status = model_manager.test_providers()
        available = [m for m, v in model_status.items() if v]
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'openrouter_valid': validate_openrouter(),
            'python_version': sys.version,
            'providers': {
                'available': available,
                'total': len(model_status),
                'status': model_status
            },
            'memory_enabled': os.getenv('MEMORY_ENABLED', 'True').lower() == 'true'
        })
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/support', methods=['POST'])
@limiter.limit("50/day")
def handle_support():
    """Handle a customer support inquiry"""
    try:
        logger.info("=" * 50)
        logger.info("Received support request")
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided',
                'status': 'error'
            }), 400
        
        customer = bleach.clean(data.get('customer', '').strip())
        person = bleach.clean(data.get('person', '').strip())
        inquiry = bleach.clean(data.get('inquiry', '').strip())
        
        if not customer:
            customer = "DeepLearningAI"
        if not person:
            person = "Customer"
        if not inquiry:
            return jsonify({
                'error': 'Inquiry is required',
                'status': 'error'
            }), 400
        
        if not validate_openrouter():
            return jsonify({
                'error': 'OpenRouter not configured',
                'status': 'error'
            }), 500
        
        # Process the inquiry
        from app.crew import SupportCrew
        crew = SupportCrew()
        
        result = crew.process_inquiry(customer, person, inquiry)
        
        return jsonify({
            'status': 'success',
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error handling support: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/support/escalate', methods=['POST'])
@limiter.limit("20/day")
def escalate_support():
    """Handle a complex support inquiry with escalation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided',
                'status': 'error'
            }), 400
        
        customer = bleach.clean(data.get('customer', 'DeepLearningAI').strip())
        person = bleach.clean(data.get('person', 'Customer').strip())
        inquiry = bleach.clean(data.get('inquiry', '').strip())
        complexity = bleach.clean(data.get('complexity', 'high').strip())
        
        if not inquiry:
            return jsonify({
                'error': 'Inquiry is required',
                'status': 'error'
            }), 400
        
        from app.crew import SupportCrew
        crew = SupportCrew()
        
        result = crew.process_with_escalation(customer, person, inquiry, complexity)
        
        return jsonify({
            'status': 'success',
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in escalation: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/analytics', methods=['POST'])
@limiter.limit("10/day")
def analyze_patterns():
    """Analyze support patterns"""
    try:
        data = request.get_json()
        conversations = data.get('conversations', [])
        
        from app.crew import SupportCrew
        crew = SupportCrew()
        
        result = crew.analyze_support_patterns(conversations)
        
        return jsonify({
            'status': 'success',
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in analytics: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    try:
        from app.model_manager import model_manager
        results = model_manager.test_providers()
        available = [m for m, v in results.items() if v]
        
        return jsonify({
            'status': 'success',
            'models': {
                'primary': os.getenv('OPENROUTER_PRIMARY_MODEL', 'openai/gpt-4o-mini'),
                'fallbacks': os.getenv('OPENROUTER_FALLBACK_MODELS', '').split(','),
                'available': available,
                'all_tested': results
            }
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🤖 CUSTOMER SUPPORT AGENT (OpenRouter)")
    logger.info("=" * 60)
    
    if not validate_openrouter():
        logger.warning("⚠️ OpenRouter not configured. Get API key from: https://openrouter.ai/keys")
    
    try:
        from app.model_manager import model_manager
        model_status = model_manager.test_providers()
        available = [m for m, v in model_status.items() if v]
        if available:
            logger.info(f"✅ Available models: {available}")
        else:
            logger.warning("❌ No models available! Check your OpenRouter API key.")
    except Exception as e:
        logger.error(f"Error testing models: {str(e)}")
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)