from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_candidate_not_found():
    response = client.get("/api/v1/candidate/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate not found."

def test_candidate_exists():
    response = client.get("/api/v1/candidate/1")

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "name" in data
    assert "skills" in data
    assert "education" in data
    assert "experience" in data
    assert "projects" in data
    assert "certifications" in data
    assert "languages" in data
    assert "accessibility_requirements" in data
    assert "work_preferences" in data


def test_update_accessibility():
    payload = {
        "screen_reader": True,
        "captions": False,
        "sign_language_interpreter": False,
        "wheelchair_accessible": False,
        "flexible_working_hours": True,
        "remote_work": True,
        "assistive_technology": True,
        "accessible_transportation": False,
        "other": ""
    }

    response = client.put(
        "/api/v1/profile/1/accessibility",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["candidate_id"] == 1
    assert data["accessibility_requirements"]["screen_reader"] is True
    assert data["accessibility_requirements"]["remote_work"] is True


def test_update_preferences():
    payload = {
        "work_mode": ["remote"],
        "preferred_locations": ["Raipur"],
        "job_types": ["full_time"],
        "preferred_roles": [
            "Data Scientist",
            "Machine Learning Engineer"
        ]
    }

    response = client.put(
        "/api/v1/profile/1/preferences",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["candidate_id"] == 1
    assert data["work_preferences"]["work_mode"] == ["remote"]
    assert "Data Scientist" in data["work_preferences"]["preferred_roles"]

def test_resume_rejects_unsupported_file():
    response = client.post(
        "/api/v1/resume/upload",
        files={
            "file": (
                "resume.txt",
                b"This is not a supported resume format.",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert "PDF and DOCX" in response.json()["detail"]


def test_resume_rejects_empty_file():
    response = client.post(
        "/api/v1/resume/upload",
        files={
            "file": (
                "resume.pdf",
                b"",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty."


def test_profile_completeness():
    response = client.get(
        "/api/v1/candidate/1/completeness"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["candidate_id"] == 1
    assert "completion_percentage" in data
    assert "completed_sections" in data
    assert "total_sections" in data
    assert "missing_sections" in data

    assert 0 <= data["completion_percentage"] <= 100
    assert data["completed_sections"] <= data["total_sections"]

def test_update_basic_profile():
    payload = {
        "name": "Kanishka Goswami",
        "email": "kanishkagoswami113@gmail.com",
        "phone": "+91-7000186166",
        "location": "Raipur, Chhattisgarh, India"
    }

    response = client.put(
        "/api/v1/candidate/1",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["candidate_id"] == 1
    assert data["candidate"]["name"] == "Kanishka Goswami"
    assert data["candidate"]["email"] == (
        "kanishkagoswami113@gmail.com"
    )
    assert data["candidate"]["location"] == (
        "Raipur, Chhattisgarh, India"
    )


def test_update_basic_profile_rejects_invalid_email():
    payload = {
        "name": "Kanishka Goswami",
        "email": "not-an-email",
        "phone": "+91-7000186166",
        "location": "Raipur, Chhattisgarh, India"
    }

    response = client.put(
        "/api/v1/candidate/1",
        json=payload
    )

    assert response.status_code == 422