import os
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from ..data.prompts import outreach_prompt
from ..data.models import TopCandidate, JobData
from dotenv import load_dotenv

# Initialize LangChain components
load_dotenv()
api_key = os.environ['OPENAI_API_KEY']
llm = ChatOpenAI(api_key=SecretStr(api_key), model='gpt-4o-mini')


def generate_outreach_message(candidate: TopCandidate, job: JobData) -> str:
    """
    Generate a personalized outreach message for a candidate.
    
    Args:
        candidate: TopCandidate object with profile and scores
        job: JobData object with job requirements
        
    Returns:
        Personalized outreach message string
    """
    # Extract candidate information from profile data
    # This would need to be enhanced based on actual profile data structure
    candidate_info = {
        "name": candidate.name,
        "current_role": "Software Engineer",  # Placeholder - would come from profile
        "current_company": "Tech Company",    # Placeholder - would come from profile
        "location": "San Francisco, CA",      # Placeholder - would come from profile
        "education": "Bachelor's in Computer Science",  # Placeholder
        "experience": "5+ years in software development"  # Placeholder
    }
    
    # Prepare inputs for the prompt
    inputs = {
        "job_title": job.title,
        "job_location": job.location,
        "experience_level": job.experience_level,
        "keywords": ", ".join(job.keywords),
        "candidate_name": candidate_info["name"],
        "current_role": candidate_info["current_role"],
        "current_company": candidate_info["current_company"],
        "candidate_location": candidate_info["location"],
        "education": candidate_info["education"],
        "experience": candidate_info["experience"],
        "fit_score": f"{candidate.fit_score:.1f}"
    }
    
    try:
        # Generate the message
        message = llm.invoke(outreach_prompt.format(**inputs))
        return str(message.content)
        
    except Exception as e:
        print(f"Error generating outreach message: {e}")
        # Fallback message
        return f"""Hi {candidate_info['name']},

I came across your profile and was impressed by your background in {candidate_info['current_role']} at {candidate_info['current_company']}. 

We have a {job.title} position available at {job.location} that I believe would be a great fit for your experience. The role requires expertise in {', '.join(job.keywords[:3])} and {job.experience_level} level experience.

Would you be interested in learning more about this opportunity? I'd love to discuss how your background aligns with our needs.

Best regards,
[Your Name]""" 