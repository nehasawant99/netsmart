import os
import sqlite3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB_FILE = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database with all 20 real-world scams and details."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)  # Refresh database schema entirely

    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Comprehensive Scams Table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            steps TEXT NOT NULL,
            warning_signs TEXT NOT NULL,
            real_example TEXT NOT NULL,
            safety_tip TEXT NOT NULL,
            victim_action TEXT NOT NULL
        )
    """
    )

    # Dataset containing the requested 20 real-world scams
    scams_data = [
        (
            "Phishing Emails",
            "Identity Theft",
            "Fake emails pretending to be a bank, company, or government asking you to click a malicious link.",
            "1. Scammer sends urgent mail.|2. User clicks fake link.|3. Spoofed page steals credentials.",
            "Urgent language, generic greetings, mismatched sender email addresses, suspicious domains.",
            "An email from 'support@arnazon-security.com' claiming your account is locked and asking you to log in.",
            "Verify the sender address, look for typos, and never click unknown links.",
            "Change compromised passwords immediately, alert your security team, and scan your device for malware.",
        ),
        (
            "SMS Smishing",
            "Mobile Fraud",
            "Fake SMS messages text claiming your bank account is blocked, electricity will be cut off, or a delivery failed.",
            "1. Threatening SMS arrives.|2. User panics and dials number/clicks link.|3. Money or details are extracted.",
            "Sent from regular 10-digit mobile numbers instead of official corporate headers, uses high-pressure threats.",
            "An SMS saying: 'Your electricity will be disconnected tonight at 9:30 PM. Call 98765XXXXX immediately.'",
            "Never open suspicious links from SMS. Companies use official alphanumeric IDs (e.g., BR-BEST).",
            "Block the sender, report the message to your network provider, and monitor your bank statements.",
        ),
        (
            "QR Code Scam",
            "UPI/Payment Fraud",
            "Scammer sends a QR code claiming it will transfer money *to* you, but scanning it actually deducts your money.",
            "1. Scammer poses as buyer.|2. Sends QR code via WhatsApp.|3. Convinced user scans code and enters PIN.",
            "Insistence on using a QR code to credit your account, requiring your UPI PIN during the process.",
            "An OLX buyer says: 'Scan this code to receive the advance deposit for your sofa.'",
            "Remember: QR codes are strictly for paying, never for receiving money.",
            "Contact your bank instantly to freeze your UPI portal, block the fraudulent handle, and secure your banking app.",
        ),
        (
            "OTP Fraud",
            "Account Takeover",
            "Caller pretends to be bank staff, telecom agents, or courier delivery personnel asking for your OTP.",
            "1. Scammer initiates transaction.|2. OTP arrives on user's phone.|3. Scammer talks user into reading it aloud.",
            "High-pressure dialogue, calls outside business hours, requesting codes explicitly labeled 'Do Not Share'.",
            "A caller claiming to update your bank KYC says: 'I just sent a verification code. Please read it back to keep your card active.'",
            "Never share an OTP with anyone under any circumstances. Banks will never call to ask for it.",
            "Report unauthorized transactions to your bank within 3 hours to invoke zero-liability security policies.",
        ),
        (
            "UPI Collect Request Scam",
            "UPI/Payment Fraud",
            "Scammer sends a direct payment collection request over apps like GPay or PhonePe instead of sending funds.",
            "1. Fraudster promises payment.|2. Pushes a hidden 'Collect Request'.|3. User clicks 'Pay' thinking it is an intake form.",
            "A green 'Pay' or 'Approve' button flashing on your screen when you are expecting to receive funds.",
            "An online buyer pushes a request for Rs. 5,000 onto your payment app under the description 'Payment Received'.",
            "Read payment requests carefully before approving. Look for terms like 'Requested By'.",
            "File an immediate dispute directly inside the UPI app's transaction history logs.",
        ),
        (
            "Fake Customer Care",
            "Impersonation Fraud",
            "Fake support numbers planted online on search engines or maps to hijack customer support issues.",
            "1. User searches help number on Google.|2. Call connects to scammer.|3. Scammer requests payment or remote access.",
            "Mobile numbers listed as official customer care, demands for money to resolve a complaint.",
            "Finding a helpline number for Swiggy or Zomato on a random blog that turns out to be a personal mobile phone.",
            "Use only official customer support options listed directly within the legitimate app or website.",
            "Report the fraudulent phone number to platforms like Truecaller and national cyber units.",
        ),
        (
            "Remote Access App Scam",
            "Technical Fraud",
            "Victims are guided into installing screen-sharing applications to 'fix' a technical issue, allowing full control.",
            "1. Caller claims technical breakdown.|2. Instructs user to install app.|3. Scammer steals passwords visible on screen.",
            "Demands to install third-party connectivity apps, asking you to read out highly sensitive login codes.",
            "A 'bank executive' asks you to download AnyDesk from the Play Store so they can fix your mobile banking error.",
            "Never give remote screen access or installation privileges to unexpected or unknown callers.",
            "Uninstall the remote software immediately, disconnect your internet, and change all passwords.",
        ),
        (
            "Job Offer Scam",
            "Employment Fraud",
            "Fake recruiters offer lucrative positions but demand processing, training, or laptop allocation fees beforehand.",
            "1. Fake job posting or email.|2. Brief online 'interview'.|3. Demand for money to unlock the offer letter.",
            "Lack of formal interviews, generic email templates, demands for upfront processing or documentation fees.",
            "Receiving an offer letter from 'Air India Careers' demanding a refundable security deposit of Rs. 10,000 for uniform costs.",
            "Genuine employers never ask for advance payments or registration fees during recruitment.",
            "Cease all communication, trace the payment route, and flag the firm on business portals like LinkedIn.",
        ),
        (
            "Work From Home Scam",
            "Employment Fraud",
            "Promises of extraordinary income for simple online tasks like liking videos, typing data, or filling review sheets.",
            "1. WhatsApp message invites user.|2. Initial small task pays Rs. 200.|3. User is forced into high-stake deposit tiers.",
            "No skill requirements, extremely high payout promises for basic tasks, communication exclusively via Telegram/WhatsApp.",
            "An anonymous message offering Rs. 5,000 per day simply for liking 10 YouTube video links.",
            "Thoroughly research company domains and profiles before accepting unsolicited online task jobs.",
            "Refuse further crypto/bank deposits and extract transaction records for evidentiary filing.",
        ),
        (
            "Investment / Trading Scam",
            "Financial Investment Fraud",
            "Guaranteed high returns through fake cryptocurrency exchanges, foreign index options, or institutional IPO allocations.",
            "1. Targeted via social media ads.|2. Added to massive trading advice groups.|3. Fake app shows high returns but blocks cashouts.",
            "Promises of zero-risk high profits, peer pressure within private text channels, bank transfers to unrelated export accounts.",
            "A WhatsApp trading group showing screenshots of members making 50% daily returns using a secret app.",
            "If it sounds too good to be true, it is. Stick entirely to official, SEBI-registered broker portals.",
            "Notify your local cyber crime node immediately before fraudsters move assets off global exchanges.",
        ),
        (
            "Lottery Scam",
            "Advance Fee Fraud",
            "Messages claim you won a massive prize, vehicle, or lottery but must pay local processing taxes to release it.",
            "1. Message states you won a lottery.|2. Victim contacts admin.|3. Admin requests custom customs/clearance fees.",
            "Winning a contest you never entered, requests for processing fees before the reward can be dispatched.",
            "A WhatsApp message with a fake certificate claiming you won Rs. 25 Lakhs from the KBC Lottery department.",
            "Ignore unexpected prize notices. Real lotteries never collect taxes or clearances from the winner first.",
            "Do not transfer any cash. Block the sender and report the group links immediately.",
        ),
        (
            "Romance Scam",
            "Social Engineering",
            "Criminals build long-distance emotional relationships online and later fabricate emergencies requiring financial aid.",
            "1. Fraudster connects on social media.|2. Builds trust over weeks.|3. Fabricates a medical or customs crisis to request emergency cash.",
            "Refusal to video call or meet in person, rapid confessions of deep affection, repeated sudden financial crises.",
            "An online companion claims they shipped you an expensive diamond watch but it got seized at customs, requiring Rs. 40,000.",
            "Never send money or personal identification records to individuals you have only met online.",
            "Stop sending funds immediately, preserve chat logs, and run a reverse-image search on their profile pictures.",
        ),
        (
            "Fake Shopping Website",
            "E-commerce Fraud",
            "Cloned e-commerce platforms selling hot items at extreme discounts to collect credit cards or keep upfront money.",
            "1. Ad displays 80% off premium shoes.|2. User purchases via credit card.|3. Site vanishes or delivers cheap garbage.",
            "Unbelievable price discounts, suspicious looking URL strings, absence of Cash on Delivery (COD) options.",
            "A website named 'zara-clearance-sale.shop' offering designer jackets normally priced at Rs. 5,000 for just Rs. 299.",
            "Verify spelling, check domain lookup records, and buy only from verified, well-known vendors.",
            "Initiate a chargeback dispute directly with your credit card issuing bank to reverse the transaction.",
        ),
        (
            "Delivery / Courier Scam",
            "Impersonation Fraud",
            "Fake messages claiming a parcel addressed to you is held up, demanding a small adjustment fee via a link.",
            "1. SMS says your packet cannot be dropped.|2. User clicks link to settle fee.|3. Malware downloads or card is skimmed.",
            "Unexpected delivery issues on items you never ordered, links that direct to unverified external payment gateways.",
            "A text stating: 'Your IndiaPost parcel is tracking errors. Pay Rs. 15 to update address parameters at this link.'",
            "Verify shipment tracking status exclusively through the official tracking panel of the actual provider.",
            "Freeze the transaction channel immediately if payment portal details were typed into the fraudulent link.",
        ),
        (
            "Social Media Giveaway Scam",
            "Social Engineering",
            "Cloned celebrity profiles run fake contests asking for delivery processing fees or system account access.",
            "1. Fake account tags you as winner.|2. Requests administrative authentication fee.|3. Steals profile access parameters.",
            "Accounts lacking verification badges, profiles with low follower counts, demands for payment to redeem gifts.",
            "An Instagram profile named '@tech_influencer_giveaways' messaging you that you won a free iPhone 15 Pro Max.",
            "Always verify profile history and handle strings before handing credentials to promotional events.",
            "Report the profile to the host social media platform for swift community account termination.",
        ),
        (
            "SIM Swap Scam",
            "Mobile Fraud",
            "Fraudsters trick telecom operators into issuing a duplicate SIM card to hijack bank OTPs and bypass 2FA.",
            "1. Attacker gathers personal details.|2. Files fake lost-SIM report.|3. User's phone loses signal while attacker gets OTPs.",
            "Sudden, unexplained loss of network connectivity on your phone, receiving strange carrier update text requests.",
            "Your mobile network bars completely drop to zero at home, and you cannot place outbound network calls.",
            "Lock your SIM card configuration with a custom PIN and contact your operator instantly if connectivity drops without reason.",
            "Alert your bank immediately to freeze network authorization pathways and check log audits.",
        ),
        (
            "Identity Verification Scam",
            "Impersonation Fraud",
            "Fake alerts warning that your identity records, files, or bank link cards will be permanently suspended or blocked.",
            "1. Phishing alert arrives.|2. Threatens total blocking within hours.|3. Steals document pictures and data via a form portal.",
            "Extreme deadlines, requests to upload unredacted government IDs to unencrypted form pages.",
            "An SMS claiming: 'Your PAN card link is inactive. Update now at link-pan-verification.net to avoid a penalty.'",
            "Manage document links and compliance parameters only via official government portals.",
            "File an alert on government identity recovery frameworks if scanned copies were leaked.",
        ),
        (
            "Tech Support Scam",
            "Technical Fraud",
            "Intrusive popups simulate system system infections, locking screens to force victims into calling bogus support hotlines.",
            "1. Browser triggers loud alert script.|2. Claims total hard drive collapse.|3. Demands payment for software removal.",
            "Loud warning sounds, full-screen browser lockdowns, demands for payment via online gift cards.",
            "A flashing window stating: 'WINDOWS HELPLINE: Your computer is infected with Trojan-X. Call 1800-XXX-XXXX.'",
            "Force-close your browser entirely. Do not call numbers flashed by non-system browser alerts.",
            "Scan the workstation system partitions using a trusted local anti-malware client tool.",
        ),
        (
            "Fake Loan App Scam",
            "Mobile Fraud",
            "Instant credit applications that harvest contacts, photo galleries, and subsequently blackmail victims for extortion.",
            "1. Quick loan application installed.|2. App pulls storage data.|3. Scammer morphs photos to extort extreme interest fees.",
            "Demanding unrelated permissions (like full contacts/gallery access) for a simple loan valuation check.",
            "An app promising Rs. 50,000 cash credit instantly without documentation checking, then calling family contacts.",
            "Download financial applications exclusively from regulated entities verified by national banking authorities.",
            "Revoke application storage access, alter account structures, and file an extortion report with police agencies.",
        ),
        (
            "Deepfake Voice/Video Scam",
            "Artificial Intelligence",
            "AI algorithms mimic family members or high-ranking executives over phone/video calls to siphon emergency cash.",
            "1. Caller profile matches target's child.|2. Simulates acoustic emergency panic loop.|3. Demands immediate UPI deployment.",
            "Unnatural video artifacts, robotic synchronization glitches, extreme pressure to wire money without giving time to verify.",
            "A video call showing your cousin claiming they are trapped at an airport checkpoint and need Rs. 20,000 immediately.",
            "Hang up and dial the person back on their known, verified primary line, or ask a personal question only they would know.",
            "Alert close networks, compile call telemetry, and report voice signature profiles to cyber cells.",
        ),
    ]

    cursor.executemany(
        "INSERT INTO scams (title, category, description, steps, warning_signs, real_example, safety_tip, victim_action) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        scams_data,
    )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/scams", methods=["GET"])
def get_scams():
    search_query = request.args.get("search", "").strip()
    conn = get_db_connection()

    if search_query:
        scams = conn.execute(
            "SELECT * FROM scams WHERE title LIKE ? OR description LIKE ? OR category LIKE ?",
            (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"),
        ).fetchall()
    else:
        scams = conn.execute("SELECT * FROM scams").fetchall()

    conn.close()
    return jsonify([dict(row) for row in scams])


if __name__ == "__main__":
    init_db()
    # Use the port provided by the host environment, default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)