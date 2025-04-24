from flask import Blueprint, request, jsonify
from app.services.generator import generate_job_description, regenerate_with_instruction
from werkzeug.exceptions import BadRequest
from app.utils.tone_enum import Format, JobDescriptionLength, Tone

from dotenv import load_dotenv
import os

load_dotenv()  # l load variables from .env 

DJ_API_KEY = os.getenv("JOB_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 

api = Blueprint('api', __name__)

@api.route("/generate_job_description", methods=["POST"])
def generate():
        # Check Authorization Header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid authorization header"}), 401

    token = auth_header.split(" ")[1]
    if token !=DJ_API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
    try:
        data = request.get_json()  
    except BadRequest:
            return jsonify({"error": "Invalid JSON "}), 400

    if not isinstance(data, dict):
            return jsonify({"error": "Payload must be a JSON object"}), 400

    # Extract required fields from JSON
    job_title = data.get("job_title")
    job_type = data.get("job_type")
    job_level = data.get("job_level")
    department = data.get("department")
    location = data.get("location")
    work_arrangement = data.get("work_arrangement")
    salary_range = data.get("salary_range")
    application_deadline = data.get("application_deadline")
    company_name = data.get("company_name")
    language=data.get("language")
    tone=data.get("tone" ,"professional")
    emoji=data.get("emoji")
    keywords = data.get("keywords", [])  
    format=data.get('format',"mixed")
    length=data.get('length',"Medium")
    notes=data.get('notes')
    sections=data.get("sections",["description"])
    try:
        format_enum = Format(format)
    except ValueError:
        valid_formats = [f.value for f in Format]
        return jsonify({"error": f"Invalid template format/ structure . Choose from: {', '.join(valid_formats)}"}), 400
    
    try:
        length_enum = JobDescriptionLength(length)
    except ValueError:
        valid_length = [f.value for f in JobDescriptionLength]
        return jsonify({"error": f"Invalid length choices . Choose from: {', '.join(valid_length)}"}), 400
    # Validate keywords length
    if len(keywords) > 10:
        return jsonify({"error": "The keywords list cannot contain more than 10 items."}), 400

    # Check for missing fields
    required_fields = ["job_title", "company_name","language"]
    missing_fields=[field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    try:
        tone_enum = Tone(tone)
    except ValueError:
        valid_tones = [t.value for t in Tone]
        return jsonify({"error": f"Invalid tone. Choose from: {', '.join(valid_tones)}"}), 400
    try:
            result = generate_job_description(
                job_title, job_type, job_level, department, location,
                work_arrangement, company_name, salary_range, application_deadline, notes,language,tone_enum.value,emoji=emoji,keywords=keywords,format=format_enum.value,length=length_enum.value,
                sections=sections
                  )          
            # Return JSON with the job description
            return jsonify({"job_description": result}), 200
    except Exception as e:
            return jsonify({"error": str(e)}), 500
    
   


@api.route("/tone_options", methods=["GET"])
def get_tone_options():
    return jsonify({
        "tones": [tone.value for tone in Tone]
    })



@api.route('/regenerate', methods=['POST'])
def regenerate_api():
    try:
        json_data = request.get_json()
        
        if not json_data or 'base' not in json_data:
            return jsonify({'error': 'Missing "base" in request data'}), 400
        
        existing_description = json_data['base']
        user_preferences = {k: v for k, v in json_data.items() if k != 'base'}

        result = regenerate_with_instruction(existing_description, user_preferences)
        return jsonify({'updated_description': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
