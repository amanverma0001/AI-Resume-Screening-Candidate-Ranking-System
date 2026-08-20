"""
Export utilities for AI Resume Screening System.
Generates CSV, Multi-Tab Excel, and Executive PDF reports with rankings and skill gaps.
"""

import io
import datetime
import pandas as pd
from typing import List, Dict, Any

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_summary_dataframe(ranked_candidates: List[Dict[str, Any]]) -> pd.DataFrame:
    """Converts ranked candidates list into a structured Pandas DataFrame."""
    rows = []
    for c in ranked_candidates:
        rows.append({
            "Rank": c.get("rank"),
            "Candidate Name": c.get("candidate_name"),
            "Overall Match (%)": c.get("final_score"),
            "Fit Status": c.get("fit_status"),
            "Skill Overlap (%)": c.get("skill_score"),
            "Semantic Match (%)": c.get("semantic_score"),
            "Experience (Years)": c.get("experience_years"),
            "Education": ", ".join(c.get("education", [])),
            "Matched Skills": ", ".join(c.get("matched_skills", [])),
            "Missing Skills": ", ".join(c.get("missing_skills", [])),
            "Email": c.get("email"),
            "Phone": c.get("phone"),
            "File Name": c.get("filename")
        })
    return pd.DataFrame(rows)

def export_to_csv(ranked_candidates: List[Dict[str, Any]]) -> bytes:
    """Exports candidate ranking list to CSV bytes."""
    df = create_summary_dataframe(ranked_candidates)
    return df.to_csv(index=False).encode('utf-8')

def export_to_excel(ranked_candidates: List[Dict[str, Any]], jd_skills: List[str] = None) -> bytes:
    """Exports candidate ranking list to Excel bytes with multiple sheets."""
    df_summary = create_summary_dataframe(ranked_candidates)
    
    # Create a Skill Matrix DataFrame
    if jd_skills:
        matrix_rows = []
        for c in ranked_candidates:
            cand_skills = set([s.lower() for s in c.get("matched_skills", [])])
            row = {"Candidate Name": c.get("candidate_name"), "Rank": c.get("rank")}
            for skill in jd_skills:
                row[skill] = "✅ Yes" if skill.lower() in cand_skills else "❌ Missing"
            matrix_rows.append(row)
        df_matrix = pd.DataFrame(matrix_rows)
    else:
        df_matrix = pd.DataFrame()

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name="Candidate Rankings", index=False)
        if not df_matrix.empty:
            df_matrix.to_excel(writer, sheet_name="Skill Match Matrix", index=False)
            
    return output.getvalue()

def export_to_pdf(ranked_candidates: List[Dict[str, Any]], jd_title: str = "Target Role", jd_skills: List[str] = None) -> bytes:
    """Generates a professional executive PDF report using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#1E1B4B'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor('#4338CA'),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        textColor=colors.HexColor('#334155'),
        leading=12
    )

    # 1. Header Banner Title
    story.append(Paragraph("AI RESUME SCREENING & CANDIDATE EVALUATION REPORT", title_style))
    story.append(Paragraph(f"<b>Target Role:</b> {jd_title} &nbsp;|&nbsp; <b>Generated:</b> {datetime.datetime.now().strftime('%b %d, %Y - %H:%M')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#6366F1'), spaceAfter=12))

    # 2. Executive Summary Metrics Box
    total_cands = len(ranked_candidates)
    shortlisted_count = len([c for c in ranked_candidates if c.get("final_score", 0) >= 50])
    avg_score = round(sum(c.get("final_score", 0) for c in ranked_candidates) / total_cands, 1) if total_cands > 0 else 0

    metrics_data = [
        [
            Paragraph("<b>Total Applicants Evaluated</b>", body_style),
            Paragraph("<b>Shortlisted Candidates (&ge;50%)</b>", body_style),
            Paragraph("<b>Average Match Score</b>", body_style)
        ],
        [
            Paragraph(f"<font size=13 color='#1E1B4B'><b>{total_cands}</b></font>", body_style),
            Paragraph(f"<font size=13 color='#10B981'><b>{shortlisted_count}</b></font>", body_style),
            Paragraph(f"<font size=13 color='#4F46E5'><b>{avg_score}%</b></font>", body_style)
        ]
    ]

    metrics_table = Table(metrics_data, colWidths=[180, 180, 180])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 12))

    # 3. Candidate Rankings Leaderboard Table
    story.append(Paragraph("1. Candidate Ranking Leaderboard", h2_style))

    table_header = ["Rank", "Candidate Name", "Match Score", "Fit Status", "Experience", "Skills Matched"]
    table_rows = [table_header]

    for c in ranked_candidates:
        matched_str = f"{len(c.get('matched_skills', []))} / {len(jd_skills) if jd_skills else 'N/A'}"
        table_rows.append([
            f"#{c.get('rank')}",
            c.get('candidate_name', 'Unknown'),
            f"{c.get('final_score')}%",
            c.get('fit_status', 'N/A'),
            f"{c.get('experience_years')} yrs",
            matched_str
        ])

    leaderboard_table = Table(table_rows, colWidths=[40, 130, 75, 95, 75, 125])
    leaderboard_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E1B4B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,0), 5),
        ('TOPPADDING', (0,0), (-1,0), 5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('PADDING', (0,1), (-1,-1), 4),
    ]))
    story.append(leaderboard_table)
    story.append(Spacer(1, 12))

    # 4. Individual Candidate Deep-Dive Summaries
    story.append(Paragraph("2. Candidate Skill Gap Analysis Deep-Dive", h2_style))

    for c in ranked_candidates:
        matched_skills_str = ", ".join(c.get("matched_skills", [])) if c.get("matched_skills") else "None"
        missing_skills_str = ", ".join(c.get("missing_skills", [])) if c.get("missing_skills") else "None"
        edu_str = ", ".join(c.get("education", [])) if c.get("education") else "Not Specified"

        cand_text = f"""
        <b>Rank #{c.get('rank')} — {c.get('candidate_name')}</b> ({c.get('final_score')}% Match - {c.get('fit_status')})<br/>
        • <b>Email / Phone:</b> {c.get('email')} | {c.get('phone')}<br/>
        • <b>Experience:</b> {c.get('experience_years')} Years | <b>Education:</b> {edu_str}<br/>
        • <font color="#10B981"><b>Matched Skills ({len(c.get('matched_skills', []))}):</b></font> {matched_skills_str}<br/>
        • <font color="#EF4444"><b>Missing Skills ({len(c.get('missing_skills', []))}):</b></font> {missing_skills_str}
        """
        story.append(Paragraph(cand_text, body_style))
        story.append(Spacer(1, 6))

    doc.build(story)
    return buffer.getvalue()
