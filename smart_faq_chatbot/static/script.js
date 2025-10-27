const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = content;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;
    
    // Add user message
    addMessage(question, true);
    userInput.value = '';
    
    // Show loading
    sendBtn.textContent = 'Thinking...';
    sendBtn.disabled = true;
    
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        addMessage(data.answer);
        
    } catch (error) {
        addMessage('Sorry, I encountered an error. Please try again.');
    }
    
    // Reset button
    sendBtn.textContent = 'Send';
    sendBtn.disabled = false;
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Welcome message
addMessage("Hi! I'm your Indian cities travel assistant. Ask me about Delhi, Mumbai, Jaipur, or any other destination!");