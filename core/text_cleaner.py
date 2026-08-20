"""
Text Preprocessing, Regex Patterns, and Entity Extraction Helpers.
"""

import re
from typing import List, Optional, Tuple

EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REGEX = r'(?:(?:\+|0{0,2})91[\s.-]?)?(?:(?:\(\d{3}\)|\d{3})[\s.-]?)?\d{3}[\s.-]?\d{4}|\b\d{10}\b'
LINKEDIN_REGEX = r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+'
GITHUB_REGEX = r'(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+'

EDUCATION_KEYWORDS = [
    "b.tech", "btech", "b.e", "be", "bachelor of technology", "bachelor of engineering",
    "b.sc", "bsc", "bachelor of science", "bca", "bachelor of computer applications",
    "m.tech", "mtech", "m.e", "me", "master of technology", "master of engineering",
    "m.sc", "msc", "master of science", "mca", "master of computer applications",
    "mba", "master of business administration", "ph.d", "phd", "doctor of philosophy",
    "diploma", "associate degree", "bachelors", "masters"
]

def clean_text(text: str) -> str:
    """Normalizes whitespace, removes unprintable characters, and keeps alphanumeric tokens."""
    if not text:
        return ""
    # Replace non-breaking spaces and line breaks with standard space
    text = text.replace('\xa0', ' ').replace('\r', ' ')
    # Normalize multiple newlines/spaces
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def preprocess_for_nlp(text: str) -> str:
    """Lowercase and clean text for TF-IDF / Bag of Words processing."""
    if not text:
        return ""
    text = text.lower()
    # Keep alphanumeric, basic punctuation for tech terms like c++, .net, node.js
    text = re.sub(r'[^a-z0-9\s\+\#\.\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_email(text: str) -> Optional[str]:
    """Extracts first valid email address from text."""
    match = re.search(EMAIL_REGEX, text)
    return match.group(0) if match else None

def extract_phone(text: str) -> Optional[str]:
    """Extracts first valid phone number from text."""
    match = re.search(PHONE_REGEX, text)
    if match:
        cleaned = re.sub(r'[^\d+]', '', match.group(0))
        if len(cleaned) >= 10:
            return match.group(0).strip()
    return None

def extract_links(text: str) -> dict:
    """Extracts LinkedIn and GitHub URLs."""
    linkedin = re.search(LINKEDIN_REGEX, text, re.IGNORECASE)
    github = re.search(GITHUB_REGEX, text, re.IGNORECASE)
    return {
        "linkedin": linkedin.group(0) if linkedin else None,
        "github": github.group(0) if github else None
    }

def extract_education(text: str) -> List[str]:
    """Finds mention of educational degrees in text."""
    text_lower = text.lower()
    found_degrees = []
    for deg in EDUCATION_KEYWORDS:
        # Use word boundary search
        pattern = r'\b' + re.escape(deg) + r'\b'
        if re.search(pattern, text_lower):
            display_deg = deg.upper() if len(deg) <= 4 else deg.title()
            if display_deg not in found_degrees:
                found_degrees.append(display_deg)
    return found_degrees

def extract_experience_years(text: str) -> float:
    """
    Heuristic to estimate candidate's total years of professional work experience.
    Strips out Education blocks/degrees and extracts experience years from Work History.
    """
    text_lower = text.lower()
    
    # 1. Strip out Education section entirely from text
    # Matches from "Education" header down to the next major section or end of string
    text_no_edu = re.sub(
        r'(?:education|academic\s+qualifications?|qualification).*?(?=\n\s*(?:work\s+experience|experience|employment|skills|technical\s+skills|projects|certifications|\Z))',
        '',
        text_lower,
        flags=re.DOTALL
    )

    # 2. Also remove individual lines containing degree / school / university keywords
    clean_lines = []
    for line in text_no_edu.split('\n'):
        line_str = line.strip()
        if not line_str:
            continue
        if any(edu_w in line_str for edu_w in [
            "university", "college", "school", "b.tech", "btech", "b.e", "be ",
            "m.tech", "mtech", "bca", "mca", "b.sc", "bsc", "m.sc", "msc",
            "class xii", "class x", "cbse", "icse", "higher secondary", "senior secondary"
        ]):
            continue
        clean_lines.append(line_str)
        
    target_text = "\n".join(clean_lines)

    years = []
    
    # 3. Look for explicit 'X years/yrs of experience' phrases (e.g. 5+ years, 4 yrs)
    exp_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)?', target_text)
    for m in exp_matches:
        try:
            val = float(m)
            if 0 < val <= 40:
                years.append(val)
        except ValueError:
            pass

    # 4. Look for date ranges (e.g. 2018 - 2024, 2020 to Present) in work experience text
    current_year = 2026
    date_ranges = re.findall(r'\b(20\d{2}|19\d{2})\s*(?:-|–|to)\s*(20\d{2}|present|current)\b', target_text)
    for start, end in date_ranges:
        try:
            start_yr = int(start)
            end_yr = current_year if end in ['present', 'current'] else int(end)
            diff = end_yr - start_yr
            if 0 <= diff <= 40:
                years.append(float(diff))
        except ValueError:
            pass

    if years:
        return round(max(years), 1)
    return 0.0

def extract_candidate_name(text: str, filename: str = "") -> str:
    """
    Extracts candidate name using top lines of resume or falls back to filename.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines[:5]:
        # Filter out common header words
        line_lower = line.lower()
        if any(w in line_lower for w in ["resume", "curriculum", "vitae", "profile", "contact", "email", "phone", "http", "page", "summary"]):
            continue
        # Check if line looks like a person's name (2-4 words, alphabetic)
        words = line.split()
        if 2 <= len(words) <= 4 and all(w.replace('.', '').isalpha() for w in words):
            return line.title()
    
    # Fallback to sanitized filename
    if filename:
        clean_name = re.sub(r'[\._\-\(\)0-9]', ' ', filename.replace('.pdf', '').replace('.docx', '').replace('.txt', ''))
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()
        if clean_name:
            return clean_name.title()
            
    return "Candidate Profile"
