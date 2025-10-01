import streamlit as st
from streamlit_drawable_canvas import st_canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import tempfile
import os

st.set_page_config(page_title="AI Business Owner Agreement", layout="wide")

st.title("📄 Independent AI Business Owner Agreement")
st.write("Please review the agreement below, sign on the canvas, and download your completed PDF.")

# Full agreement text
tagreement_text = """
Independent Artificial Intelligence Business Owner & Sales Representative Agreement
ATM Agency (Artificial Intelligence Technology Marketing Agency)

1. Parties
This Independent Artificial Intelligence Business Owner & Sales Representative Agreement (“Agreement”) is entered into by and between:
ATM Agency, LLC (“Company”), a marketing and technology solutions provider specializing in Artificial Intelligence SaaS products and services; and
[Representative Full Name] (“Independent AI Business Owner” or “Representative”), an independent business owner engaged in the marketing and sale of the Company’s AI SaaS products and services.
Effective Date: [Insert Date]

2. Independent Business Relationship
The Representative is engaged as an independent business owner and contractor, not as an employee, agent, or legal partner of the Company.
The Representative has full discretion to manage their business operations, including scheduling, marketing methods, and resource allocation, provided all efforts align with the Company’s ethical guidelines, branding standards, and compliance requirements.
The Representative is solely responsible for:
- Business expenses, tools, and operations.
- Taxes, insurance, and regulatory compliance.
- Any employees, subcontractors, or resources they engage.
Nothing in this Agreement shall be construed to establish an employer-employee relationship, joint venture, or partnership between the parties.

3. Compensation Plan
3.1 Commission-Only Base
The Representative’s earnings are 100% commission-based.
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
Avoid false or misleading representations regarding the Company’s AI SaaS offerings.

8. Confidentiality & Non-Compete
The Representative shall maintain strict confidentiality of all Company trade secrets, client data, and proprietary information both during and after the term of this Agreement.
The Representative shall not directly market or sell competing AI SaaS solutions to the Company’s active or prospective clients for a period of 12 months after termination.
Breach of this section may result in immediate termination and legal remedies.

9. Term & Termination
This Agreement remains in effect until terminated.
Either party may terminate with 30 days’ written notice.
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
The Representative agrees to indemnify and hold harmless the Company from any liability, claims, damages, or expenses arising from the Representative’s business activities, except when caused by the Company’s negligence or misconduct.

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

with st.expander("📜 View Full Agreement"):
    st.text_area("Agreement Content", agreement_text, height=600)

st.subheader("✍️ Please Sign Below")

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFFFFF",
    update_streamlit=True,
    height=200,
    width=600,
    drawing_mode="freedraw",
    key="canvas",
)

if st.button("Generate Signed PDF"):
    if canvas_result.image_data is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            c = canvas.Canvas(tmpfile.name, pagesize=LETTER)
            width, height = LETTER

            # Add agreement text, split across pages if needed
            text_object = c.beginText(40, height - 50)
            text_object.setFont("Times-Roman", 10)
            line_height = 14
            y = height - 50

            for line in agreement_text.split("\n"):
                if y < 100:  # Start new page
                    c.drawText(text_object)
                    c.showPage()
                    text_object = c.beginText(40, height - 50)
                    text_object.setFont("Times-Roman", 10)
                    y = height - 50
                text_object.textLine(line)
                y -= line_height

            c.drawText(text_object)

            # Save signature
            signature_path = tmpfile.name.replace(".pdf", "_sig.png")
            from PIL import Image
            sig_image = Image.fromarray((canvas_result.image_data).astype("uint8"))
            sig_image.save(signature_path)

            c.drawImage(signature_path, 40, 80, width=200, height=50, mask='auto')
            c.drawString(40, 70, "Signature:")
            c.save()

            with open(tmpfile.name, "rb") as f:
                st.download_button(
                    label="⬇️ Download Signed Agreement",
                    data=f,
                    file_name="Independent_AI_Business_Owner_Agreement.pdf",
                    mime="application/pdf"
                )

            os.remove(signature_path)
