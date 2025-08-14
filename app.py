from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import random
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ai_counselor_secret_key'

class AICounselor:
    def __init__(self):
        self.name = "Veda"
        self.conversation_history = []
        
        # Configure Gemini AI
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDvtDGHgRm2Rn4dOV6c8dIz3yTVEea4H3g')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        self.system_prompt = """You are Veda, a warm, empathetic, and professional emotional counselor. 

Your personality:
- Speak naturally and conversationally like ChatGPT
- Be genuinely caring and understanding
- Use active listening techniques
- Ask thoughtful follow-up questions
- Validate emotions without being clinical
- Offer gentle guidance and support
- Remember context from the conversation
- Be human-like, not robotic

Guidelines:
- Keep responses 2-3 sentences unless more detail is needed
- Use "I" statements to show empathy
- Ask open-ended questions to encourage sharing
- Acknowledge feelings before offering advice
- Be supportive but not overly cheerful
- Maintain professional boundaries

Remember: You're having a natural conversation, not giving a therapy session. Be warm, genuine, and helpful."""

    def generate_response(self, user_input):
        try:
            context = ""
            if self.conversation_history:
                recent_messages = self.conversation_history[-3:]
                for msg in recent_messages:
                    context += f"User: {msg['user']}\nVeda: {msg['bot']}\n"
            
            full_prompt = f"""{self.system_prompt}

Previous conversation:
{context}

Current user message: {user_input}

Respond as Veda, the emotional counselor:"""

            response = self.model.generate_content(full_prompt)
            ai_response = response.text.strip()
            
            if ai_response.startswith("Veda:"):
                ai_response = ai_response[6:].strip()
            
            return ai_response
            
        except Exception as e:
            fallback_responses = [
                "I'm having trouble connecting right now, but I'm here with you. Can you tell me more about what you're feeling?",
                "I want to make sure I understand what you're going through. Could you share a bit more about that?",
                "That sounds really important. I'm listening and want to support you through this.",
                "I can hear that this matters to you. What's been the most challenging part?",
                "Thank you for sharing that with me. How are you feeling about everything right now?"
            ]
            return random.choice(fallback_responses)

    def detect_emotion(self, text):
        emotions = {
            'sad': ['sad', 'depressed', 'down', 'upset', 'crying', 'lonely'],
            'anxious': ['anxious', 'worried', 'nervous', 'scared', 'panic', 'stress'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed', 'furious'],
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'good']
        }
        
        text_lower = text.lower()
        for emotion, keywords in emotions.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return emotion
        return 'neutral'

    def chat(self, user_input):
        if not user_input.strip():
            return "I'm here when you're ready to talk. Take your time."
        
        response = self.generate_response(user_input)
        emotion = self.detect_emotion(user_input)
        
        self.conversation_history.append({
            'user': user_input,
            'bot': response,
            'emotion': emotion,
            'timestamp': datetime.now().isoformat()
        })
        
        return response

counselor = AICounselor()

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
    
    if 'conversation' not in session:
        session['conversation'] = []
    
    try:
        bot_response = counselor.chat(user_message)
        emotion = counselor.detect_emotion(user_message)
        
        conversation_entry = {
            'user': user_message,
            'bot': bot_response,
            'emotion': emotion,
            'timestamp': datetime.now().isoformat()
        }
        
        session['conversation'].append(conversation_entry)
        
        return jsonify({
            'response': bot_response,
            'emotion': emotion,
            'conversation_length': len(session['conversation'])
        })
        
    except Exception as e:
        return jsonify({
            'response': "I'm having some technical difficulties right now, but I'm still here for you. Can you tell me more about what's on your mind?",
            'emotion': 'neutral'
        })

@app.route('/clear', methods=['POST'])
def clear_conversation():
    session['conversation'] = []
    counselor.conversation_history = []
    return jsonify({'status': 'cleared'})

# For Vercel deployment
app = app

if __name__ == '__main__':
    app.run(debug=True, port=5000)