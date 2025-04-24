#entry point for testing




import os
from dotenv import load_dotenv
from app.services.generator import generate_job_description, regenerate_with_instruction
from app.utils.config import GROQ_API_KEY
# Example job description fields
job_title = "Software Engineer"
job_type="CIVP"
job_level="Entry level"
department="IT"
location = "Tunisia"
work_arrangement="On site"
salary_range = "$80,000 - $120,000 per year"
application_deadline="2 months"
company_name="astrolab"
language="french"
# Generate the job description
#job_description = generate_job_description(job_title, job_type, job_level, department, location, work_arrangement,company_name,salary_range,application_deadline,language)

# Print the generated job description
#print(job_description)

#with open("output_arabic.txt", "w", encoding="utf-8") as f:
#    f.write(job_description)
# Sample original job description
original_jd = """
We're seeking a talented Front End Engineer to shape user experiences that impact millions! As a key member of our dynamic team, you will build cutting-edge web applications, developing and maintaining scalable front-end code using HTML/CSS, JavaScript, and modern web techniques. You'll collaborate closely with UI/UX designers to create engaging user interfaces and implement responsive designs for seamless cross-device functionality. Optimizing front-end performance, participating in code reviews, integrating APIs with back-end engineers, and troubleshooting front-end issues will also be integral to your role.

To qualify, you’ll need a Bachelor's degree in Computer Science or related experience, plus 3+ years of front-end development experience. Proficiency , JavaScript, and related web technologies is essential, as is experience with modern JavaScript frameworks (React.js, Vue.js, or Angular). A solid understanding of responsive design, experience with Git, and excellent problem-solving and communication skills are also required.   

We're a forward-thinking tech company revolutionizing how people connect with information through innovative software. We foster a collaborative culture of continuous learning and growth. Apply now at www.linkdin.com.    
"""

# Sample user preferences (data)
data = {
   
    "keywords":["HTML/CSS"],
    "length": "short",
    "base": original_jd  # This will be excluded from the instructions
}

# Generate the updated job description prompt
#prompt = regenerate_with_instruction(original_jd, data)

# Output the generated prompt (for testing or feeding to the model)
#print(prompt)

# Correct way (Python example)
import google.generativeai as genai
genai.configure(api_key="AIzaSyClE0sKTVx8IWUrmxgoWeufv5peue3E4v4")

model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content("Hello, world!")
print(response.text)