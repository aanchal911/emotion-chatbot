const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const clearBtn = document.getElementById('clear-btn');

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    addMessage(message, true);
    userInput.value = '';
    sendBtn.disabled = true;
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (data.error) {
            addMessage('Sorry, something went wrong. Please try again.');
        } else {
            addMessage(data.response);
        }
    } catch (error) {
        addMessage('Sorry, I\'m having trouble connecting. Please try again.');
    }
    
    sendBtn.disabled = false;
    userInput.focus();
}

async function clearChat() {
    try {
        await fetch('/clear', { method: 'POST' });
        chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-content">
                    Hello! I'm Emma, your emotional support counselor. Feel free to share what's on your mind.
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
}

sendBtn.addEventListener('click', sendMessage);
clearBtn.addEventListener('click', clearChat);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

userInput.focus();