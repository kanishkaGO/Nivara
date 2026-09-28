SKILL_CATEGORIES = {
    "technology": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#",
        "React", "Angular", "Vue", "HTML", "CSS", "Django", "Flask",
        "FastAPI", "Node.js", "SQL", "MySQL", "PostgreSQL", "MongoDB",
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git",
        "REST API", "Machine Learning", "Deep Learning",
        "Artificial Intelligence", "Data Science", "Data Analysis"
    ],

    "business_finance": [
        "Accounting", "Bookkeeping", "Financial Analysis", "Auditing",
        "Taxation", "Payroll", "Budgeting", "Forecasting",
        "Financial Reporting", "Excel", "Tally", "SAP", "QuickBooks"
    ],

    "human_resources": [
        "Recruitment", "Talent Acquisition", "Human Resources",
        "Employee Relations", "HR Management",
        "Performance Management", "Training and Development"
    ],

    "sales_marketing": [
        "Sales", "Business Development", "Digital Marketing",
        "Marketing", "Content Marketing", "SEO", "SEM",
        "Social Media Marketing", "Email Marketing", "CRM",
        "Lead Generation", "Customer Relationship Management"
    ],

    "design_creative": [
        "Graphic Design", "UI Design", "UX Design", "UI/UX",
        "Figma", "Adobe Photoshop", "Adobe Illustrator",
        "Video Editing", "Photography", "Illustration",
        "Content Creation", "Copywriting"
    ],

    "education": [
        "Teaching", "Lesson Planning", "Curriculum Development",
        "Classroom Management", "Tutoring", "Training",
        "Instructional Design", "Research"
    ],

    "healthcare": [
        "Patient Care", "Nursing", "Clinical Research",
        "Medical Coding", "Medical Billing", "Healthcare Management",
        "Pharmacy", "First Aid", "Patient Counseling"
    ],

    "customer_service": [
        "Customer Service", "Customer Support", "Technical Support",
        "Call Center", "Communication", "Complaint Resolution",
        "Help Desk", "Client Relations"
    ],

    "administration": [
        "Administration", "Office Management", "Data Entry",
        "Documentation", "Scheduling", "Record Keeping",
        "Microsoft Office", "Communication"
    ],

    "operations": [
        "Operations Management", "Project Management",
        "Supply Chain Management", "Inventory Management",
        "Logistics", "Procurement", "Quality Control",
        "Process Improvement"
    ],

    "legal": [
        "Legal Research", "Contract Management", "Compliance",
        "Corporate Law", "Legal Writing", "Litigation"
    ],

    "general": [
        "Leadership", "Teamwork", "Problem Solving",
        "Time Management", "Critical Thinking",
        "Organization", "Adaptability"
    ]
}

def extract_skills(description: str) -> list[str]:
    if not description:
        return []

    description_lower = description.lower()

    found_skills = []

    for skills in SKILL_CATEGORIES.values():
        for skill in skills:
            if skill.lower() in description_lower:
                found_skills.append(skill)

    return list(dict.fromkeys(found_skills))