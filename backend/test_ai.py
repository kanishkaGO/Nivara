from app.services.ai_parser import parse_resume_with_ai


sample_resume = """
Rahul Sharma
rahul@example.com
+91 9876543210

Software Developer

Skills:
Python, FastAPI, PostgreSQL, Git

Education:
B.Tech in Computer Science, ABC University, 2024

Experience:
Software Developer at XYZ Technologies for 2 years.

Projects:
Nivara - AI powered inclusive career platform.
Technologies: Python, FastAPI, PostgreSQL

Certifications:
Python Programming Certificate

Languages:
English, Hindi
"""


profile = parse_resume_with_ai(sample_resume)

print(profile.model_dump_json(indent=2))