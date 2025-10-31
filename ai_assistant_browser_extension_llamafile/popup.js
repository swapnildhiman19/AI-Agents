const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const statusDiv = document.getElementById('status');

// Configuration
const LLAMAFILE_URL = 'http://localhost:8080/v1/chat/completions';
const MODEL_NAME = 'LLaMA_CPP'; // Adjust to your model name

// Add message to chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = content;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show status message
function showStatus(message, type = 'info') {
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
    statusDiv.classList.remove('hidden');
    
    if (type !== 'error') {
        setTimeout(() => {
            statusDiv.classList.add('hidden');
        }, 3000);
    }
}

// Query llamafile API
async function queryLlamafile(prompt) {
    try {
        const response = await fetch(LLAMAFILE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: MODEL_NAME,
                messages: [
                    {
                        role: 'system',
                        content: 'You are a helpful AI assistant built into a browser extension.'
                    },
                    {
                        role: 'user',
                        content: prompt
                    }
                ],
                temperature: 0.7,
                max_tokens: 200
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.choices[0].message.content;

    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Send message
async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;

    // Add user message
    addMessage(question, true);
    userInput.value = '';

    // Disable input
    sendBtn.disabled = true;
    sendBtn.textContent = 'Thinking...';
    showStatus('Asking AI...', 'info');

    try {
        // Query llamafile
        const answer = await queryLlamafile(question);
        
        // Add AI response
        addMessage(answer);
        showStatus('Response received', 'success');

    } catch (error) {
        addMessage('Sorry, I encountered an error. Make sure llamafile is running on localhost:8080');
        showStatus('Error: Could not connect to llamafile', 'error');
    } finally {
        // Re-enable input
        sendBtn.disabled = false;
        sendBtn.textContent = 'Send';
    }
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Welcome message
addMessage('Hi! I\'m your local AI assistant. Ask me anything!');
showStatus('Make sure llamafile is running on localhost:8080', 'info');
