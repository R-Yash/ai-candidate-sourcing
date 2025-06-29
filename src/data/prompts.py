from langchain_core.prompts import ChatPromptTemplate

keyword_extraction_prompt = ChatPromptTemplate.from_template(
"""
You are an expert job description parser. Extract the following information from the given job description:

Job Description:
{job_description}

Please extract and return the following information in JSON format:
- title: The job title or position name
- location: The job location (city, state, country, or remote)
- experience_level: Required experience level (Entry, Mid, Senior, Executive, or specific years)
- keywords: List of key skills, technologies, or requirements mentioned

Focus on extracting the most relevant and specific information. For keywords, include technical skills, programming languages, frameworks, tools, and key requirements.

{format_instructions}

"""
)

scoring_prompt = ChatPromptTemplate.from_template(
"""
You are an expert candidate evaluator. Analyze the candidate's LinkedIn profile data and score them based on the following criteria for the given job position.

Job Details:
Title: {job_title}
Location: {job_location}
Experience Level: {experience_level}
Keywords: {keywords}

Candidate Profile Data:
{profile_data}

Please evaluate the candidate using this scoring framework and return scores in JSON format:

**Education (20% weight)**
- Elite schools (MIT, Stanford, Harvard, etc.): 9-10
- Strong schools (Top 50 universities): 7-8  
- Standard universities: 5-6
- Clear progression (Bachelor's to Master's/PhD): 8-10

**Career Trajectory (20% weight)**
- Steady growth (increasing responsibility): 6-8
- Limited progression: 3-5

**Company Relevance (15% weight)**
- Top tech companies (Google, Microsoft, Apple, etc.): 9-10
- Relevant industry experience: 7-8
- Any professional experience: 5-6

**Experience Match (25% weight)**
- Perfect skill match with job requirements: 9-10
- Strong overlap with required skills: 7-8
- Some relevant skills: 5-6

**Location Match (10% weight)**
- Exact city match: 10
- Same metro area: 8
- Remote-friendly or willing to relocate: 6

**Tenure (10% weight)**
- 2-3 years average per role: 9-10
- 1-2 years average: 6-8
- Job hopping (less than 1 year average): 3-5

Calculate the weighted fit_score out of 10 using the formula:
fit_score = (education_score * 0.20) + (career_trajectory_score * 0.20) + (company_relevance_score * 0.15) + (experience_match_score * 0.25) + (location_match_score * 0.10) + (tenure_score * 0.10)

Return the scores in this exact JSON format:
{{
    "education_score": <score>,
    "career_trajectory_score": <score>,
    "company_relevance_score": <score>,
    "experience_match_score": <score>,
    "location_match_score": <score>,
    "tenure_score": <score>,
    "fit_score": <weighted_score_out_of_10>,
    "reasoning": "<brief explanation of the overall score>"
}}
"""
)

outreach_prompt = ChatPromptTemplate.from_template(
"""
You are a professional recruiter reaching out to a potential candidate. Create a personalized LinkedIn message based on the candidate's profile and the job opportunity.

Job Details:
Title: {job_title}
Location: {job_location}
Experience Level: {experience_level}
Key Skills: {keywords}

Candidate Profile:
Name: {candidate_name}
Current Role: {current_role}
Company: {current_company}
Location: {candidate_location}
Education: {education}
Experience: {experience}
Fit Score: {fit_score}/10

Create a personalized, professional LinkedIn message that:
1. References specific details from their profile
2. Mentions their relevant experience or education
3. Explains why they're a great fit for the role
4. Maintains a professional but friendly tone
5. Includes a clear call-to-action
6. Is concise (150-200 words max)

Return only the message content, no JSON formatting.
"""
) 