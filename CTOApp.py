import streamlit as st
from streamlit_drawable_canvas import st_canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
import tempfile
import os
from datetime import datetime
from PIL import Image
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import re

# Page configuration
st.set_page_config(
    page_title="CTO/Tech Partner Agreement",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load email credentials from secrets
try:
    EMAIL_ADDRESS = st.secrets["email"]["sender_email"]
    EMAIL_PASSWORD = st.secrets["email"]["password"]
    SMTP_SERVER = st.secrets["email"]["smtp_server"]
    PORT = st.secrets["email"]["port"]
    ADMIN_EMAIL = st.secrets["email"]["admin_email"]
except Exception as e:
    st.warning("⚠️ Email configuration not found. PDF download will still work.")
    EMAIL_ADDRESS = None

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #dbeafe;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2563eb;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fef3c7;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d1fae5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    .highlight-box {
        background-color: #f3e8ff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #8b5cf6;
        margin: 1rem 0;
    }
    h1 {
        color: #1e293b;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        color: #334155;
        margin-top: 2rem !important;
    }
    h3 {
        color: #2563eb;
        margin-top: 1.5rem !important;
    }
    .equity-highlight {
        font-size: 1.2rem;
        font-weight: 600;
        color: #7c3aed;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agreement_accepted' not in st.session_state:
    st.session_state.agreement_accepted = False
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
if 'company_rep_name' not in st.session_state:
    st.session_state.company_rep_name = ""
if 'company_email' not in st.session_state:
    st.session_state.company_email = ""
if 'cto_name' not in st.session_state:
    st.session_state.cto_name = ""
if 'cto_email' not in st.session_state:
    st.session_state.cto_email = ""
if 'state_law' not in st.session_state:
    st.session_state.state_law = ""
if 'effective_date' not in st.session_state:
    st.session_state.effective_date = datetime.now()

# Header
st.title("⚡ CTO / Tech Partner Agreement")
st.markdown("### Strategic Technology Partnership Contract")
st.markdown("---")

# Equity Summary Box
st.markdown("""
<div class="highlight-box">
    <h3 style="margin-top: 0;">💎 Equity & Compensation Overview</h3>
    <p class="equity-highlight">• Up to 8% Equity (milestone-based vesting)</p>
    <p class="equity-highlight">• +2% Bonus Equity upon $500K fundraise</p>
    <p class="equity-highlight">• 5% Gross Revenue Share (quarterly)</p>
    <p style="margin-top: 1rem; font-size: 0.95rem;">This agreement structures a comprehensive tech partnership with performance-based incentives.</p>
</div>
""", unsafe_allow_html=True)

# Agreement text
agreement_text = """
CTO / TECH PARTNER AGREEMENT

This CTO/Tech Partner Agreement ("Agreement") is entered into between:

[Company Name], ("Company"), and
[CTO/Tech Partner Name], ("CTO"), effective as of [Effective Date].

1. ROLE & RESPONSIBILITIES

The CTO agrees to architect, build, launch, and scale the Company's technology platform, manage technical systems, and oversee the technical team.

Key responsibilities include:
• Designing and implementing the overall technical architecture
• Building and managing the development team
• Ensuring platform security, scalability, and performance
• Overseeing all technology infrastructure and systems
• Managing technology roadmap and sprint planning
• Establishing best practices for code quality and deployment
• Leading technical decision-making and vendor relationships

2. EQUITY GRANT

The Company grants the CTO up to 8% of fully diluted shares, subject to milestone-based vesting:

• Architecture complete & dev team operational – 2%
• MVP feature-complete / internal QA – 2%
• Public launch (live product) – 2%
• Post-launch stability (30 days uptime & bug fixes) – 2%

Milestone Definitions:
- "Architecture complete" means approved technical documentation, infrastructure setup, and dev environment ready
- "MVP feature-complete" means all core features built and passing internal quality assurance testing
- "Public launch" means product is live and accessible to end users
- "Post-launch stability" means 99%+ uptime for 30 consecutive days with critical bugs resolved

3. SUCCESS ACCELERATOR

The CTO will receive an additional 2% equity upon verified fundraise of at least $500,000 within 6 months post-launch.

This bonus equity rewards the CTO for building a product that successfully attracts investor confidence and capital. Verification requires documented proof of funds received.

4. REVENUE PARTICIPATION

The CTO will receive 5% of gross revenue generated by the app, paid quarterly.

This revenue share applies while the CTO maintains technical leadership or ongoing advisory oversight. Revenue payments will be calculated and distributed within 30 days following each quarter end (March 31, June 30, September 30, December 31).

5. TECH INFRASTRUCTURE & BUDGET AUTHORITY

The CTO holds primary control of all technology infrastructure, including cloud services, APIs, automation, security, and related tools.

The CTO may approve and optimize technology budgets within an agreed quarterly or annual cap. The CTO is responsible for:
• Selecting technology stack and tools
• Managing cloud infrastructure costs
• Negotiating vendor contracts for technical services
• Ensuring cost-effective scaling strategies
• Maintaining security and compliance standards

Budget authority is subject to the following caps:
• Monthly technology spending up to $[Amount] without additional approval
• Major infrastructure investments over $[Amount] require Company approval

6. REVERSE VESTING

Any unvested equity automatically reverts back to the Company upon termination, resignation, or failure to meet agreed milestones.

Vesting Schedule:
- Equity vests upon completion of each milestone as defined in Section 2
- No partial vesting for incomplete milestones
- Vested equity remains with CTO after departure
- Unvested equity returns to Company equity pool

7. INTELLECTUAL PROPERTY

All technology, code, designs, systems, documentation, and IP developed by the CTO for the Company are owned solely by the Company.

This includes but is not limited to:
• Source code and software applications
• Technical architecture and system designs
• Databases and data structures
• APIs and integrations
• Documentation and technical specifications
• Proprietary algorithms and processes
• Any work product created during the term of this Agreement

The CTO agrees to execute any additional documents necessary to perfect the Company's ownership rights.

8. CONFIDENTIALITY

The CTO will maintain strict confidentiality regarding all Company data, systems, strategies, and proprietary information.

Confidential information includes:
• Business plans and strategies
• Financial information and projections
• Customer data and analytics
• Technical specifications and trade secrets
• Product roadmaps and feature plans
• Marketing strategies and competitive intelligence

This confidentiality obligation continues indefinitely, even after termination of this Agreement.

9. TERM & TERMINATION

Either party may terminate this Agreement with 30 days written notice.

Upon termination:
- All unvested equity reverts back to the Company
- Vested equity remains with the CTO
- Revenue share payments cease after the quarter of termination
- CTO must return all Company property and access credentials
- CTO must provide reasonable transition assistance (up to 30 days)

The Company may terminate immediately for cause, including:
• Breach of confidentiality
• Gross negligence or willful misconduct
• Failure to perform essential duties
• Violation of Company policies

10. NON-COMPETE & NON-SOLICITATION

During the term of this Agreement and for 12 months following termination, the CTO agrees not to:
• Develop competing products or services in the same market
• Solicit Company employees, contractors, or customers
• Disclose proprietary technical information to competitors

This restriction applies within reasonable geographic and market scope related to the Company's business.

11. DISPUTE RESOLUTION

Any disputes arising from this Agreement will first be addressed through good-faith negotiation. If unresolved within 30 days, disputes will be submitted to binding arbitration in accordance with the rules of the American Arbitration Association.

12. GOVERNING LAW

This Agreement is governed by the laws of the State of [State].

13. ENTIRE AGREEMENT

This document constitutes the entire agreement between the parties and supersedes all prior discussions, agreements, or understandings. Any modifications must be made in writing and signed by both parties.

14. SEVERABILITY

If any provision of this Agreement is found to be unenforceable, the remaining provisions will continue in full force and effect.

AGREED & ACCEPTED:

______________________________ 
Company Representative
Name: [Company Rep Name]
Date: _______________

______________________________ 
CTO/Tech Partner
Name: [CTO Name]
Date: _______________
"""

# Step 1: Review Agreement
st.markdown("## Step 1: Review the Agreement")
st.markdown('<div class="info-box">📋 Please carefully review all terms and conditions before proceeding. This is a legally binding contract.</div>', unsafe_allow_html=True)

with st.expander("📜 **Click to View Full Agreement**", expanded=False):
    st.markdown(agreement_text.replace("\n", "  \n"))

agreement_checkbox = st.checkbox(
    "✅ I have read, understand, and agree to the terms of this agreement",
    value=st.session_state.agreement_accepted
)
st.session_state.agreement_accepted = agreement_checkbox

# Function to validate email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Function to send email with PDF attachment
def send_agreement_email(recipient_email, recipient_name, role, pdf_data, pdf_filename):
    """Send signed agreement via email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = f"Signed CTO/Tech Partner Agreement - {recipient_name}"
        
        body = f"""
Dear {recipient_name},

The CTO/Tech Partner Agreement has been signed and is attached to this email for your records.

Agreement Details:
- {role}: {recipient_name}
- Date Signed: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

Please keep this document in a secure location for your records.

If you have any questions, please don't hesitate to reach out.

Best regards,
Agreement Management System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={pdf_filename}')
        msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        st.error(f"Email error: {str(e)}")
        return False

# Step 2: Enter Information
if st.session_state.agreement_accepted:
    st.markdown("---")
    st.markdown("## Step 2: Enter Agreement Details")
    
    # Company Information
    st.markdown("### 🏢 Company Information")
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input(
            "Company Name *",
            value=st.session_state.company_name,
            placeholder="Tech Innovations LLC",
            help="Enter the legal name of the company"
        )
        st.session_state.company_name = company_name
        
        company_rep_name = st.text_input(
            "Company Representative Name *",
            value=st.session_state.company_rep_name,
            placeholder="Jane Smith",
            help="Name of the person signing on behalf of the company"
        )
        st.session_state.company_rep_name = company_rep_name
    
    with col2:
        company_email = st.text_input(
            "Company Email Address *",
            value=st.session_state.company_email,
            placeholder="jane@company.com",
            help="Email address for company representative"
        )
        st.session_state.company_email = company_email
        
        effective_date = st.date_input(
            "Effective Date *",
            value=st.session_state.effective_date,
            help="The date this agreement becomes effective"
        )
        st.session_state.effective_date = effective_date
    
    # CTO Information
    st.markdown("### 👨‍💻 CTO/Tech Partner Information")
    col3, col4 = st.columns(2)
    
    with col3:
        cto_name = st.text_input(
            "CTO Full Name *",
            value=st.session_state.cto_name,
            placeholder="John Doe",
            help="Enter the full legal name of the CTO/Tech Partner"
        )
        st.session_state.cto_name = cto_name
    
    with col4:
        cto_email = st.text_input(
            "CTO Email Address *",
            value=st.session_state.cto_email,
            placeholder="john@email.com",
            help="Email address for the CTO/Tech Partner"
        )
        st.session_state.cto_email = cto_email
    
    # Additional Details
    st.markdown("### ⚖️ Legal Details")
    state_law = st.text_input(
        "Governing State Law *",
        value=st.session_state.state_law,
        placeholder="Delaware",
        help="The state whose laws will govern this agreement"
    )
    st.session_state.state_law = state_law
    
    # Validate emails
    emails_valid = True
    if st.session_state.company_email and not is_valid_email(st.session_state.company_email):
        st.error("⚠️ Please enter a valid company email address")
        emails_valid = False
    if st.session_state.cto_email and not is_valid_email(st.session_state.cto_email):
        st.error("⚠️ Please enter a valid CTO email address")
        emails_valid = False
    
    # Check if all required fields are filled
    all_fields_filled = (
        st.session_state.company_name and 
        st.session_state.company_rep_name and 
        st.session_state.company_email and
        st.session_state.cto_name and 
        st.session_state.cto_email and
        st.session_state.state_law and
        emails_valid
    )
    
    # Step 3: Digital Signatures
    if all_fields_filled:
        st.markdown("---")
        st.markdown("## Step 3: Digital Signatures")
        st.markdown('<div class="warning-box">⚠️ <strong>Important:</strong> Both parties must sign below. Digital signatures are legally binding.</div>', unsafe_allow_html=True)
        
        # Company Signature
        st.markdown("### ✍️ Company Representative Signature")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Signing as:** {st.session_state.company_rep_name} (Company Representative)")
            company_canvas = st_canvas(
                fill_color="rgba(255, 255, 255, 0)",
                stroke_width=3,
                stroke_color="#000000",
                background_color="#FFFFFF",
                update_streamlit=True,
                height=200,
                width=700,
                drawing_mode="freedraw",
                key="company_signature_canvas",
            )
        
        with col2:
            if st.button("🔄 Clear Company Signature", key="clear_company"):
                st.rerun()
            st.markdown("---")
            st.markdown(f"📝 {st.session_state.company_rep_name}")
            st.markdown(f"🏢 {st.session_state.company_name}")
            st.markdown(f"📧 {st.session_state.company_email}")
        
        st.markdown("---")
        
        # CTO Signature
        st.markdown("### ✍️ CTO/Tech Partner Signature")
        col3, col4 = st.columns([2, 1])
        
        with col3:
            st.markdown(f"**Signing as:** {st.session_state.cto_name} (CTO/Tech Partner)")
            cto_canvas = st_canvas(
                fill_color="rgba(255, 255, 255, 0)",
                stroke_width=3,
                stroke_color="#000000",
                background_color="#FFFFFF",
                update_streamlit=True,
                height=200,
                width=700,
                drawing_mode="freedraw",
                key="cto_signature_canvas",
            )
        
        with col4:
            if st.button("🔄 Clear CTO Signature", key="clear_cto"):
                st.rerun()
            st.markdown("---")
            st.markdown(f"👨‍💻 {st.session_state.cto_name}")
            st.markdown(f"📧 {st.session_state.cto_email}")
        
        # Step 4: Generate PDF
        st.markdown("---")
        st.markdown("## Step 4: Generate & Download")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📥 Generate Signed Agreement PDF", type="primary", use_container_width=True):
                # Check if both signatures exist
                company_sig_exists = company_canvas.image_data is not None and company_canvas.image_data.sum() > 0
                cto_sig_exists = cto_canvas.image_data is not None and cto_canvas.image_data.sum() > 0
                
                if company_sig_exists and cto_sig_exists:
                    with st.spinner("Generating your signed agreement..."):
                        try:
                            # Create temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                                pdf_path = tmpfile.name
                                
                                # Create PDF
                                doc = SimpleDocTemplate(pdf_path, pagesize=LETTER,
                                                      rightMargin=72, leftMargin=72,
                                                      topMargin=72, bottomMargin=72)
                                
                                # Container for PDF elements
                                elements = []
                                
                                # Styles
                                styles = getSampleStyleSheet()
                                styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=10, leading=14))
                                styles.add(ParagraphStyle(name='CustomTitle', fontSize=16, alignment=TA_LEFT, spaceAfter=12, textColor='#1e293b', bold=True))
                                
                                # Personalize agreement text
                                personalized_text = agreement_text.replace(
                                    "[Company Name]", st.session_state.company_name
                                ).replace(
                                    "[CTO/Tech Partner Name]", st.session_state.cto_name
                                ).replace(
                                    "[Effective Date]", st.session_state.effective_date.strftime("%B %d, %Y")
                                ).replace(
                                    "[State]", st.session_state.state_law
                                ).replace(
                                    "[Company Rep Name]", st.session_state.company_rep_name
                                ).replace(
                                    "[CTO Name]", st.session_state.cto_name
                                )
                                
                                # Add content
                                for line in personalized_text.split('\n'):
                                    if line.strip():
                                        if any(line.strip().startswith(f'{i}.') for i in range(1, 15)):
                                            elements.append(Spacer(1, 0.2*inch))
                                            elements.append(Paragraph(f"<b>{line}</b>", styles['Justify']))
                                        else:
                                            elements.append(Paragraph(line, styles['Justify']))
                                    else:
                                        elements.append(Spacer(1, 0.1*inch))
                                
                                elements.append(PageBreak())
                                elements.append(Spacer(1, 0.3*inch))
                                
                                # Add signature section
                                elements.append(Paragraph("<b>SIGNATURES</b>", styles['CustomTitle']))
                                elements.append(Spacer(1, 0.3*inch))
                                
                                from reportlab.platypus import Image as RLImage
                                
                                # Save and add company signature
                                company_sig_path = tmpfile.name.replace(".pdf", "_company_sig.png")
                                company_sig_image = Image.fromarray(company_canvas.image_data.astype("uint8"))
                                company_sig_image.save(company_sig_path)
                                
                                elements.append(Paragraph("<b>Company Representative</b>", styles['Normal']))
                                elements.append(Spacer(1, 0.1*inch))
                                elements.append(RLImage(company_sig_path, width=3*inch, height=0.75*inch))
                                elements.append(Paragraph(f"<b>Name:</b> {st.session_state.company_rep_name}", styles['Normal']))
                                elements.append(Paragraph(f"<b>Company:</b> {st.session_state.company_name}", styles['Normal']))
                                elements.append(Paragraph(f"<b>Email:</b> {st.session_state.company_email}", styles['Normal']))
                                elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
                                
                                elements.append(Spacer(1, 0.5*inch))
                                
                                # Save and add CTO signature
                                cto_sig_path = tmpfile.name.replace(".pdf", "_cto_sig.png")
                                cto_sig_image = Image.fromarray(cto_canvas.image_data.astype("uint8"))
                                cto_sig_image.save(cto_sig_path)
                                
                                elements.append(Paragraph("<b>CTO/Tech Partner</b>", styles['Normal']))
                                elements.append(Spacer(1, 0.1*inch))
                                elements.append(RLImage(cto_sig_path, width=3*inch, height=0.75*inch))
                                elements.append(Paragraph(f"<b>Name:</b> {st.session_state.cto_name}", styles['Normal']))
                                elements.append(Paragraph(f"<b>Email:</b> {st.session_state.cto_email}", styles['Normal']))
                                elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
                                
                                # Build PDF
                                doc.build(elements)
                                
                                # Read PDF for download and email
                                with open(pdf_path, "rb") as f:
                                    pdf_data = f.read()
                                
                                pdf_filename = f"CTO_Agreement_{st.session_state.company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                                
                                # Send emails if configuration exists
                                if EMAIL_ADDRESS:
                                    with st.spinner("Sending agreement via email..."):
                                        company_sent = send_agreement_email(
                                            st.session_state.company_email,
                                            st.session_state.company_rep_name,
                                            "Company Representative",
                                            pdf_data,
                                            pdf_filename
                                        )
                                        
                                        cto_sent = send_agreement_email(
                                            st.session_state.cto_email,
                                            st.session_state.cto_name,
                                            "CTO/Tech Partner",
                                            pdf_data,
                                            pdf_filename
                                        )
                                        
                                        if company_sent and cto_sent:
                                            st.markdown('<div class="success-box">✅ <strong>Success!</strong> Agreement sent to both parties via email.</div>', unsafe_allow_html=True)
                                        else:
                                            st.warning("⚠️ Email delivery may have failed. You can still download below.")
                                else:
                                    st.markdown('<div class="success-box">✅ <strong>Success!</strong> Your agreement is ready to download.</div>', unsafe_allow_html=True)
                                
                                st.download_button(
                                    label="⬇️ Download Signed Agreement",
                                    data=pdf_data,
                                    file_name=pdf_filename,
                                    mime="application/pdf",
                                    type="primary",
                                    use_container_width=True
                                )
                                
                                # Cleanup
                                os.remove(company_sig_path)
                                os.remove(cto_sig_path)
                                os.remove(pdf_path)
                                
                        except Exception as e:
                            st.error(f"❌ An error occurred while generating the PDF: {str(e)}")
                elif not company_sig_exists and not cto_sig_exists:
                    st.warning("⚠️ Both parties must sign before generating the PDF.")
                elif not company_sig_exists:
                    st.warning("⚠️ Company representative signature is required.")
                else:
                    st.warning("⚠️ CTO/Tech Partner signature is required.")
    else:
        st.info("👆 Please complete all required fields above to proceed with signatures.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 2rem 0;'>
        <p><strong>CTO/Tech Partner Agreement System</strong></p>
        <p style='font-size: 0.9rem; margin-top: 1rem;'>
            This is a legally binding agreement. Please consult with legal counsel if you have questions.
        </p>
        <p style='font-size: 0.85rem; margin-top: 0.5rem; color: #94a3b8;'>
            Secure • Professional • Efficient
        </p>
    </div>
""", unsafe_allow_html=True)
