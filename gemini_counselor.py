import google.generativeai as genai
import random
from datetime import datetime

class GeminiCounselor:
    def __init__(self):
        self.name = "Aashu"
        self.conversation_history = []
        
        # Configure Gemini with your API key
        genai.configure(api_key="AIzaSyDvtDGHgRm2Rn4dOV6c8dIz3yTVEea4H3g")
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Counselor personality prompt
        self.system_prompt = """You are Aashu, a warm, empathetic, and professional emotional counselor. 

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

    def generate_response(self, user_input, conversation_context=""):
        try:
            # Build conversation context
            context = ""
            if self.conversation_history:
                recent_messages = self.conversation_history[-3:]  # Last 3 exchanges
                for msg in recent_messages:
                    context += f"User: {msg['user']}\nAashu: {msg['bot']}\n"
            
            # Create full prompt
            full_prompt = f"""{self.system_prompt}

Previous conversation:
{context}

Current user message: {user_input}

Respond as Aashu, the emotional counselor:"""

            # Generate response using Gemini
            response = self.model.generate_content(full_prompt)
            
            # Clean up response
            ai_response = response.text.strip()
            
            # Remove any "Aashu:" prefix if present
            if ai_response.startswith("Aashu:"):
                ai_response = ai_response[6:].strip()
            
            return ai_response
            
        except Exception as e:
            # Fallback responses if API fails
            fallback_responses = [
                "I'm having trouble connecting right now, but I'm here with you. Can you tell me more about what you're feeling?",
                "I want to make sure I understand what you're going through. Could you share a bit more about that?",
                "That sounds really important. I'm listening and want to support you through this.",
                "I can hear that this matters to you. What's been the most challenging part?",
                "Thank you for sharing that with me. How are you feeling about everything right now?"
            ]
            return random.choice(fallback_responses)

    def detect_emotion(self, text):
        """Simple emotion detection for tracking"""
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
        """Main chat function"""
        if not user_input.strip():
            return "I'm here when you're ready to talk. Take your time."
        
        # Generate AI response
        response = self.generate_response(user_input)
        
        # Store conversation
        emotion = self.detect_emotion(user_input)
        self.conversation_history.append({
            'user': user_input,
            'bot': response,
            'emotion': emotion,
            'timestamp': datetime.now().isoformat()
        })
        
        return response

# Test function
def test_counselor():
    counselor = GeminiCounselor()
    
    print("🤗 Aashu - AI Emotional Counselor (Powered by Gemini)")
    print("Note: Add your Gemini API key to enable AI responses")
    print("Get free API key: https://makersuite.google.com/app/apikey")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print(f"\nAashu: Take care of yourself. Remember, you're stronger than you know, and it's always okay to reach out for support. 💙")
            break
        
        response = counselor.chat(user_input)
        print(f"\nAashu: {response}")

if __name__ == "__main__":
    test_counselor()