import re
import zlib
from typing import Dict, Any, List


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Pure Python PDF text extraction using standard library (zlib & regex).
    Extracts uncompressed and FlateDecode compressed text streams.
    """
    text_parts = []
    
    # 1. Search for FlateDecode compressed streams
    stream_pattern = re.compile(rb'stream[\r\n]+(.*?)[\r\n]+endstream', re.DOTALL)
    for match in stream_pattern.finditer(pdf_bytes):
        stream_data = match.group(1)
        try:
            decompressed = zlib.decompress(stream_data)
            # Find PDF text operators: (string) Tj or [(array)] TJ
            strings = re.findall(rb'\((.*?)\)\s*Tj', decompressed)
            for s in strings:
                try:
                    text_parts.append(s.decode('latin1', errors='ignore'))
                except Exception:
                    pass
            
            # TJ array operator
            array_matches = re.findall(rb'\[(.*?)\]\s*TJ', decompressed)
            for arr in array_matches:
                inner_strings = re.findall(rb'\((.*?)\)', arr)
                for s in inner_strings:
                    try:
                        text_parts.append(s.decode('latin1', errors='ignore'))
                    except Exception:
                        pass
        except Exception:
            # Not a zlib stream or plain stream
            pass
            
    # 2. Plain text fallback in raw PDF
    raw_strings = re.findall(rb'\(([a-zA-Z0-9\s,.\-+#@:/]{2,})\)\s*Tj', pdf_bytes)
    for s in raw_strings:
        try:
            text_parts.append(s.decode('latin1', errors='ignore'))
        except Exception:
            pass

    return " ".join(text_parts).strip()


def analyze_resume_ats(resume_text: str, job) -> Dict[str, Any]:
    """
    Comprehensive ATS (Applicant Tracking System) parser and compatibility analyzer.
    Analyzes resume against target job description and required skills.
    """
    resume_lower = resume_text.lower() if resume_text else ""
    
    # Extract target job skills and keywords
    job_skills = job.get_skills_list()
    # Extract additional important technical keywords from title and description
    title_words = [w.lower().strip(",.") for w in job.title.split() if len(w) > 3]
    desc_sample_keywords = [
        "python", "django", "react", "sql", "mysql", "postgresql", "rest", "api", "docker", 
        "kubernetes", "aws", "gcp", "azure", "redis", "celery", "git", "ci/cd", 
        "microservices", "distributed", "linux", "testing", "pytest", "agile", 
        "architecture", "scalability", "typescript", "javascript", "html", "css", "bootstrap"
    ]
    
    # Relevant keywords for this specific job
    job_desc_lower = (job.description + " " + job.responsibilities).lower()
    expanded_job_keywords = set(job_skills)
    for kw in desc_sample_keywords:
        if kw in job_desc_lower or kw in job.title.lower():
            expanded_job_keywords.add(kw)
    
    for tw in title_words:
        if tw in desc_sample_keywords:
            expanded_job_keywords.add(tw)

    # 1. Keyword Matching
    matched_keywords = []
    missing_keywords = []
    
    for kw in sorted(expanded_job_keywords):
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, resume_lower):
            matched_keywords.append(kw)
        else:
            missing_keywords.append(kw)

    total_keywords = len(expanded_job_keywords)
    keyword_match_rate = int((len(matched_keywords) / total_keywords) * 100) if total_keywords else 100

    # 2. Structural & ATS Readability Format Checks
    format_checks = {
        'has_contact_info': bool(re.search(r'[\w\.-]+@[\w\.-]+', resume_text) or re.search(r'\+?\d[\d\s-]{8,}', resume_text)),
        'has_skills_section': bool(re.search(r'\b(skills?|technical skills?|competencies|technologies)\b', resume_lower)),
        'has_experience_section': bool(re.search(r'\b(experience|work history|employment|career)\b', resume_lower)),
        'has_education_section': bool(re.search(r'\b(education|academic|university|degree|b\.tech|b\.e|bachelor|master)\b', resume_lower)),
        'has_bullet_points': bool('•' in resume_text or '-' in resume_text or '*' in resume_text or '\n-' in resume_text),
        'word_count_optimal': 200 <= len(resume_text.split()) <= 1500 if resume_text else False,
    }

    passed_checks = sum(1 for passed in format_checks.values() if passed)
    format_score = int((passed_checks / len(format_checks)) * 100)

    # 3. Overall Weighted ATS Score (70% Keyword Alignment + 30% Structural Format)
    overall_ats_score = int((keyword_match_rate * 0.70) + (format_score * 0.30))
    overall_ats_score = min(max(overall_ats_score, 15 if resume_text else 0), 100)

    # 4. Accuracy / Match Grade Level
    if overall_ats_score >= 80:
        grade = "High ATS Pass Rate (Likely to pass recruiter screen)"
        badge_class = "success"
    elif overall_ats_score >= 60:
        grade = "Moderate ATS Pass Rate (Needs key keyword additions)"
        badge_class = "warning"
    else:
        grade = "Low ATS Pass Rate (High risk of rejection by ATS filters)"
        badge_class = "danger"

    # 5. Tailored Actionable Suggestions
    suggestions = []
    if missing_keywords:
        top_missing = missing_keywords[:5]
        suggestions.append(
            f"Add high-impact missing keywords to your Skills and Work Experience sections: {', '.join([k.title() for k in top_missing])}."
        )
    if not format_checks['has_skills_section']:
        suggestions.append("Add a distinct 'Technical Skills' section header so ATS algorithms can index your proficiencies.")
    if not format_checks['has_experience_section']:
        suggestions.append("Include a clear 'Professional Experience' section with company name, role title, and dates.")
    if not format_checks['has_contact_info']:
        suggestions.append("Ensure your professional email address, phone number, and LinkedIn URL are clearly visible in the header.")
    if not format_checks['has_bullet_points']:
        suggestions.append("Use standard bullet points (-) under each role describing quantifiable impact and tools used.")
    
    suggestions.append(
        f"Mirror role-specific keywords from '{job.title}' in your project bullet points to maximize relevance."
    )

    # 6. ATS-Friendly Tailored Resume Draft Template
    ats_resume_template = f"""[YOUR FULL NAME]
