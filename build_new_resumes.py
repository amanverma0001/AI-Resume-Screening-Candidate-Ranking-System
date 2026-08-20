"""
Script to generate the 4 new candidate PDF resumes based on the user's uploaded images.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf(filename: str, title: str, name: str, contact: str, summary: str, experience: list, education: str, skills: str):
    resumes_dir = os.path.join(os.path.dirname(__file__), "sample_data", "resumes")
    os.makedirs(resumes_dir, exist_ok=True)
    pdf_path = os.path.join(resumes_dir, filename)

    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'NameTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=2
    )

    role_style = ParagraphStyle(
        'RoleTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.HexColor('#6366F1'),
        spaceAfter=4
    )

    contact_style = ParagraphStyle(
        'ContactInfo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'H2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor('#1E1B4B'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#334155'),
        leading=13
    )

    story.append(Paragraph(name, title_style))
    story.append(Paragraph(title, role_style))
    story.append(Paragraph(contact, contact_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#6366F1'), spaceAfter=10))

    # Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", h2_style))
    story.append(Paragraph(summary, body_style))
    story.append(Spacer(1, 8))

    # Skills
    story.append(Paragraph("TECHNICAL & CORE SKILLS", h2_style))
    story.append(Paragraph(f"<b>Skills:</b> {skills}", body_style))
    story.append(Spacer(1, 8))

    # Experience
    story.append(Paragraph("WORK EXPERIENCE", h2_style))
    for exp_item in experience:
        story.append(Paragraph(f"• {exp_item}", body_style))
        story.append(Spacer(1, 4))

    # Education
    story.append(Spacer(1, 4))
    story.append(Paragraph("EDUCATION", h2_style))
    story.append(Paragraph(education, body_style))

    doc.build(story)
    print(f"Generated: {filename}")

if __name__ == "__main__":
    # 1. Stephanie Prestridge
    generate_pdf(
        filename="stephanie_prestridge_english_teacher.pdf",
        title="English Teacher",
        name="Stephanie Prestridge",
        contact="Email: stephanie.prestri.ge@emailme.com | Phone: 318-316-4514 | Location: New Orleans, LA",
        summary="State certified English teacher with 3+ years of experience in educating middle and high school students. Knowledgeable of English Language Arts Standards, modern teaching methods, and assessment systems. At St James High School helped grad class students improve final test scores by 20%.",
        experience=[
            "<b>English Teacher - St James High School, New Orleans, LA (2017 - 2018, 1 year):</b> Supervised students progress in acquiring CCSS skills. Planned tests and assessment methods for checking students CCSS skills. Created full curriculum according to state standards. Improved final test scores by 20%.",
            "<b>English Teacher - Baker Middle School, Baker, LA (2015 - 2017, 2 years):</b> Delivered English language lessons incorporating audio-visual aids. Coordinated over 50 school trips to cultural institutions."
        ],
        education="<b>Master of Arts in Teaching English and Literature</b> - Louisiana State University (2011 - 2015)<br/><b>Bachelor of Arts in English Literature</b> - Louisiana State University (2008 - 2011)",
        skills="Communication, Curriculum Development, Educational Technology, Lesson Planning, Classroom Management, Organization, Self motivation, Planning, Evaluation, Literature Analysis"
    )

    # 2. Ryan Frank
    generate_pdf(
        filename="ryan_frank_ai_engineer.pdf",
        title="Artificial Intelligence Engineer",
        name="Ryan Frank",
        contact="Email: info@resumekraft.com | Phone: 202-555-0120 | Location: Chicago, Illinois, US | LinkedIn: linkedin.com/resumekraft",
        summary="Results-driven Artificial Intelligence Engineer with a solid background in machine learning and deep learning algorithms. Skilled in developing AI and ML models, analyzing complex data sets, and implementing natural language processing techniques. Proficient in programming languages such as Python and Java.",
        experience=[
            "<b>Senior Associate Software Engineer - Oracle Cerner Healthcare Solutions (Dec 2022 - Present, 3 years):</b> Adapted new technologies to build cutting-edge artificial intelligence products. Developed data science skills to prototype machine learning model applications.",
            "<b>Senior Associate Software Engineer - Oracle Cerner Healthcare Solutions (Jul 2019 - Dec 2022, 3 years):</b> Applied industry best practices for software development with Java and OIC technologies. Designed robust solutions for functionality, scalability, and performance.",
            "<b>Project: Preterm Birth Detection Developer:</b> Preterm birth detection model with EHR using Python, Oracle ADS SDKs, Oracle AutoML.",
            "<b>Project: Infusion Rate Calculation Developer:</b> Infusion rate calculation for IV solutions using normalized rates."
        ],
        education="<b>M.Tech IT (Integrated)</b> - International Institute of Professional Studies, DAVV (Jun 2014 - Dec 2019, CGPA: 9.53)",
        skills="Artificial Intelligence, Machine Learning, Deep Learning, Natural Language Processing, Python, Java, REST APIs, Oracle ADS SDKs, Oracle AutoML, Microservices, Data Science"
    )

    # 3. David Clark
    generate_pdf(
        filename="david_clark_english_teacher.pdf",
        title="English Teacher | Literature Enthusiast | Curriculum Development",
        name="David Clark",
        contact="Email: help@enhancv.com | Phone: +1-(234)-555-1234 | Location: San Antonio, Texas | LinkedIn: linkedin.com",
        summary="With 7 years of experience in teaching English, expertise in English literature and curriculum development drives an ability to inspire and nurture a love for reading. Adept at utilizing educational technology to enhance learning experiences. Achieved a 20% improvement in student reading comprehension scores over one academic year.",
        experience=[
            "<b>English Teacher - Hilltop School, Austin, TX (01/2026 - Present):</b> Develop and implement engaging and diverse curricula that emphasize literature, writing skills, and critical thinking. Utilize educational technology to create interactive lessons leading to 15% increase in engagement.",
            "<b>High School English Teacher - Eagle Ridge Academy, Houston, TX (06/2023 - 12/2025, 2.5 years):</b> Designed comprehensive lesson plans aligned with state standards for English literature. Mentored a group of 30 students resulting in 10% increase in AP English scores.",
            "<b>Middle School English Teacher - Creekside School, Dallas, TX (06/2019 - 05/2023, 4 years):</b> Facilitated active learning experiences focusing on grammar, vocabulary, and comprehension. Led project that improved reading proficiency by 25%."
        ],
        education="<b>Bachelor of Arts in English</b> - University of Texas at San Antonio (01/2016 - 01/2019)",
        skills="Curriculum Development, Educational Technology, Classroom Management, Literature Analysis, Communication, Microsoft Office Suite, Google Classroom, Creative Writing"
    )

    # 4. Scarlett Anderson
    generate_pdf(
        filename="scarlett_anderson_ai_product_manager.pdf",
        title="AI Product Manager | Strategic Integration | Technology Leadership",
        name="Scarlett Anderson",
        contact="Email: help@enhancv.com | Phone: +1-(234)-555-1234 | Location: Philadelphia, Pennsylvania | LinkedIn: linkedin.com",
        summary="With over a decade of experience in AI and technology management, I am deeply passionate about driving business transformation. Proven track record of delivering innovative AI solutions and fostering collaborative environments that achieve significant business outcomes.",
        experience=[
            "<b>Senior AI Strategist - TechNova Solutions, Philadelphia, PA (02/2018 - Present, 6 years):</b> Directed a team of data scientists and developers in creating AI applications that increased operational efficiency by 25%. Implemented machine learning models that enhanced customer engagement.",
            "<b>AI Product Manager - Innovatech Ltd, New York, NY (06/2015 - 01/2018, 2.5 years):</b> Collaborated with business stakeholders to identify AI opportunities. Oversaw successful deployment of AI-driven marketing tools.",
            "<b>AI Solutions Architect - FuturaTech Consulting, San Francisco, CA (09/2011 - 05/2015, 3.5 years):</b> Designed and implemented scalable AI frameworks adopted company-wide. Led development of chatbot improving response times by 50%."
        ],
        education="<b>Master of Science in Artificial Intelligence</b> - Stanford University (01/2009 - 01/2011)<br/><b>Bachelor of Science in Computer Science</b> - University of Pennsylvania (01/2005 - 01/2009)",
        skills="Artificial Intelligence, Machine Learning, AI Strategy, Project Management, Strategic Planning, Cross-functional Leadership, Product Development, Deep Learning, Python"
    )
