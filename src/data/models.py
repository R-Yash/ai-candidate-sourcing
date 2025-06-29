from typing import List, Optional
from pydantic import BaseModel, Field, RootModel

class Education(BaseModel):
    school: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None

class Experience(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class ProfileData(BaseModel):
    educations: List[Education] = Field(default_factory=list)
    experiences: List[Experience] = Field(default_factory=list)
    city: Optional[str] = None
    full_name: Optional[str] = None

class JobData(BaseModel):
    title: str
    location: str
    experience_level: str
    keywords: List[str] = Field(default_factory=list)

class ScoreBreakdown(BaseModel):
    education: float = Field(ge=0, le=10)
    trajectory: float = Field(ge=0, le=10)
    company: float = Field(ge=0, le=10)
    skills: float = Field(ge=0, le=10)
    location: float = Field(ge=0, le=10)
    tenure: float = Field(ge=0, le=10)

class CandidateScores(BaseModel):
    education_score: float = Field(ge=0, le=10)
    career_trajectory_score: float = Field(ge=0, le=10)
    company_relevance_score: float = Field(ge=0, le=10)
    experience_match_score: float = Field(ge=0, le=10)
    location_match_score: float = Field(ge=0, le=10)
    tenure_score: float = Field(ge=0, le=10)
    fit_score: float = Field(ge=0, le=10)

class TopCandidate(BaseModel):
    name: str
    linkedin_url: str
    fit_score: float = Field(ge=0, le=10)
    score_breakdown: ScoreBreakdown
    outreach_message: Optional[str] = None

class JobResult(BaseModel):
    job_id: str
    candidates_found: int = Field(ge=0)
    top_candidates: List[TopCandidate] = Field(default_factory=list)
    all_candidates: List[TopCandidate] = Field(default_factory=list)
    error: Optional[str] = None

class FinalResults(RootModel[List[JobResult]]):
    pass 