from pathlib import Path

from candidate_ai.utils.resume_parser import extract_resume_text
from candidate_ai.services.resume_analyzer import analyze_resume


def analyze_resume_file(file_path: str):
    path = Path(file_path)

    print("\n===================================")
    print("NIVARA RESUME ANALYSIS")
    print("===================================")

    print(f"\nFile: {path.name}")

    # Step 1: Extract text
    resume_text = extract_resume_text(str(path))

    if not resume_text:
        raise ValueError("No readable text found in the resume.")

    print("\nResume text extracted successfully.")
    print(f"Characters extracted: {len(resume_text)}")

    # Step 2: Analyze using Ollama
    profile = analyze_resume(resume_text)

    print("\n===================================")
    print("CANDIDATE PROFILE")
    print("===================================")

    print(profile.model_dump_json(indent=2))

    return profile


if __name__ == "__main__":
    # Change this to your actual PDF/DOCX file.
    resume_file =  r"C:\Users\KANISHKA GOSWAMI\Downloads\ResumeRIDHI.PDF"

    analyze_resume_file(resume_file)