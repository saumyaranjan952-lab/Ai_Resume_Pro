import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os

from utils.extractor import extract_text
from utils.analyzer import load_job_roles, analyze_resume

# Page Configuration
st.set_page_config(page_title="AI Resume Dashboard", page_icon="✨", layout="wide")

# Advanced Custom CSS for SaaS-like Premium Dashboard
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #f8fafc;
    }

    /* Premium Header Area */
    .hero-container {
    /* Modern SaaS Hero */
    .hero-container {
        text-align: center;
        margin-bottom: 3rem;
    }
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: -webkit-linear-gradient(right, #4f46e5, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #64748b;
        font-size: 1.25rem;
        font-weight: 500;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Friendly Instruction Card */
    .instruction-card {
        background-color: #f0fdf4;
        border: 1px solid #dcfce7;
        border-radius: 16px;
        padding: 1.25rem;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    
    /* Config Cards (Sidebar replacement) */
    .config-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #f1f5f9;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.025);
        margin-bottom: 1.5rem;
    }
    .config-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #334155;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Steps guide */
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }
    .step-circle {
        background: #dbeafe;
        color: #2563eb;
        width: 1.5rem;
        height: 1.5rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        flex-shrink: 0;
        margin-top: 0.1rem;
    }
    .step-circle-inactive {
        background: #f1f5f9;
        color: #64748b;
    }
    .step-text h4 {
        margin: 0;
        font-size: 0.9rem;
        font-weight: 600;
        color: #1e293b;
    }
    .step-text p {
        margin: 0;
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 0.1rem;
    }
    
    /* Override Streamlit Elements inside specific layout */
    .stFileUploader > div > div {
        background: #ffffff;
        border-radius: 24px;
        border: 2px dashed #e2e8f0;
        padding: 2rem 1rem;
        transition: all 0.3s ease;
    }
    .stFileUploader > div > div:hover {
        border-color: #3b82f6;
        background: #eff6ff;
    }

    /* Dashboard Header Cards */
    .dashboard-header {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        padding: 1.5rem 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.025);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    .dashboard-header:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.05);
        border-color: #3b82f6;
    }
    .dashboard-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    .dashboard-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
    }
    
    /* Rounded Skill Tags */
    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    .tag-match {
        background: #ecfdf5;
        color: #059669;
        border: 1px solid #a7f3d0;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .tag-missing {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Circular Progress Container */
    .circular-progress-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        padding: 1rem;
    }
    
    /* Modern Interactive Recommendation Cards */
    .rec-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .rec-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
    }
    .rec-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .rec-icon {
        font-size: 1.5rem;
        background: #f1f5f9;
        padding: 0.5rem;
        border-radius: 10px;
    }
    .rec-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    .rec-badge {
        font-size: 0.70rem;
        font-weight: 700;
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        text-transform: uppercase;
        margin-left: auto;
    }
    .rec-meta {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
        display: flex;
        justify-content: space-between;
    }
    .rec-desc {
        font-size: 0.90rem;
        color: #475569;
        margin: 0;
        line-height: 1.5;
    }
    .rec-resources {
        font-size: 0.85rem;
        color: #3b82f6;
        font-weight: 600;
        margin-top: 0.25rem;
    }
    .rec-progress-bg {
        width: 100%;
        background: #e2e8f0;
        border-radius: 9999px;
        height: 6px;
        margin-top: 0.25rem;
        overflow: hidden;
    }
    .rec-progress-fill {
        height: 100%;
        border-radius: 9999px;
    }
    
    /* Gradients for dividers */
    .gradient-line {
        height: 3px;
        background: linear-gradient(90deg, transparent, #e2e8f0, #3b82f6, #e2e8f0, transparent);
        margin: 2rem 0;
        border-radius: 5px;
        opacity: 0.7;
    }

    /* Override Streamlit Top Padding */
    .block-container {
        padding-top: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Main Dashboard Header
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">AI Resume Pro</h1>
    <p class="hero-subtitle">Elevate your career with AI-powered resume analysis, skill gap detection, and personalized insights.</p>
</div>
""", unsafe_allow_html=True)

# Load Database safely
try:
    job_roles_db = load_job_roles('data/job_roles.json')
except Exception as e:
    st.error("Failed to load job roles database.")
    job_roles_db = {}

# --- Modern SaaS Layout: Hero & Upload Area ---
main_col1, main_col2 = st.columns([1.8, 1], gap="large")

with main_col1:
    # Friendly Instruction Card
    st.markdown("""
    <div class="instruction-card">
        <div style="background: #dcfce7; padding: 0.5rem; border-radius: 50%; color: #166534; flex-shrink: 0;">
            💡
        </div>
        <div>
            <h3 style="margin:0; font-size: 1.05rem; font-weight: 600; color: #166534;">Getting Started</h3>
            <p style="margin:0; margin-top:0.25rem; font-size: 0.95rem; color: #15803d; line-height: 1.5;">
                Upload your resume securely. Our AI engine instantly extracts skills, detects gaps, and maps your trajectory to your target role.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Large Drag & Drop element
    uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=['pdf', 'docx'], help="Max 200MB file size limits.", label_visibility="collapsed")

with main_col2:
    # Sidebar Configuration Area (Now in Main Layout)
    st.markdown("""
    <div class="config-card" style="padding-bottom: 0.5rem;">
        <div class="config-title">💼 Target Job Role</div>
    """, unsafe_allow_html=True)
    
    selected_role = st.selectbox("Select Target Job Role", [""] + list(job_roles_db.keys()) if job_roles_db else [""], label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # UI Workflow Hints
    st.markdown(f"""
    <div class="config-card">
        <div class="config-title">⚙️ How it Works</div>
        <div class="step-item">
            <div class="step-circle {'step-circle-inactive' if uploaded_file else ''}">1</div>
            <div class="step-text">
                <h4>Upload Resume</h4>
                <p>Drop your latest CV file.</p>
            </div>
        </div>
        <div class="step-item">
            <div class="step-circle {'step-circle-inactive' if not uploaded_file or selected_role else ''}">2</div>
            <div class="step-text">
                <h4>Select Target Role</h4>
                <p>Choose your dream job.</p>
            </div>
        </div>
        <div class="step-item">
            <div class="step-circle {'step-circle-inactive' if not (uploaded_file and selected_role) else ''}">3</div>
            <div class="step-text">
                <h4>Get AI Insights</h4>
                <p>Review your gap analysis.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def generate_pdf_report(analysis_results, role):
    """Generate a downloadable PDF report matching Streamlit results."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Resume Analysis Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Target Role: {role}")
    c.drawString(50, 700, f"Match Score: {analysis_results['score_out_of_100']}%")
    
    # Matched Skills
    c.drawString(50, 670, "Matched Skills:")
    y = 650
    for skill in analysis_results['matched_skills']:
        c.drawString(70, y, f"- {skill}")
        y -= 20
        
    # Missing Skills
    c.drawString(50, y - 10, "Missing Skills (Suggestions):")
    y -= 30
    for skill in analysis_results['missing_skills']:
        c.drawString(70, y, f"- {skill}")
        y -= 20
        if y < 50:  # New page if running out of space
            c.showPage()
            y = 750
            
    c.save()
    buffer.seek(0)
    return buffer

# --- Analysis Execution ---
if uploaded_file is None or not selected_role:
    # Render an empty placeholder spacing to keep layout clean before run
    st.write("")
else:
    with st.spinner("Analyzing resume using NLP..."):
        # Extract text based on file format
        file_type = uploaded_file.type
        resume_text = extract_text(uploaded_file, file_type)
        
        if resume_text.strip() == "":
            st.error("Could not extract text from the uploaded file. Please verify it is a valid format.")
        else:
            # Run analysis
            results = analyze_resume(resume_text, selected_role, job_roles_db)
            
            st.markdown("---")
            st.header(f"📊 Comprehensive Analysis for {selected_role}")
            
            # Divide into Premium Layout
            col1, col2, col3 = st.columns([1, 1.2, 1.2])
            
            with col1:
                st.markdown("""
                <div class="dashboard-header">
                    <span class="dashboard-icon">🎯</span>
                    <h3 class="dashboard-title">Match Score</h3>
                </div>
                """, unsafe_allow_html=True)
                score = int(results['score_out_of_100'])
                color = "#10b981" if score > 70 else "#f59e0b" if score > 40 else "#ef4444"
                
                # HTML Circular Progress Meter
                st.markdown(f"""
                <div class="circular-progress-container">
                    <svg viewBox="0 0 36 36" style="width: 150px; height: 150px; display: block;">
                      <path
                        d="M18 2.0845
                          a 15.9155 15.9155 0 0 1 0 31.831
                          a 15.9155 15.9155 0 0 1 0 -31.831"
                        fill="none"
                        stroke="#e2e8f0"
                        stroke-width="3"
                        stroke-dasharray="100, 100"
                      />
                      <path
                        d="M18 2.0845
                          a 15.9155 15.9155 0 0 1 0 31.831
                          a 15.9155 15.9155 0 0 1 0 -31.831"
                        fill="none"
                        stroke="{color}"
                        stroke-width="3.5"
                        stroke-dasharray="{score}, 100"
                        stroke-linecap="round"
                        style="animation: progress 1s ease-out forwards;"
                      />
                      <text x="18" y="20.5" text-anchor="middle" font-size="8" font-weight="bold" fill="#1e293b">{score}%</text>
                    </svg>
                </div>
                """, unsafe_allow_html=True)
                
                if 'creative_feedback' in results:
                    st.markdown(f"<p style='text-align: center; color: #475569; font-size: 0.9rem; margin-top: 1rem;'>{results['creative_feedback']}</p>", unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                <div class="dashboard-header">
                    <span class="dashboard-icon">📊</span>
                    <h3 class="dashboard-title">Skill Analysis</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if len(results['matched_skills']) == 0 and len(results['missing_skills']) == 0:
                    st.warning("Not enough data to graph.")
                else:
                    import plotly.graph_objects as go
                    fig = go.Figure(go.Pie(
                        labels=['Matched Skills', 'Missing Skills'],
                        values=[len(results['matched_skills']), len(results['missing_skills'])],
                        hole=0.6,
                        marker=dict(colors=["#10B981", "#EF4444"], line=dict(color='#ffffff', width=2)),
                        textinfo='percent',
                        hoverinfo='label+value'
                    ))
                    fig.update_layout(
                        margin=dict(t=20, b=20, l=20, r=20),
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                        height=250,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
            with col3:
                st.markdown("""
                <div class="dashboard-header">
                    <span class="dashboard-icon">🤖</span>
                    <h3 class="dashboard-title">AI Insight Panel</h3>
                </div>
                """, unsafe_allow_html=True)
                if 'ai_insights' in results:
                    st.markdown("**(💪) Core Strengths**")
                    for s in results['ai_insights']['strengths']:
                        st.markdown(f"- {s}")
                        
                    st.markdown("**(⚠️) Growth Areas**")
                    for w in results['ai_insights']['weaknesses']:
                        st.markdown(f"- {w}")
                        
                    st.markdown("**(🚀) Career Trajectory**")
                    st.info(results['ai_insights']['career_suggestions'])
            
            st.markdown("<div class='gradient-line'></div>", unsafe_allow_html=True)
            
            # Skills Extracted / Badges
            st.subheader("✅ Extracted & Matched Skills")
            if results['matched_skills']:
                tags_html = "<div class='tag-container'>" + "".join([f"<span class='tag-match'>{skill}</span>" for skill in results['matched_skills']]) + "</div>"
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.write("No matching skills found from DB.")
                
            st.markdown("<br>", unsafe_allow_html=True)
                
            # Skill Gap Suggestions
            st.markdown("""
            <div class="dashboard-header">
                <span class="dashboard-icon">💡</span>
                <h3 class="dashboard-title">AI Skill Recommendations</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if results['missing_skills']:
                st.info(f"📈 **AI Prediction:** Mastering these {len(results['missing_skills'])} missing skills can increase your Match Score by up to {100 - int(results['score_out_of_100'])}% and dramatically boost interview chances for a **{selected_role}** role.")
                
                # Category Filter
                categories = ["All"] + sorted(list(set([sd['category'] for sd in results['missing_skills_data']])))
                selected_cat = st.radio("Filter by Category", categories, horizontal=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Display missing skills as sophisticated cards in a grid 
                cols = st.columns(3)
                
                filtered_skills = [sd for sd in results['missing_skills_data'] if selected_cat == "All" or sd['category'] == selected_cat]
                
                if not filtered_skills:
                    st.warning(f"No missing skills found in the '{selected_cat}' category. Great job!")
                else:
                    for i, skill_data in enumerate(filtered_skills):
                        with cols[i % 3]:
                            prog_val = 85 if skill_data['priority'] == 'High Priority' else 55 if skill_data['priority'] == 'Medium Priority' else 35
                            filled = int(prog_val / 10)
                            bar = "█" * filled + "░" * (10 - filled)
                            
                            st.markdown(f"""<div class="rec-card" style="border-left: 5px solid {skill_data['border_color']};"><div class="rec-header"><div class="rec-icon">{skill_data['icon']}</div><h4 class="rec-title">{skill_data['skill']}</h4><div class="rec-badge" style="background: {skill_data['bg_color']}; color: {skill_data['border_color']}; border-color: {skill_data['border_color']};">{skill_data['priority']}</div></div><div class="rec-meta"><span>⏱️ {skill_data['time']}</span><span style="background: #f1f5f9; padding: 2px 8px; border-radius: 12px; color:#334155;">{skill_data['category']}</span></div><p class="rec-desc">{skill_data['tip']}</p><div style="font-size: 0.85rem; font-weight: 600; color: #334155; margin-bottom: 0.2rem;">Skill Readiness</div><div style="font-family: monospace; font-size: 0.95rem; color: {skill_data['border_color']}; margin-bottom: 1rem;">{bar} {prog_val}%</div><div style="font-size: 0.85rem; font-weight: 600; color: #334155;">Recommended Resource:</div><div class="rec-resources">{skill_data['resources']}</div></div>""", unsafe_allow_html=True)
            else:
                st.success("🌟 **Perfect Match!** You have all the core required skills for this role! Excellent profile.")
                
            st.markdown("<div class='gradient-line'></div>", unsafe_allow_html=True)
            
            # AI Profile Highlights
            st.markdown("""
            <div class="dashboard-header">
                <span class="dashboard-icon">📋</span>
                <h3 class="dashboard-title">AI Profile Breakdown</h3>
            </div>
            """, unsafe_allow_html=True)
            
            prof = results.get('structured_profile', {})
            
            # AI Summary Insight Box
            st.info(f"💡 **AI Summary Insight:** {prof.get('summary', 'Candidate profile extracted successfully.')}")
            
            # Structuring the data into interactive Expanders with styled cards inside
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.expander("🎓 Education", expanded=True):
                if prof.get("education"):
                    for edu in prof["education"]:
                        st.markdown(f"""
                        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; border-left: 4px solid #3b82f6;">
                            <h4 style="margin:0; color:#1e293b; font-size:1.1rem; font-weight:700;">{edu.get('Institution', 'Institution Name')}</h4>
                            <div style="color:#64748b; font-size:0.95rem; font-weight:600; margin-top:0.2rem;">{edu.get('Degree', 'Degree Name')}</div>
                            <div style="display:flex; justify-content:space-between; margin-top:0.5rem; font-size:0.85rem; color:#475569;">
                                <span><strong style="color:#0f172a;">CGPA:</strong> {edu.get('CGPA', 'N/A')}</span>
                                <span><strong style="color:#0f172a;">Duration:</strong> {edu.get('Duration', 'N/A')}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No distinct education lines detected.")
                    
            with st.expander("💼 Experience", expanded=True):
                if prof.get("experience"):
                    for exp in prof["experience"]:
                        st.markdown(f"""
                        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; border-left: 4px solid #f59e0b;">
                            <h4 style="margin:0; color:#1e293b; font-size:1.1rem; font-weight:700;">{exp.get('Role', 'Professional Role')}</h4>
                            <div style="color:#64748b; font-size:0.95rem; font-weight:600; margin-top:0.2rem;">{exp.get('Organization', 'Organization Name')}</div>
                            <div style="margin-top:0.5rem; font-size:0.85rem; color:#475569;">
                                <strong style="color:#0f172a;">Duration:</strong> {exp.get('Duration', 'N/A')}
                            </div>
                            <div style="margin-top:0.5rem; font-size:0.90rem; color:#334155; line-height:1.4;">
                                {exp.get('Description', '')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No distinct experience lines detected.")
            
            col_con, col_ach = st.columns(2)
            with col_con:
                with st.expander("📞 Contact Information", expanded=False):
                    email = prof.get('contact', {}).get('email', 'Not Found')
                    phone = prof.get('contact', {}).get('phone', 'Not Found')
                    st.markdown(f"""
                    <ul style="color:#334155; font-size:0.95rem; line-height:1.8;">
                        <li><strong>Email:</strong> {email}</li>
                        <li><strong>Phone:</strong> {phone}</li>
                    </ul>
                    """, unsafe_allow_html=True)
                    
            with col_ach:
                with st.expander("🏆 Achievements", expanded=False):
                    if prof.get("achievements"):
                        ach_html = "<ul style='color:#334155; font-size:0.95rem; line-height:1.8;'>" + "".join([f"<li>{ach}</li>" for ach in prof["achievements"]]) + "</ul>"
                        st.markdown(ach_html, unsafe_allow_html=True)
                    else:
                        st.write("No notable achievements extracted.")
            
            
            st.markdown("---")
            
            # Download interactive report
            pdf_buffer = generate_pdf_report(results, selected_role)
            st.download_button(
                label="📥 Download Analysis Report (PDF)",
                data=pdf_buffer,
                file_name=f"{selected_role.replace(' ', '_')}_Analysis_Report.pdf",
                mime="application/pdf"
            )
