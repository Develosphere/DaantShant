"""Intent classification for conversational routing."""

import logging
import re
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class UserIntent(str, Enum):
    """User message intent categories."""
    GREETING = "greeting"
    GENERAL_ORAL_QUESTION = "general_oral_question"
    IMAGE_ANALYSIS = "image_analysis"
    SYMPTOM_DISCUSSION = "symptom_discussion"
    FOLLOW_UP = "follow_up"
    COMPARE_HISTORY = "compare_history"
    UNKNOWN = "unknown"


class IntentClassifier:
    """Rule-based intent classifier for user messages."""
    
    # Greeting patterns
    GREETING_PATTERNS = [
        r'\b(hi|hello|hey|greetings|good\s+(morning|afternoon|evening))\b',
        r'^(hi|hello|hey)[\s!.]*$',
    ]
    
    # General oral health question patterns
    GENERAL_ORAL_PATTERNS = [
        r'\b(how\s+(often|many\s+times)|should\s+i)\s+(brush|floss|clean)',
        r'\b(what|which)\s+(toothpaste|mouthwash|brush|floss)',
        r'\b(best\s+way|how\s+to)\s+(brush|floss|clean|maintain)',
        r'\b(prevent|avoid)\s+(cavit|decay|plaque|tartar|gum\s+disease)',
        r'\b(recommend|suggest|advice)\s+(for|about)',
        r'\bwhat\s+(causes|is)\s+(cavit|plaque|tartar|gingivitis|sensitivity)',
        r'\b(dental|oral)\s+(care|health|hygiene)',
        r'\b(whitening|whiten)\s+teeth',
    ]
    
    # Symptom discussion patterns
    SYMPTOM_PATTERNS = [
        r'\b(pain|hurt|ache|aching|painful|sore)',
        r'\b(bleed|bleeding|blood)',
        r'\b(sensitive|sensitivity)',
        r'\b(swollen|swelling|inflamed)',
        r'\b(loose|wobbly)\s+tooth',
        r'\b(bad\s+breath|halitosis)',
        r'\b(tooth|teeth)\s+(hurt|pain|ache)',
        r'\b(gum|gums)\s+(hurt|pain|bleed|sore)',
        r'\bwhen\s+i\s+(eat|drink|bite|chew)',
    ]
    
    # Follow-up patterns
    FOLLOW_UP_PATTERNS = [
        r'^(yes|yeah|yep|no|nope|okay|ok|sure|thanks|thank\s+you)[\s!.]*$',
        r'\b(what\s+about|how\s+about)\b',
        r'\b(also|additionally|furthermore)\b',
        r'\b(and\s+what|what\s+else)\b',
    ]
    
    # History comparison patterns
    COMPARE_HISTORY_PATTERNS = [
        r'\b(compare|comparison|difference|changed|improve|worse)',
        r'\b(last\s+time|previous|before|earlier)',
        r'\b(better|worse)\s+than',
        r'\b(progress|improvement|deteriorat)',
    ]
    
    def classify(self, text: str, has_image: bool = False) -> UserIntent:
        """
        Classify user message intent.
        
        Args:
            text: User message text
            has_image: Whether message includes an image
            
        Returns:
            Classified intent
        """
        if not text or not text.strip():
            if has_image:
                return UserIntent.IMAGE_ANALYSIS
            return UserIntent.UNKNOWN
        
        text_lower = text.lower().strip()
        
        # Image analysis takes priority if image is present
        if has_image:
            logger.info(f"Intent: IMAGE_ANALYSIS (image present)")
            return UserIntent.IMAGE_ANALYSIS
        
        # Check greeting
        if self._matches_patterns(text_lower, self.GREETING_PATTERNS):
            logger.info(f"Intent: GREETING")
            return UserIntent.GREETING
        
        # Check symptom discussion (high priority)
        if self._matches_patterns(text_lower, self.SYMPTOM_PATTERNS):
            logger.info(f"Intent: SYMPTOM_DISCUSSION")
            return UserIntent.SYMPTOM_DISCUSSION
        
        # Check history comparison
        if self._matches_patterns(text_lower, self.COMPARE_HISTORY_PATTERNS):
            logger.info(f"Intent: COMPARE_HISTORY")
            return UserIntent.COMPARE_HISTORY
        
        # Check general oral health questions
        if self._matches_patterns(text_lower, self.GENERAL_ORAL_PATTERNS):
            logger.info(f"Intent: GENERAL_ORAL_QUESTION")
            return UserIntent.GENERAL_ORAL_QUESTION
        
        # Check follow-up (short messages)
        if len(text_lower.split()) <= 5 and self._matches_patterns(text_lower, self.FOLLOW_UP_PATTERNS):
            logger.info(f"Intent: FOLLOW_UP")
            return UserIntent.FOLLOW_UP
        
        # Default to general question if it's a question
        if '?' in text or text_lower.startswith(('what', 'how', 'why', 'when', 'where', 'can', 'should', 'is', 'are', 'do', 'does')):
            logger.info(f"Intent: GENERAL_ORAL_QUESTION (question detected)")
            return UserIntent.GENERAL_ORAL_QUESTION
        
        logger.info(f"Intent: UNKNOWN")
        return UserIntent.UNKNOWN
    
    def _matches_patterns(self, text: str, patterns: list[str]) -> bool:
        """Check if text matches any of the given regex patterns."""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False


# Global classifier instance
intent_classifier = IntentClassifier()