[City, State/Country] | [Your Phone] | [Your Email] | [LinkedIn / GitHub Profile]

PROFESSIONAL SUMMARY
Results-driven software engineer with proven experience in {', '.join(job_skills[:3]) if job_skills else 'software engineering'}. Demonstrated track record of designing scalable backends, robust REST APIs, and high-performance software solutions aligned with {job.company.name}'s technical requirements.

CORE TECHNICAL SKILLS
• Programming & Frameworks: {', '.join(sorted(expanded_job_keywords))}
• Database & Cloud: PostgreSQL, SQL, Docker, Redis, Cloud Architecture
• Practices: CI/CD, Unit Testing, Agile/Scrum, Code Review

PROFESSIONAL EXPERIENCE
Software Engineer | [Current / Recent Company]
[Month, Year] - Present | [Location / Remote]
• Architected and shipped scalable microservices using {job_skills[0] if job_skills else 'Python'} and {job_skills[1] if len(job_skills) > 1 else 'Django'}, boosting application performance by 30%.
• Designed and optimized relational database schemas on PostgreSQL, reducing slow query execution times by 45%.
• Integrated automated testing pipelines with over 85% code coverage, ensuring zero production downtime.
• Collaborated in cross-functional engineering teams to implement secure authentication and API workflows.

EDUCATION
Bachelor of Technology / Bachelor of Engineering in Computer Science (or related field)
[University Name] | [Graduation Year]
"""

    return {
        'ats_score': overall_ats_score,
        'keyword_match_rate': keyword_match_rate,
        'format_score': format_score,
        'grade': grade,
        'badge_class': badge_class,
        'matched_keywords': matched_keywords,
        'missing_keywords': missing_keywords,
        'format_checks': format_checks,
        'suggestions': suggestions,
        'ats_resume_template': ats_resume_template,
        'total_keywords_analyzed': total_keywords,
    }
