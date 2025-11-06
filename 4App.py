import streamlit as st
from streamlit_drawable_canvas import st_canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
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
    page_title="Fit2Clean Partnership Agreement",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load email credentials from secrets (optional)
try:
    EMAIL_ADDRESS = st.secrets["email"]["sender_email"]
    EMAIL_PASSWORD = st.secrets["email"]["password"]
    SMTP_SERVER = st.secrets["email"]["smtp_server"]
    PORT = st.secrets["email"]["port"]
    ADMIN_EMAIL = st.secrets["email"]["admin_email"]
except:
    EMAIL_ADDRESS = None
    st.info("💡 Email notifications are disabled. Configure email secrets to enable automatic delivery.")

# Custom CSS for professional styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.875rem 1.5rem;
        border-radius: 0.75rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        font-size: 1rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        opacity: 0.95;
        font-weight: 400;
    }
    
    .info-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 5px solid #0284c7;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 5px solid #f59e0b;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 5px solid #10b981;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .commission-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 2px solid #e5e7eb;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        /* Making all text in cards black for better readability */
        color: #000000;
    }
    
    .commission-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    .commission-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .commission-value {
        font-size: 2rem;
        font-weight: 700;
        /* Changed from #1f2937 to pure black */
        color: #000000;
        margin: 0.5rem 0;
    }
    
    .step-header {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        margin: 2rem 0 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    .step-number {
        display: inline-block;
        background: #667eea;
        color: white;
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        text-align: center;
        line-height: 2rem;
        font-weight: 700;
        margin-right: 0.75rem;
    }
    
    h1, h2, h3 {
        color: #1f2937;
    }
    
    .signature-canvas {
        border: 3px dashed #667eea;
        border-radius: 0.75rem;
        padding: 1rem;
        background: #fafafa;
    }
    
    .partner-info-display {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 2px solid #e5e7eb;
        margin: 1rem 0;
    }
    
    .footer-section {
        text-align: center;
        color: #6b7280;
        padding: 3rem 0 2rem 0;
        margin-top: 3rem;
        border-top: 2px solid #e5e7eb;
    }
    
    .stExpander {
        border: 2px solid #e5e7eb;
        border-radius: 0.75rem;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agreement_accepted' not in st.session_state:
    st.session_state.agreement_accepted = False
if 'partner_name' not in st.session_state:
    st.session_state.partner_name = ""
if 'partner_entity' not in st.session_state:
    st.session_state.partner_entity = ""
if 'partner_email' not in st.session_state:
    st.session_state.partner_email = ""
if 'partner_phone' not in st.session_state:
    st.session_state.partner_phone = ""
if 'partnership_type' not in st.session_state:
    st.session_state.partnership_type = "Full Partnership"

# Partnership Agreement Text
agreement_text = """
FIT2CLEAN PARTNERSHIP AGREEMENT

This Partnership Agreement ("Agreement") is made and entered into as of [DATE], by and between:

Fit2Clean, LLC, a cleaning and technology company ("Company"), with its principal place of business at [Company Address], and

[PARTNER_NAME] / [PARTNER_ENTITY], an independent partner or affiliate ("Partner"), with contact information as provided below.

Collectively referred to as the "Parties."

RECITALS

WHEREAS, the Company operates a comprehensive cleaning services franchise system, technology platform (Fit2Clean.app), and AI-powered CRM software (Meticulous Systems) designed for cleaning businesses;

WHEREAS, the Partner desires to promote, market, and facilitate sales of the Company's franchises, software solutions, and platform services;

WHEREAS, the Parties wish to establish a mutually beneficial partnership framework with clearly defined compensation structures and responsibilities;

NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the Parties agree as follows:

1. PURPOSE AND SCOPE OF PARTNERSHIP

1.1 Purpose
The purpose of this Agreement is to establish a comprehensive partnership framework under which the Partner will promote, refer, market, and assist in the sale of Fit2Clean franchises, software subscriptions, platform services, and related products, in exchange for commissions and recurring revenue participation as detailed herein.

1.2 Authorized Activities
The Partner is expressly authorized to:
   a) Promote and facilitate the sale of Fit2Clean Franchise opportunities to qualified prospects;
   b) Onboard vendors, cleaning service providers, and sellers to the Fit2Clean.app marketplace platform;
   c) Promote and resell subscriptions to Meticulous Systems, the Company's AI-powered CRM software for cleaning businesses;
   d) Market any approved Fit2Clean products, services, or software solutions;
   e) Represent the Company at trade shows, networking events, and business development opportunities (with prior approval);
   f) Provide initial consultation and information to prospective franchisees and software clients.

1.3 Restrictions
The Partner shall NOT:
   a) Make any binding commitments or contracts on behalf of the Company without express written authorization;
   b) Modify pricing, terms, or conditions of any Company offerings;
   c) Use Company intellectual property outside the scope of this Agreement;
   d) Engage in any activities that could damage the Company's reputation or brand;
   e) Compete directly with the Company or represent competing cleaning franchise or software systems during the term of this Agreement.

2. COMPREHENSIVE COMMISSION STRUCTURE

2.1 Franchise Sales Commission
   • The Partner will receive a 10% Finder's Fee for each successful sale of a Fit2Clean Franchise directly referred and closed by the Partner.
   • The Finder's Fee is calculated based on the initial franchise fee paid by the franchisee.
   • Payment will be made within 30 days of the final franchise purchase, execution of the franchise agreement, and confirmation of payment receipt by the Company.
   • Example: If the franchise fee is $50,000, the Partner receives $5,000.

2.2 Seller Onboarding Revenue (Fit2Clean.app Platform)
   • The Partner will earn 10% recurring profit share from all active sellers or service providers successfully onboarded by the Partner through the Fit2Clean.app marketplace platform.
   • Recurring payments are calculated based on the net profit generated by each onboarded seller, after deduction of platform operational fees, payment processing costs, and other direct expenses.
   • This recurring revenue continues for the lifetime of the seller's active participation on the platform, or until termination of this Agreement.
   • Payments are calculated monthly and paid within 15 days of the end of each calendar month.
   • Example: If an onboarded seller generates $10,000 in net profit for the platform in a month, the Partner receives $1,000.

2.3 Software Sales Commission (Initial Sale)
   • The Partner will earn a 20% commission on the initial sale, setup fee, or licensing fee of any Fit2Clean software, automation system, or Meticulous Systems CRM sold through their direct referral.
   • This applies to one-time setup fees, annual prepayments, and initial licensing agreements.
   • Payment will be made within 30 days of receipt of payment from the customer.
   • Example: If a software setup and annual license costs $5,000, the Partner receives $1,000.

2.4 Recurring Software Subscription Revenue
   • The Partner will receive a 5% recurring revenue share on all ongoing Meticulous Systems AI CRM software subscriptions generated by their referred users.
   • This recurring commission applies to monthly or annual subscription renewals for the lifetime of the customer's active subscription.
   • Payments are calculated monthly and paid within 15 days of the end of each calendar month.
   • Example: If a referred customer pays $200/month for CRM software, the Partner receives $10/month recurring.

2.5 Commission Eligibility and Tracking
   • All referrals must be properly documented and attributed to the Partner through the Company's tracking system.
   • The Partner must use designated referral links, codes, or registration forms provided by the Company.
   • Commissions are earned only on verified, completed transactions with confirmed payment receipt.
   • The Company reserves the right to withhold commissions on fraudulent, disputed, or refunded transactions.

3. PAYMENT TERMS AND PROCEDURES

3.1 Payment Schedule
   • All commissions and recurring revenue shares will be calculated on a monthly basis following the Company's internal revenue verification and accounting processes.
   • Payments will be issued within 15 days following the end of each calendar month via the Partner's chosen payment method.

3.2 Payment Methods
   • Payments will be made via Bank Transfer (ACH), PayPal, Stripe, or other mutually agreed electronic payment methods.
   • The Partner must provide accurate banking and tax information to receive payments.
   • The Partner is responsible for any fees associated with their chosen payment method.

3.3 Invoicing Requirements
   • The Partner must provide a detailed invoice to the Company for each payment period.
   • Invoices must include: Partner name, payment period, breakdown of commissions by type, total amount due, and payment instructions.

3.4 Tax Responsibilities
   • The Partner is solely responsible for all tax obligations related to commission income.
   • The Company will issue appropriate tax documentation (e.g., Form 1099 in the United States) as required by law.
   • The Partner agrees to provide all necessary tax identification information.

3.5 Chargebacks and Refunds
   • If a customer requests a refund or initiates a chargeback within 90 days of purchase, any commissions paid to the Partner for that transaction will be deducted from future payments or must be repaid to the Company.

4. TERM, RENEWAL, AND TERMINATION

4.1 Initial Term
   • This Agreement will commence on the Effective Date stated above and continue for an initial term of one (1) year.

4.2 Automatic Renewal
   • This Agreement will automatically renew for successive one-year terms unless either Party provides written notice of non-renewal at least 60 days prior to the end of the current term.

4.3 Termination for Convenience
   • Either Party may terminate this Agreement for any reason with 30 days' written notice to the other Party.

4.4 Termination for Cause
   • The Company may terminate this Agreement immediately, without notice, if the Partner:
     a) Engages in fraud, misrepresentation, or unethical business practices;
     b) Violates any material term of this Agreement;
     c) Engages in activities that damage the Company's reputation or brand;
     d) Fails to comply with applicable laws or regulations;
     e) Becomes insolvent or files for bankruptcy.

4.5 Effect of Termination
   • Upon termination:
     a) All commissions earned on closed and collected revenue up to the termination date will be paid according to the normal payment schedule;
     b) Recurring commissions will cease as of the termination date;
     c) The Partner must immediately cease all promotional activities and use of Company intellectual property;
     d) The Partner must return or destroy all Company confidential information and materials;
     e) Obligations regarding confidentiality, non-compete, and indemnification will survive termination.

5. INTELLECTUAL PROPERTY RIGHTS

5.1 Company Ownership
   • All trademarks, service marks, trade names, logos, domain names, software, technology, processes, and proprietary systems related to Fit2Clean, Fit2Clean.app, and Meticulous Systems remain the exclusive property of Fit2Clean, LLC.

5.2 Limited License
   • The Company grants the Partner a limited, non-exclusive, non-transferable, revocable right to use Fit2Clean's brand materials, logos, and marketing collateral solely for promotional purposes under this Agreement.
   • This license terminates immediately upon termination of this Agreement.

5.3 Usage Guidelines
   • The Partner must use all Company intellectual property in accordance with brand guidelines provided by the Company.
   • The Partner may not modify, alter, or create derivative works from Company intellectual property without express written permission.

5.4 No Ownership Rights
   • Nothing in this Agreement grants the Partner any ownership rights, equity interest, or claims to Company intellectual property.

6. CONFIDENTIALITY AND NON-DISCLOSURE

6.1 Confidential Information
   • Both Parties agree to keep all business information, client data, financial information, trade secrets, marketing strategies, software code, and proprietary processes strictly confidential.

6.2 Non-Disclosure Obligation
   • Neither Party shall disclose Confidential Information to any third party without the express written consent of the other Party.

6.3 Exceptions
   • Confidential Information does not include information that:
     a) Is or becomes publicly available through no breach of this Agreement;
     b) Was rightfully in the receiving Party's possession prior to disclosure;
     c) Is independently developed by the receiving Party without use of Confidential Information;
     d) Must be disclosed pursuant to legal requirement or court order (with prior notice to the disclosing Party).

6.4 Survival
   • The confidentiality obligations under this Section shall survive termination of this Agreement for a period of five (5) years.

7. NON-COMPETE AND NON-SOLICITATION

7.1 Non-Compete Covenant
   • During the term of this Agreement and for a period of twelve (12) months following termination, the Partner shall not directly or indirectly:
     a) Market, promote, or sell competing cleaning franchise systems;
     b) Promote or sell competing CRM software or cleaning technology platforms;
     c) Assist competitors in recruiting Fit2Clean franchisees or platform sellers.

7.2 Non-Solicitation
   • During the term and for twelve (12) months after termination, the Partner shall not solicit, recruit, or attempt to hire any Company employees, contractors, franchisees, or platform sellers.

7.3 Reasonableness
   • The Parties acknowledge that the restrictions in this Section are reasonable in scope, duration, and geographic area, and are necessary to protect the Company's legitimate business interests.

8. INDEPENDENT CONTRACTOR RELATIONSHIP

8.1 Status
   • The Partner is engaged as an independent contractor and not as an employee, agent, legal representative, or partner of the Company.

8.2 Control and Discretion
   • The Partner has full discretion to manage their business operations, including scheduling, marketing methods, resource allocation, and business development strategies, provided all efforts align with this Agreement and Company guidelines.

8.3 Partner Responsibilities
   • The Partner is solely responsible for:
     a) All business expenses, tools, equipment, and operational costs;
     b) Federal, state, and local taxes, including self-employment taxes;
     c) Business insurance, liability coverage, and professional licenses;
     d) Any employees, subcontractors, or resources they engage;
     e) Compliance with all applicable laws and regulations.

8.4 No Employment Relationship
   • Nothing in this Agreement shall be construed to establish an employer-employee relationship, joint venture, partnership, or agency relationship between the Parties.
   • The Company will not withhold taxes, provide employee benefits, or make contributions on behalf of the Partner.

9. REPRESENTATIONS AND WARRANTIES

9.1 Company Representations
   • The Company represents and warrants that:
     a) It is duly organized and validly existing under applicable law;
     b) It has the authority to enter into this Agreement;
     c) Its products and services comply with applicable laws and regulations;
     d) It will provide accurate information about its offerings to the Partner.

9.2 Partner Representations
   • The Partner represents and warrants that:
     a) They have the authority to enter into this Agreement;
     b) They will conduct business in a professional and ethical manner;
     c) They will comply with all applicable laws and regulations;
     d) They will not make false or misleading representations about Company products or services;
     e) They have or will obtain all necessary licenses and permits to conduct their business.

10. INDEMNIFICATION

10.1 Mutual Indemnification
   • Each Party agrees to indemnify, defend, and hold harmless the other Party from and against any and all claims, damages, losses, liabilities, costs, and expenses (including reasonable attorneys' fees) arising from:
     a) Breach of any representation, warranty, or covenant in this Agreement;
     b) Negligence or willful misconduct;
     c) Violation of applicable laws or regulations.

10.2 Procedure
   • The indemnified Party must provide prompt written notice of any claim and cooperate in the defense.
   • The indemnifying Party has the right to control the defense and settlement of any claim.

11. LIMITATION OF LIABILITY

11.1 Exclusion of Consequential Damages
   • Neither Party shall be liable for any indirect, incidental, consequential, special, or punitive damages, including lost profits, even if advised of the possibility of such damages.

11.2 Cap on Liability
   • Each Party's total liability under this Agreement shall not exceed the total commissions paid or payable to the Partner in the twelve (12) months preceding the claim.

12. COMPLIANCE AND LEGAL REQUIREMENTS

12.1 Laws and Regulations
   • Both Parties agree to comply with all applicable federal, state, and local laws, regulations, and ordinances in the performance of this Agreement.

12.2 Franchise Disclosure
   • The Partner acknowledges that franchise sales are subject to franchise disclosure laws and regulations.
   • The Partner will not make any representations about franchise opportunities that are not contained in the Company's Franchise Disclosure Document (FDD).

12.3 Data Protection
   • Both Parties agree to comply with applicable data protection and privacy laws, including but not limited to GDPR, CCPA, and other relevant regulations.

13. DISPUTE RESOLUTION

13.1 Negotiation
   • In the event of any dispute arising from this Agreement, the Parties agree to first attempt to resolve the matter through good-faith negotiation.

13.2 Mediation
   • If negotiation fails, the Parties agree to submit the dispute to mediation before a mutually agreed mediator.

13.3 Arbitration
   • If mediation is unsuccessful, any remaining disputes shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association.

13.4 Governing Law and Venue
   • This Agreement shall be governed by and construed in accordance with the laws of the State of [STATE], without regard to its conflict of law principles.
   • Any legal action must be brought in the state or federal courts located in [COUNTY], [STATE].

14. GENERAL PROVISIONS

14.1 Entire Agreement
   • This document constitutes the entire agreement between the Parties and supersedes all prior agreements, understandings, negotiations, and discussions, whether written or oral, relating to the subject matter herein.

14.2 Amendments
   • This Agreement may only be amended or modified by a written document signed by both Parties.

14.3 Waiver
   • No waiver of any provision of this Agreement shall be deemed or shall constitute a waiver of any other provision, nor shall any waiver constitute a continuing waiver.

14.4 Severability
   • If any provision of this Agreement is held to be invalid or unenforceable, the remaining provisions shall continue in full force and effect.

14.5 Assignment
   • Neither Party may assign this Agreement without the prior written consent of the other Party, except that the Company may assign this Agreement to a successor or affiliate.

14.6 Notices
   • All notices under this Agreement must be in writing and delivered via email, certified mail, or courier service to the addresses provided by the Parties.

14.7 Force Majeure
   • Neither Party shall be liable for any failure or delay in performance due to circumstances beyond their reasonable control, including acts of God, war, terrorism, pandemic, or government action.

14.8 Counterparts
   • This Agreement may be executed in counterparts, each of which shall be deemed an original and all of which together shall constitute one and the same instrument.

14.9 Survival
   • Provisions regarding confidentiality, indemnification, limitation of liability, intellectual property, and dispute resolution shall survive termination of this Agreement.

15. ACKNOWLEDGMENT AND ACCEPTANCE

By signing below, both Parties acknowledge that they have read, understood, and agree to be bound by all terms and conditions of this Partnership Agreement.

SIGNATURES

FOR FIT2CLEAN, LLC (Company)
Signature: _______________________________
Name: ___________________________________
Title: ___________________________________
Date: ___________________________________

FOR PARTNER
Signature: _______________________________
Name: ___________________________________
Entity/Business Name: _____________________
Date: ___________________________________
"""

# Step 1: Partnership Type Selection
st.markdown('<div class="step-header"><span class="step-number">1</span><strong>Select Partnership Type</strong></div>', unsafe_allow_html=True)

partnership_options = {
    "Full Partnership": "Access to all commission structures (Franchise, Platform, Software)",
    "Franchise Focus": "Primary focus on franchise sales with 10% finder's fee",
    "Software & Platform": "Focus on software sales and platform onboarding",
    "Software Only": "Exclusive focus on Meticulous Systems CRM sales"
}

selected_partnership = st.radio(
    "Choose your partnership focus:",
    options=list(partnership_options.keys()),
    help="Select the type of partnership that best fits your business goals"
)
st.session_state.partnership_type = selected_partnership
st.info(f"**{selected_partnership}:** {partnership_options[selected_partnership]}")

# Commission Structure Display
st.markdown('<div class="step-header"><span class="step-number">2</span><strong>Review Commission Structure</strong></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="commission-card">
            <div class="commission-title">🏢 Franchise Sales</div>
            <div class="commission-value">10%</div>
            <p><strong>Finder's Fee</strong> on each franchise sold</p>
            <p style="color: #000000; font-size: 0.9rem;">Example: $50,000 franchise = $5,000 commission</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="commission-card">
            <div class="commission-title">💻 Software Sales</div>
            <div class="commission-value">20%</div>
            <p><strong>Initial Sale Commission</strong> on software setup</p>
            <p style="color: #000000; font-size: 0.9rem;">Example: $5,000 setup = $1,000 commission</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="commission-card">
            <div class="commission-title">🔄 Platform Sellers</div>
            <div class="commission-value">10%</div>
            <p><strong>Recurring Profit Share</strong> from onboarded sellers</p>
            <p style="color: #000000; font-size: 0.9rem;">Example: $10,000 profit = $1,000/month recurring</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="commission-card">
            <div class="commission-title">📱 Software Subscriptions</div>
            <div class="commission-value">5%</div>
            <p><strong>Recurring Revenue</strong> on CRM subscriptions</p>
            <p style="color: #000000; font-size: 0.9rem;">Example: $200/month = $10/month recurring</p>
        </div>
    """, unsafe_allow_html=True)

# Step 3: Review Agreement
st.markdown('<div class="step-header"><span class="step-number">3</span><strong>Review Partnership Agreement</strong></div>', unsafe_allow_html=True)
st.markdown('<div class="info-box">📋 <strong>Important:</strong> Please carefully review all terms and conditions before proceeding. This is a legally binding agreement.</div>', unsafe_allow_html=True)

with st.expander("📜 **Click to View Complete Partnership Agreement**", expanded=False):
    st.markdown(agreement_text.replace("\n", "  \n"))

agreement_checkbox = st.checkbox(
    "✅ I have read, understood, and agree to all terms and conditions of this Partnership Agreement",
    value=st.session_state.agreement_accepted
)
st.session_state.agreement_accepted = agreement_checkbox

# Function to validate email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Function to validate phone
def is_valid_phone(phone):
    pattern = r'^[\d\s\-\+$$$$]{10,}$'
    return re.match(pattern, phone) is not None

# Function to send email with PDF attachment
def send_agreement_email(recipient_email, partner_name, pdf_data, pdf_filename):
    """Send signed agreement via email"""
    if not EMAIL_ADDRESS:
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = f"Fit2Clean Partnership Agreement - {partner_name}"
        
        body = f"""
Dear {partner_name},

Welcome to the Fit2Clean Partnership Program!

Thank you for signing the Partnership Agreement. Your signed agreement is attached to this email for your records.

Partnership Details:
- Partner Name: {partner_name}
- Partnership Type: {st.session_state.partnership_type}
- Date Signed: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

Commission Structure Summary:
• Franchise Sales: 10% Finder's Fee
• Platform Sellers: 10% Recurring Profit Share
• Software Sales: 20% Initial Commission
• Software Subscriptions: 5% Recurring Revenue

Next Steps:
1. Review your signed agreement
2. Access your partner dashboard (link will be sent separately)
3. Receive your unique referral codes and tracking links
4. Begin promoting Fit2Clean services

We're excited to have you as part of the Fit2Clean family! Together, we'll revolutionize the cleaning industry with cutting-edge technology and exceptional franchise opportunities.

If you have any questions, please don't hesitate to reach out to our partnership team.

Best regards,
The Fit2Clean Team
Cleaning Technology & Franchise Excellence

---
Fit2Clean, LLC
www.fit2clean.app
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
        st.error(f"Email delivery error: {str(e)}")
        return False

# Function to send admin notification
def send_admin_notification(partner_name, partner_email, partner_entity, pdf_data, pdf_filename):
    """Send notification to admin with signed agreement"""
    if not EMAIL_ADDRESS or not ADMIN_EMAIL:
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = f"New Partnership Agreement Signed - {partner_name}"
        
        body = f"""
New Fit2Clean Partnership Agreement Signed

Partner Information:
- Name: {partner_name}
- Entity/Business: {partner_entity if partner_entity else 'N/A'}
- Email: {partner_email}
- Phone: {st.session_state.partner_phone if st.session_state.partner_phone else 'N/A'}
- Partnership Type: {st.session_state.partnership_type}
- Date Signed: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

The signed partnership agreement is attached to this email.

Action Required:
1. Review partner information
2. Set up partner dashboard access
3. Generate referral codes and tracking links
4. Send welcome package and onboarding materials

Fit2Clean Partnership System
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
        st.error(f"Admin notification error: {str(e)}")
        return False

# Step 4: Enter Partner Information
if st.session_state.agreement_accepted:
    st.markdown('<div class="step-header"><span class="step-number">4</span><strong>Enter Partner Information</strong></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        partner_name = st.text_input(
            "Full Legal Name *",
            value=st.session_state.partner_name,
            placeholder="John Doe",
            help="Enter your full legal name as it should appear on the agreement"
        )
        st.session_state.partner_name = partner_name
        
        partner_email = st.text_input(
            "Email Address *",
            value=st.session_state.partner_email,
            placeholder="john.doe@example.com",
            help="Enter your email address to receive the signed agreement"
        )
        st.session_state.partner_email = partner_email
        
        partner_phone = st.text_input(
            "Phone Number",
            value=st.session_state.partner_phone,
            placeholder="+1 (555) 123-4567",
            help="Enter your contact phone number"
        )
        st.session_state.partner_phone = partner_phone
    
    with col2:
        partner_entity = st.text_input(
            "Business/Entity Name",
            value=st.session_state.partner_entity,
            placeholder="ABC Consulting LLC",
            help="Enter your business or entity name if applicable"
        )
        st.session_state.partner_entity = partner_entity
        
        partner_address = st.text_area(
            "Business Address",
            value=st.session_state.partner_address,
            placeholder="123 Main Street\nCity, State ZIP",
            help="Enter your business address",
            height=100
        )
        st.session_state.partner_address = partner_address
    
    # Validation
    email_valid = True
    phone_valid = True
    
    if st.session_state.partner_email and not is_valid_email(st.session_state.partner_email):
        st.error("⚠️ Please enter a valid email address")
        email_valid = False
    
    if st.session_state.partner_phone and not is_valid_phone(st.session_state.partner_phone):
        st.warning("⚠️ Phone number format may be invalid. Please verify.")
        phone_valid = True  # Allow to proceed with warning
    
    # Step 5: Digital Signature
    if st.session_state.partner_name and st.session_state.partner_email and email_valid:
        st.markdown('<div class="step-header"><span class="step-number">5</span><strong>Digital Signature</strong></div>', unsafe_allow_html=True)
        st.markdown('<div class="warning-box">⚠️ <strong>Legal Notice:</strong> Your digital signature legally binds you to this partnership agreement. Please sign clearly within the canvas below. By signing, you acknowledge that you have read, understood, and agree to all terms and conditions.</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### ✍️ Sign Here")
            st.markdown('<div class="signature-canvas">', unsafe_allow_html=True)
            canvas_result = st_canvas(
                fill_color="rgba(255, 255, 255, 0)",
                stroke_width=3,
                stroke_color="#000000",
                background_color="#FFFFFF",
                update_streamlit=True,
                height=300,
                width=700,
                drawing_mode="freedraw",
                key="signature_canvas",
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🎨 Signature Actions")
            if st.button("🔄 Clear Signature", use_container_width=True):
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 📋 Agreement Summary")
            st.markdown(f"""
                <div class="partner-info-display">
                    <p><strong>Partner Name:</strong><br/>{st.session_state.partner_name}</p>
                    <p><strong>Email:</strong><br/>{st.session_state.partner_email}</p>
                    {f'<p><strong>Business:</strong><br/>{st.session_state.partner_entity}</p>' if st.session_state.partner_entity else ''}
                    {f'<p><strong>Phone:</strong><br/>{st.session_state.partner_phone}</p>' if st.session_state.partner_phone else ''}
                    <p><strong>Partnership Type:</strong><br/>{st.session_state.partnership_type}</p>
                    <p><strong>Date:</strong><br/>{datetime.now().strftime('%B %d, %Y')}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Step 6: Generate PDF
        st.markdown('<div class="step-header"><span class="step-number">6</span><strong>Generate & Download Agreement</strong></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📥 Generate Signed Partnership Agreement", type="primary", use_container_width=True):
                if canvas_result.image_data is not None and canvas_result.image_data.sum() > 0:
                    with st.spinner("🔄 Generating your signed partnership agreement..."):
                        try:
                            # Create temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                                pdf_path = tmpfile.name
                                
                                # Create PDF
                                doc = SimpleDocTemplate(
                                    pdf_path,
                                    pagesize=LETTER,
                                    rightMargin=72,
                                    leftMargin=72,
                                    topMargin=72,
                                    bottomMargin=72
                                )
                                
                                # Container for PDF elements
                                elements = []
                                
                                # Styles
                                styles = getSampleStyleSheet()
                                styles.add(ParagraphStyle(
                                    name='Justify',
                                    alignment=TA_JUSTIFY,
                                    fontSize=10,
                                    leading=14,
                                    spaceAfter=6
                                ))
                                styles.add(ParagraphStyle(
                                    name='CustomTitle',
                                    fontSize=18,
                                    alignment=TA_CENTER,
                                    spaceAfter=12,
                                    textColor=colors.HexColor('#667eea'),
                                    fontName='Helvetica-Bold'
                                ))
                                styles.add(ParagraphStyle(
                                    name='SectionHeader',
                                    fontSize=12,
                                    alignment=TA_LEFT,
                                    spaceAfter=8,
                                    spaceBefore=12,
                                    fontName='Helvetica-Bold',
                                    textColor=colors.HexColor('#1f2937')
                                ))
                                
                                # Add header
                                elements.append(Paragraph("FIT2CLEAN PARTNERSHIP AGREEMENT", styles['CustomTitle']))
                                elements.append(Spacer(1, 0.3*inch))
                                
                                # Personalize agreement text
                                current_date = datetime.now().strftime("%B %d, %Y")
                                personalized_text = agreement_text.replace(
                                    "[PARTNER_NAME]",
                                    st.session_state.partner_name
                                ).replace(
                                    "[PARTNER_ENTITY]",
                                    st.session_state.partner_entity if st.session_state.partner_entity else st.session_state.partner_name
                                ).replace(
                                    "[DATE]",
                                    current_date
                                ).replace(
                                    "[STATE]",
                                    "Delaware"
                                ).replace(
                                    "[COUNTY]",
                                    "New Castle"
                                ).replace(
                                    "[Company Address]",
                                    "Fit2Clean, LLC - www.fit2clean.app"
                                )
                                
                                # Add content
                                for line in personalized_text.split('\n'):
                                    line = line.strip()
                                    if line:
                                        # Section headers
                                        if any(line.startswith(f"{i}.") for i in range(1, 16)):
                                            elements.append(Spacer(1, 0.2*inch))
                                            elements.append(Paragraph(f"<b>{line}</b>", styles['SectionHeader']))
                                        # Subsection headers
                                        elif line[0].isdigit() and '.' in line[:5]:
                                            elements.append(Paragraph(f"<b>{line}</b>", styles['Justify']))
                                        # Regular text
                                        else:
                                            elements.append(Paragraph(line, styles['Justify']))
                                    else:
                                        elements.append(Spacer(1, 0.05*inch))
                                
                                # Add signature page
                                elements.append(PageBreak())
                                elements.append(Spacer(1, 0.5*inch))
                                elements.append(Paragraph("<b>SIGNATURE PAGE</b>", styles['CustomTitle']))
                                elements.append(Spacer(1, 0.4*inch))
                                
                                # Save signature image
                                signature_path = tmpfile.name.replace(".pdf", "_sig.png")
                                sig_image = Image.fromarray(canvas_result.image_data.astype("uint8"))
                                sig_image.save(signature_path)
                                
                                # Partner signature section
                                from reportlab.platypus import Image as RLImage
                                
                                elements.append(Paragraph("<b>FOR PARTNER:</b>", styles['SectionHeader']))
                                elements.append(Spacer(1, 0.2*inch))
                                elements.append(RLImage(signature_path, width=4*inch, height=1*inch))
                                elements.append(Spacer(1, 0.1*inch))
                                
                                # Partner info table
                                partner_data = [
                                    ["Name:", st.session_state.partner_name],
                                    ["Entity/Business:", st.session_state.partner_entity if st.session_state.partner_entity else "N/A"],
                                    ["Email:", st.session_state.partner_email],
                                    ["Phone:", st.session_state.partner_phone if st.session_state.partner_phone else "N/A"],
                                    ["Partnership Type:", st.session_state.partnership_type],
                                    ["Date Signed:", current_date]
                                ]
                                
                                partner_table = Table(partner_data, colWidths=[2*inch, 4*inch])
                                partner_table.setStyle(TableStyle([
                                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                                    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
                                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                                ]))
                                elements.append(partner_table)
                                
                                elements.append(Spacer(1, 0.5*inch))
                                elements.append(Paragraph("<b>FOR FIT2CLEAN, LLC:</b>", styles['SectionHeader']))
                                elements.append(Spacer(1, 0.2*inch))
                                elements.append(Paragraph("_________________________________", styles['Normal']))
                                elements.append(Paragraph("Authorized Signatory", styles['Normal']))
                                elements.append(Paragraph(f"Date: {current_date}", styles['Normal']))
                                
                                # Build PDF
                                doc.build(elements)
                                
                                # Read PDF for download and email
                                with open(pdf_path, "rb") as f:
                                    pdf_data = f.read()
                                
                                pdf_filename = f"Fit2Clean_Partnership_Agreement_{st.session_state.partner_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                                
                                # Send emails if configuration exists
                                email_sent = False
                                admin_sent = False
                                
                                if EMAIL_ADDRESS:
                                    with st.spinner("📧 Sending agreement via email..."):
                                        email_sent = send_agreement_email(
                                            st.session_state.partner_email,
                                            st.session_state.partner_name,
                                            pdf_data,
                                            pdf_filename
                                        )
                                        
                                        admin_sent = send_admin_notification(
                                            st.session_state.partner_name,
                                            st.session_state.partner_email,
                                            st.session_state.partner_entity,
                                            pdf_data,
                                            pdf_filename
                                        )
                                
                                # Success message
                                if email_sent and admin_sent:
                                    st.markdown("""
                                        <div class="success-box">
                                            <h3 style="margin-top: 0;">✅ Success! Welcome to Fit2Clean Partnership!</h3>
                                            <p>Your partnership agreement has been successfully generated and sent to:</p>
                                            <ul>
                                                <li>Your email: <strong>{}</strong></li>
                                                <li>Fit2Clean admin team</li>
                                            </ul>
                                            <p>You'll receive your partner dashboard access and referral codes within 24 hours.</p>
                                        </div>
                                    """.format(st.session_state.partner_email), unsafe_allow_html=True)
                                elif email_sent:
                                    st.markdown('<div class="success-box">✅ Agreement sent to your email! (Admin notification pending)</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown('<div class="success-box">✅ Your partnership agreement has been generated successfully!</div>', unsafe_allow_html=True)
                                
                                # Download button
                                st.download_button(
                                    label="⬇️ Download Signed Partnership Agreement",
                                    data=pdf_data,
                                    file_name=pdf_filename,
                                    mime="application/pdf",
                                    type="primary",
                                    use_container_width=True
                                )
                                
                                # Cleanup
                                os.remove(signature_path)
                                os.remove(pdf_path)
                                
                                # Celebration
                                st.balloons()
                                
                        except Exception as e:
                            st.error(f"❌ An error occurred while generating the PDF: {str(e)}")
                            st.error("Please try again or contact support if the issue persists.")
                else:
                    st.warning("⚠️ Please provide your signature in the canvas above before generating the agreement.")
    else:
        st.info("👆 Please complete all required fields (Name and Email) to proceed with the signature.")

# Footer
st.markdown(f"""
    <div class="footer-section">
        <h3 style="color: #667eea; margin-bottom: 1rem;">🧹 Fit2Clean, LLC</h3>
        <p style="font-size: 1.1rem; margin-bottom: 0.5rem;"><strong>Cleaning Technology & Franchise Excellence</strong></p>
        <p style="margin-bottom: 1.5rem;">www.fit2clean.app | Meticulous Systems AI CRM</p>
        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 2rem auto; max-width: 600px;">
        <p style="font-size: 0.9rem; color: #9ca3af; max-width: 800px; margin: 0 auto;">
            <strong>Legal Notice:</strong> This is a legally binding partnership agreement. 
            By signing this document, you acknowledge that you have read, understood, and agree to all terms and conditions. 
            Please consult with legal counsel if you have any questions or concerns before signing.
        </p>
        <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 1rem;">
            © {datetime.now().year} Fit2Clean, LLC. All rights reserved.
        </p>
    </div>
""", unsafe_allow_html=True)
