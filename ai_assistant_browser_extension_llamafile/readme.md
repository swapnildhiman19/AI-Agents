Perfect! Here's a **complete guide** to building a browser extension that queries your local llamafile API. This will work in Chrome, Edge, Brave, and Firefox (with minor adjustments).

***

## **Project: AI Assistant Browser Extension**

### **What You'll Build**
A browser extension that:
- Has a popup with a chat interface
- Sends questions to your local llamafile (running on `localhost:8080`)
- Displays AI responses in real-time
- Works completely offline (no cloud API needed!)

***

## **Project Structure**

```
ai-assistant-extension/
├── manifest.json          # Extension configuration
├── popup.html            # Chat interface
├── popup.css             # Styling
├── popup.js              # Logic to call llamafile API
├── background.js         # Background service worker (optional)
├── icons/
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── README.md
```

***

## **Step-by-Step Implementation**

### **Step 1: Create `manifest.json`**

This is the configuration file for your extension:

```json
{
  "manifest_version": 3,
  "name": "Local AI Assistant",
  "version": "1.0",
  "description": "Chat with your local LLM powered by llamafile",
  "permissions": [
    "activeTab"
  ],
  "host_permissions": [
    "http://localhost:8080/*"
  ],
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

**Key parts:**
- `host_permissions`: Allows the extension to call your local llamafile API
- `action.default_popup`: The chat interface that appears when you click the extension icon

***

### **Step 2: Create `popup.html`**

The user interface for your chat:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local AI Assistant</title>
    <link rel="stylesheet" href="popup.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 AI Assistant</h1>
            <p class="subtitle">Powered by local llamafile</p>
        </header>
        
        <div id="chat-messages"></div>
        
        <div class="input-container">
            <textarea 
                id="user-input" 
                placeholder="Ask me anything..."
                rows="2"
            ></textarea>
            <button id="send-btn">Send</button>
        </div>
        
        <div id="status" class="status"></div>
    </div>
    
    <script src="popup.js"></script>
</body>
</html>
```

***

### **Step 3: Create `popup.css`**

Beautiful, modern styling:

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    width: 400px;
    height: 500px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
    height: 100%;
    display: flex;
    flex-direction: column;
    background: white;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px;
    text-align: center;
}

header h1 {
    font-size: 20px;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 12px;
    opacity: 0.9;
}

#chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
    background: #f8f9fa;
}

.message {
    margin-bottom: 12px;
    padding: 10px 12px;
    border-radius: 8px;
    max-width: 85%;
    word-wrap: break-word;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-message {
    background: #667eea;
    color: white;
    margin-left: auto;
}

.bot-message {
    background: white;
    color: #333;
    border: 1px solid #e0e0e0;
}

.input-container {
    padding: 15px;
    background: white;
    border-top: 1px solid #e0e0e0;
    display: flex;
    gap: 10px;
}

#user-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    resize: none;
    font-family: inherit;
}

#user-input:focus {
    outline: none;
    border-color: #667eea;
}

#send-btn {
    padding: 10px 20px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: background 0.2s;
}

#send-btn:hover {
    background: #5568d3;
}

#send-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.status {
    padding: 8px 15px;
    font-size: 12px;
    text-align: center;
    background: #fff3cd;
    color: #856404;
    border-top: 1px solid #ffeaa7;
}

.status.hidden {
    display: none;
}

.status.error {
    background: #f8d7da;
    color: #721c24;
    border-color: #f5c6cb;
}

.status.success {
    background: #d4edda;
    color: #155724;
    border-color: #c3e6cb;
}

/* Custom scrollbar */
#chat-messages::-webkit-scrollbar {
    width: 6px;
}

#chat-messages::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
}

#chat-messages::-webkit-scrollbar-thumb:hover {
    background: #555;
}
```

***

### **Step 4: Create `popup.js`**

The logic to communicate with your llamafile API:

```javascript
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
```

***

### **Step 5: Create Icons**

Create simple icon images or download free AI icons. Save them as:
- `icons/icon16.png` (16×16)
- `icons/icon48.png` (48×48)
- `icons/icon128.png` (128×128)

**Quick way:** Use a free icon generator or emoji as PNG.

***

### **Step 6: Load the Extension**

**In Chrome/Edge/Brave:**
1. Open `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select your `ai-assistant-extension` folder

**In Firefox:**
1. Open `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on"
3. Select the `manifest.json` file

***

### **Step 7: Test It!**

1. **Start your llamafile:**
   ```bash
   ./Meta-Llama-3.1-8B-Instruct.Q8_0.llamafile
   ```

2. **Click the extension icon** in your browser toolbar

3. **Ask a question** like "What is Python?" and watch the AI respond!

---

## **Enhancements You Can Add**

1. **Chat history:** Store conversation in `chrome.storage.local`
2. **Settings page:** Let users configure API URL and model
3. **Context menu:** Right-click selected text → "Ask AI about this"
4. **Summarize page:** Add a button to summarize the current webpage
5. **Dark mode:** Add theme toggle
6. **Export chat:** Save conversations as text/JSON

***

## **Troubleshooting**

**"Could not connect to llamafile"**
- Make sure llamafile is running: `./your-model.llamafile`
- Check it's on port 8080: visit `http://localhost:8080` in browser
- Verify CORS is enabled (llamafile allows this by default)

**Extension won't load**
- Check `manifest.json` is valid JSON (no trailing commas)
- Ensure all files are in the correct folders
- Check browser console for errors

---

This gives you a fully functional browser extension that works with your local AI—completely private, no cloud required!