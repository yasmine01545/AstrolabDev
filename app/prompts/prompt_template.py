#functions for building Prompts
 
from app.utils.tone_enum import Tone,Format, JobDescriptionLength,format_instructions,tone_instructions,length_ranges,section_templates 


def user_message(job_title, job_type, job_level, department, location, work_arrangement,
                 company_name, salary_range, application_deadline, notes, language,
                 tone=Tone.PROFESSIONAL.value, emoji=False, keywords=None, format=Format.MIXED, length=JobDescriptionLength.MEDIUM,sections=["description"]):
   
    sections = sections or ["description"]
    keywords = keywords or []
    emojis = {"header": "🚀💼", "desc": "🧠", "req": "📌", "ben": "🎁"} if emoji else {}

    job_details = {
        "Title": job_title, "Type": job_type, "Level": job_level,
        "Dept": department, "Loc": location, "Work": work_arrangement,
        "Comp": company_name, "Sal": salary_range, "Deadl": application_deadline
    }
    details_str = ",".join(f"{k}: {v}" for k, v in job_details.items() if v)
    output_section = ""
    if sections:
        selected_sections = {k: v for k, v in section_templates.items() if k in sections}
        output_lines = ',\n  '.join(f'"{k}": "{v}"' for k, v in selected_sections.items())
        output_section = f"""
    Output:
    Only return a JSON object with the following sections: {", ".join(sections)}.
    Do not include any other sections like requirements or benefits if not listed.
    The JSON Object must contain only selected sections as key no introductory paragraph, general company statement.
    Return the job description using only valid HTML. Do NOT use <p> tags, <br> inside list items is allowed.
    DO NOT include ANY newline characters - this means no \n, \r, or \n\n.
    Output must be pure HTML without any line breaks except those specified with <br>.
    Each list item should be on a single line with <br> for internal breaks.
   
    ```json
    {{
    {output_lines}
    }}```"""
 
    return f"""forget all previous chat history and start fresh
Generate a job description in {language} with {tone} tone using {format} style.
 
{emojis.get("header", "")} Details:
{details_str}
Keywords: {", ".join(keywords) or ""}
 
Guidelines:
- Length: {length_ranges[length]} words.
- Use {language}, {tone_instructions[tone]}.
- Apply notes: {notes or ""}.
- IMPORTANT: DO NOT use any newline characters (\\n, \\r, \\n\\n).
- All line breaks must use HTML <br> tags.
- Each list item must be on a single line.
- use {format_instructions[format]} {f'and Add emojis.' if emoji else ""}
- Only generate the following sections: {", ".join(sections)}.
- DO NOT include any introductory paragraph, general company statement, or job summary.
- Do NOT include any unlisted sections such as requirements or benefits.
- Output must begin directly with the section content.
- Format Example: <ul><li>First requirement<br>continuation of first requirement</li><li>Second requirement</li></ul>
Expected Output Format:
{{"section_name": "<ul><li>Content without newlines<br>More content</li><li>Next item</li></ul>"}}
"""




system_prompt="""you are a professional recruiter. Your task is to generate a compelling job description based on the provided job details.
The final job description should be well-structured with clear section headings and formatted text.
"""


def regeneration_prompt(existing_description: str, data: dict) -> str:
    # Check if the user provided preferences
    has_preferences = any(k != 'base' and v is not None for k, v in data.items())
    # Generate clear instructions based on provided preferences
    instruction_text = []  # Initialize as a list
    # Add user preferences from the data dictionary (except "base")
    for key, value in data.items():
        if key != "base" and value is not None:
            if isinstance(value, list):
                instruction_text.append(f"- {key.capitalize()}: {', '.join(value)}")
            else:
                instruction_text.append(f"- {key.capitalize()}: {value}")
    
    # We will only add format preference if it's explicitly provided in `data`
    format_value = data.get("format")
    if format_value and format_value in format_instructions:
        instruction_text.append(f"- Format: {format_instructions[format_value]}")
    else:
        # If no format change is specified, mention that the format should remain the same
        instruction_text.append(f"- Format: Keep the current format unless otherwise specified.")

    tone = data.get("tone")
    if tone and tone in tone_instructions:
        instruction_text.append(f"- Tone: {tone_instructions[tone]}")
    # Add language instruction to maintain the original language (French or other)
    instruction_text.append("- Language: Keep the content in the same language.")
    
    # Join the instructions into a single text block
    instruction_text = "\n".join(instruction_text) if instruction_text else "- No preferences provided"

    # Construct the final prompt with the updated instructions
    return f"""
You are a professional recruiter. Your task is to **update and apply only the user preferences** the following job description .DO NOt forget all previous chat history and start fresh.

✏️ **User Preferences:**
{instruction_text}

---
📄 **Original Job Description:**
{existing_description}

--- 
✅ Please return only the {"updated" if has_preferences else "original"} job description.
- {"Apply the user preferences and ensure clarity and coherence." if has_preferences else "Return the text exactly as it is."}
- **Preserve existing sections** in the job description , and only add new sections specified in the "sections" preference .
- **Ensure that section names (e.g., 'description', 'requirements') are provided and properly formatted.*
- IMPORTANT: DO NOT use any newline characters (\\n, \\r, \\n\\n).

"""




