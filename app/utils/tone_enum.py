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




    # Add tone instructions
tone_instructions = {
        Tone.PROFESSIONAL.value: "Keep the tone polished, concise, and suitable for a corporate audience.",
        Tone.FORMAL.value: "Use formal language. Maintain a professional and respectful tone throughout.",
       Tone.FRIENDLY.value: "Make the tone warm, approachable, and inviting. Slightly conversational.",
        Tone.CASUAL.value: "Use a relaxed and conversational tone, even inside list items. Feel free to simplify or rephrase formal statements into everyday language.",
        Tone.ENGAGING.value: "Use enthusiastic and dynamic language to draw attention and keep the reader interested."
    }


length_ranges = {JobDescriptionLength.SHORT.value: "150-300", JobDescriptionLength.MEDIUM.value: "300-500", JobDescriptionLength.LONG.value: "500-800"}



format_instructions = {
        Format.BULLET_ONLY.value: "Use valid HTML tags only (<ul>/<li>).",
        Format.PARAGRAPH_ONLY.value: "Use HTML <p> only, no list tags.",
        Format.MIXED.value: "Mix HTML <p> and <ul>/<li>, start with intro <p>."
    }

section_templates = {
    "description": "Only introduce the company overview, mission, culture and the purpose of the job.",
    "requirements": "Only list the duties, tasks, and skills required.",
    "benefits":  "Only list compensation, perks, and career growth."
}
