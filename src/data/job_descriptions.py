job_descriptions = [
    """
Software Engineer, ML Research
Windsurf • Full Time • Mountain View, CA • On-site • $140,000 – $300,000 + Equity
ID: SRN2025-10916

About the Company:
Windsurf (formerly Codeium) is a Forbes AI 50 company building the future of developer productivity through AI. With over 200 employees and $243M raised across multiple rounds including a Series C, Windsurf provides cutting-edge in-editor autocomplete, chat assistants, and full IDEs powered by proprietary LLMs. Their user base spans hundreds of thousands of developers worldwide, reflecting strong product-market fit and commercial traction.

Roles and Responsibilities:
• Train and fine-tune LLMs focused on developer productivity
• Design and prioritize experiments for product impact
• Analyze results, conduct ablation studies, and document findings
• Convert ML discoveries into scalable product features
• Participate in the ML reading group and contribute to knowledge sharing

Job Requirements:
• 2+ years in software engineering with fast promotions
• Strong software engineering and systems thinking skills
• Proven experience training and iterating on large production neural networks
• Strong GPA from a top CS undergrad program (MIT, Stanford, CMU, UIUC, etc.)
• Familiarity with tools like Copilot, ChatGPT, or Windsurf is preferred
• Deep curiosity for the code generation space
• Excellent documentation and experimentation discipline
• Prior experience with applied research (not purely academic publishing)
• Must be able to work in Mountain View, CA full-time onsite
• Excited to build product-facing features from ML research

Interview Process
1. Recruiter Chat (15 min)
2. Virtual Algorithm Round (LeetCode-style, 45 min)
3. Virtual ML Case Study (1 hour)
4. Onsite (3 hours): Additional ML case, implementation project, and culture interview
5. Offer Extended
""",

"""
Data Scientist, Google Play, Product
Google, Bengaluru, Karnataka, India

Minimum qualifications:
• Bachelor's degree in Statistics, Mathematics, Data Science, Engineering, Physics, Economics, or a related quantitative field.
• 5 years of experience with analysis applications (extracting insights, performing statistical analysis, or solving business problems), and coding (Python, R, SQL), or 2 years of experience with a Master's degree.

Preferred qualifications:
• Master's degree in Statistics, Mathematics, Data Science, Engineering, Physics, Economics, or a related quantitative field.
• Experience with developing machine learning models (supervised and unsupervised), Launch Experiments (A/B Testing), end-to-end Data infrastructure and Analytics pipelines.
• Experience with classification and regression, prediction and inferential tasks, training/validation criteria for machine learning algorithm performance.
• Experience in identifying opportunities for business/product improvement and defining the initiatives.
• Experience in developing new models, methods, analysis and approaches.

About the job
Help serve Google's worldwide user base of more than a billion people. Data Scientists provide quantitative support, market understanding and a strategic perspective to our partners throughout the organization. As a data-loving member of the team, you serve as an analytics expert for your partners, using numbers to help them make better decisions. You will weave stories with meaningful insight from data. You'll make critical recommendations for your fellow Googlers in Engineering and Product Management. You relish tallying up the numbers one minute and communicating your findings to a team leader the next.

Responsibilities
• Partner with Play/Apps Product Managers, Engineering, UX and other Play teams to understand user behaviors, design and analyze experiments and drive product insights to improve user experiences.
• Act as a thought partner to produce insights and metrics for various technical and business stakeholders across the Play/Apps team.
• Deliver presentations of findings and recommendations to multiple levels of leadership, creating visual displays of quantitative information.
• Follow engineering best practice to create data pipelines and models.
• Develop and automate reports, build and prototype dashboards to provide insights for problem-solving needs.
"""
# More can be added here....
]

def add_job_description(jd: str):
    """Add a new job description to the list"""
    job_descriptions.append(jd)
    print(f"Added job description. Total JDs: {len(job_descriptions)}")

def get_all_job_descriptions():
    """Get all job descriptions"""
    return job_descriptions

def get_job_description_by_index(index: int):
    """Get a specific job description by index"""
    if 0 <= index < len(job_descriptions):
        return job_descriptions[index]
    else:
        raise IndexError(f"Index {index} out of range. Total JDs: {len(job_descriptions)}") 