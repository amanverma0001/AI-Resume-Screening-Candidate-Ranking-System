"""
Authentication and User Session Management Engine for AI Resume Screening System.
Supports Login, User Registration, and 1-Click Guest Demo access.
"""

import hashlib
from typing import Dict, Optional, Tuple

DEFAULT_USERS = {
    "demo@edufyi.com": {
        "name": "Alex Mercer",
        "email": "demo@edufyi.com",
        "role": "Senior Talent Acquisition",
        "organization": "Edufyi Tech Solutions",
        "password_hash": hashlib.sha256("demo123".encode()).hexdigest()
    },
    "admin@screener.ai": {
        "name": "Amandeep Verma",
        "email": "admin@screener.ai",
        "role": "Lead HR Architect",
        "organization": "AI Screening Labs",
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest()
    },
    "evaluator@mentor.com": {
        "name": "Technical Mentor",
        "email": "evaluator@mentor.com",
        "role": "Chief Evaluation Officer",
        "organization": "Evaluation Board",
        "password_hash": hashlib.sha256("mentor123".encode()).hexdigest()
    }
}

def hash_password(password: str) -> str:
    """Computes SHA-256 hash for secure string comparison."""
    return hashlib.sha256(password.strip().encode()).hexdigest()

def verify_credentials(email: str, password: str, registered_users: Dict[str, Dict]) -> Tuple[bool, Optional[Dict], str]:
    """
    Validates user credentials against default and registered user databases.
    Returns: (is_success, user_dict, message)
    """
    clean_email = email.strip().lower()
    
    # Check session-registered users first, then default users
    all_users = {**DEFAULT_USERS, **registered_users}
    
    if not clean_email:
        return False, None, "Please enter your email address."
    if not password:
        return False, None, "Please enter your password."
        
    if clean_email not in all_users:
        return False, None, "User email not found. Please check spelling or create an account."
        
    user = all_users[clean_email]
    pwd_hash = hash_password(password)
    
    if user["password_hash"] == pwd_hash:
        return True, user, f"Welcome back, {user['name']}!"
    else:
        return False, None, "Incorrect password. Please try again."

def register_new_user(
    name: str,
    email: str,
    organization: str,
    password: str,
    registered_users: Dict[str, Dict]
) -> Tuple[bool, Optional[Dict], str]:
    """
    Registers a new recruiter or evaluator into the user database.
    """
    clean_email = email.strip().lower()
    clean_name = name.strip()
    clean_org = organization.strip() or "Independent Recruiter"
    
    if not clean_name:
        return False, None, "Please provide your Full Name."
    if not clean_email or "@" not in clean_email:
        return False, None, "Please provide a valid Work Email."
    if len(password) < 4:
        return False, None, "Password must be at least 4 characters long."
        
    all_users = {**DEFAULT_USERS, **registered_users}
    if clean_email in all_users:
        return False, None, "An account with this email already exists. Please login instead."
        
    new_user = {
        "name": clean_name,
        "email": clean_email,
        "role": "Recruitment Specialist",
        "organization": clean_org,
        "password_hash": hash_password(password)
    }
    
    return True, new_user, f"Account created successfully for {clean_name}!"
