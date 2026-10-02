import { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  /* =====================================================
     REFS
     ===================================================== */

  const fileInputRef = useRef(null);
  const editProfileRef = useRef(null);
  const accessibilityRef = useRef(null);
  const preferencesRef = useRef(null);

  /* =====================================================
     MAIN STATE
     ===================================================== */

  const [candidateId, setCandidateId] = useState(null);
  const [candidate, setCandidate] = useState(null);

  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const [completeness, setCompleteness] = useState(null);
  const [loadingCompleteness, setLoadingCompleteness] =
    useState(false);

  const [editingProfile, setEditingProfile] = useState(false);

  /* =====================================================
     EDIT PROFILE STATE
     ===================================================== */

  const [profileForm, setProfileForm] = useState({
    name: "",
    email: "",
    phone: "",
    location: "",
  });

  const [savingProfile, setSavingProfile] = useState(false);

  /* =====================================================
     ACCESSIBILITY STATE
     ===================================================== */

  const defaultAccessibility = {
    screen_reader: false,
    captions: false,
    sign_language_interpreter: false,
    wheelchair_accessible: false,
    flexible_working_hours: false,
    remote_work: false,
    assistive_technology: false,
    accessible_transportation: false,
    other: "",
  };

  const [accessibility, setAccessibility] = useState(
    defaultAccessibility
  );

  const [savingAccessibility, setSavingAccessibility] =
    useState(false);

  /* =====================================================
     WORK PREFERENCES STATE
     ===================================================== */

  const defaultPreferences = {
    work_mode: [],
    preferred_locations: [],
    job_types: [],
    preferred_roles: [],
  };

  const [preferences, setPreferences] = useState(
    defaultPreferences
  );

  const [savingPreferences, setSavingPreferences] =
    useState(false);

  /* =====================================================
     READ ALOUD STATE
     ===================================================== */

  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  /* =====================================================
     SCROLLING
     ===================================================== */

  const scrollToSection = (ref) => {
    ref.current?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  const scrollToId = (id) => {
    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  /* =====================================================
     RESUME UPLOAD
     ===================================================== */

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleResumeUpload = async (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setError("");
    setCandidate(null);
    setCompleteness(null);
    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/resume/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Resume upload failed."
        );
      }

      setCandidateId(data.candidate_id);
      setCandidate(data.candidate);

      setProfileForm({
        name: data.candidate?.name || "",
        email: data.candidate?.email || "",
        phone: data.candidate?.phone || "",
        location: data.candidate?.location || "",
      });

      setAccessibility({
        ...defaultAccessibility,
        ...(data.candidate?.accessibility_requirements || {}),
      });

      setPreferences({
        ...defaultPreferences,
        ...(data.candidate?.work_preferences || {}),
      });

      await fetchProfileCompleteness(data.candidate_id);

      setTimeout(() => {
        scrollToId("profile");
      }, 100);
    } catch (err) {
      setError(
        err.message || "Something went wrong while processing the resume."
      );
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  /* =====================================================
     PROFILE COMPLETENESS
     ===================================================== */

  const fetchProfileCompleteness = async (id) => {
    if (!id) {
      return;
    }

    setLoadingCompleteness(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/v1/candidate/${id}/completeness`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Could not load profile completeness."
        );
      }

      setCompleteness(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingCompleteness(false);
    }
  };

  /* =====================================================
     EDIT PROFILE
     ===================================================== */

  const startEditingProfile = () => {
    if (!candidate) {
      return;
    }

    setProfileForm({
      name: candidate.name || "",
      email: candidate.email || "",
      phone: candidate.phone || "",
      location: candidate.location || "",
    });

    setEditingProfile(true);

    setTimeout(() => {
      scrollToSection(editProfileRef);
    }, 50);
  };

  const cancelEditingProfile = () => {
    setEditingProfile(false);
  };

  const handleProfileChange = (event) => {
    const { name, value } = event.target;

    setProfileForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const saveProfile = async (event) => {
    event.preventDefault();

    if (!candidateId) {
      return;
    }

    setSavingProfile(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/v1/candidate/${candidateId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(profileForm),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Could not update profile."
        );
      }

      setCandidate((previous) => ({
        ...previous,
        ...data.candidate,
      }));

      setEditingProfile(false);

      await fetchProfileCompleteness(candidateId);
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingProfile(false);
    }
  };

  /* =====================================================
     ACCESSIBILITY
     ===================================================== */

  const handleAccessibilityChange = (event) => {
    const { name, type, checked, value } = event.target;

    setAccessibility((previous) => ({
      ...previous,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const saveAccessibility = async () => {
    if (!candidateId) {
      return;
    }

    setSavingAccessibility(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/v1/profile/${candidateId}/accessibility`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(accessibility),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Could not save accessibility requirements."
        );
      }

      setCandidate((previous) => ({
        ...previous,
        accessibility_requirements:
          data.accessibility_requirements,
      }));

      await fetchProfileCompleteness(candidateId);
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingAccessibility(false);
    }
  };

  /* =====================================================
     WORK PREFERENCES
     ===================================================== */

  const toggleArrayValue = (field, value) => {
    setPreferences((previous) => {
      const currentValues = Array.isArray(previous[field])
        ? previous[field]
        : [];

      const exists = currentValues.includes(value);

      return {
        ...previous,
        [field]: exists
          ? currentValues.filter((item) => item !== value)
          : [...currentValues, value],
      };
    });
  };

  const handleLocationChange = (event) => {
    const locations = event.target.value
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

    setPreferences((previous) => ({
      ...previous,
      preferred_locations: locations,
    }));
  };

  const savePreferences = async () => {
    if (!candidateId) {
      return;
    }

    setSavingPreferences(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/v1/profile/${candidateId}/preferences`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(preferences),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Could not save work preferences."
        );
      }

      setCandidate((previous) => ({
        ...previous,
        work_preferences: data.work_preferences,
      }));

      await fetchProfileCompleteness(candidateId);
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingPreferences(false);
    }
  };

  /* =====================================================
     PROFILE COMPLETENESS CLICK
     ===================================================== */

  const handleMissingSectionClick = (section) => {
    switch (section) {
      case "basic_information":
        startEditingProfile();
        break;

      case "accessibility_requirements":
        scrollToSection(accessibilityRef);
        break;

      case "work_preferences":
        scrollToSection(preferencesRef);
        break;

      case "skills":
      case "education":
      case "experience":
      case "projects":
      case "certifications":
      case "languages":
        scrollToId("profile");
        break;

      default:
        break;
    }
  };

  /* =====================================================
     READ ALOUD
     ===================================================== */

  const getPageText = () => {
    const main = document.querySelector("main");

    if (!main) {
      return "";
    }

    return main.innerText.replace(/\s+/g, " ").trim();
  };

  const handleReadAloud = () => {
    if (!("speechSynthesis" in window)) {
      setError(
        "Read Aloud is not supported by this browser."
      );
      return;
    }

    window.speechSynthesis.cancel();

    const text = getPageText();

    if (!text) {
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);

    utterance.rate = 0.95;
    utterance.pitch = 1;

    utterance.onstart = () => {
      setIsSpeaking(true);
      setIsPaused(false);
    };

    utterance.onend = () => {
      setIsSpeaking(false);
      setIsPaused(false);
    };

    utterance.onerror = () => {
      setIsSpeaking(false);
      setIsPaused(false);
    };

    window.speechSynthesis.speak(utterance);
  };

  const handlePauseSpeech = () => {
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.pause();
      setIsPaused(true);
    }
  };

  const handleResumeSpeech = () => {
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
    }
  };

  const handleStopSpeech = () => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
    setIsPaused(false);
  };

  /* =====================================================
     OPTIONS
     ===================================================== */

  const accessibilityOptions = [
    {
      name: "screen_reader",
      label: "Screen reader support",
    },
    {
      name: "captions",
      label: "Captions",
    },
    {
      name: "sign_language_interpreter",
      label: "Sign language interpreter",
    },
    {
      name: "wheelchair_accessible",
      label: "Wheelchair accessible workplace",
    },
    {
      name: "flexible_working_hours",
      label: "Flexible working hours",
    },
    {
      name: "remote_work",
      label: "Remote work",
    },
    {
      name: "assistive_technology",
      label: "Assistive technology",
    },
    {
      name: "accessible_transportation",
      label: "Accessible transportation",
    },
  ];

  const workModeOptions = [
    {
      value: "remote",
      label: "Remote",
    },
    {
      value: "hybrid",
      label: "Hybrid",
    },
    {
      value: "onsite",
      label: "On-site",
    },
  ];

  const jobTypeOptions = [
    {
      value: "full_time",
      label: "Full-time",
    },
    {
      value: "part_time",
      label: "Part-time",
    },
    {
      value: "contract",
      label: "Contract",
    },
    {
      value: "internship",
      label: "Internship",
    },
  ];

  const roleOptions = [
    "Software Developer",
    "Backend Developer",
    "Frontend Developer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Data Analyst",
    "UI/UX Designer",
  ];

  

  /* =====================================================
     RENDER
     ===================================================== */

  return (
    <div className="app">
      {/* =================================================
          NAVIGATION
          ================================================= */}

      <header className="navbar">
        <a
          href="#home"
          className="logo-link"
          aria-label="Nivara home"
        >
          <img
            src="logo.png"
            alt="Nivara"
            className="logo-image"
          />
        </a>

        <nav aria-label="Main navigation">
          <a href="#home">Home</a>
          <a href="#how-it-works">How It Works</a>
          <a href="#jobs">Jobs</a>
          <a href="#accessibility">Accessibility</a>
        </nav>

        <div className="speech-controls">
          {!isSpeaking && (
            <button
              className="accessibility-button"
              type="button"
              onClick={handleReadAloud}
              aria-label="Read page aloud"
            >
              🔊 Read Aloud
            </button>
          )}

          {isSpeaking && !isPaused && (
            <button
              className="accessibility-button"
              type="button"
              onClick={handlePauseSpeech}
              aria-label="Pause reading"
            >
              ⏸ Pause
            </button>
          )}

          {isSpeaking && isPaused && (
            <button
              className="accessibility-button"
              type="button"
              onClick={handleResumeSpeech}
              aria-label="Resume reading"
            >
              ▶ Resume
            </button>
          )}

          {isSpeaking && (
            <button
              className="stop-button"
              type="button"
              onClick={handleStopSpeech}
              aria-label="Stop reading"
            >
              ■ Stop
            </button>
          )}
        </div>
      </header>

      <main>
        {/* =================================================
            HERO
            ================================================= */}

        <section
          id="home"
          className="hero"
          aria-labelledby="hero-heading"
        >
          <div className="hero-content">
            <p className="eyebrow">
              INCLUSIVE CAREER PLATFORM
            </p>

            <h1 id="hero-heading">
              Your skills.
              <br />
              Your possibilities.
            </h1>

            <p className="hero-text">
              A career platform designed around you.
              Nivara connects Persons with Disabilities
              with opportunities that match their skills,
              accessibility needs, and work preferences.
            </p>

            <div className="hero-actions">
              <button
                className="primary-button"
                type="button"
                onClick={handleUploadClick}
                disabled={uploading}
              >
                {uploading
                  ? "Processing Resume..."
                  : "Upload Resume"}
              </button>

              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx"
                onChange={handleResumeUpload}
                hidden
              />

              <button
                className="secondary-button"
                type="button"
                onClick={() => scrollToId("jobs")}
              >
                Explore Opportunities
              </button>
            </div>

            {error && (
              <div
                className="error-message"
                role="alert"
                aria-live="assertive"
              >
                {error}
              </div>
            )}

            <div className="hero-highlights">
              <span>✓ Skills-based matching</span>
              <span>✓ Accessibility-aware</span>
              <span>✓ Candidate-controlled preferences</span>
            </div>
          </div>

          <div className="hero-card">
            <div
              className="card-icon"
              aria-hidden="true"
            >
              ♿
            </div>

            <h2>
              Career opportunities built around you.
            </h2>

            <p>
              Skills + Accessibility + Preferences
            </p>
          </div>
        </section>

        {/* =================================================
            HOW NIVARA WORKS
            ================================================= */}

        <section
          id="how-it-works"
          className="how-section"
          aria-labelledby="how-heading"
        >
          <div className="section-heading">
            <p className="eyebrow">HOW NIVARA WORKS</p>

            <h2 id="how-heading">
              From profile to opportunity.
            </h2>

            <p>
              Nivara brings your professional skills,
              accessibility requirements, and work
              preferences together in one place.
            </p>
          </div>

          <div className="steps-grid">
            <article className="step-card">
              <span className="step-number">01</span>
              <h3>Build your profile</h3>
              <p>
                Upload your resume and let Nivara
                understand your skills, education,
                experience, and projects.
              </p>
            </article>

            <article className="step-card">
              <span className="step-number">02</span>
              <h3>Tell us what you need</h3>
              <p>
                Choose accessibility requirements and
                work preferences that matter to you.
              </p>
            </article>

            <article className="step-card">
              <span className="step-number">03</span>
              <h3>Discover matched jobs</h3>
              <p>
                Find opportunities based on skills,
                preferences, and workplace accessibility.
              </p>
            </article>

            <article className="step-card">
              <span className="step-number">04</span>
              <h3>Apply with confidence</h3>
              <p>
                Get assistance with applications and
                communicate required accommodations.
              </p>
            </article>
          </div>
        </section>

        {/* =================================================
            WHY NIVARA
            ================================================= */}

        <section
          className="why-section"
          aria-labelledby="why-heading"
        >
          <div className="section-heading centered">
            <p className="eyebrow">WHY NIVARA</p>

            <h2 id="why-heading">
              More than a job search.
            </h2>

            <p>
              Nivara looks at the complete picture,
              not just a list of keywords.
            </p>
          </div>

          <div className="why-grid">
            <article className="why-card">
              <div className="why-icon">🧠</div>

              <h3>Intelligent Profile</h3>

              <p>
                Nivara understands your skills,
                experience, education, and professional
                strengths from your resume.
              </p>

              <strong>
                Skills + Experience + Potential
              </strong>
            </article>

            <article className="why-card">
              <div className="why-icon">♿</div>

              <h3>Accessibility-Aware Matching</h3>

              <p>
                Accessibility requirements and work
                preferences become part of the matching
                process.
              </p>

              <strong>
                Workplace + Accessibility + Fit
              </strong>
            </article>

            <article className="why-card">
              <div className="why-icon">🤝</div>

              <h3>AI-Assisted Applications</h3>

              <p>
                Nivara can assist throughout the journey
                from discovering an opportunity to
                preparing an application.
              </p>

              <strong>
                Discover → Match → Apply
              </strong>
            </article>
          </div>
        </section>

        {/* =================================================
            YOUR CAREER, YOUR WAY
            ================================================= */}

        <section
          className="way-section"
          aria-labelledby="way-heading"
        >
          <div className="section-heading centered">
            <p className="eyebrow">YOUR CAREER, YOUR WAY</p>

            <h2 id="way-heading">
              Work in a way that works for you.
            </h2>
          </div>

          <div className="way-grid">
            <article className="way-card">
              <div className="way-icon">🏠</div>

              <h3>Remote</h3>

              <p>
                Discover opportunities that support
                remote work.
              </p>
            </article>

            <article className="way-card">
              <div className="way-icon">↔</div>

              <h3>Flexible</h3>

              <p>
                Find working arrangements that fit
                your needs and preferences.
              </p>
            </article>

            <article className="way-card">
              <div className="way-icon">♿</div>

              <h3>Accessible</h3>

              <p>
                Accessibility is considered as part
                of the opportunity.
              </p>
            </article>
          </div>
        </section>

        {/* =================================================
            ACCESSIBILITY FIRST
            ================================================= */}

        <section
          className="accessibility-info-section"
          aria-labelledby="accessibility-info-heading"
        >
          <div className="accessibility-info-content">
            <p className="eyebrow">
              ACCESSIBILITY FIRST
            </p>

            <h2 id="accessibility-info-heading">
              Accessibility isn't an extra feature.
              <br />
              It's part of the match.
            </h2>

            <p>
              Tell Nivara what you need to work
              comfortably and effectively. These
              preferences help shape the opportunities
              shown to you.
            </p>

            <button
              className="primary-button"
              type="button"
              onClick={() =>
                candidate
                  ? scrollToSection(accessibilityRef)
                  : scrollToId("accessibility")
              }
            >
              Set Accessibility Preferences
            </button>
          </div>

          <div className="accessibility-pills">
            <span>Screen Reader</span>
            <span>Captions</span>
            <span>Flexible Hours</span>
            <span>Remote Work</span>
            <span>Assistive Technology</span>
            <span>Wheelchair Accessibility</span>
            <span>Accessible Transportation</span>
          </div>
        </section>

        {/* =================================================
            JOB OPPORTUNITIES
            ================================================= */}

        <section
          id="jobs"
          className="jobs-section"
          aria-labelledby="jobs-heading"
        >
          <div className="section-heading">
            <p className="eyebrow">
              OPPORTUNITIES
            </p>

            <h2 id="jobs-heading">
              Opportunities that could fit you.
            </h2>

            <p>
              Nivara considers skills, work preferences,
              and accessibility when helping you discover
              opportunities.
            </p>
          </div>

          <div className="jobs-grid">
            <article className="job-card">
              <div className="job-card-top">
                <div>
                  <p className="job-company">
                    Example Technologies
                  </p>

                  <h3>Python Developer</h3>
                </div>

                <span className="job-badge">
                  Remote
                </span>
              </div>

              <div className="job-skills">
                <span>Python</span>
                <span>FastAPI</span>
                <span>SQL</span>
              </div>

              <div className="job-accessibility">
                <span>♿ Accessible</span>
                <span>🏠 Remote</span>
                <span>↔ Flexible</span>
              </div>

              <button
                className="secondary-button"
                type="button"
              >
                View Opportunity →
              </button>
            </article>

            <article className="job-card">
              <div className="job-card-top">
                <div>
                  <p className="job-company">
                    Inclusive Analytics
                  </p>

                  <h3>Data Analyst</h3>
                </div>

                <span className="job-badge">
                  Hybrid
                </span>
              </div>

              <div className="job-skills">
                <span>Python</span>
                <span>SQL</span>
                <span>Power BI</span>
              </div>

              <div className="job-accessibility">
                <span>♿ Accessible</span>
                <span>🎧 Assistive Tech</span>
              </div>

              <button
                className="secondary-button"
                type="button"
              >
                View Opportunity →
              </button>
            </article>

            <article className="job-card">
              <div className="job-card-top">
                <div>
                  <p className="job-company">
                    Future AI Labs
                  </p>

                  <h3>ML Engineer</h3>
                </div>

                <span className="job-badge">
                  Remote
                </span>
              </div>

              <div className="job-skills">
                <span>Python</span>
                <span>Machine Learning</span>
                <span>TensorFlow</span>
              </div>

              <div className="job-accessibility">
                <span>🏠 Remote</span>
                <span>↔ Flexible</span>
              </div>

              <button
                className="secondary-button"
                type="button"
              >
                View Opportunity →
              </button>
            </article>
          </div>

          <p className="jobs-note">
            Job recommendations will become dynamic
            when the Nivara job-matching service is
            connected.
          </p>
        </section>

        {/* =================================================
            CANDIDATE PROFILE
            ================================================= */}

        {candidate && (
          <section
            id="profile"
            className="profile-section"
            aria-labelledby="profile-heading"
          >
            <div className="section-heading">
              <p className="eyebrow">
                CANDIDATE PROFILE
              </p>

              <h2 id="profile-heading">
                Your professional profile
              </h2>

              <p>
                Review and complete the information
                extracted from your resume.
              </p>
            </div>

            {/* Profile completeness */}

            {loadingCompleteness && (
              <p role="status">
                Loading profile completeness...
              </p>
            )}

            {completeness && (
              <div
                className="completeness-card"
                aria-labelledby="completeness-heading"
              >
                <div className="completeness-header">
                  <div>
                    <p className="eyebrow">
                      PROFILE STATUS
                    </p>

                    <h3 id="completeness-heading">
                      Profile Completeness
                    </h3>
                  </div>

                  <strong className="completion-percentage">
                    {completeness.completion_percentage}%
                  </strong>
                </div>

                <div
                  className="progress-track"
                  role="progressbar"
                  aria-valuenow={
                    completeness.completion_percentage
                  }
                  aria-valuemin="0"
                  aria-valuemax="100"
                  aria-label={`Profile ${completeness.completion_percentage}% complete`}
                >
                  <div
                    className="progress-bar"
                    style={{
                      width: `${completeness.completion_percentage}%`,
                    }}
                  />
                </div>

                <p className="completion-summary">
                  {completeness.completed_sections} of{" "}
                  {completeness.total_sections} sections
                  completed.
                </p>

                {completeness.missing_sections?.length >
                0 ? (
                  <div className="missing-sections">
                    <h4>
                      Complete these sections
                    </h4>

                    <ul>
                      {completeness.missing_sections.map(
                        (section) => (
                          <li key={section}>
                            <button
                              type="button"
                              className="missing-section-button"
                              onClick={() =>
                                handleMissingSectionClick(
                                  section
                                )
                              }
                            >
                              {section
                                .replaceAll("_", " ")
                                .replace(
                                  /\b\w/g,
                                  (letter) =>
                                    letter.toUpperCase()
                                )}

                              <span aria-hidden="true">
                                {" "}
                                →
                              </span>
                            </button>
                          </li>
                        )
                      )}
                    </ul>
                  </div>
                ) : (
                  <p className="profile-complete-message">
                    ✓ Your profile is complete!
                  </p>
                )}
              </div>
            )}

            <div className="profile-grid">
              {/* Basic information */}

              <article className="profile-card profile-basic">
                <div
                  className="profile-avatar"
                  aria-hidden="true"
                >
                  {candidate.name
                    ? candidate.name
                        .charAt(0)
                        .toUpperCase()
                    : "N"}
                </div>

                <h3>
                  {candidate.name || "Your Name"}
                </h3>

                {candidate.email && (
                  <p>
                    <strong>Email</strong>
                    <br />
                    {candidate.email}
                  </p>
                )}

                {candidate.phone && (
                  <p>
                    <strong>Phone</strong>
                    <br />
                    {candidate.phone}
                  </p>
                )}

                {candidate.location && (
                  <p>
                    <strong>Location</strong>
                    <br />
                    {candidate.location}
                  </p>
                )}

                <button
                  type="button"
                  className="secondary-button"
                  onClick={startEditingProfile}
                >
                  Edit Profile
                </button>
              </article>

              {/* Professional information */}

              <article className="profile-card">
                <h3>Skills</h3>

                {candidate.skills?.length > 0 ? (
                  <div className="skill-list">
                    {candidate.skills.map(
                      (skill, index) => (
                        <span
                          className="skill-tag"
                          key={`${skill}-${index}`}
                        >
                          {skill}
                        </span>
                      )
                    )}
                  </div>
                ) : (
                  <p>
                    No skills were extracted.
                  </p>
                )}

                <h3 className="profile-subheading">
                  Education
                </h3>

                {candidate.education?.length > 0 ? (
                  candidate.education.map(
                    (education, index) => (
                      <div
                        className="profile-item"
                        key={index}
                      >
                        <strong>
                          {education.degree ||
                            "Education"}
                        </strong>

                        {education.field_of_study && (
                          <p>
                            {
                              education.field_of_study
                            }
                          </p>
                        )}

                        {education.institution && (
                          <p>
                            {education.institution}
                          </p>
                        )}

                        {education.year && (
                          <small>
                            {education.year}
                          </small>
                        )}
                      </div>
                    )
                  )
                ) : (
                  <p>
                    No education information found.
                  </p>
                )}

                <h3 className="profile-subheading">
                  Experience
                </h3>

                {candidate.experience?.length > 0 ? (
                  candidate.experience.map(
                    (experience, index) => (
                      <div
                        className="profile-item"
                        key={index}
                      >
                        <strong>
                          {experience.job_title ||
                            "Experience"}
                        </strong>

                        {experience.company && (
                          <p>
                            {experience.company}
                          </p>
                        )}

                        {experience.duration && (
                          <small>
                            {experience.duration}
                          </small>
                        )}

                        {experience.description && (
                          <p>
                            {experience.description}
                          </p>
                        )}
                      </div>
                    )
                  )
                ) : (
                  <p>
                    No experience information found.
                  </p>
                )}
              </article>
            </div>

            {/* =================================================
                EDIT BASIC PROFILE
                ================================================= */}

            {editingProfile && (
              <article
                ref={editProfileRef}
                className="edit-profile-card"
                aria-labelledby="edit-profile-heading"
              >
                <p className="eyebrow">
                  EDIT PROFILE
                </p>

                <h3 id="edit-profile-heading">
                  Update your basic information
                </h3>

                <form onSubmit={saveProfile}>
                  <div className="profile-form-grid">
                    <div>
                      <label htmlFor="name">
                        Full Name
                      </label>

                      <input
                        id="name"
                        name="name"
                        type="text"
                        value={profileForm.name}
                        onChange={handleProfileChange}
                        required
                      />
                    </div>

                    <div>
                      <label htmlFor="email">
                        Email
                      </label>

                      <input
                        id="email"
                        name="email"
                        type="email"
                        value={profileForm.email}
                        onChange={handleProfileChange}
                        required
                      />
                    </div>

                    <div>
                      <label htmlFor="phone">
                        Phone
                      </label>

                      <input
                        id="phone"
                        name="phone"
                        type="tel"
                        value={profileForm.phone}
                        onChange={handleProfileChange}
                        required
                      />
                    </div>

                    <div>
                      <label htmlFor="location">
                        Location
                      </label>

                      <input
                        id="location"
                        name="location"
                        type="text"
                        value={profileForm.location}
                        onChange={handleProfileChange}
                        required
                      />
                    </div>
                  </div>

                  <div className="edit-profile-actions">
                    <button
                      type="submit"
                      className="primary-button"
                      disabled={savingProfile}
                    >
                      {savingProfile
                        ? "Saving..."
                        : "Save Profile"}
                    </button>

                    <button
                      type="button"
                      className="secondary-button"
                      onClick={cancelEditingProfile}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </article>
            )}
          </section>
        )}

        {/* =================================================
            ACCESSIBILITY & PREFERENCES
            ================================================= */}

        <section
          ref={accessibilityRef}
          id="accessibility"
          className="settings-section"
          aria-labelledby="settings-heading"
        >
          <div className="section-heading">
            <p className="eyebrow">
              PERSONALIZATION
            </p>

            <h2 id="settings-heading">
              Tell Nivara what works for you.
            </h2>

            <p>
              Your accessibility requirements and work
              preferences help Nivara understand which
              opportunities may fit your needs.
            </p>
          </div>

          <div className="settings-grid">
            {/* Accessibility */}

            <article className="settings-card">
              <h3>
                Accessibility Requirements
              </h3>

              <p className="settings-description">
                Select the support or workplace features
                that are important to you.
              </p>

              <fieldset>
                <legend>
                  What do you need?
                </legend>

                <div className="checkbox-list">
                  {accessibilityOptions.map(
                    (option) => (
                      <label
                        className="checkbox-item"
                        key={option.name}
                      >
                        <input
                          type="checkbox"
                          name={option.name}
                          checked={
                            accessibility[
                              option.name
                            ] || false
                          }
                          onChange={
                            handleAccessibilityChange
                          }
                        />

                        <span>
                          {option.label}
                        </span>
                      </label>
                    )
                  )}
                </div>
              </fieldset>

              <label
                className="field-label"
                htmlFor="accessibility-other"
              >
                Other requirements
              </label>

              <textarea
                id="accessibility-other"
                name="other"
                rows="4"
                value={accessibility.other || ""}
                onChange={handleAccessibilityChange}
                placeholder="Tell us about any other accessibility requirements..."
              />

              <button
                type="button"
                className="primary-button save-button"
                onClick={saveAccessibility}
                disabled={
                  savingAccessibility || !candidateId
                }
              >
                {savingAccessibility
                  ? "Saving..."
                  : "Save Accessibility"}
              </button>
            </article>

            {/* Work Preferences */}

            <article
              ref={preferencesRef}
              className="settings-card"
            >
              <h3>Work Preferences</h3>

              <p className="settings-description">
                Tell us how and where you prefer to work.
              </p>

              <fieldset>
                <legend>Preferred work mode</legend>

                <div className="checkbox-list">
                  {workModeOptions.map(
                    (option) => (
                      <label
                        className="checkbox-item"
                        key={option.value}
                      >
                        <input
                          type="checkbox"
                          checked={
                            Array.isArray(
                              preferences.work_mode
                            ) &&
                            preferences.work_mode.includes(
                              option.value
                            )
                          }
                          onChange={() =>
                            toggleArrayValue(
                              "work_mode",
                              option.value
                            )
                          }
                        />

                        <span>
                          {option.label}
                        </span>
                      </label>
                    )
                  )}
                </div>
              </fieldset>

              <label
                className="field-label"
                htmlFor="preferred-locations"
              >
                Preferred locations
              </label>

              <input
                id="preferred-locations"
                type="text"
                value={
                  Array.isArray(
                    preferences.preferred_locations
                  )
                    ? preferences.preferred_locations.join(
                        ", "
                      )
                    : ""
                }
                onChange={handleLocationChange}
                placeholder="e.g. Raipur, Pune, Remote"
              />

              <fieldset>
                <legend>
                  Preferred job types
                </legend>

                <div className="checkbox-list">
                  {jobTypeOptions.map(
                    (option) => (
                      <label
                        className="checkbox-item"
                        key={option.value}
                      >
                        <input
                          type="checkbox"
                          checked={
                            Array.isArray(
                              preferences.job_types
                            ) &&
                            preferences.job_types.includes(
                              option.value
                            )
                          }
                          onChange={() =>
                            toggleArrayValue(
                              "job_types",
                              option.value
                            )
                          }
                        />

                        <span>
                          {option.label}
                        </span>
                      </label>
                    )
                  )}
                </div>
              </fieldset>

              <fieldset>
                <legend>
                  Preferred roles
                </legend>

                <div className="checkbox-list">
                  {roleOptions.map((role) => (
                    <label
                      className="checkbox-item"
                      key={role}
                    >
                      <input
                        type="checkbox"
                        checked={
                          Array.isArray(
                            preferences.preferred_roles
                          ) &&
                          preferences.preferred_roles.includes(
                            role
                          )
                        }
                        onChange={() =>
                          toggleArrayValue(
                            "preferred_roles",
                            role
                          )
                        }
                      />

                      <span>{role}</span>
                    </label>
                  ))}
                </div>
              </fieldset>

              <button
                type="button"
                className="primary-button save-button"
                onClick={savePreferences}
                disabled={
                  savingPreferences || !candidateId
                }
              >
                {savingPreferences
                  ? "Saving..."
                  : "Save Work Preferences"}
              </button>
            </article>
          </div>
        </section>

        {/* =================================================
            FINAL CTA
            ================================================= */}

        <section
          className="final-cta"
          aria-labelledby="cta-heading"
        >
          <div>
            <p className="eyebrow">
              YOUR NEXT OPPORTUNITY
            </p>

            <h2 id="cta-heading">
              Start with understanding you.
            </h2>

            <p>
              Your skills. Your preferences. Your
              accessibility needs. One profile.
            </p>

            <button
              className="primary-button"
              type="button"
              onClick={handleUploadClick}
            >
              Upload Your Resume →
            </button>
          </div>
        </section>
      </main>

      {/* =================================================
          FOOTER
          ================================================= */}

      <footer>
        <p>
          Nivara — Inclusive careers, designed around
          people.
        </p>
      </footer>
    </div>
  );
}

export default App;