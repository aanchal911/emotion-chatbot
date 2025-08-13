const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const clearBtn = document.getElementById('clear-btn');
const currentMoodSpan = document.getElementById('current-mood');
const typingIndicator = document.getElementById('typing-indicator');

// Emotion emojis mapping
const emotionEmojis = {
    'sad': '😢',
    'anxious': '😰',
    'angry': '😠',
    'happy': '😊',
    'neutral': '😐'
};

function formatTime() {
    return new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

function addMessage(content, isUser = false, emotion = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = isUser ? '👤' : (emotion ? emotionEmojis[emotion] || '🤗' : '🤗');
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = content;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = formatTime();
    
    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timeDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Update mood indicator
    if (!isUser && emotion) {
        updateMoodIndicator(emotion);
    }
}

function updateMoodIndicator(emotion) {
    const emoji = emotionEmojis[emotion] || '🤖';
    const emotionText = emotion ? emotion.charAt(0).toUpperCase() + emotion.slice(1) : 'Listening';
    currentMoodSpan.textContent = `${emoji} Detected: ${emotionText}`;
}

function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    addMessage(message, true);
    userInput.value = '';
    sendBtn.disabled = true;
    
    showTypingIndicator();
    
    // Simulate thinking time
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        hideTypingIndicator();
        
        if (data.error) {
            addMessage('I apologize, but I\'m having trouble processing that right now. Could you try rephrasing?', false, 'neutral');
        } else {
            addMessage(data.response, false, data.emotion);
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('I\'m having trouble connecting right now. Please check your connection and try again.', false, 'neutral');
    }
    
    sendBtn.disabled = false;
    userInput.focus();
}

async function clearChat() {
    if (confirm('Are you sure you want to clear this conversation? This action cannot be undone.')) {
        try {
            await fetch('/clear', { method: 'POST' });
            chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-avatar">🤗</div>
                    <div class="message-content">
                        <div class="message-text">Hello! I'm Aashu, your AI emotional counselor. I can understand context, remember our conversation, and respond naturally. I'm here to provide genuine support and have meaningful conversations about whatever is on your mind. What would you like to talk about today?</div>
                        <div class="message-time">${formatTime()}</div>
                    </div>
                </div>
            `;
            currentMoodSpan.textContent = '🤖 AI Ready';
        } catch (error) {
            console.error('Error clearing chat:', error);
        }
    }
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
clearBtn.addEventListener('click', clearChat);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Auto-resize input for mobile
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 100) + 'px';
});

// Focus input on load
userInput.focus();

// Prevent zoom on input focus for iOS
if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
    userInput.addEventListener('focus', function() {
        this.style.fontSize = '16px';
    });
}