document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.getElementById('submitBtn');
    const escalateBtn = document.getElementById('escalateBtn');
    const customerInput = document.getElementById('customer');
    const personInput = document.getElementById('person');
    const inquiryInput = document.getElementById('inquiry');
    const processing = document.getElementById('processing');
    const response = document.getElementById('response');
    const responseContent = document.getElementById('responseContent');
    const responseCustomer = document.getElementById('responseCustomer');
    const responseTime = document.getElementById('responseTime');
    const progressLog = document.getElementById('progressLog');
    const copyBtn = document.getElementById('copyBtn');

    // Load models on startup
    async function loadModels() {
        try {
            const response = await fetch('/api/models');
            const data = await response.json();
            
            const modelList = document.getElementById('modelList');
            modelList.innerHTML = '';
            
            if (data.status === 'success') {
                const models = data.models;
                const allModels = [models.primary, ...models.fallbacks];
                
                allModels.forEach(model => {
                    if (model.trim()) {
                        const div = document.createElement('div');
                        div.className = 'model-item';
                        const isAvailable = models.available.includes(model);
                        if (!isAvailable) {
                            div.classList.add('unavailable');
                        }
                        div.textContent = `${model} ${isAvailable ? '✅' : '❌'}`;
                        modelList.appendChild(div);
                    }
                });
            }
        } catch (error) {
            console.error('Error loading models:', error);
        }
    }

    // Update agent status
    function updateAgentStatus(status, message) {
        const statusMap = {
            'idle': { agent1: '⏳ Support Agent: Idle', agent2: '⏳ QA Agent: Idle', agent3: '⏳ Memory: Active' },
            'searching': { agent1: '🔍 Support Agent: Searching Knowledge Base...', agent2: '⏳ QA Agent: Waiting', agent3: '🧠 Memory: Loading' },
            'analyzing': { agent1: '📝 Support Agent: Analyzing Inquiry...', agent2: '⏳ QA Agent: Waiting', agent3: '🧠 Memory: Processing' },
            'drafting': { agent1: '✏️ Support Agent: Drafting Response...', agent2: '⏳ QA Agent: Waiting', agent3: '🧠 Memory: Active' },
            'reviewing': { agent1: '✅ Support Agent: Complete', agent2: '🔍 QA Agent: Reviewing...', agent3: '🧠 Memory: Active' },
            'complete': { agent1: '✅ Support Agent: Complete', agent2: '✅ QA Agent: Complete', agent3: '✅ Memory: Updated' },
            'error': { agent1: '❌ Support Agent: Error', agent2: '❌ QA Agent: Error', agent3: '❌ Memory: Error' }
        };

        const statuses = statusMap[status] || statusMap.idle;
        document.getElementById('agent1').textContent = statuses.agent1;
        document.getElementById('agent2').textContent = statuses.agent2;
        document.getElementById('agent3').textContent = statuses.agent3;
        
        if (message) {
            const logEntry = document.createElement('div');
            logEntry.textContent = `🔄 ${new Date().toLocaleTimeString()}: ${message}`;
            progressLog.appendChild(logEntry);
            progressLog.scrollTop = progressLog.scrollHeight;
        }
    }

    // Handle support submission
    async function handleSupport(escalate = false) {
        const customer = customerInput.value.trim();
        const person = personInput.value.trim();
        const inquiry = inquiryInput.value.trim();

        if (!inquiry) {
            alert('Please enter an inquiry');
            return;
        }

        // Show processing
        processing.classList.remove('hidden');
        response.classList.add('hidden');
        progressLog.innerHTML = '';
        submitBtn.disabled = true;
        escalateBtn.disabled = true;
        
        updateAgentStatus('idle', 'Starting support process...');

        try {
            const endpoint = escalate ? '/api/support/escalate' : '/api/support';
            const payload = { customer, person, inquiry };
            
            if (escalate) {
                payload.complexity = 'high';
            }

            updateAgentStatus('searching', 'Initializing support agents...');
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                updateAgentStatus('complete', 'Support process completed successfully!');
                displayResponse(data.result, customer, person);
            } else {
                updateAgentStatus('error', `Error: ${data.error || 'Unknown error'}`);
                alert(`Error: ${data.error || 'Failed to process inquiry'}`);
            }
        } catch (error) {
            console.error('Error:', error);
            updateAgentStatus('error', `Network error: ${error.message}`);
            alert('Error processing inquiry. Please try again.');
        } finally {
            processing.classList.add('hidden');
            submitBtn.disabled = false;
            escalateBtn.disabled = false;
        }
    }

    // Display response
    function displayResponse(result, customer, person) {
        response.classList.remove('hidden');
        responseCustomer.textContent = `👤 ${customer} (${person})`;
        responseTime.textContent = `🕐 ${new Date().toLocaleString()}`;
        
        let content = result.response || result.message || 'No response content';
        
        // Convert markdown-like formatting to HTML
        content = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            .replace(/^\* (.*$)/gm, '<li>$1</li>')
            .replace(/\n/g, '<br>');
        
        // Wrap lists
        content = content.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
        
        responseContent.innerHTML = content;
        
        // Scroll to response
        response.scrollIntoView({ behavior: 'smooth' });
    }

    // Copy response
    copyBtn.addEventListener('click', function() {
        const text = responseContent.textContent;
        navigator.clipboard.writeText(text).then(() => {
            const original = this.textContent;
            this.textContent = '✅ Copied!';
            setTimeout(() => {
                this.textContent = original;
            }, 2000);
        }).catch(() => {
            // Fallback
            const range = document.createRange();
            range.selectNode(responseContent);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            document.execCommand('copy');
            const original = this.textContent;
            this.textContent = '✅ Copied!';
            setTimeout(() => {
                this.textContent = original;
            }, 2000);
        });
    });

    // Example cards
    document.querySelectorAll('.example-card').forEach(card => {
        card.addEventListener('click', function() {
            const inquiry = this.dataset.inquiry;
            const customer = this.dataset.customer;
            const person = this.dataset.person;
            
            if (inquiry) inquiryInput.value = inquiry;
            if (customer) customerInput.value = customer;
            if (person) personInput.value = person;
            
            // Auto-submit
            handleSupport(false);
        });
    });

    // Button events
    submitBtn.addEventListener('click', () => handleSupport(false));
    escalateBtn.addEventListener('click', () => handleSupport(true));

    // Enter key support
    inquiryInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            handleSupport(false);
        }
    });

    // Initialize
    loadModels();
    updateAgentStatus('idle', 'Ready to assist with your support needs!');
    console.log('🤖 Customer Support Agent loaded successfully!');
});