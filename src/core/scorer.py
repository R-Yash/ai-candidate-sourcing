import os
import json
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field, SecretStr
from ..data.prompts import scoring_prompt
from ..data.models import ProfileData, CandidateScores, JobData
from dotenv import load_dotenv

# Initialize LangChain components
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = JsonOutputParser()


def score_candidate(profile: Dict[Any, Any], job: JobData) -> CandidateScores:
    """
    Score a candidate based on their LinkedIn profile data and job requirements.
    
    Args:
        profile: LinkedIn profile data from the API
        job: Job details from parsed_jobs.json
        
    Returns:
        CandidateScores object containing all scores
    """
    if not profile:
        return CandidateScores(
            education_score=0,
            career_trajectory_score=0,
            company_relevance_score=0,
            experience_match_score=0,
            location_match_score=0,
            tenure_score=0,
            fit_score=0
        )
    
    # Extract only relevant fields from profile
    profile_data = {
        "educations": profile.get("educations", []),
        "experiences": profile.get("experiences", []),
        "city": profile.get("city", "")
    }
    
    # Prepare the prompt inputs
    inputs = {
        "job_title": job.title,
        "job_location": job.location,
        "experience_level": job.experience_level,
        "keywords": ", ".join(job.keywords),
        "profile_data": json.dumps(profile_data, indent=2)
    }
    
    try:
        # Create the chain
        chain = scoring_prompt | llm | parser
        
        # Get the scores
        raw_scores = chain.invoke(inputs)
        
        # Ensure all scores are numeric and validate with Pydantic
        scores = CandidateScores(
            education_score=float(raw_scores.get('education_score', 0)),
            career_trajectory_score=float(raw_scores.get('career_trajectory_score', 0)),
            company_relevance_score=float(raw_scores.get('company_relevance_score', 0)),
            experience_match_score=float(raw_scores.get('experience_match_score', 0)),
            location_match_score=float(raw_scores.get('location_match_score', 0)),
            tenure_score=float(raw_scores.get('tenure_score', 0)),
            fit_score=float(raw_scores.get('fit_score', 0))
        )
        
        return scores
        
    except Exception as e:
        print(f"Error scoring candidate: {e}")
        return CandidateScores(
            education_score=0,
            career_trajectory_score=0,
            company_relevance_score=0,
            experience_match_score=0,
            location_match_score=0,
            tenure_score=0,
            fit_score=0
        ) 