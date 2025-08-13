import random
import re
from datetime import datetime

class EnhancedEmotionalCounselor:
    def __init__(self):
        self.name = "Aashu"
        
        # Enhanced emotion patterns with warm, empathetic responses
        self.emotion_patterns = {
            'sad': {
                'keywords': ['sad', 'depressed', 'down', 'upset', 'crying', 'tears', 'lonely', 'empty', 'hopeless', 'miserable', 'heartbroken', 'devastated', 'grief', 'mourning', 'blue', 'melancholy', 'hurt', 'pain'],
                'responses': {
                    'initial': [
                        "Oh, I can really feel the weight of sadness in your words. 💙 You know what? It's completely okay to feel this way - sadness is just your heart processing something important. I'm right here with you, and you don't have to go through this alone.",
                        "My heart goes out to you right now. 🤗 What you're feeling is so valid, and I want you to know that sharing this with me takes real courage. Sometimes when we're sad, it feels like the world has lost its color, doesn't it?",
                        "I can sense how heavy your heart feels right now, and I just want to sit with you in this moment. 💝 Sadness isn't something to fix or rush through - it's something to honor. What's been weighing on your soul lately?"
                    ],
                    'follow_up': [
                        "Tell me more about what's been making your heart ache. Sometimes just putting it into words can help lighten the load a little.",
                        "I'm wondering... when did you first start noticing this sadness creeping in? Was there a particular moment or has it been building up slowly?",
                        "You mentioned feeling sad - I can imagine there might be layers to what you're experiencing. What feels like the deepest part of this sadness for you?"
                    ],
                    'supportive': [
                        "You're being so brave by sharing this with me. 🌟 In your past, when sadness has visited you before, what small things have helped bring even tiny moments of comfort?",
                        "I want you to know that your sadness doesn't define you - it's just something you're moving through right now. What would feel like the gentlest form of self-care for you today?"
                    ]
                }
            },
            'anxious': {
                'keywords': ['anxious', 'worried', 'nervous', 'panic', 'stress', 'overwhelmed', 'scared', 'fear', 'terrified', 'paranoid', 'restless', 'tense', 'uneasy', 'apprehensive', 'dread', 'anxious', 'freaking out'],
                'responses': {
                    'initial': [
                        "I can feel the anxiety radiating from your words, and I want you to know that you're safe here with me. 🌸 Anxiety can make everything feel so urgent and scary, but right now, in this moment, you're okay. Let's breathe through this together.",
                        "Oh, anxiety is such a tough visitor, isn't it? 🤍 It makes our minds race and our hearts pound, but I want you to know that what you're feeling is completely normal. Your nervous system is just trying to protect you, even when there's no real danger.",
                        "I can sense how overwhelming everything must feel right now. 🌊 Anxiety has this way of making molehills feel like mountains, doesn't it? But you reached out, and that shows incredible strength. Let's take this one breath at a time."
                    ],
                    'follow_up': [
                        "What does the anxiety feel like in your body right now? Sometimes naming the physical sensations can help us understand what our nervous system is trying to tell us.",
                        "I'm curious - when you close your eyes, what's the biggest worry that comes up? Sometimes our anxiety is trying to protect us from something specific.",
                        "Has this anxiety been your companion for a while, or is it something new that's shown up recently? Either way is completely valid."
                    ],
                    'supportive': [
                        "You know what's amazing? You've survived 100% of your anxious moments so far. 🌟 That's a pretty incredible track record. What's helped you get through the tough moments before?",
                        "Let's bring you back to this moment - you're here, you're breathing, you're safe. What's one tiny thing around you right now that brings you even the smallest sense of calm?"
                    ]
                }
            },
            'angry': {
                'keywords': ['angry', 'mad', 'furious', 'irritated', 'frustrated', 'rage', 'annoyed', 'pissed', 'livid', 'outraged', 'resentful', 'bitter', 'hostile', 'aggravated', 'fed up', 'hate'],
                'responses': {
                    'initial': [
                        "Wow, I can really feel the fire in your words right now. 🔥 Anger is such a powerful emotion, and you know what? It's completely valid. Your anger is telling me that something important to you has been threatened or hurt. I'm here to listen to every bit of it.",
                        "I can sense how intensely you're feeling right now, and I want you to know that your anger makes complete sense. 🤍 Sometimes anger is our heart's way of saying 'this isn't okay' - and that's actually really important information.",
                        "The energy I'm feeling from you right now is so strong, and I honor that. 💪 Anger often gets a bad reputation, but it's actually trying to protect something precious inside you. What do you think it's trying to protect?"
                    ],
                    'follow_up': [
                        "Tell me what happened - I want to understand the whole story. Sometimes when we're angry, we need someone to really hear us and validate that what happened wasn't okay.",
                        "I can imagine this situation has been eating at you. What's the part that makes you feel most fired up when you think about it?",
                        "If your anger could speak, what do you think it would want the world to know? Sometimes our anger carries really important messages."
                    ],
                    'supportive': [
                        "You know, underneath anger there's often hurt, disappointment, or feeling unheard. 💝 What other feelings might be hiding under this fire? It's okay if there are layers.",
                        "Your anger is valid, and so are you. What would help you honor these feelings while also taking care of yourself? Sometimes we need to feel the anger fully before we can move through it."
                    ]
                }
            },
            'happy': {
                'keywords': ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing', 'good', 'fantastic', 'thrilled', 'elated', 'cheerful', 'delighted', 'content', 'grateful', 'blessed', 'awesome', 'brilliant', 'perfect'],
                'responses': {
                    'initial': [
                        "Oh my goodness, your happiness is absolutely radiating through the screen! ✨ I can feel your joy from here, and it's making me smile too. There's something so beautiful about sharing happy moments - it's like sunshine spreading from person to person.",
                        "I am absolutely loving this energy you're bringing! 🌟 Your happiness is contagious, and I feel so honored that you're sharing this beautiful moment with me. Joy looks absolutely wonderful on you!",
                        "Wow, I can practically feel you glowing with happiness right now! 🌈 This is exactly the kind of energy the world needs more of. Your joy is a gift, not just to yourself but to everyone around you."
                    ],
                    'follow_up': [
                        "I'm so curious - what's been filling your heart with all this beautiful joy? I love hearing about the things that make people light up like this!",
                        "Tell me everything! What does this happiness feel like in your body? Sometimes when we're really happy, we can feel it from our toes to the top of our head.",
                        "I want to soak up every detail of what's making you feel so amazing. What's the story behind this wonderful feeling?"
                    ],
                    'supportive': [
                        "You know what I love about this? You're taking the time to really notice and celebrate your happiness. 🎉 That's such a beautiful practice. How can we bottle up some of this joy for the days when you might need a reminder?",
                        "Your happiness is like a little beacon of light in the world. How does it feel to carry this joy with you? I have a feeling it's touching other people's lives too."
                    ]
                }
            },
            'confused': {
                'keywords': ['confused', 'lost', 'uncertain', 'unclear', 'mixed up', 'puzzled', 'bewildered', 'conflicted', 'torn', 'unsure'],
                'responses': {
                    'initial': [
                        "Confusion can feel really unsettling. It's okay not to have all the answers right now. 🤔",
                        "Sometimes life presents us with complex situations that don't have clear solutions. You're not alone in feeling this way.",
                        "It takes wisdom to recognize when we're confused. Let's explore this together."
                    ],
                    'follow_up': [
                        "What's the main thing that's causing this confusion?",
                        "Are there multiple options or paths you're trying to choose between?",
                        "What would clarity look like for you in this situation?"
                    ],
                    'supportive': [
                        "Sometimes sitting with confusion for a while can lead to unexpected insights. What feels most important to you right now?",
                        "What would your wisest self tell you about this situation?"
                    ]
                }
            },
            'lonely': {
                'keywords': ['lonely', 'alone', 'isolated', 'disconnected', 'abandoned', 'rejected', 'excluded', 'solitary'],
                'responses': {
                    'initial': [
                        "Loneliness can feel so profound and painful. I want you to know that you're not truly alone - I'm here with you now. 🤗",
                        "The feeling of being alone can be one of the hardest emotions to bear. Your reaching out shows incredible strength.",
                        "Even in loneliness, you've found the courage to connect. That says something beautiful about who you are."
                    ],
                    'follow_up': [
                        "What does loneliness feel like for you?",
                        "Are there people in your life you'd like to feel closer to?",
                        "What kinds of connections are you most longing for?"
                    ],
                    'supportive': [
                        "Connection starts with small steps. What's one tiny way you could reach out to someone today?",
                        "You have value and deserve meaningful connections. What qualities do you bring to relationships?"
                    ]
                }
            }
        }
        
        # Context-aware responses
        self.context_responses = {
            'work': [
                "Work stress can really impact our overall well-being. How is this affecting other areas of your life?",
                "Career challenges can feel overwhelming. What aspects of work are most concerning to you?",
                "It sounds like work is weighing heavily on you. What would an ideal work situation look like?"
            ],
            'relationship': [
                "Relationships can be both our greatest source of joy and our deepest challenge. What's been most difficult?",
                "It takes courage to work on relationships. What are you hoping will change?",
                "Human connections are complex. What do you need most in your relationships right now?"
            ],
            'family': [
                "Family dynamics can be particularly complex because of the deep history involved. What's been most challenging?",
                "Family relationships often carry a lot of emotional weight. How is this affecting you?",
                "It sounds like family is on your mind. What would feel most healing in this situation?"
            ],
            'health': [
                "Health concerns can create a lot of anxiety and uncertainty. How are you taking care of yourself through this?",
                "Physical and mental health are deeply connected. What support do you have right now?",
                "Health challenges can feel isolating. What would help you feel more supported?"
            ]
        }
        
        # Therapeutic techniques
        self.therapeutic_responses = [
            "What would you tell a close friend who was going through the same thing?",
            "If you could wave a magic wand and change one thing about this situation, what would it be?",
            "What's one small step you could take today that might help?",
            "How would you like to feel instead of how you're feeling now?",
            "What strengths have helped you through difficult times before?",
            "What would self-compassion look like in this situation?",
            "If this feeling had a message for you, what do you think it would be?"
        ]
        
        self.supportive_responses = [
            "You know what strikes me most about what you've shared? The incredible courage it takes to be so honest about what you're feeling. 💝 Your emotions are not just valid - they're important, and so are you.",
            "I feel so honored that you've trusted me with something so personal and meaningful. 🤗 The fact that you're here, opening up and being vulnerable, shows such beautiful strength.",
            "I can really hear how much this matters to you, and I want you to know that I'm sitting here with you in this moment. 🌟 Your feelings deserve to be heard and held with care.",
            "What you're going through right now - it's so deeply human. 🌊 You're not broken, you're not too much, you're just beautifully, messily human, and that's exactly as it should be.",
            "I'm really moved by how you're showing up for yourself right now, even when things feel difficult. 🌱 That takes such courage, and I see you doing that hard work of being present with your feelings.",
            "Sometimes life hands us experiences that are just... a lot. 💙 And here you are, not running away from it, but sitting with it and trying to understand it. That's actually pretty incredible.",
            "I can feel how much you're carrying right now, and I just want you to know that you don't have to carry it all alone. 🤍 I'm here with you, and your feelings matter deeply to me."
        ]

    def detect_emotion(self, text):
        text_lower = text.lower()
        detected_emotions = []
        
        for emotion, data in self.emotion_patterns.items():
            for keyword in data['keywords']:
                if keyword in text_lower:
                    detected_emotions.append(emotion)
                    break
        
        return detected_emotions[0] if detected_emotions else None
    
    def detect_context(self, text):
        text_lower = text.lower()
        contexts = {
            'work': ['job', 'work', 'boss', 'colleague', 'office', 'career', 'workplace', 'employment', 'fired', 'quit'],
            'relationship': ['boyfriend', 'girlfriend', 'partner', 'spouse', 'husband', 'wife', 'dating', 'breakup', 'relationship'],
            'family': ['mom', 'dad', 'mother', 'father', 'parent', 'family', 'sibling', 'brother', 'sister', 'child'],
            'health': ['sick', 'illness', 'doctor', 'hospital', 'pain', 'health', 'medical', 'therapy', 'medication']
        }
        
        for context, keywords in contexts.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return context
        return None

    def get_contextual_response(self, user_input, conversation_history):
        emotion = self.detect_emotion(user_input)
        context = self.detect_context(user_input)
        
        # Determine response type based on conversation flow
        if len(conversation_history) == 0:
            response_type = 'initial'
        elif len(conversation_history) < 3:
            response_type = 'follow_up'
        else:
            response_type = 'supportive'
        
        # Generate response based on emotion and context
        if emotion and emotion in self.emotion_patterns:
            if response_type in self.emotion_patterns[emotion]['responses']:
                response = random.choice(self.emotion_patterns[emotion]['responses'][response_type])
            else:
                response = random.choice(self.emotion_patterns[emotion]['responses']['initial'])
        elif context and context in self.context_responses:
            response = random.choice(self.context_responses[context])
        elif len(conversation_history) > 2:
            response = random.choice(self.therapeutic_responses)
        else:
            response = random.choice(self.supportive_responses)
        
        return response

    def generate_response(self, user_input, conversation_history=[]):
        return self.get_contextual_response(user_input, conversation_history)