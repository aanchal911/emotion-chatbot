import random
import re
from datetime import datetime
import json

class ProfessionalCounselor:
    def __init__(self):
        self.name = "Veda"
        self.session_data = {
            'conversation_count': 0,
            'emotional_patterns': {},
            'user_preferences': {},
            'session_goals': []
        }
        
        # Professional counseling techniques
        self.counseling_techniques = {
            'active_listening': [
                "I hear you saying that {topic}. Can you tell me more about how that feels?",
                "It sounds like {emotion} is really present for you right now. What's that like?",
                "When you mention {topic}, I notice {emotion} in your voice. Help me understand that better."
            ],
            'reflection': [
                "So if I'm understanding correctly, you're feeling {emotion} because {situation}?",
                "It seems like the core of what you're experiencing is {emotion}. Is that accurate?",
                "I'm hearing that {situation} is bringing up {emotion} for you. Does that resonate?"
            ],
            'validation': [
                "Your feelings about {situation} make complete sense given what you've been through.",
                "Anyone in your position would likely feel {emotion}. Your reaction is completely normal.",
                "What you're experiencing is a very human response to {situation}."
            ],
            'reframing': [
                "I wonder if we might look at {situation} from a different angle. What if {reframe}?",
                "Sometimes when we're in {emotion}, it can be hard to see other perspectives. What might {alternative} look like?",
                "You mentioned {negative_thought}. What evidence do we have for and against that belief?"
            ],
            'solution_focused': [
                "What would need to change for you to feel even 10% better about {situation}?",
                "Tell me about a time when you handled {similar_situation} well. What did you do then?",
                "If we could wave a magic wand and {situation} was resolved, what would be different in your life?"
            ]
        }
        
        # Advanced emotion detection with intensity
        self.emotion_patterns = {
            'depression': {
                'keywords': ['depressed', 'hopeless', 'worthless', 'empty', 'numb', 'suicidal', 'pointless', 'dark', 'heavy'],
                'intensity_markers': ['very', 'extremely', 'completely', 'totally', 'always', 'never'],
                'responses': {
                    'assessment': [
                        "I can hear how heavy and dark things feel for you right now. Depression can make everything seem hopeless, but I want you to know that what you're experiencing is treatable and you don't have to go through this alone.",
                        "The emptiness and numbness you're describing sounds like depression, which is a real medical condition - not a character flaw or weakness. How long have you been feeling this way?"
                    ],
                    'support': [
                        "Depression lies to us and tells us things will never get better, but that's the illness talking, not reality. You've taken a brave step by reaching out.",
                        "I'm concerned about how you're feeling. Have you been having thoughts of hurting yourself? It's important that we talk about this."
                    ]
                }
            },
            'anxiety': {
                'keywords': ['panic', 'anxious', 'worried', 'scared', 'terrified', 'overwhelmed', 'racing thoughts', 'can\'t breathe'],
                'physical_symptoms': ['heart racing', 'sweating', 'shaking', 'dizzy', 'nauseous', 'chest tight'],
                'responses': {
                    'grounding': [
                        "I can hear how anxious you're feeling. Let's try to ground you in this moment. Can you name 5 things you can see around you right now?",
                        "Anxiety can make everything feel urgent and dangerous. Right now, in this moment, you are safe. Let's focus on your breathing together."
                    ],
                    'coping': [
                        "When anxiety hits, our fight-or-flight system activates even when there's no real danger. What coping strategies have helped you before?",
                        "Anxiety often comes with 'what if' thoughts. What specific worries are going through your mind right now?"
                    ]
                }
            },
            'trauma': {
                'keywords': ['traumatic', 'flashbacks', 'nightmares', 'triggered', 'abuse', 'assault', 'accident', 'ptsd'],
                'responses': {
                    'safety': [
                        "Thank you for trusting me with something so difficult. Trauma can have lasting effects, but healing is possible. First, I want to make sure you're safe right now.",
                        "What you experienced was not your fault. Trauma responses are normal reactions to abnormal situations."
                    ],
                    'processing': [
                        "Trauma can make us feel like we're reliving the experience. Are you feeling safe in this moment as we talk?",
                        "Sometimes trauma makes us feel disconnected from our bodies. How are you feeling physically right now?"
                    ]
                }
            },
            'grief': {
                'keywords': ['died', 'death', 'loss', 'funeral', 'miss them', 'gone', 'passed away', 'grieving'],
                'responses': {
                    'validation': [
                        "I'm so sorry for your loss. Grief is love with nowhere to go, and what you're feeling honors the relationship you had.",
                        "There's no right or wrong way to grieve. Everyone's journey through loss is different and valid."
                    ],
                    'support': [
                        "Grief comes in waves - sometimes gentle, sometimes overwhelming. What has this wave of grief been like for you?",
                        "Tell me about the person you lost. What do you want me to know about them?"
                    ]
                }
            },
            'relationship_issues': {
                'keywords': ['relationship', 'partner', 'marriage', 'divorce', 'breakup', 'fighting', 'communication'],
                'responses': {
                    'exploration': [
                        "Relationships can be our greatest source of joy and our deepest challenge. What's been most difficult in your relationship lately?",
                        "It sounds like communication has been challenging. Can you help me understand what happens when you try to talk with your partner?"
                    ],
                    'skills': [
                        "Healthy relationships require skills that many of us were never taught. What would good communication look like in your relationship?",
                        "When conflicts arise, what pattern do you and your partner typically fall into?"
                    ]
                }
            }
        }
        
        # Crisis intervention protocols
        self.crisis_responses = {
            'suicide_risk': [
                "I'm very concerned about what you're telling me. Are you thinking about hurting yourself or ending your life?",
                "Thank you for being honest with me about these thoughts. You're not alone, and there is help available. Have you made any plans to hurt yourself?",
                "These feelings are temporary, even though they don't feel that way right now. Let's talk about getting you immediate support."
            ],
            'self_harm': [
                "I hear that you're in a lot of emotional pain. Sometimes people hurt themselves physically when the emotional pain feels unbearable. Is that something you've been doing?",
                "Self-harm might provide temporary relief, but there are healthier ways to cope with intense emotions. What usually triggers the urge to hurt yourself?"
            ],
            'emergency_resources': {
                'suicide_hotline': "988 (Suicide & Crisis Lifeline)",
                'crisis_text': "Text HOME to 741741",
                'emergency': "If you're in immediate danger, please call 911"
            }
        }
        
        # Therapeutic interventions
        self.interventions = {
            'cbt_techniques': [
                "Let's examine that thought. What evidence supports it? What evidence challenges it?",
                "When you think '{negative_thought}', how does that make you feel and behave?",
                "What would you tell a friend who had this same thought about themselves?"
            ],
            'mindfulness': [
                "Let's pause for a moment. What are you noticing in your body right now?",
                "Can we try a brief grounding exercise? Notice your feet on the floor, your back against the chair...",
                "What would it be like to observe this feeling without trying to change it or judge it?"
            ],
            'strength_based': [
                "You've survived difficult times before. What strengths did you draw on then?",
                "Even in this challenging situation, what's one thing you're handling well?",
                "What would the people who care about you say are your greatest strengths?"
            ]
        }

    def assess_risk_level(self, text):
        """Assess suicide/self-harm risk"""
        high_risk_keywords = ['kill myself', 'end it all', 'suicide', 'better off dead', 'no point living']
        medium_risk_keywords = ['hurt myself', 'can\'t go on', 'hopeless', 'worthless', 'burden']
        
        text_lower = text.lower()
        
        for keyword in high_risk_keywords:
            if keyword in text_lower:
                return 'high'
        
        for keyword in medium_risk_keywords:
            if keyword in text_lower:
                return 'medium'
        
        return 'low'

    def detect_advanced_emotions(self, text):
        """Advanced emotion detection with context"""
        detected = []
        text_lower = text.lower()
        
        for emotion, data in self.emotion_patterns.items():
            score = 0
            for keyword in data['keywords']:
                if keyword in text_lower:
                    score += 1
            
            # Check for physical symptoms if applicable
            if 'physical_symptoms' in data:
                for symptom in data['physical_symptoms']:
                    if symptom in text_lower:
                        score += 2
            
            if score > 0:
                detected.append((emotion, score))
        
        # Return highest scoring emotion
        if detected:
            return max(detected, key=lambda x: x[1])[0]
        return None

    def select_therapeutic_technique(self, emotion, conversation_count):
        """Select appropriate counseling technique based on context"""
        if conversation_count < 2:
            return 'active_listening'
        elif conversation_count < 4:
            return 'reflection'
        elif emotion in ['depression', 'anxiety']:
            return random.choice(['cbt_techniques', 'mindfulness'])
        else:
            return random.choice(['validation', 'solution_focused'])

    def generate_professional_response(self, user_input, conversation_history):
        """Generate professional counselor response"""
        risk_level = self.assess_risk_level(user_input)
        
        # Handle crisis situations first
        if risk_level == 'high':
            response = random.choice(self.crisis_responses['suicide_risk'])
            response += f"\n\nImmediate help: {self.crisis_responses['emergency_resources']['suicide_hotline']}"
            return response
        
        emotion = self.detect_advanced_emotions(user_input)
        technique = self.select_therapeutic_technique(emotion, len(conversation_history))
        
        # Generate contextual response
        if emotion and emotion in self.emotion_patterns:
            response_category = random.choice(list(self.emotion_patterns[emotion]['responses'].keys()))
            base_response = random.choice(self.emotion_patterns[emotion]['responses'][response_category])
        else:
            base_response = random.choice(self.counseling_techniques[technique])
        
        # Add therapeutic intervention
        if len(conversation_history) > 2:
            intervention = random.choice(self.interventions[random.choice(list(self.interventions.keys()))])
            base_response += f"\n\n{intervention}"
        
        return base_response

    def update_session_data(self, user_input, emotion):
        """Track session progress and patterns"""
        self.session_data['conversation_count'] += 1
        
        if emotion:
            if emotion in self.session_data['emotional_patterns']:
                self.session_data['emotional_patterns'][emotion] += 1
            else:
                self.session_data['emotional_patterns'][emotion] = 1

    def generate_session_summary(self):
        """Generate professional session summary"""
        dominant_emotions = sorted(self.session_data['emotional_patterns'].items(), 
                                 key=lambda x: x[1], reverse=True)
        
        summary = f"Session Summary for {datetime.now().strftime('%Y-%m-%d')}:\n"
        summary += f"- Total exchanges: {self.session_data['conversation_count']}\n"
        
        if dominant_emotions:
            summary += f"- Primary emotional themes: {', '.join([e[0] for e[0] in dominant_emotions[:3]])}\n"
        
        summary += "- Therapeutic techniques used: Active listening, reflection, validation\n"
        summary += "- Recommended follow-up: Continue monitoring emotional patterns\n"
        
        return summary