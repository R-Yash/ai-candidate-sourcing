import json
from src.data.models import JobData
from src.core.candidate_processor import process_all_jobs
from src.core.parse_jd import process_all_job_descriptions

def save_results(results, filename: str = 'final.json'):
    """Save results to JSON file"""
    with open(filename, 'w') as f:
        json.dump([result.model_dump() for result in results.root], f, indent=2)


def main():
    """Main workflow: parse jobs, process candidates, save results"""
    print("Starting candidate scoring and outreach generation...")
    print("Processing mode: concurrent (3 workers)")
    
    # Parse job descriptions
    print("\nParsing job descriptions...")
    jobs = process_all_job_descriptions()
    print(f"Found {len(jobs)} jobs to process")
    
    # Process all jobs
    print("\nProcessing candidates and generating scores...")
    results = process_all_jobs(jobs, max_workers=3)
    
    # Save results
    print("\nSaving results...")
    save_results(results, 'final.json')
    
    # Summary
    total_candidates = sum(result.candidates_found for result in results.root)
    total_top_candidates = sum(len(result.top_candidates) for result in results.root)
    successful_jobs = len([r for r in results.root if not r.error])
    failed_jobs = len([r for r in results.root if r.error])
    
    print(f"\nComplete! Processed {total_candidates} candidates across {len(jobs)} jobs.")
    print(f"Top candidates with outreach messages: {total_top_candidates}")
    print(f"Successful jobs: {successful_jobs}, Failed jobs: {failed_jobs}")
    print(f"Results saved to 'final.json'")


if __name__ == "__main__":
    main() 