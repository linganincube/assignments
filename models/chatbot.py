from utils.nlp_processor import NLPProcessor
import datetime


class CUZChatbot:
    def __init__(self):
        self.nlp_processor = NLPProcessor('data/knowledge_base.json')
        self.session = {
            'start_time': datetime.datetime.now(),
            'interaction_count': 0,
            'preferred_category': None
        }

    def respond(self, user_input):
        self.session['interaction_count'] += 1

        # Check for category selection
        lower_input = user_input.lower()
        if lower_input in ['admissions', 'programs', 'services']:
            self.session['preferred_category'] = lower_input
            return {
                "response": f"Okay, I'll focus on {lower_input}. What would you like to know?",
                "category": "system",
                "confidence": 1.0
            }

        # Get NLP response
        response = self.nlp_processor.get_response(user_input)

        # If preferred category is set and response is generic, try to focus
        if (self.session['preferred_category'] and
                response['confidence'] < 0.6 and
                response['category'] == 'unknown'):
            return self._try_category_focus(user_input)

        return response

    def _try_category_focus(self, user_input):
        """Try to find a better match within the preferred category"""
        category = self.session['preferred_category']
        return {
            "response": f"I found this information about {category}: " +
                        "Our Bulawayo office can be reached at byocuz@university.ac.zw " +
                        "or phone 0773561045. Would you like me to connect you?",
            "category": category,
            "confidence": 0.7
        }

    def get_session_stats(self):
        duration = datetime.datetime.now() - self.session['start_time']
        return {
            'duration': str(duration),
            'interaction_count': self.session['interaction_count'],
            'preferred_category': self.session['preferred_category']
        }