

#the main logic for generating job description

from typing import List
from app.prompts.prompt_template import regeneration_prompt, user_message
from app.models.llm_client import generate_with_fallback

def generate_job_description(job_title: str, job_type: str,job_level: str,department: str,location: str,work_arrangement: str,company_name: str,salary_range: str,application_deadline: str,notes:str,language:str,
                              tone: str,emoji:bool,keywords:List[str]=None,format:str="mixed",length:str="Medium",sections: List[str] = None) -> str:
    

    #,sections:List[str]=None
    if keywords is None:
        keywords = []
    user_prompt = user_message(
        job_title=job_title,
        job_type=job_type,
        job_level=job_level,
         department= department,
         location=location,
          work_arrangement = work_arrangement,
          company_name=company_name,
        salary_range=salary_range,
        application_deadline=application_deadline,
        notes=notes,
        language=language,
        tone=tone,
        emoji=emoji,
        keywords=keywords,
        format=format,
        length=length,
        sections=sections
        
        
    )
    print("------------------------------------------------------------------------"+user_prompt)
    #if the first api fails ,change the api
    return generate_with_fallback(user_prompt)
 
   


def regenerate_with_instruction(existing_description: str, data: dict) -> str:
    # regeneration function
    prompt = regeneration_prompt(existing_description, data)




    print("#######################################################"+prompt)
    # Call the model 
    return generate_with_fallback(prompt)





