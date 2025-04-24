from enum import Enum

class Tone(str, Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    FORMAL = "formal"
    CASUAL = "casual"
    ENGAGING = "engaging"




from enum import Enum

class Format(Enum):
    BULLET_ONLY = "bullet_only"
    PARAGRAPH_ONLY = "paragraph_only"
    MIXED = "mixed"


class JobDescriptionLength(Enum):
    SHORT = "Short"
    MEDIUM = "Medium"
    LONG = "Long"
