"""
Information Extraction Engine for Resumes and Job Descriptions.
Extracts Candidate Profile: Name, Contact, Skills, Experience, Education.
"""

import re
from typing import Dict, List, Set, Any
from core.skills_database import ALL_SKILLS, SKILL_MAP, get_skill_category
from core.text_cleaner import (
    clean_text,
    extract_email,
    extract_phone,
    extract_links,
    extract_education,
    extract_experience_years,
    extract_candidate_name
)

def extract_skills_from_text(text: str) -> Dict[str, Any]:
    """
    Extracts all recognized technical and soft skills from the input text.
    Returns:
      - 'skills_list': List of canonical skill names found
      - 'by_category': Dictionary grouping skills by category
      - 'raw_set': Set of lowercase matches
    """
    text_lower = " " + text.lower() + " "
    found_skills_raw: Set[str] = set()
    
    # Sort skills by length descending so longer multi-word phrases match before subsets
    # e.g., 'machine learning' matches before 'learning'
    sorted_skills = sorted(ALL_SKILLS, key=len, reverse=True)
    
    for skill in sorted_skills:
        # Punctuation-safe regex matching:
        # Handles skills with special symbols like 'c++', '.net', 'c#', 'react.js', 'node.js'
        escaped_skill = re.escape(skill)
        pattern = r'(?<![a-zA-Z0-9])' + escaped_skill + r'(?![a-zA-Z0-9])'
        
        if re.search(pattern, text_lower):
            found_skills_raw.add(skill)

    # Convert to canonical display names and categorize
    skills_list = []
    by_category: Dict[str, List[str]] = {}
    
    for raw in sorted(found_skills_raw):
        canonical = SKILL_MAP.get(raw, raw.title())
        if canonical not in skills_list:
            skills_list.append(canonical)
            
        category = get_skill_category(raw)
        if category not in by_category:
            by_category[category] = []
        if canonical not in by_category[category]:
            by_category[category].append(canonical)
            
    return {
        "skills_list": skills_list,
        "by_category": by_category,
        "raw_set": found_skills_raw
    }

def parse_candidate_profile(text: str, filename: str = "") -> Dict[str, Any]:
    """
    Extracts full structured profile from resume text.
    """
    cleaned_body = clean_text(text)
    name = extract_candidate_name(cleaned_body, filename)
    email = extract_email(cleaned_body)
    phone = extract_phone(cleaned_body)
    links = extract_links(cleaned_body)
    education = extract_education(cleaned_body)
    experience_years = extract_experience_years(cleaned_body)
    skills_data = extract_skills_from_text(cleaned_body)
    
    return {
        "filename": filename,
        "name": name,
        "email": email or "Not detected",
        "phone": phone or "Not detected",
        "linkedin": links.get("linkedin"),
        "github": links.get("github"),
        "education": education if education else ["Not specified"],
        "experience_years": experience_years,
        "skills": skills_data["skills_list"],
        "skills_by_category": skills_data["by_category"],
        "raw_skills_set": skills_data["raw_set"],
        "raw_text": cleaned_body
    }

def parse_job_description(text: str) -> Dict[str, Any]:
    """
    Parses required skills, education, and experience requirements from a Job Description.
    """
    cleaned_body = clean_text(text)
    skills_data = extract_skills_from_text(cleaned_body)
    education = extract_education(cleaned_body)
    min_experience = extract_experience_years(cleaned_body)
    
    return {
        "skills": skills_data["skills_list"],
        "skills_by_category": skills_data["by_category"],
        "raw_skills_set": skills_data["raw_set"],
        "required_education": education,
        "min_experience_years": min_experience,
        "raw_text": cleaned_body
    }
