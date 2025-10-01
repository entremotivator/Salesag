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

# Page configuration
st.set_page_config(
    page_title="AI Business Owner Agreement",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0052a3;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    h1 {
        color: #1a1a1a;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        color: #333;
        margin-top: 2rem !important;
    }
    h3 {
        color: #0066cc;
        margin-top: 1.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agreement_accepted' not in st.session_state:
    st.session_state.agreement_accepted = False
if 'rep_name' not in st.session_state:
    st.session_state.rep_name = ""
if 'rep_business' not in st.session_state:
    st.session_state.rep_business = ""
if 'signature_confirmed' not in st.session_state:
    st.session_state.signature_confirmed = False

# Header
st.title("📄 Independent AI Business Owner Agreement")
st.markdown("### ATM Agency - Artificial Intelligence Technology Marketing")
st.markdown("---")

# Agreement text
agreement_text = """
Independent Artificial Intelligence Business Owner & Sales Representative Agreement
ATM Agency (Artificial Intelligence Technology Marketing Agency)

1. Parties
This Independent Artificial Intelligence Business Owner & Sales Representative Agreement ("Agreement") is entered into by and between:
ATM Agency, LLC ("Company"), a marketing and technology solutions provider specializing in Artificial Intelligence SaaS products and services; and
[Representative Full Name] ("Independent AI Business Owner" or "Representative"), an independent business owner engaged in the marketing and sale of the Company's AI SaaS products and services.
Effective Date: [Insert Date]

2. Independent Business Relationship
The Representative is engaged as an independent business owner and contractor, not as an employee, agent, or legal partner of the Company.
The Representative has full discretion to manage their business operations, including scheduling, marketing methods, and resource allocation, provided all efforts align with the Company's ethical guidelines, branding standards, and compliance requirements.
The Representative is solely responsible for:
- Business expenses, tools, and operations.
- Taxes, insurance, and regulatory compliance.
- Any employees, subcontractors, or resources they engage.
Nothing in this Agreement shall be construed to establish an employer-employee relationship, joint venture, or partnership between the parties.

3. Compensation Plan
3.1 Commission-Only Base
The Representative's earnings are 100% commission-based.
Commission begins at 15% of qualified closed and collected sales revenue.
No salary or benefits are provided (the Company may, at its discretion, extend a recoverable draw).
3.2 Commission Structure
Monthly Recurring Revenue (MRR): 15% commission on new MRR.
Example: $5,000 MRR closed = $750 commission.
Annual Contract Value (ACV): 15% commission on ACV booked.
Example: $36,000 ACV closed = $5,400 commission.
3.3 Quota Expectations
Early-stage SaaS sales: $20,000–$50,000 MRR per quarter.
Mid-Market/Enterprise: $250,000–$500,000 ACV per year.

4. Bonus & Incentive Plan
Accelerator Bonuses
15% commission on sales up to 100% of quota.
20% commission on sales beyond quota.
Tiered MRR Bonus
$500 bonus for every additional $10,000 MRR above quota.
Multi-Year Contract Bonus
+2% commission on contracts with 2–3 year commitments.
Team Incentives
$1,000 bonus per Representative if the team achieves its quarterly quota.
Non-Cash Incentives
Public leaderboard recognition.
Monthly performance prizes (e.g., travel, tech gear, experiences).
Eligibility for stock options or equity after consistent overperformance.

5. Payment Terms
Commissions are earned only on net collected revenue, not on signed contracts.
Payments will be issued within 15 days after the end of each month by direct deposit or another agreed method.
Canceled or refunded deals within 60 days will result in commission reversal or deduction from future payments.
The Representative agrees to provide valid banking or payment information for commission transfers.

6. Earnings Potential
SDR/BDR (commission-only): $80K–$100K+ annually.
AE Mid-Market: $150K–$200K+ annually.
Enterprise AE: $250K–$350K+ annually.
(15%+ commission rates are designed to reward high-performing entrepreneurs and top-tier sales talent.)

7. Representative Responsibilities
The Representative agrees to:
Conduct business with professionalism and integrity.
Protect Company reputation, intellectual property, and client relationships.
Adhere to Company branding, sales material guidelines, and compliance standards.
Avoid false or misleading representations regarding the Company's AI SaaS offerings.

8. Confidentiality & Non-Compete
The Representative shall maintain strict confidentiality of all Company trade secrets, client data, and proprietary information both during and after the term of this Agreement.
The Representative shall not directly market or sell competing AI SaaS solutions to the Company's active or prospective clients for a period of 12 months after termination.
Breach of this section may result in immediate termination and legal remedies.

9. Term & Termination
This Agreement remains in effect until terminated.
Either party may terminate with 30 days' written notice.
The Company may terminate immediately for fraud, breach of contract, misrepresentation, or unethical practices.
Upon termination:
- Commissions earned on closed and collected revenue will be paid.
- No future commissions, bonuses, or residuals shall accrue.

10. Independent Business Compliance
The Representative shall:
- Operate as an independent business owner.
- Be fully responsible for business filings, tax obligations, insurance, and compliance with federal, state, and local laws.
- Acknowledge that the Company will not withhold taxes or provide employee benefits.

11. Indemnification
The Representative agrees to indemnify and hold harmless the Company from any liability, claims, damages, or expenses arising from the Representative's business activities, except when caused by the Company's negligence or misconduct.

12. Governing Law
This Agreement shall be governed by and construed in accordance with the laws of the State of [Insert State], without regard to conflict-of-law principles.

13. Entire Agreement
This document contains the entire understanding between the parties. No verbal or written agreements made prior shall be binding unless incorporated herein. This Agreement may only be amended in writing and signed by both parties.

14. Signatures
ATM Agency, LLC
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

Independent AI Business Owner (Sales Representative)
Signature: ______________________
Name: _________________________
Business Name (if applicable): __________________
Date: __________________________
"""

# Step 1: Review Agreement
st.markdown("## Step 1: Review the Agreement")
st.markdown('<div class="info-box">📋 Please carefully review all terms and conditions before proceeding.</div>', unsafe_allow_html=True)

with st.expander("📜 **Click to View Full Agreement**", expanded=False):
    st.markdown(agreement_text.replace("\n", "  \n"))

agreement_checkbox = st.checkbox(
    "✅ I have read and understand the terms of this agreement",
    value=st.session_state.agreement_accepted
)
st.session_state.agreement_accepted = agreement_checkbox

# Step 2: Enter Information
if st.session_state.agreement_accepted:
    st.markdown("---")
    st.markdown("## Step 2: Enter Your Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rep_name = st.text_input(
            "Full Legal Name *",
            value=st.session_state.rep_name,
            placeholder="John Doe",
            help="Enter your full legal name as it should appear on the agreement"
        )
        st.session_state.rep_name = rep_name
    
    with col2:
        rep_business = st.text_input(
            "Business Name (Optional)",
            value=st.session_state.rep_business,
            placeholder="ABC Consulting LLC",
            help="Enter your business name if applicable"
        )
        st.session_state.rep_business = rep_business
    
    # Step 3: Digital Signature
    if st.session_state.rep_name:
        st.markdown("---")
        st.markdown("## Step 3: Digital Signature")
        st.markdown('<div class="warning-box">⚠️ <strong>Important:</strong> Your digital signature legally binds you to this agreement. Please sign clearly within the canvas below.</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### ✍️ Sign Here")
            canvas_result = st_canvas(
                fill_color="rgba(255, 255, 255, 0)",
                stroke_width=3,
                stroke_color="#000000",
                background_color="#FFFFFF",
                update_streamlit=True,
                height=250,
                width=700,
                drawing_mode="freedraw",
                key="signature_canvas",
            )
        
        with col2:
            st.markdown("### Actions")
            if st.button("🔄 Clear Signature", use_container_width=True):
                st.rerun()
            
            st.markdown("---")
            st.markdown("**Signing as:**")
            st.markdown(f"📝 {st.session_state.rep_name}")
            if st.session_state.rep_business:
                st.markdown(f"🏢 {st.session_state.rep_business}")
            st.markdown(f"📅 {datetime.now().strftime('%B %d, %Y')}")
        
        # Step 4: Generate PDF
        st.markdown("---")
        st.markdown("## Step 4: Generate & Download")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📥 Generate Signed Agreement PDF", type="primary", use_container_width=True):
                if canvas_result.image_data is not None:
                    # Check if signature is not empty
                    if canvas_result.image_data.sum() > 0:
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
                                    styles.add(ParagraphStyle(name='CustomTitle', fontSize=16, alignment=TA_LEFT, spaceAfter=12, bold=True))
                                    
                                    # Add content
                                    current_date = datetime.now().strftime("%B %d, %Y")
                                    personalized_text = agreement_text.replace(
                                        "[Representative Full Name]", 
                                        st.session_state.rep_name
                                    ).replace(
                                        "[Insert Date]",
                                        current_date
                                    )
                                    
                                    for line in personalized_text.split('\n'):
                                        if line.strip():
                                            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '14.')):
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
                                    
                                    # Save signature image
                                    signature_path = tmpfile.name.replace(".pdf", "_sig.png")
                                    sig_image = Image.fromarray(canvas_result.image_data.astype("uint8"))
                                    sig_image.save(signature_path)
                                    
                                    # Add Representative signature info
                                    from reportlab.platypus import Image as RLImage
                                    elements.append(Paragraph("<b>Independent AI Business Owner (Sales Representative)</b>", styles['Normal']))
                                    elements.append(Spacer(1, 0.1*inch))
                                    elements.append(RLImage(signature_path, width=3*inch, height=0.75*inch))
                                    elements.append(Paragraph(f"<b>Name:</b> {st.session_state.rep_name}", styles['Normal']))
                                    if st.session_state.rep_business:
                                        elements.append(Paragraph(f"<b>Business Name:</b> {st.session_state.rep_business}", styles['Normal']))
                                    elements.append(Paragraph(f"<b>Date:</b> {current_date}", styles['Normal']))
                                    
                                    # Build PDF
                                    doc.build(elements)
                                    
                                    # Read PDF for download
                                    with open(pdf_path, "rb") as f:
                                        pdf_data = f.read()
                                    
                                    # Success message and download button
                                    st.markdown('<div class="success-box">✅ <strong>Success!</strong> Your agreement has been generated and is ready to download.</div>', unsafe_allow_html=True)
                                    
                                    st.download_button(
                                        label="⬇️ Download Signed Agreement",
                                        data=pdf_data,
                                        file_name=f"ATM_Agency_Agreement_{st.session_state.rep_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                        mime="application/pdf",
                                        type="primary",
                                        use_container_width=True
                                    )
                                    
                                    # Cleanup
                                    os.remove(signature_path)
                                    os.remove(pdf_path)
                                    
                            except Exception as e:
                                st.error(f"❌ An error occurred while generating the PDF: {str(e)}")
                    else:
                        st.warning("⚠️ Please provide your signature in the canvas above before generating the PDF.")
                else:
                    st.warning("⚠️ Please provide your signature in the canvas above before generating the PDF.")
    else:
        st.info("👆 Please enter your name to proceed with the signature.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>ATM Agency, LLC</strong></p>
        <p>Artificial Intelligence Technology Marketing Agency</p>
        <p style='font-size: 0.9rem; margin-top: 1rem;'>
            This is a legally binding agreement. Please consult with legal counsel if you have questions.
        </p>
    </div>
""", unsafe_allow_html=True)
