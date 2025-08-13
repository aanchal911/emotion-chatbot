from flask import Flask, render_template, request, jsonify, session
import random
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'emotional_counselor_secret_key'

class EmotionalCounselor:
    def __init__(self):
        self.name = "Emma"
        
        self.emotion_patterns = {
            'sad': {
                'keywords': ['sad', 'depressed', 'down', 'upset', 'crying', 'tears', 'lonely', 'empty'],
                'responses': [
                    "I hear that you're feeling sad. It's okay to feel this way. Can you tell me what's been weighing on your heart?",
                    "Sadness is a natural emotion. You're not alone in this. What's been making you feel down lately?",
                    "I'm here to listen. Sometimes talking about what's making us sad can help lighten the burden."
                ]
            },
            'anxious': {
                'keywords': ['anxious', 'worried', 'nervous', 'panic', 'stress', 'overwhelmed', 'scared', 'fear'],
                'responses': [
                    "Anxiety can feel overwhelming. Let's take this one step at a time. What's been causing you the most worry?",
                    "I understand you're feeling anxious. Remember, you've overcome challenges before. What's on your mind?",
                    "Feeling anxious is tough. Let's talk through what's worrying you. Sometimes sharing helps reduce the anxiety."
                ]
            },
            'angry': {
                'keywords': ['angry', 'mad', 'furious', 'irritated', 'frustrated', 'rage', 'annoyed'],
                'responses': [
                    "I can sense your anger. It's a valid emotion. What situation has made you feel this way?",
                    "Anger often comes from feeling hurt or misunderstood. Can you help me understand what happened?",
                    "Your feelings are important. Let's explore what's behind this anger together."
                ]
            },
            'happy': {
                'keywords': ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing', 'good', 'fantastic'],
                'responses': [
                    "It's wonderful to hear you're feeling happy! What's been bringing you joy lately?",
                    "I love hearing positive energy! Tell me more about what's making you feel so good.",
                    "Happiness is beautiful. I'd love to hear about what's been going well for you."
                ]
            }
        }
        
        self.supportive_responses = [
            "That sounds really challenging. How are you coping with this?",
            "Thank you for sharing that with me. Your feelings are completely valid.",
            "I'm here to support you through this. What would help you feel better right now?",
            "You're being very brave by talking about this. How can I best support you?",
            "I appreciate you opening up. What do you think might help in this situation?"
        ]

    def detect_emotion(self, text):
        text_lower = text.lower()
        for emotion, data in self.emotion_patterns.items():
            for keyword in data['keywords']:
                if keyword in text_lower:
                    return emotion
        return None

    def generate_response(self, user_input):
        emotion = self.detect_emotion(user_input)
        if emotion:
            return random.choice(self.emotion_patterns[emotion]['responses'])
        return random.choice(self.supportive_responses)

counselor = EmotionalCounselor()

@app.route('/')
def index():
    if 'conversation' not in session:
        session['conversation'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'})
    
    # Initialize conversation if not exists
    if 'conversation' not in session:
        session['conversation'] = []
    
    # Generate response
    bot_response = counselor.generate_response(user_message)
    emotion = counselor.detect_emotion(user_message)
    
    # Store conversation
    session['conversation'].append({
        'user': user_message,
        'bot': bot_response,
        'emotion': emotion,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({
        'response': bot_response,
        'emotion': emotion
    })

@app.route('/clear', methods=['POST'])
def clear_conversation():
    session['conversation'] = []
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(debug=True)