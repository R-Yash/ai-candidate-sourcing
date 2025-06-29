import os
import json
import time
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..data.models import JobData, JobResult, TopCandidate, FinalResults, ScoreBreakdown
from ..services.api_client import search_linkedin_profiles, get_linkedin_profile
from .scorer import score_candidate
from .outreach import generate_outreach_message


def process_job(job: JobData) -> JobResult:
    """
    Process a single job: find candidates, score them, and generate outreach messages.
    
    Args:
        job: JobData object containing job information
        
    Returns:
        JobResult object with top candidates and scores
    """
    print(f"Processing job: {job.title}")
    
    # Search for LinkedIn profiles
    search_query = f"{job.title} {job.location} site:linkedin.com/in/"
    profile_urls = search_linkedin_profiles(search_query)
    
    if not profile_urls:
        print("No LinkedIn profiles found")
        return JobResult(job_id=job.title, candidates_found=0, top_candidates=[])
    
    print(f"Found {len(profile_urls)} LinkedIn profiles")
    
    # Fetch and score candidates
    candidates = []
    for i, url in enumerate(profile_urls):       
        # Rate limiting
        time.sleep(1)
        
        # Fetch profile data
        profile_data = get_linkedin_profile(url)
        if not profile_data:
            continue
        
        # Get candidate name for logging
        candidate_name = profile_data.get('full_name', 'Unknown')
        print(f"Processing: {candidate_name} for job: {job.title}")
        
        # Score the candidate
        scores = score_candidate(profile_data, job)
        
        # Create candidate object
        candidate = TopCandidate(
            name=profile_data.get('full_name', 'Unknown'),
            linkedin_url=url,
            fit_score=scores.fit_score,
            score_breakdown=ScoreBreakdown(
                education=scores.education_score,
                trajectory=scores.career_trajectory_score,
                company=scores.company_relevance_score,
                skills=scores.experience_match_score,
                location=scores.location_match_score,
                tenure=scores.tenure_score
            )
        )
        
        candidates.append(candidate)
    
    # Sort by fit score and take top 5
    candidates.sort(key=lambda x: x.fit_score, reverse=True)
    top_candidates = candidates[:5]
    
    # Generate outreach messages for top candidates only
    for candidate in top_candidates:
        try:
            message = generate_outreach_message(candidate, job)
            candidate.outreach_message = message
        except Exception as e:
            print(f"Error generating outreach message: {e}")
            candidate.outreach_message = "Unable to generate personalized message."
    
    # Set empty outreach messages for all other candidates
    for candidate in candidates[5:]:
        candidate.outreach_message = ""
    
    return JobResult(
        job_id=job.title,
        candidates_found=len(candidates),
        top_candidates=top_candidates,
        all_candidates=candidates
    )


def process_all_jobs(jobs: List[JobData], max_workers: int = 3) -> FinalResults:
    """
    Process all jobs concurrently and return comprehensive results.
    
    Args:
        jobs: List of JobData objects to process
        max_workers: Maximum number of concurrent jobs to process (default: 3)
        
    Returns:
        FinalResults object containing all job results
    """
    results = []
    completed_jobs = 0
    
    print(f"Starting concurrent processing with {max_workers} workers...")
    
    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all jobs to the executor
        future_to_job = {executor.submit(process_job, job): job for job in jobs}
        
        # Process completed jobs as they finish
        for future in as_completed(future_to_job):
            job = future_to_job[future]
            completed_jobs += 1
            
            try:
                result = future.result()
                results.append(result)
                
                # Summary for this job
                print(f"\nCompleted job {completed_jobs}/{len(jobs)}: {job.title}")
                print(f"Candidates found: {result.candidates_found}")
                if result.top_candidates:
                    print(f"Top candidate score: {result.top_candidates[0].fit_score:.1f}/10")
                print("-" * 50)
                
            except Exception as e:
                print(f"\nError processing job {job.title}: {e}")
                # Create a failed result
                failed_result = JobResult(
                    job_id=job.title,
                    candidates_found=0,
                    top_candidates=[],
                    error=f"Processing failed: {str(e)}"
                )
                results.append(failed_result)
    
    print(f"\nConcurrent processing complete! Processed {len(results)} jobs.")
    return FinalResults(results)


def process_all_jobs_sequential(jobs: List[JobData]) -> FinalResults:
    """
    Process all jobs sequentially (original implementation).
    Kept for comparison or when concurrent processing is not desired.
    
    Args:
        jobs: List of JobData objects to process
        
    Returns:
        FinalResults object containing all job results
    """
    results = []
    
    for i, job in enumerate(jobs):
        print(f"\nProcessing job {i+1}/{len(jobs)}")
        result = process_job(job)
        results.append(result)
        
        # Summary for this job
        print(f"Job: {job.title}")
        print(f"Candidates found: {result.candidates_found}")
        if result.top_candidates:
            print(f"Top candidate score: {result.top_candidates[0].fit_score:.1f}/10")
        print("-" * 50)
    
    return FinalResults(results) 