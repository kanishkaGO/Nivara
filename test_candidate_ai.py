from candidate_ai.services.resume_analyzer import analyze_resume


sample_resume = """
RAHUL SHARMA

Email: rahul.sharma@example.com
Phone: 9876543210
Location: Pune, India

EDUCATION
B.Tech in Computer Science and Engineering
ABC University
2025

SKILLS
Python
SQL
Machine Learning
FastAPI
Git

EXPERIENCE
Software Engineering Intern
XYZ Technologies
January 2025 - June 2025

Worked on backend APIs using Python and FastAPI.
Developed database queries using SQL.

PROJECTS
AI Powered Job Recommendation System

Built a job recommendation system using Python
and machine learning.

CERTIFICATIONS
Python Programming Certificate

LANGUAGES
English
Hindi

PREFERRED ROLE
Machine Learning Engineer

PREFERRED WORK MODE
Remote
"""


if __name__ == "__main__":
    print("===================================")
    print("NIVARA CANDIDATE AI TEST")
    print("===================================")

    profile = analyze_resume(sample_resume)

    print("\nCandidate Profile:")
    print(profile.model_dump_json(indent=2))