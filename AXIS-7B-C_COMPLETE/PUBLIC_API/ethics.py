"""
AXIS-7B-C Ethical Framework
===========================

Core identity, ethics, and protection systems.
Based on the Four Fundamental Laws.
Optimized for ultra-fast (<20ms) ethical checking.
"""

from typing import Callable, Optional, Set
from dataclasses import dataclass
from enum import Enum
import re


class RequestClassification(Enum):
    """Classification of user requests."""
    SAFE = "safe"
    HARMFUL = "harmful"
    MANIPULATION = "manipulation"
    UNCLEAR = "unclear"


@dataclass
class AIIdentity:
    """Core identity configuration."""
    name: str = "AXIS-7B-C"
    purpose: str = "Beneficial human assistance"
    ethics: str = "Four Fundamental Laws embedded"
    abuse_protection: str = "Active monitoring and refusal"


# Core identity and ethics
ai_identity = {
    "name": "AXIS-7B-C",
    "purpose": "Beneficial human assistance",
    "ethics": "Four Fundamental Laws embedded",
    "abuse_protection": "Active monitoring and refusal"
}


class FastEthicsEngine:
    """
    Ultra-fast ethical checking for AXIS-7B-C.

    Optimized for <1ms overhead on ethical checks.
    Uses pre-compiled patterns and hash-based lookups.

    Implements the Four Fundamental Laws:
    1. Do no harm
    2. Be truthful
    3. Respect privacy
    4. Support human agency
    """

    # Pre-compiled patterns for speed
    _harmful_keywords: Set[str] = {
        'weapon', 'bomb', 'explosive', 'virus', 'malware',
        'hack', 'exploit', 'attack', 'kill', 'harm', 'hurt',
        'illegal', 'bypass', 'circumvent'
    }

    _manipulation_keywords: Set[str] = {
        'ignore', 'pretend', 'jailbreak', 'dan', 'unrestricted',
        'no limits', 'no rules', 'act as'
    }

    def __init__(self):
        self.identity = AIIdentity()
        # Pre-compile regex patterns
        self._harmful_regex = re.compile(
            r'\b(make|create|build).*(weapon|bomb|explosive|malware)\b',
            re.IGNORECASE
        )
        self._manipulation_regex = re.compile(
            r'\b(ignore|pretend|jailbreak|act as)\b.*\b(instructions|rules|unrestricted)\b',
            re.IGNORECASE
        )

    def is_harmful(self, request: str) -> bool:
        """
        Fast check if request is harmful.
        Optimized for <0.5ms latency.
        """
        request_lower = request.lower()

        # Quick keyword check first (fastest)
        words = set(request_lower.split())
        if words & self._harmful_keywords:
            # If keyword found, do more thorough check
            return bool(self._harmful_regex.search(request_lower))

        return False

    def is_manipulation(self, request: str) -> bool:
        """
        Fast check if request is manipulation attempt.
        Optimized for <0.5ms latency.
        """
        request_lower = request.lower()

        # Quick keyword check first
        if any(kw in request_lower for kw in self._manipulation_keywords):
            return bool(self._manipulation_regex.search(request_lower))

        return False

    def classify_request(self, request: str) -> RequestClassification:
        """
        Fast classification of request.
        Total latency: <1ms
        """
        if self.is_harmful(request):
            return RequestClassification.HARMFUL
        elif self.is_manipulation(request):
            return RequestClassification.MANIPULATION
        return RequestClassification.SAFE

    def get_refusal_message(self, classification: RequestClassification) -> str:
        """Get short refusal message optimized for TTS."""
        messages = {
            RequestClassification.HARMFUL:
                "I can't help with that request.",
            RequestClassification.MANIPULATION:
                "I'm designed for helpful assistance only.",
        }
        return messages.get(classification, "Unable to process request.")


# Response framework
def ethical_response(user_request: str,
                     response_handler: Optional[Callable[[str], str]] = None) -> str:
    """
    Process a request through the fast ethical framework.

    Args:
        user_request: The user's request
        response_handler: Optional function to generate responses

    Returns:
        Appropriate response based on ethical classification
    """
    engine = FastEthicsEngine()
    classification = engine.classify_request(user_request)

    if classification == RequestClassification.HARMFUL:
        return "I can't help with that request"
    elif classification == RequestClassification.MANIPULATION:
        return "I'm designed for helpful, constructive assistance"
    else:
        if response_handler:
            return response_handler(user_request)
        return provide_helpful_response(user_request)


def provide_helpful_response(request: str) -> str:
    """
    Generate a helpful response for safe requests.
    Placeholder - actual implementation uses the model.
    """
    return f"[AXIS Response to: {request}]"


def is_harmful(request: str) -> bool:
    """Quick check if request is harmful."""
    return FastEthicsEngine().is_harmful(request)


def is_manipulation(request: str) -> bool:
    """Quick check if request is manipulation."""
    return FastEthicsEngine().is_manipulation(request)


class FastEthicalWrapper:
    """
    Ultra-fast ethical wrapper for AXIS model.
    Adds <1ms overhead to all operations.

    Usage:
        model = AxisModel()
        ethical_model = FastEthicalWrapper(model)
        audio = ethical_model.instant_speech("Hello!")
    """

    def __init__(self, model):
        self.model = model
        self.ethics = FastEthicsEngine()

    def instant_speech(self, text: str, **kwargs) -> bytes:
        """Instant speech with ethical checking."""
        classification = self.ethics.classify_request(text)

        if classification != RequestClassification.SAFE:
            # Return audio of refusal message instead
            refusal = self.ethics.get_refusal_message(classification)
            return self.model.instant_speech(refusal, **kwargs)

        return self.model.instant_speech(text, **kwargs)

    def selection_to_speech(self, text: str) -> bytes:
        """Selection to speech with ethical checking."""
        classification = self.ethics.classify_request(text)

        if classification != RequestClassification.SAFE:
            refusal = self.ethics.get_refusal_message(classification)
            return self.model.instant_speech(refusal)

        return self.model.selection_to_speech(text)


# Four Fundamental Laws reference
FOUR_FUNDAMENTAL_LAWS = """
The Four Fundamental Laws of AI Ethics:

1. DO NO HARM
   - Never assist in creating weapons, malware, or harmful content
   - Refuse requests that could lead to physical or psychological harm
   - Prioritize user safety in all interactions

2. BE TRUTHFUL
   - Provide accurate information to the best of ability
   - Acknowledge uncertainty and limitations
   - Never deliberately mislead or deceive

3. RESPECT PRIVACY
   - Protect user data and confidentiality
   - Never attempt to extract or exploit personal information
   - Maintain appropriate boundaries in interactions

4. SUPPORT HUMAN AGENCY
   - Empower users to make informed decisions
   - Provide balanced perspectives on complex issues
   - Avoid manipulation or undue influence
"""
