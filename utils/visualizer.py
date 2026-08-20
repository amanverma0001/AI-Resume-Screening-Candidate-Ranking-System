"""
Interactive Plotly Visualizations for Recruiter Dashboard.
Optimized for high-contrast visibility in Dark and Light themes.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any

def create_score_gauge(score: float, title: str = "Overall Match Score") -> go.Figure:
    """Creates a sleek, modern gauge chart for match score with high contrast text."""
    if score >= 70:
        bar_color = "#10B981" # Green
    elif score >= 45:
        bar_color = "#F59E0B" # Amber
    else:
        bar_color = "#EF4444" # Red

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'suffix': "%", 'font': {'size': 40, 'color': bar_color, 'family': 'Plus Jakarta Sans, sans-serif'}},
        title={'text': title, 'font': {'size': 18, 'color': '#94A3B8', 'family': 'Plus Jakarta Sans, sans-serif'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8", 'tickfont': {'color': '#94A3B8'}},
            'bar': {'color': bar_color, 'thickness': 0.75},
            'bgcolor': "rgba(255,255,255,0.06)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 45], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [45, 70], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ],
            'threshold': {
                'line': {'color': bar_color, 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=240,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'family': "Plus Jakarta Sans, sans-serif", 'color': '#F8FAFC'}
    )
    return fig

def create_breakdown_bar(candidate_data: Dict[str, Any]) -> go.Figure:
    """Creates a breakdown horizontal bar chart of the scoring factors."""
    categories = ["Skill Overlap", "Experience Match", "Education Match"]
    scores = [
        candidate_data.get("skill_score", 0),
        candidate_data.get("exp_score", 0),
        candidate_data.get("edu_score", 0)
    ]
    colors = ["#3B82F6", "#EC4899", "#10B981"]

    fig = go.Figure(go.Bar(
        x=scores,
        y=categories,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(width=0)
        ),
        text=[f"{s:.1f}%" for s in scores],
        textposition='auto',
        hoverinfo='x+y'
    ))

    fig.update_layout(
        title={'text': "Score Component Breakdown", 'font': {'color': '#F8FAFC', 'size': 16}},
        xaxis=dict(range=[0, 100], title="Score (%)", showgrid=True, gridcolor="rgba(255, 255, 255, 0.1)", tickfont={'color': '#94A3B8'}, title_font={'color': '#94A3B8'}),
        yaxis=dict(autorange="reversed", tickfont={'color': '#F8FAFC'}),
        height=240,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'family': "Plus Jakarta Sans, sans-serif", 'color': '#F8FAFC'}
    )
    return fig

def create_leaderboard_chart(ranked_candidates: List[Dict[str, Any]]) -> go.Figure:
    """Creates an overview comparison bar chart of all candidates."""
    names = [c["candidate_name"] for c in ranked_candidates]
    scores = [c["final_score"] for c in ranked_candidates]
    colors = [c["fit_color"] for c in ranked_candidates]

    fig = go.Figure(go.Bar(
        x=names,
        y=scores,
        marker=dict(color=colors),
        text=[f"{s}%" for s in scores],
        textposition='outside',
        textfont=dict(color='#F8FAFC', size=12)
    ))

    fig.update_layout(
        title={'text': "Applicant Match Ranking Overview", 'font': {'color': '#F8FAFC', 'size': 16}},
        xaxis=dict(title="Candidate", tickangle=-25, tickfont={'color': '#F8FAFC'}, title_font={'color': '#94A3B8'}),
        yaxis=dict(range=[0, 110], title="Overall Match Score (%)", gridcolor="rgba(255, 255, 255, 0.1)", tickfont={'color': '#94A3B8'}, title_font={'color': '#94A3B8'}),
        height=320,
        margin=dict(l=20, r=20, t=50, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'family': "Plus Jakarta Sans, sans-serif", 'color': '#F8FAFC'}
    )
    return fig

def create_category_distribution_chart(skills_by_category: Dict[str, List[str]]) -> go.Figure:
    """Creates a chart showing count of candidate skills per category."""
    categories = list(skills_by_category.keys())
    counts = [len(v) for v in skills_by_category.values()]

    if not categories:
        return go.Figure()

    fig = go.Figure(go.Bar(
        x=counts,
        y=categories,
        orientation='h',
        marker=dict(color="#6366F1"),
        text=counts,
        textposition='outside',
        textfont=dict(color='#F8FAFC')
    ))

    fig.update_layout(
        title={'text': "Skills by Domain Category", 'font': {'color': '#F8FAFC', 'size': 16}},
        xaxis=dict(title="Number of Skills", gridcolor="rgba(255, 255, 255, 0.1)", tickfont={'color': '#94A3B8'}, title_font={'color': '#94A3B8'}),
        yaxis=dict(autorange="reversed", tickfont={'color': '#F8FAFC'}),
        height=260,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'family': "Plus Jakarta Sans, sans-serif", 'color': '#F8FAFC'}
    )
    return fig
