from flask import Flask, render_template, request, jsonify, session
from gemini_counselor import GeminiCounselor
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'gemini_counselor_secret_key'

# Initialize Gemini counselor
counselor = GeminiCounselor()

@app.route('/')
def index():
    if 'conversation' not in session:
        session['conversation'] = []
    return render_template('gemini_index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'})
    
    # Initialize conversation if not exists
    if 'conversation' not in session:
        session['conversation'] = []
    
    try:
        # Generate AI response using Gemini
        bot_response = counselor.chat(user_message)
        emotion = counselor.detect_emotion(user_message)
        
        # Store conversation
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
            'emotion': 'neutral',
            'error': str(e)
        })

@app.route('/mood-summary', methods=['GET'])
def mood_summary():
    if 'conversation' not in session:
        return jsonify({'emotions': {}, 'total_messages': 0})
    
    emotions = {}
    for entry in session['conversation']:
        if entry.get('emotion'):
            emotions[entry['emotion']] = emotions.get(entry['emotion'], 0) + 1
    
    return jsonify({
        'emotions': emotions,
        'total_messages': len(session['conversation']),
        'session_duration': len(session['conversation']) * 2
    })

@app.route('/clear', methods=['POST'])
def clear_conversation():
    session['conversation'] = []
    counselor.conversation_history = []  # Clear AI memory too
    return jsonify({'status': 'cleared'})

@app.route('/export-chat', methods=['GET'])
def export_chat():
    if 'conversation' not in session:
        return jsonify({'conversation': []})
    
    formatted_conversation = []
    for entry in session['conversation']:
        formatted_conversation.append({
            'timestamp': entry['timestamp'],
            'user_message': entry['user'],
            'aashu_response': entry['bot'],
            'detected_emotion': entry.get('emotion', 'neutral')
        })
    
    return jsonify({'conversation': formatted_conversation})

if __name__ == '__main__':
    print("🚀 Starting Aashu - AI Emotional Counselor (Gemini Powered)")
    print("📝 Don't forget to add your Gemini API key in gemini_counselor.py")
    print("🔗 Get free API key: https://makersuite.google.com/app/apikey")
    print("🌐 Server will run on: http://localhost:5002")
    print("-" * 60)
    app.run(debug=True, port=5002)