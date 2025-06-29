# Syn - AI-Powered Candidate Sourcing and Outreach

An intelligent system that parses job descriptions, finds relevant candidates on LinkedIn, scores them based on job requirements, and generates personalized outreach messages.

## Project Structure

```
Syn/
├── src/
│   ├── core/           # Core business logic
│   │   ├── parse_jd.py           # Job description parsing
│   │   ├── scorer.py             # Candidate scoring
│   │   ├── candidate_processor.py # Main processing pipeline
│   │   └── outreach.py           # Outreach message generation
│   ├── data/           # Data models and job descriptions
│   │   ├── models.py             # Pydantic data models
│   │   ├── job_descriptions.py   # Job description data
│   │   └── prompts.py            # LangChain prompts
│   └── services/       # External API integrations
│       └── api_client.py         # LinkedIn and Google APIs
├── main.py             # Main entry point
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## Quick Start

### Prerequisites

1. **Python 3.8+** with uv package manager
2. **API Keys** (set in `.env` file):
   - `OPENAI_API_KEY` - For GPT-4 parsing and scoring
   - `GOOGLE_SEARCH_API_KEY` - For LinkedIn profile search
   - `GOOGLE_SEARCH_CSE_ID` - Google Custom Search Engine ID
   - `RAPID_API_KEY` - For LinkedIn profile data extraction
   - `RAPID_API_HOST` - RapidAPI host for LinkedIn service

### Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd Syn
   uv sync
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Add job descriptions**:
   Edit `src/data/job_descriptions.py` to add your job descriptions.

### Usage

Run the complete pipeline:
```bash
python main.py
```

**Performance Notes:**
- Concurrent mode can significantly speed up processing when you have multiple jobs
- Default worker count (3) balances speed with API rate limits
- Adjust worker count based on your API limits and system resources

This will:
1. Parse all job descriptions using GPT-4
2. Search for relevant candidates on LinkedIn
3. Score candidates based on job requirements
4. Generate personalized outreach messages
5. Save results to specified output file

## Features

### Concurrent Job Processing
- **Multi-threaded execution**: Process multiple jobs simultaneously
- **Configurable workers**: Adjust concurrent worker count based on API limits
- **Error handling**: Graceful handling of individual job failures
- **Progress tracking**: Real-time progress updates for each job
- **Fallback mode**: Option to use sequential processing when needed

### Job Description Parsing
- Extracts job title, location, experience level, and keywords
- Uses GPT-4 for intelligent parsing
- Structured output with Pydantic validation

### Candidate Sourcing
- Google Custom Search API for LinkedIn profile discovery
- RapidAPI for detailed profile data extraction
- Configurable search queries based on job requirements

### AI-Powered Scoring
- Multi-criteria scoring system:
  - **Education** (20%): School prestige and degree progression
  - **Career Trajectory** (20%): Growth and responsibility progression
  - **Company Relevance** (15%): Industry and company prestige
  - **Experience Match** (25%): Skills alignment with job requirements
  - **Location Match** (10%): Geographic compatibility
  - **Tenure** (10%): Job stability and progression patterns

### Personalized Outreach
- GPT-4 generated personalized messages
- References specific candidate experience and education
- Professional tone with clear call-to-action
- 150-200 word optimal length

## Configuration

### Job Descriptions
Add job descriptions in `src/data/job_descriptions.py`:
```python
job_descriptions = [
    """
    Your job description here...
    """,
]
```

### Scoring Weights
Modify scoring weights in `src/data/prompts.py` under the `scoring_prompt`.

### API Configuration
All API configurations are in `.env`:
```env
OPENAI_API_KEY=your_openai_key
GOOGLE_SEARCH_API_KEY=your_google_key
GOOGLE_SEARCH_CSE_ID=your_cse_id
RAPID_API_KEY=your_rapidapi_key
RAPID_API_HOST=your_rapidapi_host
```

## Output

Results are saved to `final.json` with the following structure:
```json
[
  {
    "job_id": "unique_id",
    "candidates_found": 10,
    "top_candidates": [
      {
        "name": "Top Candidate Name",
        "linkedin_url": "https://linkedin.com/in/...",
        "fit_score": 8.5,
        "score_breakdown": {
          "education": 9.0,
          "trajectory": 8.0,
          "company": 7.5,
          "skills": 9.0,
          "location": 8.0,
          "tenure": 8.5
        },
        "outreach_message": "Personalized message..."
      }
    ],
    "all_candidates": [
      {
        "name": "All Candidate Names",
        "linkedin_url": "https://linkedin.com/in/...",
        "fit_score": 7.2,
        "score_breakdown": {
          "education": 8.0,
          "trajectory": 7.0,
          "company": 6.5,
          "skills": 7.5,
          "location": 7.0,
          "tenure": 7.0
        },
        "outreach_message": "Personalized message..." // For top 5 candidates
        // "outreach_message": "" // Empty for other candidates
      }
    ]
  }
]
```

**Data Structure Notes:**
- **top_candidates**: Top 5 candidates with personalized outreach messages
- **all_candidates**: All processed candidates with scores (top 5 have outreach messages, others have empty messages)
- **candidates_found**: Total number of candidates processed for this job

## Development

### Project Structure
- **Core Logic**: Business logic in `src/core/`
- **Data Models**: Pydantic models in `src/data/`
- **External Services**: API clients in `src/services/`

### Adding New Features
1. Add new modules to appropriate `src/` subdirectories
2. Update `__init__.py` files for clean imports
3. Add tests for new functionality
4. Update this README

### Testing
```bash
# Run tests (when implemented)
uv run pytest

# Run linting
uv run ruff check .

# Run formatting
uv run ruff format .
```

## License

[Add your license here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For questions or issues, please open a GitHub issue or contact [your-email].
