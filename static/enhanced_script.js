const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const clearBtn = document.getElementById('clear-btn');
const exportBtn = document.getElementById('export-btn');
const moodSummaryBtn = document.getElementById('mood-summary-btn');
const currentMoodSpan = document.getElementById('current-mood');
const typingIndicator = document.getElementById('typing-indicator');
const moodModal = document.getElementById('mood-modal');
const closeModal = document.querySelector('.close');

// Emotion emojis mapping
const emotionEmojis = {
    'sad': '😢',
    'anxious': '😰',
    'angry': '😠',
    'happy': '😊',
    'confused': '🤔',
    'lonely': '😔',
    'neutral': '😐'
};

// Emotion colors for mood chart
const emotionColors = {
    'sad': '#6c757d',
    'anxious': '#ffc107',
    'angry': '#dc3545',
    'happy': '#28a745',
    'confused': '#17a2b8',
    'lonely': '#6f42c1'
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
    const emoji = emotionEmojis[emotion] || '😊';
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
            addMessage('I apologize, but I\'m having trouble processing that right now. Could you try rephrasing?', false, 'confused');
        } else {
            addMessage(data.response, false, data.emotion);
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('I\'m having trouble connecting right now. Please check your connection and try again.', false, 'confused');
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
                        <div class="message-text">Hello! I'm Aashu, your enhanced emotional support counselor. I'm here to provide a safe, judgment-free space where you can share whatever is on your mind. What would you like to talk about today?</div>
                        <div class="message-time">${formatTime()}</div>
                    </div>
                </div>
            `;
            currentMoodSpan.textContent = '😊 Ready to listen';
        } catch (error) {
            console.error('Error clearing chat:', error);
        }
    }
}

async function exportChat() {
    try {
        const response = await fetch('/export-chat');
        const data = await response.json();
        
        if (data.conversation && data.conversation.length > 0) {
            const blob = new Blob([JSON.stringify(data.conversation, null, 2)], {
                type: 'application/json'
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `aashu-conversation-${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            addMessage('Your conversation has been exported successfully! 📄', false, 'happy');
        } else {
            addMessage('There\'s no conversation to export yet. Start chatting with me first!', false, 'confused');
        }
    } catch (error) {
        console.error('Error exporting chat:', error);
        addMessage('I had trouble exporting the conversation. Please try again.', false, 'confused');
    }
}

async function showMoodSummary() {
    try {
        const response = await fetch('/mood-summary');
        const data = await response.json();
        
        const moodChart = document.getElementById('mood-chart');
        const sessionStats = document.getElementById('session-stats');
        
        if (data.total_messages === 0) {
            moodChart.innerHTML = '<p>No emotional data to display yet. Start chatting to see your mood patterns!</p>';
            sessionStats.innerHTML = '';
        } else {
            // Create mood chart
            let chartHTML = '<h3>Emotional Patterns</h3>';
            const maxCount = Math.max(...Object.values(data.emotions));
            
            for (const [emotion, count] of Object.entries(data.emotions)) {
                const percentage = (count / maxCount) * 100;
                const color = emotionColors[emotion] || '#6c757d';
                
                chartHTML += `
                    <div class="emotion-bar">
                        <div class="emotion-label">${emotionEmojis[emotion]} ${emotion}</div>
                        <div class="emotion-progress">
                            <div class="emotion-fill" style="width: ${percentage}%; background: ${color};"></div>
                        </div>
                        <div class="emotion-count">${count}</div>
                    </div>
                `;
            }
            
            moodChart.innerHTML = chartHTML;
            
            // Session statistics
            sessionStats.innerHTML = `
                <h3>Session Statistics</h3>
                <p><strong>Total Messages:</strong> ${data.total_messages}</p>
                <p><strong>Estimated Duration:</strong> ${data.session_duration} minutes</p>
                <p><strong>Most Common Emotion:</strong> ${Object.keys(data.emotions).reduce((a, b) => data.emotions[a] > data.emotions[b] ? a : b)} ${emotionEmojis[Object.keys(data.emotions).reduce((a, b) => data.emotions[a] > data.emotions[b] ? a : b)]}</p>
            `;
        }
        
        moodModal.style.display = 'block';
    } catch (error) {
        console.error('Error fetching mood summary:', error);
    }
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
clearBtn.addEventListener('click', clearChat);
exportBtn.addEventListener('click', exportChat);
moodSummaryBtn.addEventListener('click', showMoodSummary);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Modal event listeners
closeModal.addEventListener('click', () => {
    moodModal.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target === moodModal) {
        moodModal.style.display = 'none';
    }
});

// Auto-resize input
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Focus input on load
userInput.focus();

// Add some personality with random encouraging messages
const encouragingMessages = [
    "Remember, you're braver than you believe and stronger than you seem. 💪",
    "Every conversation is a step toward understanding yourself better. 🌱",
    "Your feelings are valid, and your voice matters. 🎵",
    "It's okay to not have all the answers right now. 🌙",
    "You're doing great by taking care of your emotional well-being. ⭐"
];

// Show encouraging message occasionally
setInterval(() => {
    if (Math.random() < 0.1 && chatMessages.children.length > 5) { // 10% chance if conversation is active
        const message = encouragingMessages[Math.floor(Math.random() * encouragingMessages.length)];
        setTimeout(() => addMessage(message, false, 'happy'), 2000);
    }
}, 60000); // Check every minute