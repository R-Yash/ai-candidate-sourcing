import os
import json
from typing import List, Optional
from dataclasses import dataclass, asdict
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field, SecretStr
from ..data.prompts import keyword_extraction_prompt
from dotenv import load_dotenv
from ..data.job_descriptions import get_all_job_descriptions
from ..data.models import JobData

load_dotenv()
api_key = os.environ['OPENAI_API_KEY']

llm = ChatOpenAI(api_key=SecretStr(api_key), model='gpt-4o-mini')

class JobExtractionSchema(BaseModel):
    """Pydantic schema for structured job information extraction"""
    id: str = Field(description="The job ID")
    title: str = Field(description="The job title or position name")
    location: str = Field(description="The job location (city, state, country, or remote)")
    experience_level: str = Field(description="Required experience level (e.g., Entry, Mid, Senior, Executive)")
    keywords: List[str] = Field(description="Key skills, technologies, or requirements mentioned in the job description")

output_parser = JsonOutputParser(pydantic_object=JobExtractionSchema)
chain = keyword_extraction_prompt | llm | output_parser   

def parse_job_description(job_description: str) -> Optional[JobData]:
    """
    Parse a job description and extract structured information
    
    Args:
        job_description: The text of the job description
        
    Returns:
        JobData object containing extracted information, or None if parsing fails
    """
    try:
        result = chain.invoke({
            "job_description": job_description,
            "format_instructions": output_parser.get_format_instructions()
        })
                    
        return JobData(
            title=result["title"],
            location=result["location"],
            experience_level=result["experience_level"],
            keywords=result["keywords"]
        )
        
    except Exception as e:
        print(f"Error parsing job description: {e}")
        return None

def process_all_job_descriptions() -> List[JobData]:
    """
    Process all job descriptions and return them as a list
    
    Returns:
        List of JobData objects containing parsed job information
    """
    job_descriptions = get_all_job_descriptions()
    parsed_jobs = []
    
    for i, jd in enumerate(job_descriptions):
        print(f"\nProcessing job description {i+1}/{len(job_descriptions)}")
        job_info = parse_job_description(jd)
        if job_info:
            parsed_jobs.append(job_info)
            print(f"Successfully parsed job: {job_info.title}")
        else:
            print("Failed to parse job description")
    
    print(f"\nTotal jobs parsed: {len(parsed_jobs)}")
    return parsed_jobs

if __name__ == "__main__":
    # For testing purposes, you can still run this file directly
    jobs = process_all_job_descriptions()
    print(f"Parsed {len(jobs)} jobs successfully")
