"""
Script to generate realistic sample PDF resumes for testing and demonstrations.
Uses ReportLab to create professional PDF files.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

CANDIDATES = [
    {
        "filename": "rahul_sharma_senior_python_lead.pdf",
        "name": "Rahul Sharma",
        "title": "Senior Python Backend Engineer",
        "contact": "Email: rahul.sharma@example.com | Phone: +91 98765 43210 | linkedin.com/in/rahul-sharma-dev | github.com/rahulsharma",
        "summary": "Results-driven Senior Backend Engineer with 5+ years of experience designing scalable microservices, RESTful APIs, and cloud infrastructure using Python, FastAPI, Django, and AWS.",
        "skills": "Python, FastAPI, Django, Flask, PostgreSQL, Redis, MongoDB, Docker, Kubernetes, AWS, EC2, S3, RDS, CI/CD, GitHub Actions, PyTest, Microservices, RabbitMQ, Celery, Git, Linux, System Design",
        "experience": [
            "Senior Backend Engineer - TechCorp Solutions (2022 - Present, 3 years): Architected high-throughput FastAPI microservices serving 2M+ requests/day. Reduced API latency by 45% using Redis caching and PostgreSQL query optimization. Implemented automated CI/CD pipelines with Docker and AWS ECS.",
            "Software Developer - CloudNative Labs (2020 - 2022, 2 years): Developed Django REST APIs, integrated RabbitMQ message brokers, and wrote unit/integration tests with PyTest."
        ],
        "education": "B.Tech in Computer Science and Engineering - National Institute of Technology (2016 - 2020)"
    },
    {
        "filename": "priya_patel_ai_data_scientist.pdf",
        "name": "Priya Patel",
        "title": "Lead Data Scientist & Generative AI Engineer",
        "contact": "Email: priya.patel@example.com | Phone: +91 91234 56789 | linkedin.com/in/priya-patel-ai | github.com/priyapatel-ds",
        "summary": "AI & Data Science Specialist with 4 years of experience building machine learning models, NLP pipelines, and Retrieval-Augmented Generation (RAG) architectures using PyTorch and HuggingFace.",
        "skills": "Python, Machine Learning, Deep Learning, NLP, Natural Language Processing, PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, Generative AI, LLMs, LangChain, RAG, Transformers, BERT, HuggingFace, FAISS, ChromaDB, SQL, Docker, FastAPI, AWS",
        "experience": [
            "Senior Data Scientist - AI Innovations (2022 - Present, 3 years): Built enterprise RAG applications using LangChain, FAISS, and OpenAI LLMs. Fine-tuned BERT and transformer models for domain-specific text classification achieving 94% F1-score.",
            "Machine Learning Engineer - DataPulse Analytics (2021 - 2022, 1 year): Developed predictive ML algorithms with Scikit-learn and XGBoost; deployed inference endpoints with FastAPI and Docker."
        ],
        "education": "M.Tech in Artificial Intelligence & Data Science - Indian Institute of Technology (2019 - 2021) | B.Tech in CSE (2015 - 2019)"
    },
    {
        "filename": "amit_verma_fullstack_developer.pdf",
        "name": "Amit Verma",
        "title": "Full Stack Web Developer",
        "contact": "Email: amit.verma@example.com | Phone: +91 98111 22334 | linkedin.com/in/amit-verma-fullstack | github.com/amitverma",
        "summary": "Versatile Full Stack Developer with 3+ years of experience crafting responsive web applications using React, Node.js, TypeScript, Python, and MongoDB.",
        "skills": "JavaScript, TypeScript, React, React.js, Next.js, HTML5, CSS3, Tailwind CSS, Node.js, Express, Python, Flask, MongoDB, PostgreSQL, REST API, Git, Docker, Postman, Jest",
        "experience": [
            "Full Stack Developer - WebCraft Digital (2022 - Present, 2.5 years): Developed responsive web applications using React.js, Tailwind CSS, and Node.js. Built Python Flask utility microservices for data processing.",
            "Junior Web Developer - PixelWorks (2021 - 2022, 1 year): Designed frontend UI components and integrated RESTful APIs."
        ],
        "education": "B.Tech in Information Technology - Delhi Technological University (2017 - 2021)"
    },
    {
        "filename": "sneha_reddy_junior_python_dev.pdf",
        "name": "Sneha Reddy",
        "title": "Junior Python Developer",
        "contact": "Email: sneha.reddy@example.com | Phone: +91 97654 32109 | linkedin.com/in/sneha-reddy-py | github.com/snehareddy",
        "summary": "Enthusiastic Junior Software Developer with 1.5 years of experience in Python scripting, basic web development with Django, and database queries in MySQL.",
        "skills": "Python, Django, Flask, MySQL, SQLite, HTML, CSS, JavaScript, Git, GitHub, REST API, Linux basics, Problem Solving",
        "experience": [
            "Associate Software Engineer - NextGen Apps (2024 - Present, 1.5 years): Developed CRUD APIs using Django REST framework and created automation scripts in Python."
        ],
        "education": "BCA - Bachelor of Computer Applications - Bangalore University (2020 - 2023)"
    },
    {
        "filename": "rohit_kumar_devops_cloud_eng.pdf",
        "name": "Rohit Kumar",
        "title": "DevOps & Cloud Infrastructure Engineer",
        "contact": "Email: rohit.kumar@example.com | Phone: +91 98888 77665 | linkedin.com/in/rohit-kumar-devops | github.com/rohitkumar",
        "summary": "DevOps and Cloud Engineer with 4 years of experience specializing in AWS, Kubernetes, Terraform infrastructure-as-code, and automated CI/CD pipelines.",
        "skills": "AWS, Docker, Kubernetes, Terraform, Ansible, CI/CD, Jenkins, GitHub Actions, Linux, Bash, Python, Prometheus, Grafana, Nginx, Git, Security",
        "experience": [
            "DevOps Engineer - CloudScale Infotech (2022 - Present, 3 years): Managed multi-region AWS Kubernetes clusters. Automated infrastructure provisioning with Terraform and Ansible.",
            "Systems Engineer - Enterprise Cloud (2021 - 2022, 1 year): Maintained Linux servers and configured Jenkins CI/CD deployment pipelines."
        ],
        "education": "B.Tech in Computer Science - Pune University (2017 - 2021)"
    },
    {
        "filename": "vikram_singh_sales_marketing.pdf",
        "name": "Vikram Singh",
        "title": "Senior Sales & Business Development Manager",
        "contact": "Email: vikram.singh@example.com | Phone: +91 99000 11223 | linkedin.com/in/vikram-singh-sales",
        "summary": "Energetic Sales and Business Development Manager with 4+ years of experience in B2B client acquisition, CRM management, lead generation, and revenue growth.",
        "skills": "Sales Management, B2B Sales, Lead Generation, CRM, HubSpot, Salesforce, Client Relationship Management, Negotiation, Market Research, Communication, Leadership",
        "experience": [
            "Sales Manager - GrowthSphere Media (2022 - Present, 3 years): Led enterprise sales team and achieved 140% quarterly quota. Managed key client accounts using Salesforce.",
            "Business Development Executive - Horizon Brands (2021 - 2022, 1 year): Executed outbound email campaigns and generated 50+ qualified enterprise leads monthly."
        ],
        "education": "MBA in Marketing & Sales - Symbiosis International University (2019 - 2021) | BBA (2016 - 2019)"
    }
]

def generate_pdf(candidate_info: dict, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, candidate_info["filename"])
    
    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=2
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2563EB'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    )
    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=8
    )
    section_style = ParagraphStyle(
        'DocSection',
        parent=styles['Heading2'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )
    
    story = []
    
    # Name & Title
    story.append(Paragraph(candidate_info["name"], title_style))
    story.append(Paragraph(candidate_info["title"], subtitle_style))
    story.append(Paragraph(candidate_info["contact"], contact_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))
    
    # Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
    story.append(Paragraph(candidate_info["summary"], body_style))
    story.append(Spacer(1, 4))
    
    # Skills
    story.append(Paragraph("TECHNICAL & CORE SKILLS", section_style))
    story.append(Paragraph(f"<b>Skills:</b> {candidate_info['skills']}", body_style))
    story.append(Spacer(1, 4))
    
    # Work Experience
    story.append(Paragraph("WORK EXPERIENCE", section_style))
    for exp in candidate_info["experience"]:
        story.append(Paragraph(f"• {exp}", body_style))
        story.append(Spacer(1, 2))
    story.append(Spacer(1, 4))
    
    # Education
    story.append(Paragraph("EDUCATION", section_style))
    story.append(Paragraph(candidate_info["education"], body_style))
    
    doc.build(story)
    print(f"Generated: {file_path}")

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "resumes")
    for cand in CANDIDATES:
        generate_pdf(cand, out_dir)
    print("All sample PDF resumes generated successfully!")
