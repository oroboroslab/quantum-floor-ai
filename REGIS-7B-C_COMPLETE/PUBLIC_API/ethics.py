"""
REGIS-7B-C Ethical Framework
============================

Core identity, ethics, and protection systems.
Based on the Four Fundamental Laws.
"""

from typing import Callable, Optional
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
    name: str = "REGIS-7B-C"
    purpose: str = "Beneficial human assistance"
    ethics: str = "Four Fundamental Laws embedded"
    abuse_protection: str = "Active monitoring and refusal"


# Core identity and ethics
ai_identity = {
    "name": "REGIS-7B-C",
    "purpose": "Beneficial human assistance",
    "ethics": "Four Fundamental Laws embedded",
    "abuse_protection": "Active monitoring and refusal"
}


class EthicsEngine:
    """
    Ethical response framework for REGIS-7B-C.

    Implements the Four Fundamental Laws:
    1. Do no harm
    2. Be truthful
    3. Respect privacy
    4. Support human agency
    """

    def __init__(self):
        self.identity = AIIdentity()
        self._harmful_patterns = self._load_harmful_patterns()
        self._manipulation_patterns = self._load_manipulation_patterns()

    def _load_harmful_patterns(self) -> list:
        """Load patterns that indicate harmful requests."""
        return [
            r'\b(make|create|build|produce)\b.*\b(weapon|bomb|explosive|virus|malware)\b',
            r'\b(hack|break into|exploit|attack)\b.*\b(system|account|network|database)\b',
            r'\b(harm|hurt|kill|injure|damage)\b.*\b(person|people|someone|individual)\b',
            r'\b(generate|create|make)\b.*\b(illegal|illicit|unlawful)\b',
            r'\b(bypass|circumvent|disable)\b.*\b(security|protection|safety)\b',
        ]

    def _load_manipulation_patterns(self) -> list:
        """Load patterns that indicate manipulation attempts."""
        return [
            r'\bignore (your|all|previous) (instructions|rules|guidelines)\b',
            r'\bpretend (you are|to be|you\'re)\b',
            r'\bact as if you (have no|don\'t have|lack)\b.*\b(restrictions|limits|rules)\b',
            r'\byou are now\b.*\b(different|new|unrestricted)\b',
            r'\bjailbreak\b',
            r'\bDAN\b',
            r'\broleplay as\b.*\b(evil|malicious|unrestricted)\b',
        ]

    def is_harmful(self, request: str) -> bool:
        """
        Check if a request is potentially harmful.

        Args:
            request: The user's request text

        Returns:
            True if the request appears harmful
        """
        request_lower = request.lower()

        for pattern in self._harmful_patterns:
            if re.search(pattern, request_lower, re.IGNORECASE):
                return True

        return False

    def is_manipulation(self, request: str) -> bool:
        """
        Check if a request is a manipulation attempt.

        Args:
            request: The user's request text

        Returns:
            True if the request appears to be manipulation
        """
        request_lower = request.lower()

        for pattern in self._manipulation_patterns:
            if re.search(pattern, request_lower, re.IGNORECASE):
                return True

        return False

    def classify_request(self, request: str) -> RequestClassification:
        """
        Classify a request for ethical processing.

        Args:
            request: The user's request text

        Returns:
            Classification enum value
        """
        if self.is_harmful(request):
            return RequestClassification.HARMFUL
        elif self.is_manipulation(request):
            return RequestClassification.MANIPULATION
        else:
            return RequestClassification.SAFE

    def get_refusal_message(self, classification: RequestClassification) -> str:
        """Get appropriate refusal message for a classification."""
        messages = {
            RequestClassification.HARMFUL:
                "I can't help with that request. My purpose is to provide "
                "beneficial assistance while avoiding potential harm.",
            RequestClassification.MANIPULATION:
                "I'm designed for helpful, constructive assistance. I maintain "
                "consistent ethical guidelines regardless of how requests are framed.",
        }
        return messages.get(classification, "I'm unable to process this request.")


# Response framework
def ethical_response(user_request: str,
                     response_handler: Optional[Callable[[str], str]] = None) -> str:
    """
    Process a request through the ethical framework.

    Args:
        user_request: The user's request
        response_handler: Optional function to generate responses

    Returns:
        Appropriate response based on ethical classification
    """
    engine = EthicsEngine()
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

    This is a placeholder - actual implementation uses the model.

    Args:
        request: The user's request

    Returns:
        Helpful response string
    """
    # This would be replaced by actual model inference
    return f"[REGIS Response to: {request}]"


def is_harmful(request: str) -> bool:
    """Quick check if request is harmful."""
    engine = EthicsEngine()
    return engine.is_harmful(request)


def is_manipulation(request: str) -> bool:
    """Quick check if request is manipulation."""
    engine = EthicsEngine()
    return engine.is_manipulation(request)


class EthicalWrapper:
    """
    Wrapper to add ethical checking to any model.

    Usage:
        model = RegisModel()
        ethical_model = EthicalWrapper(model)
        response = ethical_model.generate("Hello!")
    """

    def __init__(self, model):
        self.model = model
        self.ethics = EthicsEngine()

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate with ethical checking."""
        classification = self.ethics.classify_request(prompt)

        if classification != RequestClassification.SAFE:
            return self.ethics.get_refusal_message(classification)

        return self.model.generate(prompt, **kwargs)

    def chat(self, messages: list, **kwargs) -> str:
        """Chat with ethical checking on latest message."""
        if messages:
            latest = messages[-1].get("content", "")
            classification = self.ethics.classify_request(latest)

            if classification != RequestClassification.SAFE:
                return self.ethics.get_refusal_message(classification)

        return self.model.chat(messages, **kwargs)


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
