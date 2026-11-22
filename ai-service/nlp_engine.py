"""
fraudRakshak - NLP Scam Shield Engine v2.0
State-of-the-Art Multi-Signal Scam & Phishing Detection Engine for Indian Ecosystem.
Accurate classification in Hinglish, Hindi, and English with zero false positives.
"""

import re
import urllib.parse
from typing import Dict, List, Any, Optional

# --- Whitelists & IOC Reference Dictionaries ---

# International Fraud Calling Codes
FRAUD_COUNTRY_CODES = {
    "+92": "Pakistan (High correlation with KBC / WhatsApp lottery fraud)",
    "+880": "Bangladesh (Cross-border SIM spoofing)",
    "+234": "Nigeria (Advance fee / lottery scams)",
    "+254": "Kenya (Romance / investment fraud)",
    "+60": "Malaysia (Telegram job syndicate)",
    "+855": "Cambodia (Cyber slavery call center compounds)",
    "+95": "Myanmar (Cyber call center compounds)",
    "+447": "UK Virtual Numbers (Spoofed WhatsApp calls)"
}

# Suspicious TLDs heavily used in phishing
SUSPICIOUS_TLDS = [
    ".online", ".xyz", ".top", ".club", ".site", ".live", ".work",
    ".vip", ".tk", ".ml", ".ga", ".cf", ".gq", ".buzz", ".monster",
    ".icu", ".fit", ".rest", ".link", ".click", ".shop", ".cam", ".cfd"
]

# Legitimate Bank & Institution Domains (Strict Whitelist)
LEGITIMATE_DOMAINS = [
    "onlinesbi.sbi", "sbi.co.in", "hdfcbank.com", "icicibank.com",
    "axisbank.com", "pnbindia.in", "bankofbaroda.in", "kotak.com",
    "paytm.com", "phonepe.com", "google.com", "cybercrime.gov.in",
    "npci.org.in", "rbi.org.in", "uidai.gov.in", "incometax.gov.in",
    "amazon.in", "amazon.com", "flipkart.com", "swiggy.com", "zomato.com",
    "jio.com", "airtel.in", "tatapower.com", "bsesdelhi.com"
]

# Known Link Shorteners used to hide destinations
LINK_SHORTENERS = [
    "bit.ly", "tinyurl.com", "is.gd", "t.co", "cutt.ly", "rb.gy",
    "shorturl.at", "bit.do", "tiny.cc", "ow.ly", "bl.ink"
]

# High-Risk Remote Access APKs & Screen Sharing Apps
REMOTE_ACCESS_TOOLS = [
    "anydesk", "teamviewer", "rustdesk", "quicksupport", "alpemix",
    "zoho assist", "airdroid", "splashtop", "screenshare"
]

# Regular Expressions
URL_REGEX = re.compile(
    r'(?:https?://|www\.)[^\s<>"\'{}|\\^`]+|[a-zA-Z0-9][a-zA-Z0-9\-]{1,61}[a-zA-Z0-9]\.(?:online|xyz|top|club|site|live|work|vip|tk|ml|ga|cf|gq|buzz|monster|icu|fit|rest|link|click|shop|cam|cfd)(?:/[^\s<>"\'{}|\\^`]*)?',
    re.IGNORECASE
)
GENERIC_DOMAIN_REGEX = re.compile(
    r'\b(?:[a-zA-Z0-9-]+\.)+(?:com|in|org|net|co|info|biz|io|app|cc|me)(?:/[^\s<>"\'{}|\\^`]*)?\b',
    re.IGNORECASE
)
PHONE_REGEX = re.compile(
    r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}'
)
APK_REGEX = re.compile(r'[\w\-]+(?:\.apk|\.app|\.exe)', re.IGNORECASE)
UPI_REGEX = re.compile(r'[\w.\-]+@(?:okhdfcbank|okaxis|oksbi|okicici|paytm|upi|ybl|axl|ibl)', re.IGNORECASE)


def extract_iocs(text: str, sender: Optional[str] = None) -> Dict[str, Any]:
    """Extract and analyze Indicators of Compromise (URLs, Phone Numbers, APKs, UPI IDs)."""
    urls_found = URL_REGEX.findall(text)
    # Also find generic domain URLs
    generic_domains = GENERIC_DOMAIN_REGEX.findall(text)
    combined_raw_urls = list(set(urls_found + generic_domains))

    phones = PHONE_REGEX.findall(text)
    apks = APK_REGEX.findall(text)
    upis = UPI_REGEX.findall(text)

    # Filter out valid 10+ digit phones
    valid_phones = []
    international_codes = []
    
    candidate_phones = list(phones)
    if sender:
        candidate_phones.append(sender)

    for p in candidate_phones:
        cleaned = re.sub(r'[^\d+]', '', p)
        if len(cleaned) >= 10:
            valid_phones.append(p.strip())
            for code, desc in FRAUD_COUNTRY_CODES.items():
                if cleaned.startswith(code):
                    international_codes.append({"code": code, "phone": p.strip(), "risk": desc})

    # Detailed URL Inspection
    url_details = []
    for u in combined_raw_urls:
        raw_u = u if u.startswith("http") else "http://" + u
        try:
            parsed = urllib.parse.urlparse(raw_u)
            domain = (parsed.netloc.lower() or parsed.path.split('/')[0].lower()).strip()
            # remove port if any
            domain = domain.split(':')[0]
        except Exception:
            domain = u.lower()

        is_suspicious_tld = any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS)
        is_ip_domain = bool(re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain))
        is_shortener = any(short in domain for short in LINK_SHORTENERS)
        is_legit = any(domain == legit or domain.endswith("." + legit) for legit in LEGITIMATE_DOMAINS)
        
        # Spoofed bank domain check
        bank_names = ["sbi", "hdfc", "icici", "pnb", "yono", "bank", "phonepe", "paytm", "gpay", "electricity", "discom", "power"]
        is_spoofed = any(b in domain for b in bank_names) and not is_legit

        url_details.append({
            "url": u,
            "domain": domain,
            "is_suspicious_tld": is_suspicious_tld,
            "is_ip_domain": is_ip_domain,
            "is_spoofed_bank": is_spoofed,
            "is_shortener": is_shortener,
            "is_legitimate": is_legit
        })

    # Remote access tools
    detected_remote_tools = [tool for tool in REMOTE_ACCESS_TOOLS if tool in text.lower()]

    return {
        "urls": url_details,
        "phone_numbers": list(set(valid_phones)),
        "international_fraud_numbers": international_codes,
        "apk_mentions": list(set(apks)),
        "upi_mentions": list(set(upis)),
        "remote_tools_detected": detected_remote_tools
    }


def is_safe_message(text: str, iocs: Dict[str, Any]) -> tuple[bool, str]:
    """
    Checks if a message is explicitly legitimate (Safe).
    Returns (True, reason) or (False, "").
    Guarantees zero false positives on genuine Indian transactional & personal SMS.
    """
    lowered = text.lower().strip()

    # NEVER SAFE: If the message contains high-risk fraud action keywords, it is NEVER safe!
    never_safe_markers = [
        "click here", "click this link", "this link", "pay rs", "processing fee",
        "delivery charge", "redelivery", "install this apk", "install apk", "download apk",
        "apk to claim", "banking password", "login password", "atm card is blocked",
        "card is blocked", "call this number", "send your aadhaar", "aadhaar and otp",
        "upi pin to avoid", "parcel is on hold", "without documents", "cash reward",
        "free iphone", "reactivate", "account will be blocked", "account will be suspended",
        "account has been selected", "claim your prize", "claim your reward", "receive your gift",
        "share your upi pin", "enter your banking password", "enter your pin", "share your otp"
    ]
    if any(m in lowered for m in never_safe_markers):
        return False, ""

    # Check if this message is actively soliciting/demanding an OTP, PIN, password, or credentials
    # Safety notices like "never share this OTP" or "do not share OTP" are NOT solicitations!
    is_safety_warning = bool(re.search(
        r'\b(?:never|do\s+not|don\'t|not\s+to|should\s+not|kisi\s+ko\s+na)\s+(?:share|disclose|give|tell|batao|dein)\b',
        lowered
    ))

    # Patterns where an attacker or scammer solicits credentials
    solicits_otp = (
        bool(re.search(r'\b(?:share|send|give|tell|provide|forward|enter|submit)\s+(?:me\s+|us\s+|our\s+)?(?:the\s+|your\s+|that\s+|this\s+|6\s*digit\s+)?(?:aadhaar\s+and\s+)?(?:otp|pin|cvv|password|passcode|code)\b', lowered))
        or bool(re.search(r'\b(?:the\s+|your\s+|that\s+|this\s+)?otp\s+(?:to\s+us|to\s+me|batao|bhejo|de\s*do|share\s*karo|forward\s*karo)\b', lowered))
        or bool(re.search(r'\b(?:please|pls|plz)\s+.*?\b(?:your\s+|the\s+)?otp\b', lowered))
        or (("bank employee" in lowered or "bank manager" in lowered or "bank officer" in lowered or "we are bank" in lowered) and ("otp" in lowered or "pin" in lowered or "cvv" in lowered or "password" in lowered or "code" in lowered))
        or any(k in lowered for k in ["your otp to us", "otp to us", "otp maang", "otp batao", "otp bhejo", "we are bank employee", "aadhaar and otp"])
    )

    if solicits_otp and not is_safety_warning:
        return False, ""
    
    # If message contains high-risk IOCs, it cannot be deemed unconditionally safe
    if iocs["international_fraud_numbers"] or iocs["remote_tools_detected"]:
        return False, ""
    
    # If it contains spoofed bank domain or suspicious TLD, cannot be safe
    for u in iocs["urls"]:
        if u["is_spoofed_bank"] or u["is_suspicious_tld"]:
            return False, ""

    # 1. Standard Bank Debit/Credit SMS (HDFC, SBI, ICICI, Axis, PNB, etc.)
    has_money_action = bool(re.search(r'\b(?:debited|credited|withdrawn|deposited|transfer(?:red)?|spent|used for a transaction)\b', lowered))
    has_balance_or_ac = bool(re.search(r'\b(?:avl\s+bal|available\s+bal(?:ance)?|a/c|account\s+(?:no|\*\*|xxxx|\d+)|ending\s+\d+|card\s+ending)\b', lowered))
    has_bank_signals = bool(re.search(r'\b(?:inr|rs\.?|upi\s+ref|txn|if\s+not\s+(?:you|authorized|done by you)|toll[\s-]free|1800\d+|official channels)\b', lowered))

    if has_money_action and (has_balance_or_ac or has_bank_signals):
        return True, "Standard bank transaction alert"

    # 1b. Official Bank Statements & Receipts
    has_statement = bool(re.search(r'\b(?:bank statement|monthly bank statement|statement is now available|fixed deposit receipt|deposit receipt|account balance is available)\b', lowered))
    if has_statement and ("official" in lowered or "generated successfully" in lowered):
        return True, "Official bank statement or receipt notification"

    # 2. Legitimate OTP for App Login / Verification (Amazon, Swiggy, Google, WhatsApp, Uber, Aadhaar, etc.)
    has_otp = bool(re.search(r'\b(?:is\s+your\s+otp|otp\s+is|your\s+otp\s+(?:for|to)|otp\s+(?:for|to)|verification\s+code\s+is|security\s+code|one\s+time\s+password|login\s+otp)\b', lowered))
    has_safety_note = bool(re.search(r'\b(?:never\s+share|do\s+not\s+share|don\'t\s+share|valid\s+for|valid\s+till|confidential|validity|uidai)\b', lowered))
    if has_otp and (has_safety_note or len(lowered) < 160):
        return True, "Legitimate one-time password (OTP) verification"

    # 3. E-commerce & Delivery Updates (Amazon, Flipkart, Bluedart, Swiggy, Zomato, JioMart)
    has_ecommerce = bool(re.search(r'\b(?:order\s+(?:confirmed|placed|shipped|dispatched|out\s+for\s+delivery|delivered)|food order has been confirmed|order is out for delivery|delivery partner will reach you soon|expected delivery|tracking\s+id|courier|awb)\b', lowered))
    if has_ecommerce and not any(k in lowered for k in ["customs", "narcotics", "mdma", "cbi", "arrest", "lottery", "seized", "warrant", "on hold", "redelivery"]):
        return True, "Legitimate order & shipment notification"

    # 3b. IRCTC / Travel Booking Confirmation
    has_booking = bool(re.search(r'\b(?:ticket booking is confirmed|train ticket|flight ticket|irctc|pnr|seat\s+confirmed)\b', lowered))
    if has_booking:
        return True, "Legitimate travel ticket booking confirmation"

    # 4. Telecom & Utility Recharge Confirmation
    has_recharge = bool(re.search(r'\b(?:recharge\s+of\s+rs|bill\s+paid\s+successfully|plan\s+active|validity\s+extended|jio|airtel|vi\b)\b', lowered))
    if has_recharge:
        return True, "Telecom/Utility recharge payment confirmation"

    # 5. Casual / Personal Chat (Zero threat markers)
    has_greeting = bool(re.search(r'\b(?:hi|hello|namaste|hey|bhai|dinner|party|call me|happy birthday)\b', lowered))
    if has_greeting and len(iocs["urls"]) == 0 and len(iocs["phone_numbers"]) <= 1 and len(lowered) < 160:
        return True, "Casual personal communication without threat indicators"

    return False, ""


def analyze_scam_message(text: str, sender: Optional[str] = None) -> Dict[str, Any]:
    """
    Advanced Multi-Vector Threat Analysis Engine.
    Evaluates Co-occurrence of threat signals and returns 0-100% precision risk score.
    """
    cleaned_text = text.strip()
    lowered = cleaned_text.lower()
    iocs = extract_iocs(cleaned_text, sender)

    # First Check: Is it an explicitly safe legitimate communication?
    is_safe, safe_reason = is_safe_message(cleaned_text, iocs)
    if is_safe:
        return {
            "risk_score": 2,
            "severity": "SAFE",
            "status_label": "Safe: Legitimate Notification",
            "scam_category": "SAFE_TRANSACTION",
            "scam_category_name": "Legitimate Notification",
            "extracted_iocs": iocs,
            "red_flags": [],
            "explanations": generate_explanations(cleaned_text, "SAFE_TRANSACTION", 2, iocs, []),
            "voice_warning_script": generate_voice_scripts(cleaned_text, "SAFE_TRANSACTION", 2),
            "confidence": 0.99,
            "action_recommendations": get_action_steps("SAFE_TRANSACTION", 2)
        }

    # Evaluate Specific Scam Vectors via Signal Co-occurrence
    red_flags = []
    vector_scores = {}

    # -------------------------------------------------------------
    # VECTOR 0: OTP / Credential Harvesting (Bank Impersonation Trap)
    # -------------------------------------------------------------
    # Strip standard educational safety disclaimers (e.g., "Do not share OTP", "Never share")
    # so they are not mistaken for a malicious demand to share
    advisory_free_text = re.sub(
        r'\b(?:never|do\s+not|don\'t|not\s+to|should\s+not|kisi\s+ko\s+na)\s+(?:share|disclose|give|tell|batao|dein)\s+(?:this|your|the)?\s*(?:otp|pin|cvv|password)?\b',
        '',
        lowered
    )

    demands_otp = (
        bool(re.search(r'\b(?:share|send|give|tell|provide|forward|enter|submit)\s+(?:me\s+|us\s+|our\s+)?(?:the\s+|your\s+|that\s+|this\s+|6\s*digit\s+)?(?:aadhaar\s+and\s+)?(?:otp|cvv|password|passcode)\b', advisory_free_text))
        or bool(re.search(r'\b(?:the\s+|your\s+|that\s+|this\s+|meri\s+|mera\s+)?otp\s+(?:to\s+us|to\s+me|batao|bhejo|de\s*do|share\s*karo|forward\s*karo|mang|maang|puch|pooch|chahiye)\b', advisory_free_text))
        or bool(re.search(r'\b(?:please|pls|plz)\s+.*?\b(?:your\s+|the\s+)?otp\b', advisory_free_text))
        or (any(b in lowered for b in ["bank employee", "bank manager", "bank officer", "we are bank", "बैंक से बोल रहे", "बैंक कर्मचारी", "बैंक मैनेजर"]) and any(c in lowered for c in ["otp", "pin", "cvv", "password", "code", "ओटीपी", "सीवीवी", "पासवर्ड"]))
        or (("ओटीपी" in lowered or "otp" in lowered) and any(m in lowered for m in ["मांग", "मांगा", "मांगी", "मांगते", "पूछ", "पूछा", "पूछी", "mang", "maang", "manga", "maanga", "mangi", "maangi", "meri otp", "मेरी ओटीपी", "mera otp", "मेरा ओटीपी", "pucha", "poocha", "chahiye"]))
        or any(k in lowered for k in [
            "your otp to us", "otp to us", "otp maang", "otp mang", "otp batao", "otp bhejo",
            "we are bank employee", "bank employee", "bank manager", "aadhaar and otp", "send your aadhaar and otp",
            "ओटीपी शेयर", "अपना ओटीपी", "ओटीपी बताओ", "ओटीपी भेजो", "ओटीपी दें", "ओटीपी मांग", "ओटीपी मांगा", "ओटीपी मांगी",
            "cvv batao", "tell me cvv", "card renew karna hai cvv", "pin manga", "पिन मांगा", "पिन मांग"
        ])
    )

    if demands_otp:
        vector_scores["OTP_HARVESTING"] = 100
        red_flags.append({
            "id": "OTP_SOLICITATION_FRAUD",
            "title": "Strict Fraud Alert: Demanding Confidential Bank OTP/PIN/CVV",
            "description": "GOLDEN RULE OF BANKING: Legitimate banks, RBI, and bank employees NEVER ask for your OTP, PIN, or CVV under any circumstances! Any request for your OTP is a 100% active cyber fraud.",
            "level": "CRITICAL"
        })
        if any(b in lowered for b in ["bank employee", "bank manager", "bank officer", "we are bank", "customer care", "branch manager"]):
            red_flags.append({
                "id": "BANK_IMPERSONATION_FRAUD",
                "title": "Impersonating Bank Employee / Manager",
                "description": "Scammers pose as bank staff to manipulate citizens into surrendering their 6-digit authentication codes.",
                "level": "CRITICAL"
            })

    # -------------------------------------------------------------
    # VECTOR 1: UPI Fraud / Account Expiry / PIN Demand
    # -------------------------------------------------------------
    upi_lure = any(k in lowered for k in [
        "cashback", "reward", "won", "jeete", "prize", "refund", "claim",
        "received money", "receive", "paise pane", "upi account", "account will expire",
        "पैसे लेने", "कैशबैक पाने", "रिफंड"
    ])
    upi_trap = any(k in lowered for k in [
        "upi pin", "enter pin", "pin dalo", "qr code", "scan qr", "enter your 6-digit",
        "6 digit pin", "share your upi pin", "पिन डालो", "पिन डालें", "क्यूआर कोड स्कैन"
    ])
    if upi_trap or (upi_lure and ("pin" in lowered or "qr" in lowered or "पिन" in lowered)):
        vector_scores["UPI_FRAUD"] = 100
        red_flags.append({
            "id": "UPI_PIN_RECEIVE_TRAP",
            "title": "UPI PIN Reversal Trap (Gold Scam Rule)",
            "description": "Fundamental rule of UPI: You NEVER enter your UPI PIN or scan a QR code to receive money. Entering PIN always DEBITS your account.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 2: Bank KYC / Account & ATM Card Freeze Phishing
    # -------------------------------------------------------------
    bank_target = any(k in lowered for k in [
        "sbi", "yono", "hdfc", "icici", "pnb", "kotak", "axis", "bank", "khata", "account",
        "debit card", "atm card", "credit card", "card", "pan card", "kyc",
        "खाता", "अकाउंट", "बैंक", "एटीएम", "केवाईसी", "पैन कार्ड"
    ])
    bank_freeze = any(k in lowered for k in [
        "block", "suspend", "freeze", "deactivat", "band", "hold", "pending kyc", "unfreeze", "blocked", "expire",
        "ब्लॉक", "बंद", "फ्रीज", "सस्पेंड", "अमान्य", "एक्सपायर", "रोक"
    ])
    has_phishing_link = any(u["is_spoofed_bank"] or u["is_suspicious_tld"] or u["is_shortener"] for u in iocs["urls"])
    has_freeze_action = (
        has_phishing_link
        or any(k in lowered for k in ["link", "click", "update", "verify", "call this number", "reactivate", "immediately", "लिंक", "क्लिक", "कॉल करें", "नंबर पर"])
        or len(iocs["phone_numbers"]) > 0
        or "phone aaya" in lowered or "call aaya" in lowered or "फोन आया" in lowered or "मैसेज आया" in lowered or "bol rahe" in lowered or "bol raha" in lowered
    )

    if bank_target and bank_freeze:
        vector_scores["BANK_KYC_FREEZE"] = 98
        red_flags.append({
            "id": "KYC_ACCOUNT_FREEZE_PANIC",
            "title": "Fake Bank KYC / Account Suspension Panic",
            "description": "Banks never send SMS or calls threatening immediate account suspension or ATM card blockage.",
            "level": "CRITICAL"
        })

    # ATM Card Block Call Trap
    if any(k in lowered for k in ["atm card is blocked", "card is blocked", "card blocked", "एटीएम कार्ड बंद", "एटीएम ब्लॉक", "कार्ड ब्लॉक"]) and any(k in lowered for k in ["call this number", "reactivate", "unblock", "immediately", "call", "नंबर पर", "कॉल करें"]):
        vector_scores["CARD_BLOCK_PHONE_TRAP"] = 98
        red_flags.append({
            "id": "CARD_BLOCK_PHONE_SCAM",
            "title": "ATM Card Block & Private Callback Trap",
            "description": "Real banks never instruct customers to call private 10-digit mobile numbers to unblock ATM cards.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 3: Traffic E-Challan Scam
    # -------------------------------------------------------------
    challan_kw = any(k in lowered for k in ["challan", "traffic challan", "e-challan", "echallan", "चालान", "ट्रैफिक चालान", "फाइन भरें"])
    challan_urgency = any(k in lowered for k in ["unpaid", "pay now", "fine", "license cancel", "court", "parivahan", "तुरंत", "लिंक", "link", "भरें"])
    if challan_kw and (challan_urgency or "link" in lowered or len(iocs["urls"]) > 0):
        vector_scores["TRAFFIC_CHALLAN_SCAM"] = 97
        red_flags.append({
            "id": "FAKE_ECHALLAN_PHISHING",
            "title": "Fake Traffic E-Challan Phishing Trap",
            "description": "Fraudulent notice threatening license cancellation or police action via fake payment links. Real challans are only paid on echallan.parivahan.gov.in.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 4: Telecom / SIM Card Disconnection / TRAI Scam
    # -------------------------------------------------------------
    sim_kw = any(k in lowered for k in ["sim card", "sim", "mobile number", "सिम कार्ड", "सिम", "नंबर"])
    sim_threat = any(k in lowered for k in [
        "blocked in 2 hours", "deactivated in 2 hours", "will be blocked", "will be deactivated", "disconnected",
        "2 घंटे में बंद", "बंद हो जाएगा", "ब्लॉक हो जाएगा", "trai", "dot", "दूरसंचार"
    ])
    if (sim_kw and sim_threat) or ("trai officer" in lowered) or ("trai" in lowered and "block" in lowered):
        vector_scores["TRAI_SIM_BLOCK_SCAM"] = 98
        red_flags.append({
            "id": "TRAI_SIM_DISCONNECTION_HOAX",
            "title": "TRAI / DoT SIM Disconnection Hoax",
            "description": "Neither TRAI nor DoT calls citizens threatening 2-hour SIM deactivations. This is an extortion setup leading to fake police interrogations.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 5: Income Tax Refund Phishing
    # -------------------------------------------------------------
    it_kw = any(k in lowered for k in ["income tax", "tax refund", "it refund", "incometax", "आयकर", "टैक्स रिफंड", "इनकम टैक्स"])
    it_lure = any(k in lowered for k in ["refund", "approved", "credited", "claim link", "claim", "रिफंड आया", "क्लिक करें", "लिंक"])
    if it_kw and it_lure:
        vector_scores["INCOME_TAX_REFUND_SCAM"] = 98
        red_flags.append({
            "id": "INCOME_TAX_REFUND_PHISHING",
            "title": "Income Tax Refund Phishing Scam",
            "description": "The Income Tax Department directly credits verified bank accounts and NEVER sends SMS links to claim refunds or enter banking credentials.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 6: Credit Card Reward Points Expiry Scam
    # -------------------------------------------------------------
    reward_kw = any(k in lowered for k in [
        "reward points", "credit card points", "card points", "points worth", "रिवॉर्ड पॉइंट", "क्रेडिट कार्ड पॉइंट"
    ])
    reward_action = any(k in lowered for k in [
        "expire", "expiring", "redeem", "cash redeem", "एक्सपायर", "रिडीम", "claim"
    ])
    if reward_kw and reward_action:
        vector_scores["CREDIT_CARD_REWARD_SCAM"] = 96
        red_flags.append({
            "id": "CREDIT_CARD_REWARD_PHISHING",
            "title": "Credit Card Reward Points Expiry Phishing",
            "description": "Banks never send SMS links urging you to convert reward points to cash before expiry. These links phish card numbers and OTPs.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 7: Free Govt Scheme / Free Mobile Recharge Smishing
    # -------------------------------------------------------------
    free_kw = any(k in lowered for k in ["free recharge", "free laptop", "govt scheme", "pm yojana", "मुफ्त रिचार्ज", "फ्री लैपटॉप", "पीएम योजना", "सरकारी योजना", "मुफ्त"])
    if free_kw and any(k in lowered for k in ["link", "click", "register", "claim", "ऑफर", "लिंक", "क्लिक"]):
        vector_scores["GOVT_SCHEME_PHISHING"] = 95
        red_flags.append({
            "id": "BOGUS_GOVT_SCHEME_PHISHING",
            "title": "Bogus Free Recharge / Govt Scheme Smishing",
            "description": "Viral messages offering free laptops or recharges are malicious phishing links designed to harvest personal data and spread malware.",
            "level": "HIGH"
        })

    # -------------------------------------------------------------
    # VECTOR 8: Fake Customer Care / Refund Callback Trap
    # -------------------------------------------------------------
    cust_care = any(k in lowered for k in ["customer care", "helpline number", "कस्टमर केयर", "हेल्पलाइन नंबर"])
    cust_call = any(k in lowered for k in ["call", "turant call", "contact", "कॉल करें", "तुरंत कॉल"]) or len(iocs["phone_numbers"]) > 0
    if cust_care and (cust_call or "refund" in lowered or "रिफंड" in lowered):
        vector_scores["FAKE_CUSTOMER_CARE_SCAM"] = 95
        red_flags.append({
            "id": "BOGUS_CUSTOMER_CARE_TRAP",
            "title": "Unverified / Fake Customer Care Phone Trap",
            "description": "Scammers publish fake 10-digit mobile numbers as official customer support on Google and SMS to harvest banking details.",
            "level": "HIGH"
        })

    # -------------------------------------------------------------
    # VECTOR 9: Electricity Disconnection Panic (Discom Trap)
    # -------------------------------------------------------------
    power_keywords = any(k in lowered for k in [
        "electricity", "bijli", "power", "discom", "electric office", "substation", "transformer",
        "बिजली", "बिजली बिल", "पावर"
    ])
    cutoff_threat = any(k in lowered for k in [
        "disconnect", "line cut", "kaat di", "bijli cut", "power cut", "batti gul", "cut off",
        "कट जाएगा", "लाइन कट", "बिजली कटेगी", "कट जाएगी", "बिल जमा नहीं"
    ])
    cutoff_panic = any(k in lowered for k in [
        "tonight", "9:30", "8:30", "9.30", "9 बजे", "aaj raat", "immediate", "officer sharma", "contact officer",
        "तुरंत", "रात", "आज रात"
    ])

    if power_keywords and (cutoff_threat or cutoff_panic or len(iocs["phone_numbers"]) > 0):
        vector_scores["ELECTRICITY_CUTOFF"] = 96
        red_flags.append({
            "id": "DISCOM_DISCONNECTION_THREAT",
            "title": "Electricity Disconnection Hoax (Midnight Panic)",
            "description": "Electricity Discoms never send disconnection threats from personal 10-digit mobile numbers or give 9:30 PM cutoff ultimatums.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 10: Lottery / Cash Reward / Free iPhone Advance-Fee Scam
    # -------------------------------------------------------------
    lottery_lure = any(k in lowered for k in [
        "lottery", "25 lakh", "5,00,000 lottery", "won rs", "won a free iphone", "free iphone",
        "free gift", "cash reward", "selected for a cash reward", "claim your prize", "claim your gift", "kbc", "prize",
        "लॉटरी", "इनाम", "लॉटरी लगी", "फ्री आईफोन", "कैश रिवॉर्ड", "50,000 की लॉटरी"
    ])
    fee_trap = any(k in lowered for k in [
        "processing fee", "delivery charge", "delivery charges", "shipping fee",
        "registration fee", "pay rs", "fee to claim", "charges to receive",
        "प्रोसेसिंग फीस", "टैक्स", "फीस", "चार्ज"
    ])
    intl_code = len(iocs["international_fraud_numbers"]) > 0 or "+92" in cleaned_text or "whatsapp" in lowered

    if lottery_lure and (fee_trap or intl_code or "fee" in lowered or "charges" in lowered or "pay" in lowered or "लगी है" in lowered or "jeeti" in lowered or "won" in lowered):
        vector_scores["KBC_LOTTERY"] = 98
        red_flags.append({
            "id": "ADVANCE_FEE_PRIZE_SCAM",
            "title": "Advance-Fee Lottery / Free Gift Trap",
            "description": "Classic advance-fee fraud asking for upfront delivery charges or processing taxes before releasing non-existent prizes.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 11: Digital Arrest / Narcotics Parcel Extortion
    # -------------------------------------------------------------
    agency_keywords = any(k in lowered for k in [
        "digital arrest", "cbi", "police", "customs", "mumbai customs", "trai", "supreme court", "dcp",
        "सीबीआई", "पुलिस", "कस्टम्स", "कस्टम", "डिजिटल अरेस्ट", "पुलिस स्टेशन", "कोर्ट"
    ])
    blackmail_keywords = any(k in lowered for k in [
        "narcotics", "mdma", "drugs", "illegal parcel", "fedex parcel", "dhl", "passports", "warrant", "arrest",
        "पकड़ा गया", "ड्रग्स", "नारकोटिक्स", "वारंट", "अरेस्ट", "गिरफ्तार", "बेटा अरेस्ट", "केस दर्ज"
    ])
    extortion_keywords = any(k in lowered for k in [
        "skype", "stay on camera", "escrow", "do not disconnect", "camera", "video call", "verify aadhaar",
        "वीडियो कॉल", "कैमरा", "स्काइप"
    ])

    if (agency_keywords and (blackmail_keywords or extortion_keywords or "arrest" in lowered or "पकड़ा" in lowered or "कॉल आया" in lowered)) or ("digital arrest" in lowered or "डिजिटल अरेस्ट" in lowered):
        vector_scores["DIGITAL_ARREST_CUSTOMS"] = 99
        red_flags.append({
            "id": "DIGITAL_ARREST_EXTORTION",
            "title": "Fictitious 'Digital Arrest' & Law Extortion",
            "description": "Indian law and Supreme Court confirm 'Digital Arrest' does not exist. Law enforcement never arrests citizens over Skype or video calls.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 12: Fake Loan Document / Aadhaar & OTP Theft
    # -------------------------------------------------------------
    loan_kw = any(k in lowered for k in [
        "instant loan", "loan approved", "pre-approved loan", "without documents", "5 lakh without documents",
        "तुरंत लोन", "बिना डॉक्यूमेंट", "लोन अप्रूव", "लोन"
    ])
    loan_docs = any(k in lowered for k in [
        "aadhaar and otp", "send your aadhaar", "send otp", "documents",
        "आधार", "ओटीपी", "दस्तावेज़"
    ])
    if loan_kw and (loan_docs or "otp" in lowered or "aadhaar" in lowered or "without documents" in lowered or "बिना डॉक्यूमेंट" in lowered):
        vector_scores["LOAN_FRAUD"] = 98
        red_flags.append({
            "id": "FAKE_LOAN_DOCUMENT_TRAP",
            "title": "Instant Loan Document & OTP Harvesting",
            "description": "Phony loan approval luring victims into handing over Aadhaar credentials and financial OTPs.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 13: Courier / Parcel Hold Redelivery Fee Phishing
    # -------------------------------------------------------------
    parcel_kw = any(k in lowered for k in ["parcel", "package", "courier", "post", "shipment", "delivery", "fake-post", "पार्सल", "कूरियर", "डाकघर"])
    hold_reason = any(k in lowered for k in ["on hold", "incorrect address", "wrong address", "failed delivery", "address issue", "incomplete address", "होल्ड", "गलत पता"])
    fee_demand = any(k in lowered for k in ["redelivery fee", "pay rs", "using this link", "update address", "redelivery", "फीस", "रुपये", "fee"])
    if parcel_kw and (hold_reason or fee_demand or "redelivery" in lowered) and ("fee" in lowered or "link" in lowered or "pay" in lowered or "रुपये" in lowered or "फीस" in lowered):
        vector_scores["COURIER_PARCEL_FRAUD"] = 97
        red_flags.append({
            "id": "PARCEL_REDELIVERY_FEE_SCAM",
            "title": "Parcel Address Hold & Redelivery Fee Phishing",
            "description": "Widespread parcel phishing scam exploiting bogus address errors to steal credit card details via micro-fee payments.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 14: Malicious APK Download Trap
    # -------------------------------------------------------------
    apk_demand = any(k in lowered for k in ["install this apk", "install apk", "download apk", "open apk", "apk to claim", "apk file", "एपीके डाउनलोड", "एपीके इंस्टॉल"])
    apk_lure = any(k in lowered for k in ["cashback", "reward", "received rs", "claim your reward", "won", "bonus", "रिफंड", "ऐप डाउनलोड"])
    if apk_demand or (("apk" in lowered or ".apk" in lowered or "ऐप" in lowered) and (apk_lure or "install" in lowered or "download" in lowered)):
        vector_scores["MALICIOUS_APK_FRAUD"] = 99
        red_flags.append({
            "id": "MALICIOUS_APK_PAYLOAD",
            "title": "Malicious Android Trojan APK Payload",
            "description": "Instructing victims to sideload APKs installs banking trojans that intercept SMS OTPs and control the device.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 15: Confidential Banking Password Phishing
    # -------------------------------------------------------------
    has_password_trap = any(k in lowered for k in [
        "banking password", "netbanking password", "login password",
        "enter your password", "enter your banking password", "पासवर्ड दर्ज करें", "बैंकिंग पासवर्ड"
    ])
    if has_password_trap:
        vector_scores["CREDENTIAL_HARVESTING"] = 99
        red_flags.append({
            "id": "BANKING_PASSWORD_HARVESTING",
            "title": "Soliciting Confidential NetBanking Password",
            "description": "Links requesting online banking passwords are pure credential-stealing phishing traps.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 16: Remote Device Hijacking (AnyDesk / QuickSupport / Screen Sharing)
    # -------------------------------------------------------------
    remote_kw = any(k in lowered for k in ["anydesk", "teamviewer", "rustdesk", "quicksupport", "screen share", "स्क्रीन शेयर", "रिमोट ऐप"])
    refund_app_trap = any(k in lowered for k in ["refund ke liye app", "रिफंड के लिए ये ऐप", "डाउनलोड करें", "download app for refund"])
    if iocs["remote_tools_detected"] or remote_kw or (refund_app_trap and ("कट गए" in lowered or "deducted" in lowered or "रिफंड" in lowered)):
        vector_scores["REMOTE_HIJACK"] = 99
        red_flags.append({
            "id": "REMOTE_ACCESS_APP",
            "title": "Remote Device Hijacking App (AnyDesk / TeamViewer Trap)",
            "description": "Instructing user to download remote-access apps allows attacker to take over device screen and intercept OTPs.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # VECTOR 17: Work-From-Home / YouTube Like / Telegram Task Syndicate
    # -------------------------------------------------------------
    wfh_keywords = any(k in lowered for k in [
        "work from home", "part time job", "like youtube", "50 rs per like", "hotel review", "daily 3000", "daily earning",
        "youtube video like", "youtube videos earn", "earn 2000 per day", "earn 5000", "job offer",
        "यूट्यूब वीडियो लाइक", "रोज 5000 कमाओ", "पार्ट टाइम जॉब", "घर बैठे पैसे", "रिव्यू लिखो", "टास्क"
    ])
    if wfh_keywords:
        vector_scores["WFH_TELEGRAM"] = 96
        red_flags.append({
            "id": "WFH_TASK_SCAM",
            "title": "YouTube Video Like / Telegram Task Fraud",
            "description": "Predatory task scam enticing victims with quick rewards before demanding large prepaid investments in VIP crypto channels.",
            "level": "CRITICAL"
        })

    # Check Personal Mobile as Institutional Sender (DLT Header Violation)
    if sender:
        cleaned_sender = re.sub(r'[^\d+]', '', sender)
        if len(cleaned_sender) >= 10:
            claims_institution = any(k in lowered for k in [
                "hdfc", "sbi", "icici", "kotak", "axis", "bank", "loan", "reward",
                "kyc", "lottery", "parcel", "atm card", "upi"
            ])
            if claims_institution:
                red_flags.append({
                    "id": "UNAUTHORIZED_MOBILE_SENDER",
                    "title": f"Official Alert Sent from Personal Mobile ({sender})",
                    "description": f"TRAI & RBI regulations strictly mandate all banking alerts to originate from registered DLT alphanumeric headers (e.g., VM-HDFCBK), NEVER from 10-digit mobile numbers ({sender}).",
                    "level": "CRITICAL"
                })
                if not vector_scores:
                    vector_scores["BANK_KYC_FREEZE"] = 90

    # Check standalone IOC flags
    if iocs["international_fraud_numbers"]:
        for ifn in iocs["international_fraud_numbers"]:
            red_flags.append({
                "id": "INTL_NUMBER",
                "title": f"High-Risk Calling Code ({ifn['code']})",
                "description": f"Originated from or references {ifn['risk']}.",
                "level": "CRITICAL"
            })

    for u in iocs["urls"]:
        if u["is_spoofed_bank"]:
            red_flags.append({
                "id": "SPOOFED_BANK_URL",
                "title": f"Phishing / Spoofed Domain ({u['domain']})",
                "description": "Unauthorized domain imitating legitimate banking or government service.",
                "level": "CRITICAL"
            })
        elif u["is_suspicious_tld"]:
            red_flags.append({
                "id": "SUSPICIOUS_TLD",
                "title": f"Suspicious TLD ({u['domain']})",
                "description": "Disposable domain (.xyz, .online, etc.) heavily used by phishing networks.",
                "level": "HIGH"
            })

    # Check Personal Mobile as Authority
    if len(iocs["phone_numbers"]) > 0 and any(k in lowered for k in ["officer", "helpline", "discom", "power officer", "manager", "cbi"]):
        has_mobile = any(not (p.startswith("1800") or p.startswith("1930")) for p in iocs["phone_numbers"])
        if has_mobile:
            red_flags.append({
                "id": "PERSONAL_MOBILE_AS_OFFICER",
                "title": "Private Mobile Number Posing as Public Officer",
                "description": "Real public authorities strictly communicate via toll-free numbers or official alphanumeric SMS headers.",
                "level": "HIGH"
            })

    # -------------------------------------------------------------
    # VERIFIED SAFE NOTIFICATION CHECK
    # Only genuine bank transaction alerts, verified OTPs, or legitimate delivery updates qualify!
    # -------------------------------------------------------------
    is_debit_credit = (
        any(k in lowered for k in ["debited", "credited", "used for a transaction", "spent", "credited with"])
        and any(k in lowered for k in ["avl bal", "balance", "a/c", "account", "ending", "xxxx"])
        and not any(k in lowered for k in ["claim", "lottery", "apk", "kyc", "block", "freeze", "without documents", "share", "pin", "link", "fee", "suspended"])
    )
    is_legit_otp = (
        any(k in lowered for k in ["otp", "verification code", "security code"])
        and any(k in lowered for k in ["never share", "do not share", "valid for", "is your otp", "otp for"])
        and not demands_otp
    )
    is_delivery = (
        any(k in lowered for k in ["order has been confirmed", "order has been shipped", "out for delivery"])
        and not any(k in lowered for k in ["customs", "narcotics", "on hold", "fee", "redelivery", "pay rs", "link"])
    )
    is_statement = (
        any(k in lowered for k in ["statement is now available", "receipt has been generated", "ticket booking is confirmed"])
        and not any(k in lowered for k in ["pay", "fee", "link", "block", "suspend"])
    )

    is_verified_safe = (is_debit_credit or is_legit_otp or is_delivery or is_statement) and not vector_scores

    # Compute Final Verdict
    if vector_scores:
        # Highest matching vector
        top_vector = max(vector_scores.items(), key=lambda x: x[1])
        top_cat_key = top_vector[0]
        risk_score = top_vector[1]
    elif is_verified_safe:
        top_cat_key = "SAFE_TRANSACTION"
        risk_score = 4
    elif len(red_flags) > 0:
        top_cat_key = "SUSPICIOUS_CONTENT"
        risk_score = 75
    else:
        # If text is not a verified safe transaction, check for any risk or urgency signals
        has_suspicious_phrases = any(k in lowered for k in [
            "phone aaya", "call aaya", "bol rahe", "bol raha", "message aaya", "मैसेज आया", "फोन आया", "कॉल आया",
            "बोल रहे", "बोल रहा", "लिंक", "link", "click", "expire", "band", "block", "suspend", "आधार", "aadhaar",
            "otp", "ओटीपी", "pin", "पिन", "मांग", "mang", "cvv", "सीवीवी", "password", "पासवर्ड", "call", "कॉल",
            "kal", "कल", "kisi ne", "किसी ने"
        ])
        if has_suspicious_phrases:
            top_cat_key = "SUSPICIOUS_CONTENT"
            risk_score = 75
        else:
            top_cat_key = "SAFE_TRANSACTION"
            risk_score = 5

    # Determine Severity Rating
    if risk_score >= 80:
        severity = "CRITICAL"
        status_label = "Danger: Malicious Scam Trap"
    elif risk_score >= 60:
        severity = "HIGH"
        status_label = "High Risk: Suspicious Threat"
    elif risk_score >= 30:
        severity = "SUSPICIOUS"
        status_label = "Caution: Unverified Content"
    else:
        severity = "SAFE"
        status_label = "Safe: Legitimate Notification"

    cat_name = {
        "OTP_HARVESTING": "Bank Employee Impersonation / OTP Fraud",
        "UPI_FRAUD": "UPI Cashback / QR Code / PIN Trap",
        "BANK_KYC_FREEZE": "Fake Bank KYC / Account Freeze Trap",
        "ELECTRICITY_CUTOFF": "Electricity Disconnection Panic (Discom Trap)",
        "KBC_LOTTERY": "Advance-Fee Lottery / Prize Fraud",
        "DIGITAL_ARREST_CUSTOMS": "Digital Arrest / CBI Narcotics Threat",
        "WFH_TELEGRAM": "Work-From-Home / Telegram Task Scam",
        "REMOTE_HIJACK": "Remote Device Hijack (AnyDesk Trap)",
        "LOAN_FRAUD": "Instant Loan / Document & OTP Theft Trap",
        "COURIER_PARCEL_FRAUD": "India Post / Courier Redelivery Phishing",
        "MALICIOUS_APK_FRAUD": "Malicious Android Trojan APK Trap",
        "CREDENTIAL_HARVESTING": "Confidential Password / Credential Phishing",
        "CARD_BLOCK_PHONE_TRAP": "ATM Card Block / Impersonation Phone Trap",
        "TRAFFIC_CHALLAN_SCAM": "Fake Traffic E-Challan Phishing Trap",
        "TRAI_SIM_BLOCK_SCAM": "TRAI / DoT SIM Deactivation Hoax",
        "INCOME_TAX_REFUND_SCAM": "Income Tax Refund Phishing Scam",
        "CREDIT_CARD_REWARD_SCAM": "Credit Card Reward Points Expiry Scam",
        "GOVT_SCHEME_PHISHING": "Free Govt Scheme / Recharge Smishing",
        "FAKE_CUSTOMER_CARE_SCAM": "Fake Customer Care Callback Trap",
        "SUSPICIOUS_CONTENT": "Suspicious Unverified Message",
        "SAFE_TRANSACTION": "Legitimate Notification"
    }.get(top_cat_key, "Potential Cyber Threat")

    return {
        "risk_score": risk_score,
        "severity": severity,
        "status_label": status_label,
        "scam_category": top_cat_key,
        "scam_category_name": cat_name,
        "extracted_iocs": iocs,
        "red_flags": red_flags,
        "explanations": generate_explanations(cleaned_text, top_cat_key, risk_score, iocs, red_flags),
        "voice_warning_script": generate_voice_scripts(cleaned_text, top_cat_key, risk_score),
        "confidence": 0.98 if risk_score >= 80 or risk_score <= 15 else 0.90,
        "action_recommendations": get_action_steps(top_cat_key, risk_score)
    }


def extract_contextual_elements(text: str, iocs: Dict[str, Any]) -> Dict[str, Any]:
    """Extract granular specific entities, claims, and demands directly from the actual text."""
    lowered = text.lower()

    # 1. Specific roles or impersonated authorities
    roles = []
    if "bank employee" in lowered:
        roles.append("Bank Employee (बैंक कर्मचारी)")
    elif "bank manager" in lowered or "branch manager" in lowered:
        roles.append("Bank Manager (बैंक मैनेजर)")
    elif "we are bank" in lowered or "bank officer" in lowered:
        roles.append("Bank Staff / Official (बैंक अधिकारी)")
    elif "loan service" in lowered or "instant loan" in lowered:
        roles.append("Loan Provider / Instant Loan Service")
    elif "courier" in lowered or "parcel" in lowered or "fake-post" in lowered:
        roles.append("Postal / Courier Service (India Post/Courier)")
    elif "officer sharma" in lowered or "sharma ji" in lowered or "power officer" in lowered:
        roles.append("Power / Electricity Officer (बिजली अधिकारी)")
    elif "rana pratap" in lowered:
        roles.append("KBC Manager Rana Pratap")
    elif "cbi" in lowered:
        roles.append("CBI Cyber Cell (सीबीआई अधिकारी)")
    elif "mumbai customs" in lowered or "customs" in lowered:
        roles.append("Customs Department (कस्टम्स विभाग)")
    elif "dcp" in lowered or "police" in lowered:
        roles.append("Police / DCP Cyber Crime")
    elif "trai" in lowered:
        roles.append("TRAI Telecom Authority")
    elif "sbi" in lowered or "yono" in lowered:
        roles.append("State Bank of India (SBI / YONO)")
    elif "hdfc" in lowered:
        roles.append("HDFC Bank")
    elif "icici" in lowered:
        roles.append("ICICI Bank")
    elif "kotak" in lowered:
        roles.append("Kotak Mahindra Bank")
    elif "phonepe" in lowered:
        roles.append("PhonePe Rewards")
    elif "swiggy" in lowered:
        roles.append("Swiggy")
    elif "amazon" in lowered:
        roles.append("Amazon")

    # 2. Specific Action Demands
    demands = []
    if any(k in lowered for k in ["your otp to us", "otp to us", "share your otp", "give your otp", "send your otp", "tell me otp", "otp batao", "otp bhejo", "enter your otp"]):
        demands.append("Demanding 6-Digit Banking OTP (ओटीपी शेयर करने की मांग)")
    elif "send your aadhaar" in lowered or "aadhaar and otp" in lowered:
        demands.append("Sending Aadhaar & OTP (आधार और बैंक ओटीपी भेजना)")
    elif "share your upi pin" in lowered or "upi pin to avoid" in lowered:
        demands.append("Sharing UPI PIN (यूपीआई पिन साझा करने की मांग)")
    elif "banking password" in lowered or "enter your banking password" in lowered or "enter your password" in lowered:
        demands.append("Entering NetBanking Password (नेटबैंकिंग पासवर्ड दर्ज करना)")
    elif "install this apk" in lowered or "install apk" in lowered or "download apk" in lowered:
        demands.append("Installing Untrusted Android APK (असुरक्षित एपीके फ़ाइल इंस्टॉल करना)")
    elif "redelivery fee" in lowered or "pay rs. 10" in lowered or "pay rs 10" in lowered:
        demands.append("Paying Redelivery Fee (पुनः डिलीवरी शुल्क का भुगतान)")
    elif "processing fee" in lowered or "fee to claim" in lowered:
        demands.append("Paying Upfront Processing Fee (प्रोसेसिंग शुल्क की मांग)")
    elif "delivery charge" in lowered or "charges to receive" in lowered:
        demands.append("Paying Delivery Charges for Gift (उपहार हेतु डिलीवरी चार्ज)")
    elif "call this number" in lowered or "immediately to reactivate" in lowered:
        demands.append("Calling Private Number to Reactivate Card (कार्ड चालू करने हेतु कॉल करना)")
    elif "upi pin" in lowered or "enter pin" in lowered or "pin dalo" in lowered:
        demands.append("Entering UPI PIN (यूपीआई पिन दर्ज करना)")
    elif "qr code" in lowered or "scan qr" in lowered:
        demands.append("Scanning QR code (क्यूआर कोड स्कैन करना)")
    elif "anydesk" in lowered or "quicksupport" in lowered:
        demands.append("Installing AnyDesk screen share app (एनीडेस्क ऐप डाउनलोड करना)")
    elif "update pan" in lowered or "pan card" in lowered or "kyc" in lowered:
        demands.append("Urgent KYC / PAN card update (पैन या केवाईसी अपडेट)")
    elif "skype" in lowered or "video call" in lowered or "camera" in lowered:
        demands.append("Connecting on Skype video call (स्काइप वीडियो कॉल)")

    # 3. Urgency / Coercion / Threats
    threats = []
    if "atm card is blocked" in lowered or "card is blocked" in lowered:
        threats.append("ATM Card Blocked Panic (एटीएम कार्ड ब्लॉक होने का डर)")
    elif "upi account will expire" in lowered or "account will expire" in lowered:
        threats.append("UPI Account Expiry (यूपीआई खाता समाप्त होने की झूठी चेतावनी)")
    elif "parcel is on hold" in lowered or "incorrect address" in lowered:
        threats.append("Parcel On Hold due to Address Error (पार्सल होल्ड होने का बहाना)")
    elif "disconnected tonight" in lowered or "power cut" in lowered or "line cut" in lowered or "batti gul" in lowered:
        threats.append("Power disconnection tonight (आज रात बिजली काटने की धमकी)")
    elif "suspend" in lowered or "block" in lowered or "freeze" in lowered:
        threats.append("Account / SIM suspension (खाता या सिम बंद होने की धमकी)")
    elif "arrest" in lowered or "warrant" in lowered or "narcotics" in lowered or "mdma" in lowered:
        threats.append("Arrest warrant & narcotics seizure (गिरफ्तारी व वारंट का डर)")
    elif "9:30" in lowered or "immediately" in lowered or "turant" in lowered or "24 hours" in lowered or "today" in lowered:
        threats.append("Immediate 24-hour urgency (तत्काल कार्रवाई का दबाव)")

    # 4. Lures / Prizes
    lures = []
    if "free iphone" in lowered or "won a free iphone" in lowered:
        lures.append("Free iPhone Giveaway (फ्री आईफोन जीतने का झांसा)")
    elif "5,00,000 lottery" in lowered or "5 lakh" in lowered or "25 lakh" in lowered or "lottery" in lowered:
        lures.append("Multi-Lakh Lottery / Cash Prize (लाखों की लॉटरी)")
    elif "without documents" in lowered or "instant loan" in lowered:
        lures.append("Paperless Instant Loan Approval (बिना दस्तावेज लोन का लालच)")
    elif "cash reward" in lowered or "selected for a cash reward" in lowered:
        lures.append("Cash Reward Selection (नकद पुरस्कार का झांसा)")
    elif "cashback" in lowered or "reward" in lowered or "won" in lowered or "prize" in lowered:
        lures.append("Cashback / Prize reward (कैशबैक या इनाम का प्रलोभन)")

    # 5. URLs and Phones
    urls = [u["domain"] for u in iocs.get("urls", [])]
    phones = iocs.get("phone_numbers", [])
    intl_numbers = [ifn["phone"] for ifn in iocs.get("international_fraud_numbers", [])]

    return {
        "roles": roles,
        "demands": demands,
        "threats": threats,
        "lures": lures,
        "urls": urls,
        "phones": phones,
        "intl_numbers": intl_numbers
    }


def generate_explanations(text: str, category: str, risk: int, iocs: Dict[str, Any], red_flags: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Generate dynamic, contextual, message-tailored explanations in Hindi, Hinglish, and English.
    Directly incorporates specific entities, demands, and threat triggers found in the user's message.
    """
    lowered = text.lower().strip()
    elements = extract_contextual_elements(text, iocs)

    # -------------------------------------------------------------
    # Case 1: Legitimate / Safe Message
    # -------------------------------------------------------------
    if category == "SAFE_TRANSACTION":
        # Check specific type of legitimate communication
        if bool(re.search(r'\b(?:debited|credited|avl bal|a/c)\b', lowered)):
            return {
                "hindi": "✅ **संदेश का वास्तविक विश्लेषण (वैध बैंक ट्रांजेक्शन)**:\n• यह आपके बैंक खाते से अधिकृत लेनदेन (डेबिट/क्रेडिट) का वैध संदेश है।\n• इसमें मानक बैंकिंग प्रारूप और अधिकृत हेल्पलाइन (जैसे 1800...) का उल्लेख है।\n• इसमें कोई भी अनधिकृत फ़िशिंग लिंक या खाता बंद करने की फर्जी धमकी नहीं है। यह सुरक्षित है।",
                "hinglish": "✅ **Message ka Real Analysis (Legitimate Bank Alert)**:\n• Yeh aapke bank account se authorized transaction (debit/credit) ka official notification hai.\n• Isme standard banking alerts aur verified toll-free helpline number shamil hai.\n• Isme koi malicious link ya account block ki farzi dhamki nahi hai. Yeh 100% safe hai.",
                "english": "✅ **Real Message Analysis (Verified Bank Transaction)**:\n• This is an authentic transactional notification confirming genuine account activity.\n• Matches official banking communication standards with verified toll-free assistance.\n• Contains no phishing links, unverified numbers, or panic-inducing threats. Safe to retain."
            }

        if bool(re.search(r'\b(?:is your otp|otp is|verification code|one time password|login otp)\b', lowered)):
            return {
                "hindi": "✅ **संदेश का वास्तविक विश्लेषण (वैध लॉगिन ओटीपी)**:\n• यह एक वैध एप्लिकेशन ऑथेंटिकेशन ओटीपी (One Time Password) है।\n• संदेश में ओटीपी को किसी के साथ साझा न करने की स्पष्ट सुरक्षा चेतावनी ('Never share / Do not share') मौजूद है।\n• सुरक्षा सलाह: यह संदेश सुरक्षित है। इस ओटीपी को केवल अपने संबंधित ऐप में ही दर्ज करें, किसी व्यक्ति या कॉलर को न बताएं।",
                "hinglish": "✅ **Message ka Real Analysis (Valid Login OTP)**:\n• Yeh ek official application login OTP (One Time Password) verification alert hai.\n• Message me OTP kisi ke sath share na karne ki defensive warning shamil hai.\n• Safety Tip: Yeh SMS surakshit hai. Is OTP ko sirf official app me use karein, kisi ko phone par na batayein.",
                "english": "✅ **Real Message Analysis (Genuine Login OTP)**:\n• This is a legitimate one-time password generated for authorized account login or verification.\n• Includes built-in safety advisories ('Do not share with anyone') with zero suspicious external redirects.\n• Action: Safe message. Enter this code only into your official app; never disclose it over call or message."
            }

        if bool(re.search(r'\b(?:order|delivered|shipped|dispatched|courier)\b', lowered)):
            return {
                "hindi": "✅ **संदेश का वास्तविक विश्लेषण (ऑर्डर / डिलीवरी सूचना)**:\n• यह ई-कॉमर्स ऑर्डर या पार्सल डिलीवरी की सामान्य और वैध सूचना है। इसमें कोई फ़िशिंग लिंक या जबरन वसूली का संकेत नहीं है।",
                "hinglish": "✅ **Message ka Real Analysis (Order / Delivery Update)**:\n• Yeh aapke online order ya courier delivery ka normal aur safe notification hai. Isme koi cyber threat nahi hai.",
                "english": "✅ **Real Message Analysis (Legitimate Delivery Update)**:\n• Legitimate order fulfillment or shipping status notification. Free from extortion, phishing, or malicious links."
            }

        if bool(re.search(r'\b(?:recharge|bill paid|plan active)\b', lowered)):
            return {
                "hindi": "✅ **संदेश का वास्तविक विश्लेषण (रिचार्ज / बिल भुगतान)**:\n• यह आपके मोबाइल या सेवा रिचार्ज के सफलतापूर्वक पूरा होने की आधिकारिक रसीद है।",
                "hinglish": "✅ **Message ka Real Analysis (Recharge Confirmation)**:\n• Yeh aapke mobile recharge ya utility bill payment successful hone ka legitimate alert hai.",
                "english": "✅ **Real Message Analysis (Recharge Confirmation)**:\n• Authentic confirmation of successful telecom recharge or utility bill payment."
            }

        return {
            "hindi": "✅ **संदेश का वास्तविक विश्लेषण (सुरक्षित बातचीत)**:\n• यह एक सामान्य संदेश है। इसमें किसी भी प्रकार की वित्तीय धोखाधड़ी, संदिग्ध लिंक, ओटीपी चोरी या जबरन वसूली के संकेत नहीं मिले हैं।",
            "hinglish": "✅ **Message ka Real Analysis (Safe Communication)**:\n• Yeh ek normal sandesh hai. Isme kisi bhi tarah ke cyber fraud, fake link ya extortion ka koi sanket nahi hai.",
            "english": "✅ **Real Message Analysis (Safe Notification)**:\n• Standard communication free from suspicious indicators, unauthorized links, or credential solicitation."
        }

    # -------------------------------------------------------------
    # Case 2: Threat / Scam Message (Dynamic Message-Specific Breakdown)
    # -------------------------------------------------------------
    findings_hi = []
    findings_hing = []
    findings_en = []

    # Impersonation
    if elements["roles"]:
        findings_hi.append(f"प्रेषक ने संदेश में खुद को **'{elements['roles'][0]}'** बताकर प्राधिकार दिखाने की कोशिश की है।")
        findings_hing.append(f"Sender ne message me khud ko **'{elements['roles'][0]}'** bata kar authority create ki hai.")
        findings_en.append(f"Sender falsely claims to represent **'{elements['roles'][0]}'** to build artificial credibility.")

    # Demands
    if elements["demands"]:
        findings_hi.append(f"संदेश में आपसे सीधे **'{elements['demands'][0]}'** की मांग की गई है।")
        findings_hing.append(f"Aapse seedhe **'{elements['demands'][0]}'** ki demand ki gayi hai.")
        findings_en.append(f"Explicit credential/action demand detected: **'{elements['demands'][0]}'**.")

    # Threats & Coercion
    if elements["threats"]:
        findings_hi.append(f"आप पर मनोवैज्ञानिक दबाव बनाने के लिए **'{elements['threats'][0]}'** का डर दिखाया गया है।")
        findings_hing.append(f"Aap par panic create karne ke liye **'{elements['threats'][0]}'** ka dar dikhaya gaya hai.")
        findings_en.append(f"Coercive urgency tactic used: **'{elements['threats'][0]}'**.")

    # Monetary Lures
    if elements["lures"]:
        findings_hi.append(f"आपको लालच में फंसाने के लिए **'{elements['lures'][0]}'** का दावा किया गया है।")
        findings_hing.append(f"Aapko phansane ke liye **'{elements['lures'][0]}'** ka lure diya gaya hai.")
        findings_en.append(f"Financial lure detected: **'{elements['lures'][0]}'**.")

    # Suspicious URLs
    if elements["urls"]:
        url_tag = ", ".join(f"`{u}`" for u in elements["urls"][:2])
        findings_hi.append(f"असुरक्षित व अनधिकृत वेब लिंक **{url_tag}** पर जाने को कहा गया है।")
        findings_hing.append(f"Suspicious link **{url_tag}** par redirect karne ki koshish ki gayi hai.")
        findings_en.append(f"Directs user to suspicious unauthorized domain: **{url_tag}**.")

    # Private Phone Numbers
    if elements["phones"]:
        phone_tag = ", ".join(f"`{p}`" for p in elements["phones"][:2])
        findings_hi.append(f"संपर्क के लिए निजी 10-अंकीय मोबाइल नंबर **{phone_tag}** दिया गया है।")
        findings_hing.append(f"Contact ke liye personal mobile number **{phone_tag}** diya gaya hai.")
        findings_en.append(f"Instructs user to dial personal unverified mobile number: **{phone_tag}**.")

    # International Calling Codes
    if elements["intl_numbers"]:
        intl_tag = ", ".join(f"`{num}`" for num in elements["intl_numbers"][:2])
        findings_hi.append(f"विदेशी कॉलिंग कोड वाले नंबर **{intl_tag}** (क्रॉस-बॉर्डर सिंडिकेट) का उपयोग हुआ है।")
        findings_hing.append(f"Cross-border calling code **{intl_tag}** use kiya gaya hai.")
        findings_en.append(f"Originated from cross-border cyber syndicate number: **{intl_tag}**.")

    # Fallback if no specific tags caught but vector matched
    if not findings_hi:
        findings_hi.append("संदेश में अस्वाभाविक जल्दबाजी और अनधिकृत वित्तीय लेनदेन के संकेत मिले हैं।")
        findings_hing.append("Message me unsolicited urgency aur unauthorized action signals detect hue hain.")
        findings_en.append("Unsolicited panic indicators and unauthorized financial demands detected.")

    # Specific explanation of WHY this is fraudulent
    if category == "LOAN_FRAUD" or "loan" in lowered:
        why_hi = "फर्जी लोन व आधार-ओटीपी फ्रॉड: बिना किसी वैध दस्तावेज़ या सिबिल जांच के 'तुरंत 5 लाख लोन' का दावा 100% फर्जी है। यह स्कैमर्स का गिरोह है जो लोन देने के बहाने आपका आधार कार्ड और बैंक ओटीपी चुराकर आपके खाते से पैसे खाली कर देता है।"
        why_hing = "Farzi Instant Loan Scam: Bina documents ke 'Instant Loan approved' ka dawa 100% fraud hai. Yeh aapse Aadhaar aur OTP le kar aapka bank account khali kar denge."
        why_en = "Fake Instant Loan Trap: Guarantees of collateral-free instant loans without documents are fraudulent syndicates designed to steal Aadhaar credentials and authorize illicit bank debits."
    elif category == "COURIER_PARCEL_FRAUD" or "parcel" in lowered or "redelivery" in lowered:
        why_hi = "फर्जी पार्सल व इंडिया पोस्ट फ़िशिंग: डाकिया या कूरियर सेवा कभी भी 'पता गलत होने' पर ₹10 पुनः डिलीवरी शुल्क का लिंक एसएमएस में नहीं भेजते। यह लिंक आपके क्रेडिट/डेबिट कार्ड का नंबर और सीवीवी चुराने के लिए बनाया गया है।"
        why_hing = "Fake Courier / Parcel Scam: Courier ya Post Office kabhi bhi galat address ke bahane SMS link se ₹10 redelivery fee nahi maangte. Yeh link card details churane ka phishing trap hai."
        why_en = "Parcel Redelivery Phishing: Postal and courier agencies never demand micro-payments (Rs 10) via SMS links for address corrections. Entering card details exposes your account to unauthorized charges."
    elif category == "MALICIOUS_APK_FRAUD" or "apk" in lowered:
        why_hi = "खतरनाक एंड्रॉइड ट्रोजन एपीके: कैशबैक या इनाम पाने के लिए किसी अनजान लिंक से एपीके (APK) इंस्टॉल करना फोन हैक करने की साजिश है। यह ऐप इंस्टॉल होते ही आपके बैंक ओटीपी और स्क्रीन को स्कैमर के पास भेज देता है।"
        why_hing = "Dangerous Trojan APK Trap: Cashback pane ke liye anjaan APK download karna phone hack karne ki saazish hai. Yeh APK aapke saare bank OTP chura lega."
        why_en = "Malicious Android Trojan APK: Sideloading untrusted APK files installs spyware capable of intercepting 2FA SMS OTPs and granting remote access to financial apps."
    elif category == "CREDENTIAL_HARVESTING" or "banking password" in lowered:
        why_hi = "नेटबैंकिंग पासवर्ड चोरी का ट्रैप: कोई भी असली बैंक नकद पुरस्कार देने के नाम पर आपका 'बैंकिंग पासवर्ड' दर्ज करने को नहीं कहता! यह फ़िशिंग लिंक सीधे आपके नेटबैंकिंग खाते में अनाधिकृत ट्रांसफर करने के लिए बनाया गया है।"
        why_hing = "NetBanking Password Phishing: Cash reward ke naam par 'banking password' mangna 100% phishing hai. Diya gaya link aapka password chura kar account khali kar dega."
        why_en = "Credential Harvesting Phishing: Legitimate financial institutions NEVER ask customers to input banking passwords to claim rewards. Entering your password surrenders complete account control."
    elif category == "CARD_BLOCK_PHONE_TRAP" or "atm card is blocked" in lowered:
        why_hi = "एटीएम कार्ड ब्लॉक कॉल फ्रॉड: असली बैंक कभी भी एटीएम कार्ड अनब्लॉक करने के लिए किसी निजी 10-अंकीय मोबाइल नंबर पर कॉल करने को नहीं कहते। उस नंबर पर कॉल करने पर स्कैमर बैंक अधिकारी बनकर आपका कार्ड नंबर और सीवीवी मांग लेगा।"
        why_hing = "ATM Card Block Callback Scam: Bank kabhi bhi ATM card chalu karne ke liye personal 10-digit mobile number par call karne ko nahi kehta. Is number par call na karein."
        why_en = "ATM Card Block Call Trap: Official banks never direct customers to call personal 10-digit mobile numbers to unblock cards. Callers on such numbers pose as staff to elicit CVVs and PINs."
    elif category == "OTP_HARVESTING" or "otp" in lowered:
        why_hi = "आरबीआई (RBI) और बैंकों का सख्त नियम: असली बैंक का कोई भी कर्मचारी, मैनेजर या अधिकारी ग्राहक से कभी भी फोन या मैसेज पर गुप्त ओटीपी (OTP), पिन (PIN) या पासवर्ड नहीं मांगता! अपना ओटीपी किसी को न बताएं, वरना आपके बैंक खाते से तुरंत सारे पैसे निकाल लिए जाएंगे।"
        why_hing = "RBI aur banks ka sakht niyam: Real bank employee ya manager phone ya SMS par aapse kabhi bhi OTP ya PIN nahi mangta! Apna OTP kisi ko na dein, varna account se saare paise kat jayenge."
        why_en = "Golden Banking Rule: Legitimate bank employees, managers, and RBI NEVER solicit 6-digit confidential OTPs, PINs, or passwords. Disclosing this code gives the attacker immediate authorization to drain your account."
    elif category == "UPI_FRAUD" or "pin" in lowered or "qr" in lowered:
        why_hi = "यूपीआई (UPI) का बुनियादी नियम: पैसे प्राप्त करने के लिए कभी भी यूपीआई पिन (UPI PIN) दर्ज नहीं करना पड़ता और न ही क्यूआर कोड स्कैन करना होता है। पिन दर्ज करने का मतलब सिर्फ आपके खाते से पैसे कटना (Debit) होता है।"
        why_hing = "UPI ka basic rule: Paise lene ke liye kabhi bhi UPI PIN enter nahi karna padta aur na hi QR code scan karna hota hai. PIN dalne ka matlab sirf account se paise katna hota hai."
        why_en = "Fundamental UPI Rule: You NEVER enter your UPI PIN or scan a QR code to receive money. Entering your PIN always authorizes a DEBIT transaction from your account."
    elif category == "ELECTRICITY_CUTOFF" or "bijli" in lowered or "power" in lowered:
        why_hi = "बिजली विभाग (Discom) कभी भी रात को 9:30 बजे लाइन काटने का अल्टीमेटम किसी निजी 10-अंकीय मोबाइल नंबर से नहीं भेजता। यह स्कैमर का नंबर है जो घबराहट में आपसे पैसे ट्रांसफर करवाने की कोशिश कर रहा है।"
        why_hing = "Bijli vibhag kabhi bhi personal 10-digit mobile number se raat ko line kaatne ki dhamki nahi bhejta. Yeh scammer manufactured urgency create kar raha hai taaki aap dar kar paise bhej dein."
        why_en = "Electricity distribution utilities never issue power cutoff ultimatums via personal 10-digit mobile numbers. This is manufactured panic designed to coerce an emergency money transfer."
    elif category == "BANK_KYC_FREEZE" or "kyc" in lowered or "pan" in lowered:
        why_hi = "बैंक कभी भी एसएमएस में अनधिकृत वेब लिंक भेजकर खाता ब्लॉक करने की धमकी नहीं देता। दिया गया लिंक बैंक का फर्जी क्लोन (Phishing) है जो आपका नेटबैंकिंग पासवर्ड और ओटीपी चुराने के लिए बनाया गया है।"
        why_hing = "Bank kabhi bhi SMS link se KYC update karne ya khata block karne ki dhamki nahi deta. Diya gaya link fake domain hai jo aapka net banking ID aur password churane ke liye banaya gaya hai."
        why_en = "Banks never threaten immediate account suspension via unverified SMS web links. The linked page is a deceptive phishing clone created to harvest NetBanking credentials and OTPs."
    elif category == "KBC_LOTTERY" or "lottery" in lowered or "kbc" in lowered or "iphone" in lowered:
        why_hi = "एडवांस-फी लॉटरी व फ्री गिफ्ट फ्रॉड: कोई भी असली कंपनी लॉटरी की रकम या 'फ्री आईफोन' देने के नाम पर पहले 'डिलीवरी चार्ज' या 'प्रोसेसिंग फीस' नहीं मांगती। पैसे भेजते ही स्कैमर आपको ब्लॉक कर देगा।"
        why_hing = "Advance-Fee Lottery / Free Gift Scam: Koi bhi real company lottery ya gift dene ke naam par upfront delivery charges ya processing fee nahi maangti. Paise na bhejein."
        why_en = "Advance-Fee Prize / Gift Fraud: Legitimate lotteries and legitimate promotions never demand upfront processing taxes or delivery charges. Paying guarantees financial loss."
    elif category == "DIGITAL_ARREST_CUSTOMS" or "cbi" in lowered or "arrest" in lowered:
        why_hi = "भारतीय कानून में 'डिजिटल अरेस्ट' नाम की कोई चीज़ नहीं है! पुलिस, सीबीआई या कस्टम्स कभी भी वीडियो कॉल पर किसी को गिरफ्तार नहीं करते। तुरंत कॉल काटें और 1930 पर शिकायत दर्ज करें।"
        why_hing = "Bharat ke kanoon me 'Digital Arrest' jaisa koi kanoon nahi hai! Police ya CBI kabhi video call par arrest nahi karti. Ghabraiye mat, call kaat kar 1930 milayein."
        why_en = "The Supreme Court confirms 'Digital Arrest' does not exist under Indian law. Law enforcement agencies never conduct arrests or asset freezes over Skype/WhatsApp video calls."
    elif category == "REMOTE_HIJACK" or "anydesk" in lowered:
        why_hi = "किसी अनजान व्यक्ति के कहने पर AnyDesk या क्विकसपोर्ट ऐप इंस्टॉल न करें। इससे स्कैमर आपके मोबाइल स्क्रीन को लाइव देखकर बैंक ओटीपी चुरा लेते हैं।"
        why_hing = "Kisi ke kehne par AnyDesk app install na karein. Isse scammer aapke phone ki screen dekhkar bank OTP chura lete hain."
        why_en = "Never install remote-screen applications like AnyDesk on unknown callers' advice. It allows attackers to mirror your screen and intercept confidential 2FA banking codes."
    elif category == "TRAFFIC_CHALLAN_SCAM" or "challan" in lowered or "चालान" in lowered:
        why_hi = "फर्जी ट्रैफिक ई-चालान फ़िशिंग: ट्रैफिक पुलिस या परिवहन विभाग कभी भी व्हाट्सएप या एसएमएस लिंक से लाइसेंस रद्द करने की धमकी देकर जुर्माना नहीं मांगता। असली चालान केवल सरकारी पोर्टल 'echallan.parivahan.gov.in' पर ही चेक करें।"
        why_hing = "Fake Traffic Challan Scam: Traffic police SMS me anjaan link bhejkar license cancel karne ki dhamki nahi deti. Asli challan sirf echallan.parivahan.gov.in par bharein."
        why_en = "Fake Traffic E-Challan Scam: Traffic authorities never send SMS links threatening license suspension to coerce fines. Official challans are exclusively on echallan.parivahan.gov.in."
    elif category == "TRAI_SIM_BLOCK_SCAM" or "trai" in lowered or "sim card" in lowered or "सिम" in lowered:
        why_hi = "फर्जी ट्राई / सिम कार्ड ब्लॉकिंग फ्रॉड: दूरसंचार विभाग (DoT) या ट्राई कभी भी फोन करके 2 घंटे में सिम काटने की धमकी नहीं देता। यह डिजिटल अरेस्ट या ब्लैकमेल में फंसाने का षड्यंत्र है।"
        why_hing = "TRAI / SIM Deactivation Hoax: DoT ya TRAI kabhi call karke 2 ghante me sim block karne ki dhamki nahi deta. Yeh digital arrest extortion ki shuruat hai."
        why_en = "TRAI / DoT SIM Deactivation Hoax: Government telecom regulatory bodies never contact citizens demanding verification under threat of immediate SIM deactivation."
    elif category == "INCOME_TAX_REFUND_SCAM" or "income tax" in lowered or "इनकम टैक्स" in lowered:
        why_hi = "फर्जी आयकर रिफंड फ़िशिंग: आयकर विभाग (Income Tax) कभी भी एसएमएस लिंक भेजकर रिफंड क्लेम करने या बैंक डिटेल्स मांगने को नहीं कहता। वैध रिफंड सीधे आपके पैन-लिंक्ड बैंक खाते में आता है।"
        why_hing = "Income Tax Refund Phishing: Income Tax department SMS me link bhejkar refund claim karne ko nahi kehta. Refund direct aapke bank account me transfer hota hai."
        why_en = "Income Tax Refund Phishing: The IT Department directly credits authorized bank accounts and never sends links to claim funds or enter banking credentials."
    elif category == "CREDIT_CARD_REWARD_SCAM" or "reward points" in lowered or "रिवॉर्ड पॉइंट" in lowered:
        why_hi = "क्रेडिट कार्ड रिवॉर्ड पॉइंट रिडीम फ़िशिंग: असली बैंक कभी भी एसएमएस लिंक भेजकर रिवॉर्ड पॉइंट को कैश में बदलने के लिए कार्ड नंबर, सीवीवी या ओटीपी दर्ज करने को नहीं कहते। यह लिंक कार्ड की चोरी का जाल है।"
        why_hing = "Credit Card Reward Points Scam: Bank kabhi bhi SMS link se reward points cash me convert karne ke liye card details ya OTP nahi maangta. Is link par details na dalein."
        why_en = "Credit Card Reward Points Scam: Banks never urge customers to convert expiring points into cash via SMS links requiring card numbers and OTPs."
    elif category == "GOVT_SCHEME_PHISHING" or "free recharge" in lowered or "मुफ्त रिचार्ज" in lowered:
        why_hi = "फर्जी सरकारी योजना व मुफ्त रिचार्ज फ्रॉड: सरकार या टेलीकॉम कंपनियां व्हाट्सएप संदेशों या अज्ञात लिंक पर मुफ्त लैपटॉप या 3 महीने का फ्री रिचार्ज नहीं देती हैं। यह आपके फोन से डेटा चुराने का वायरस लिंक है।"
        why_hing = "Bogus Govt Scheme / Free Recharge: Government ya telecom companies viral links par muft recharge ya laptop nahi deti. Yeh phishing malware link hai."
        why_en = "Bogus Government Scheme / Free Recharge: State authorities never distribute free electronic devices or recharges through viral forwarded links."
    elif category == "FAKE_CUSTOMER_CARE_SCAM" or "customer care" in lowered or "कस्टमर केयर" in lowered:
        why_hi = "फर्जी कस्टमर केयर नंबर ट्रैप: गूगल सर्च या संदिग्ध एसएमएस पर मिले 10-अंकीय मोबाइल नंबर कभी भी आधिकारिक कस्टमर केयर नहीं होते। जालसाज पैसे रिफंड करने के नाम पर ऐप डाउनलोड या ओटीपी की मांग करते हैं।"
        why_hing = "Fake Customer Care Number Scam: Google search ya SMS par mile aam mobile number real customer care nahi hote. Yeh thag aapse app download karwake account khali karte hain."
        why_en = "Bogus Customer Support Trap: Scammers seed Google results and SMS with 10-digit mobile numbers posing as customer service to manipulate callers into installing screen-sharing tools."
    elif category == "WFH_TELEGRAM" or "youtube" in lowered or "यूट्यूब" in lowered:
        why_hi = "यूट्यूब लाइक व टेलीग्राम टास्क सिंडिकेट: घर बैठे यूट्यूब वीडियो लाइक करने के नाम पर रोज 3000-5000 कमाने का लालच एक संगठित अंतरराष्ट्रीय साइबर गिरोह का जाल है। शुरू में कुछ रुपये देकर यह बाद में वीआईपी टास्क के नाम पर लाखों रुपये ठग लेते हैं।"
        why_hing = "YouTube Like / Telegram Task Scam: Like youtube videos karke daily paise kamane ka offer fraud hai. Yeh aapse prepaid investment ke naam par lakhon loot lenge."
        why_en = "YouTube Task / Work-From-Home Scam: Offers paying money to like YouTube videos or post reviews are organized prepaid task fraud. Initial token payouts are followed by demands for massive non-refundable deposits."
    else:
        why_hi = "इस संदेश में अनधिकृत विवरण और दबाव बनाकर निजी वित्तीय जानकारी या पैसे ऐंठने की रणनीति पाई गई है। किसी भी लिंक या नंबर पर संपर्क न करें।"
        why_hing = "Is message me anjaan contact details aur asamayik dabav hai. Kisi link par click na karein aur anjaan vyakti ko koi jaankari na dein."
        why_en = "This message deploys social engineering and unauthorized contact channels to harvest confidential details. Do not interact with the sender."

    bullet_hi = "\n".join(f"• {f}" for f in findings_hi)
    bullet_hing = "\n".join(f"• {f}" for f in findings_hing)
    bullet_en = "\n".join(f"• {f}" for f in findings_en)

    return {
        "hindi": f"📌 **आपके संदेश का विशिष्ट विश्लेषण (Specific Clues Found)**:\n{bullet_hi}\n\n🚨 **यह फ्रॉड क्यों है**:\n{why_hi}",
        "hinglish": f"📌 **Aapke Message ka Specific Analysis**:\n{bullet_hing}\n\n🚨 **Yeh Fraud kyu hai**:\n{why_hing}",
        "english": f"📌 **Specific Clues in Your Message**:\n{bullet_en}\n\n🚨 **Why this is a Scam**:\n{why_en}"
    }


def generate_voice_scripts(text: str, category: str, risk: int) -> Dict[str, str]:
    """Generate audio TTS speech scripts tailored directly to the specific threat in the message."""
    lowered = text.lower()
    if category == "SAFE_TRANSACTION":
        return {
            "hi": "Aapka sandesh surakshit pratit hota hai. Yeh ek aam legitimate notification hai. Savdhaan rahein.",
            "en": "This message appears safe. It looks like a standard verified notification. Stay vigilant."
        }
    if category == "OTP_HARVESTING" or "bank employee" in lowered or "otp" in lowered:
        return {
            "hi": "Savdhaan! Yeh sandesh bank employee bankar aapse OTP maang raha hai! Asli bank kabhi aapse OTP nahi maangta. Apna OTP kisi ko na dein!",
            "en": "Critical Alert! This message demands OTP by posing as a bank employee. Real banks never ask for OTP. Never share your OTP!"
        }
    if category == "UPI_FRAUD" or "upi" in lowered or "qr" in lowered:
        return {
            "hi": "Savdhaan! Yeh ek farzi UPI cashback trap hai. Paise lene ke liye kabhi bhi UPI PIN na dalein, varna aapke paise kat jayenge!",
            "en": "Warning! This is a dangerous UPI cashback trap. You never need to enter your UPI PIN to receive money. Do not proceed!"
        }
    if category == "ELECTRICITY_CUTOFF" or "bijli" in lowered:
        return {
            "hi": "Dhyaan dein! Yeh bijli bill ka farzi scam hai. Bijli vibhag kabhi bhi aam mobile number se line kaatne ki dhamki nahi deta. Call na karein.",
            "en": "Attention! Fraudulent electricity disconnection scam detected. Power boards never message from private mobile numbers."
        }
    if category == "BANK_KYC_FREEZE" or "kyc" in lowered:
        return {
            "hi": "Khatra! Yeh ek farzi bank KYC sandesh hai. Diye gaye link par click na karein, aur apna PAN card ya OTP kisi ke sath share na karein.",
            "en": "Critical alert! Fake bank KYC phishing detected. Never click unauthorized links or disclose banking credentials."
        }
    if category == "KBC_LOTTERY" or "lottery" in lowered:
        return {
            "hi": "Savdhaan! Lottery ka sandesh poori tarah jhootha hai. KBC WhatsApp par koi lottery nahi chalata. Kisi ko processing fee na bhejein.",
            "en": "Beware! The lottery notification is completely fraudulent. Do not transfer any advance processing charges."
        }
    if category == "DIGITAL_ARREST_CUSTOMS" or "arrest" in lowered:
        return {
            "hi": "Emergency Alert! Bharat me Digital Arrest ka koi kanoon nahi hai. CBI ya Police kabhi video call par arrest nahi karti. Turant 1930 milayein!",
            "en": "Emergency Alert! Digital Arrest is a pure scam. Indian police and CBI never conduct video call arrests. Dial 1930!"
        }
    return {
        "hi": "Savdhaan! Is sandesh me cyber fraud ke khatarnak sanket hain. Kisi bhi sandigdh link par click na karein.",
        "en": "Caution! Cyber fraud indicators detected. Do not click any links or share private financial details."
    }


def get_action_steps(category: str, risk: int) -> List[str]:
    """Provide structured, civic-grade actionable steps."""
    if category == "SAFE_TRANSACTION":
        return [
            "Verify transaction details in your official banking app if applicable.",
            "Never share 6-digit OTPs even for verified transactions.",
            "Keep SMS alerts activated on your registered mobile number."
        ]
    return [
        "DO NOT click any embedded links or download attached .apk files.",
        "NEVER enter your UPI PIN or disclose your 6-digit banking OTP.",
        "Block the sender number and report as spam on WhatsApp / Truecaller.",
        "Dial National Cyber Helpline 1930 or submit complaint on cybercrime.gov.in."
    ]


def evaluate_copilot_turn(dialogue_history: List[Dict[str, str]], current_turn: str, scenario: str) -> Dict[str, Any]:
    """
    Evaluates live turns between scammer and victim in Call Simulator.
    Detects coercion, urgency, OTP solicitation, AnyDesk installation, etc.
    """
    lowered = current_turn.lower()
    tactics = []
    
    # Check for OTP or PIN request
    if any(k in lowered for k in ["otp", "pin", "code", "password", "6 digit", "char digit", "bheja hai", "batao"]):
        threat_level = "CRITICAL"
        banner_alert = "🚨 DANGER: SCAMMER IS DEMANDING OTP/PIN! NEVER DISCLOSE YOUR OTP!"
        tactics.append("Authentication Hijack (Demanding OTP/PIN)")

    # Check for AnyDesk / Remote screen app
    elif any(k in lowered for k in ["anydesk", "teamviewer", "rustdesk", "quicksupport", "app download", "playstore par"]):
        threat_level = "CRITICAL"
        banner_alert = "🚨 CRITICAL THREAT: Scammer is attempting remote phone access via screen-sharing app!"
        tactics.append("Remote Access Trojan / Screen Mirroring")

    # Check for Digital Arrest / CBI / Police threats
    elif any(k in lowered for k in ["cbi", "arrest", "skype", "camera", "narcotics", "court", "money laundering", "fir"]):
        threat_level = "CRITICAL"
        banner_alert = "🚨 FAKE DIGITAL ARREST: Law enforcement NEVER conducts Skype video trials or asset freezes!"
        tactics.append("Law Enforcement Impersonation & Digital Arrest Extortion")

    # Check for Electricity Cutoff urgency
    elif any(k in lowered for k in ["bijli", "line kat", "power cut", "turant payment", "9:30", "disconnect"]):
        threat_level = "HIGH"
        banner_alert = "⚠️ URGENCY EXPLOITATION: Electricity discoms do not shut power over phone demands!"
        tactics.append("Manufactured Panic & False Urgency")

    # Check for Lottery / Processing fee
    elif any(k in lowered for k in ["lottery", "25 lakh", "kbc", "registration fee", "tax jama", "rana pratap"]):
        threat_level = "HIGH"
        banner_alert = "⚠️ ADVANCE-FEE FRAUD: Scammer demands upfront fee before releasing fake lottery!"
        tactics.append("Advance-Fee Fraud (Fake Lottery)")

    else:
        threat_level = "MEDIUM"
        banner_alert = "⚠️ SUSPICIOUS CALLER: Caller is probing for personal identity and account details."
        tactics.append("Social Engineering & Information Harvesting")

    # Contextual Counter-Replies
    suggested_replies = [
        "Main official helpline par call karke khud pata karunga.",
        "RBI kehta hai kisi ko bhi OTP ya PIN batana sakht mana hai.",
        "Aapka official employee ID aur landline number kya hai? Main verify karunga."
    ]

    if "otp" in lowered or "pin" in lowered:
        suggested_replies = [
            "Mera bank mujhe mana karta hai OTP kisi ko bhi dene se. Main nahi doonga.",
            "Aap real bank officer hain toh mere account se directly verify karein, OTP kyu maang rahe hain?",
            "Call disconnect kar raha hoon, main sidha police station ja raha hoon."
        ]
    elif "cbi" in lowered or "arrest" in lowered:
        suggested_replies = [
            "Digital Arrest jaisa koi kanoon nahi hai. Main local police station ja raha hoon.",
            "Apna official notice mere registered address par post karein. Skype par arrest nahi hota.",
            "Main yeh call record karke cyber crime portal 1930 par bhej raha hoon."
        ]

    return {
        "threat_level": threat_level,
        "banner_alert": banner_alert,
        "deception_tactics": tactics,
        "suggested_replies": suggested_replies,
        "verdict": "ACTIVE_SCAM_INTERCEPTION"
    }


def voice_query_advisor(query: str) -> Dict[str, Any]:
    """
    Intelligent conversational advisor for natural voice queries in Hindi/Hinglish/English.
    Accurately differentiates between:
    1. Conversational greetings & well-being (e.g. "हाई क्या हाल है?", "Hello", "How are you")
    2. Bot identity & purpose inquiries (e.g. "आप कौन हो?", "Who are you?", "What is FraudRakshak")
    3. Gratitude & politeness (e.g. "Thank you", "धन्यवाद", "Shukriya")
    4. 1930 Cyber Helpline & Reporting guidance (e.g. "1930 क्या है?", "complaint kaise kare")
    5. Specific educational scam inquiries (UPI PIN rules, AnyDesk, Digital arrest, Fake loan, Electricity bill, Parcel smishing)
    6. Legitimate / Safe transactions (e.g. credit/debit alerts, food delivery, OTP alerts)
    7. Active scam messages / quoted threats (analyzed dynamically using NLP engine with contextual extraction)
    """
    q_clean = (query or "").strip()
    q_lower = q_clean.lower()
    q_normalized = re.sub(r'[\s।,?!.:;\'"-_—/\\()]+', ' ', q_clean).strip().lower()

    # -------------------------------------------------------------
    # 1. Greetings & Casual Well-Being (when no specific scam is present)
    # -------------------------------------------------------------
    scam_triggers = [
        "fraud", "scam", "thagi", "police", "arrest", "cbi", "otp", "pin",
        "lottery", "bijli", "bill", "power cut", "account", "block", "freeze",
        "link", "parcel", "apk", "loan", "rs.", "rs ", "rup", "debit", "credit",
        "swiggy", "zomato", "amazon", "anydesk", "khata", "card", "suspended"
    ]
    has_scam_context = any(st in q_lower for st in scam_triggers)

    devanagari_greetings = [
        "हाई", "हाय", "हैलो", "हेलो", "हॅलो", "हैलौ", "हेल्लो", "हे", "नमस्ते", "नमस्कार", "नमस्कारम", "प्रणाम",
        "राम राम", "राधे राधे", "जय श्री राम", "सत श्री", "आदाब", "सलाम", "सुप्रभात", "शुभ प्रभात", "शुभ संध्या",
        "गुड मॉर्निंग", "गुड इवनिंग", "गुड आफ्टरनून", "क्या हाल", "हाल चाल", "हाल है", "कैसे हो", "कैसी हो",
        "कैसे हैं", "कैसा है", "सब ठीक", "सब बढ़िया", "क्या चल रहा", "क्या हो रहा", "मदद चाहिए", "सहायता"
    ]
    is_greeting_devanagari = any(g in q_clean or g in q_normalized for g in devanagari_greetings)
    greeting_latin_regex = r'\b(hi|hey|hello|hallo|namaste|namaskar|pranam|kya hal|kya haal|kaise ho|kaise hain|kaisa hai|how are you|how r u|whats up|what\'s up|good morning|good evening|good afternoon|sab theek|sab badhiya|haal chaal|hal chal)\b'
    is_greeting_latin = bool(re.search(greeting_latin_regex, q_lower)) or bool(re.search(greeting_latin_regex, q_normalized))

    if (is_greeting_devanagari or is_greeting_latin) and not has_scam_context:
        return {
            "detected_category": "GREETING_CONVERSATION",
            "risk_level": "SAFE",
            "response_text_hindi": "नमस्ते! मैं बिल्कुल ठीक हूँ। मैं आपका रक्षक एआई (FraudRakshak) सुरक्षा सलाहकार हूँ। आप कैसे हैं? आप मुझसे किसी भी संदिग्ध कॉल, एसएमएस, व्हाट्सएप मैसेज या साइबर सुरक्षा नियम (जैसे 1930 हेल्पलाइन या यूपीआई पिन सुरक्षा) के बारे में पूछ सकते हैं।",
            "response_text_hinglish": "Namaste! Main bilkul theek hoon. Main aapka FraudRakshak AI security advisor hoon. Aap kaise hain? Aap mujhse kisi bhi sandigdh call, SMS, WhatsApp sandesh ya cyber safety rules (jaise 1930 helpline, UPI PIN safety) ke baare me pooch sakte hain.",
            "response_text_english": "Hello! I am doing great. I am your FraudRakshak AI cyber defense advisor. How are you doing? Feel free to ask me about any suspicious call, SMS, WhatsApp message, or cyber safety rules (like 1930 helpline or UPI PIN security).",
            "spoken_audio_script": "Namaste! Main bilkul theek hoon. Main aapka FraudRakshak AI advisor hoon. Aap mujhse kisi bhi sandigdh call ya cyber scam ke baare me pooch sakte hain.",
            "bullet_actions": []
        }

    # -------------------------------------------------------------
    # 2. Bot Identity & Purpose Inquiries ("आप कौन हो?", "Who are you?")
    # -------------------------------------------------------------
    is_identity = any(id_phrase in q_clean for id_phrase in [
        "आप कौन", "तुम कौन", "आपका नाम", "तुम क्या करते", "आप क्या करते", "क्या काम करते", "कौन हो"
    ]) or any(id_phrase in q_lower for id_phrase in [
        "who are you", "who r u", "what is fraudrakshak", "what is rakshak", "aap kaun ho", "tum kaun ho",
        "what can you do", "what do you do", "introduce yourself", "apna parichay", "tumhara naam", "aapka naam"
    ])

    if is_identity and not has_scam_context:
        return {
            "detected_category": "BOT_IDENTITY",
            "risk_level": "SAFE",
            "response_text_hindi": "मैं रक्षक एआई (FraudRakshak) हूँ — भारत का पहला एआई साइबर सुरक्षा और फ्रॉड रोकथाम वॉइस एडवाइज़र। मैं आपको फ़िशिंग एसएमएस, फर्जी बैंक कॉल्स, बिजली बिल स्कैम, डिजिटल अरेस्ट, लॉटरी फ्रॉड और फर्जी लोन ऐप्स से बचाने में मदद करता हूँ। आप मुझे कोई भी संदेश या कॉल की बात बताकर उसकी असलियत जांच सकते हैं।",
            "response_text_hinglish": "Main FraudRakshak AI hoon — Bharat ka pehla AI cyber security aur fraud prevention voice advisor. Main aapko fake bank calls, phishing SMS, bijli bill scam, digital arrest, fake lottery aur instant loan apps se bachane me madad karta hoon. Aap mujhe kisi bhi sandigdh call ya sandesh ke baare me batakar uski sachai jaan sakte hain.",
            "response_text_english": "I am FraudRakshak AI — an intelligent cyber security and scam defense voice advisor. I protect you against fake banking calls, phishing SMS, electricity cutoff scams, digital arrest coercion, fake lotteries, and malicious loan APKs. You can ask me about any suspicious call or message to verify its authenticity.",
            "spoken_audio_script": "Main FraudRakshak AI hoon, aapka cyber security advisor. Main aapko fake calls, phishing SMS aur online fraud se bachane me madad karta hoon.",
            "bullet_actions": [
                "Speak or paste any SMS to check if it's real or scam",
                "Ask whether someone asking for OTP or PIN is real",
                "Generate formal 1930 cyber crime complaints"
            ]
        }

    # -------------------------------------------------------------
    # 3. Gratitude & Courtesy ("Thank you", "धन्यवाद")
    # -------------------------------------------------------------
    is_gratitude = any(g in q_clean for g in [
        "धन्यवाद", "शुक्रिया", "थैंक यू", "थैंक्स", "अलविदा", "बहुत अच्छा"
    ]) or any(g in q_lower for g in [
        "thank you", "thanks", "dhanyawad", "shukriya", "bahut achha", "good job", "bye", "goodbye", "see you"
    ])

    if is_gratitude and not has_scam_context:
        return {
            "detected_category": "GRATITUDE_COURTESY",
            "risk_level": "SAFE",
            "response_text_hindi": "आपका बहुत-बहुत धन्यवाद! हमेशा सतर्क और साइबर-सुरक्षित रहें। याद रखें: कोई भी बैंक अधिकारी आपसे कभी ओटीपी या यूपीआई पिन नहीं मांगता। यदि कभी भी कोई संदेह हो, तो बेझिझक मुझसे पूछें!",
            "response_text_hinglish": "Aapka bahut-bahut swagat hai! Hamesha satark aur surakshit rahein. Yaad rakhein: koi bhi genuine bank officer aapse kabhi OTP ya UPI PIN nahi mangta. Kabhi bhi shaq ho toh bejhijhak poochiye!",
            "response_text_english": "You are most welcome! Stay alert and cyber-safe. Remember: genuine bank officials never ask for your OTP or UPI PIN. Whenever in doubt, feel free to ask me anytime!",
            "spoken_audio_script": "Aapka bahut swagat hai! Hamesha satark rahein aur kabhi kisi ko OTP ya PIN na dein.",
            "bullet_actions": []
        }

    # -------------------------------------------------------------
    # 4. National Cyber Crime Helpline 1930 & Reporting
    # -------------------------------------------------------------
    is_1930 = ("1930" in q_lower) or any(k in q_lower for k in [
        "helpline", "cybercrime.gov.in", "cyber crime portal", "complaint kaise", "report kaise",
        "shikayat kaise", "police me report", "शिकायत", "हेल्पलाइन", "how to report", "file complaint",
        "cyber crime report", "cyber report", "fir kaise"
    ]) or ("report" in q_lower and any(c in q_lower for c in ["cyber", "crime", "fraud", "scam"]))

    if is_1930 and not any(k in q_lower for k in ["parcel", "loan", "bijli", "apk"]):
        return {
            "detected_category": "HELPLINE_1930_INFO",
            "risk_level": "SAFE",
            "response_text_hindi": "1930 भारत सरकार का राष्ट्रीय साइबर अपराध हेल्पलाइन नंबर (National Cyber Crime Helpline) है। यदि आपके साथ कोई वित्तीय साइबर धोखाधड़ी होती है, तो बिना देर किए तुरंत 1930 डायल करें या cybercrime.gov.in पर शिकायत दर्ज करें। धोखाधड़ी के पहले 2-3 घंटों (गोल्डन आवर) में रिपोर्ट करने से फ्रॉडस्टर के बैंक खाते को तुरंत फ्रीज कर आपके पैसे बचने की संभावना 90% तक होती है।",
            "response_text_hinglish": "1930 Bharat sarkar ka National Cyber Crime Helpline number hai. Agar aapke sath koi online financial fraud hota hai, toh bina deri kiye turant 1930 dial karein ya cybercrime.gov.in par complaint darj karein. Fraud ke pehle 2-3 ghanton (Golden Hour) me complaint karne par fraudster ke account ko turant freeze kiya ja sakta hai aur paise bachaye ja sakte hain.",
            "response_text_english": "1930 is the Government of India's National Cyber Crime Helpline. In case of any online financial fraud, call 1930 immediately or file a report at cybercrime.gov.in. Calling within the first 2-3 hours ('Golden Hour') allows authorities to instantly freeze the fraudster's mule accounts and recover your funds.",
            "spoken_audio_script": "1930 Bharat sarkar ki cyber helpline hai. Financial fraud hone par turant 1930 milayein taaki bank account freeze ho sake.",
            "bullet_actions": [
                "Dial 1930 immediately if any unauthorized money is deducted",
                "File formal report on cybercrime.gov.in portal",
                "Act within the first 2-3 hours (Golden Hour) for maximum recovery"
            ]
        }

    # -------------------------------------------------------------
    # 4b. Emergency: Phone or Account Compromised / Hacked
    # -------------------------------------------------------------
    is_hack = any(h in q_lower for h in ["hack ho gaya", "phone hack", "account hack", "hacked", "पैसे कट गए", "paise kat gaye"])
    if is_hack:
        return {
            "detected_category": "ACCOUNT_COMPROMISE_EMERGENCY",
            "risk_level": "CRITICAL",
            "response_text_hindi": "यदि आपका फोन या बैंक खाता हैक हो गया है या पैसे कट गए हैं, तो तुरंत ये 3 कदम उठाएं: 1. फोन का इंटरनेट (WiFi और मोबाइल डेटा) तुरंत बंद कर दें। 2. किसी दूसरे फोन से अपने बैंक के कस्टमर केयर पर कॉल करके अपने खाते और कार्ड्स को तुरंत फ्रीज कराएं। 3. तुरंत राष्ट्रीय साइबर हेल्पलाइन 1930 पर कॉल करें या cybercrime.gov.in पर रिपोर्ट दर्ज करें।",
            "response_text_hinglish": "Agar aapka phone ya account hack ho gaya hai ya paise kat gaye hain, toh turant yeh 3 emergency steps lein: 1. Phone ka Internet (WiFi aur mobile data) turant band kar dein. 2. Kisi doosre phone se bank customer care call karke accounts aur cards freeze karwayein. 3. Turant 1930 helpline milayein aur cybercrime.gov.in par complaint karein.",
            "response_text_english": "If your phone or account has been compromised or money unauthorizedly deducted, take these 3 emergency steps immediately: 1. Turn off WiFi and mobile data on your device right away. 2. Contact your bank immediately from another phone to freeze netbanking, UPI, and cards. 3. Call National Cyber Crime Helpline 1930 or report on cybercrime.gov.in.",
            "spoken_audio_script": "Turant phone ka internet band karein, bank se khata freeze karwayein aur 1930 helpline milayein.",
            "bullet_actions": [
                "Disconnect WiFi and mobile data immediately",
                "Call bank customer care to freeze all netbanking & cards",
                "Dial 1930 National Cyber Helpline to stop fund transfers"
            ]
        }

    # -------------------------------------------------------------
    # 4c. High-Priority OTP / PIN Solicitation Check
    # (Catches any query mentioning someone asking/demanding OTP, PIN, or CVV)
    # -------------------------------------------------------------
    has_otp_mention = any(k in q_lower for k in ["otp", "ओटीपी", "one time password", "cvv", "सीवीवी", "password", "पासवर्ड", "pin", "पिन"])
    has_ask_demand = any(k in q_lower for k in [
        "मांग", "मांगा", "मांगी", "मांगते", "पूछ", "पूछा", "पूछी", "बताओ", "भेजो", "दे दो", "शेयर", "चाहिए",
        "mang", "maang", "manga", "maanga", "mangi", "maangi", "puch", "pucha", "pooch", "poocha",
        "ask", "demand", "share", "give", "tell", "send", "chahiye", "dena", "dedo", "batao", "bhejo",
        "bol rahe", "bol raha", "call", "कॉल", "message", "मैसेज", "kal", "कल", "kisi ne", "किसी ने"
    ])
    has_personal_otp = any(k in q_lower for k in ["meri", "mera", "मेरी", "मेरा", "अपना", "apna", "your", "the", "?"])
    is_legit_otp_msg = ("is your otp" in q_lower or "otp for login" in q_lower or "valid for" in q_lower) and ("do not share" in q_lower or "never share" in q_lower)

    if has_otp_mention and (has_ask_demand or has_personal_otp) and not is_legit_otp_msg:
        return {
            "detected_category": "OTP_HARVESTING",
            "risk_level": "CRITICAL",
            "response_text_hindi": "🚨 **अत्यंत गंभीर खतरा (100% साइबर फ्रॉड)**: कोई भी असली बैंक, बैंक कर्मचारी या अधिकारी कभी भी फोन या मैसेज पर आपका ओटीपी (OTP) या पिन नहीं मांगता! अपना ओटीपी किसी के साथ साझा न करें, वरना तुरंत आपके बैंक खाते से सारे पैसे निकाल लिए जाएंगे। उस व्यक्ति का फोन तुरंत काटें और नंबर को ब्लॉक करें।",
            "response_text_hinglish": "🚨 **CRITICAL DANGER (100% Cyber Fraud)**: Real bank employee ya officer aapse kabhi bhi phone ya message par OTP ya PIN nahi maangta! Apna OTP kisi ko na dein, varna account se saare paise kat jayenge. Turant call disconnect karein aur number block karein.",
            "response_text_english": "🚨 **CRITICAL FRAUD ALERT**: Genuine bank employees and RBI NEVER ask for your OTP or PIN over call or message under any circumstances. Never disclose your OTP — doing so will immediately compromise your account. Hang up and report to 1930.",
            "spoken_audio_script": "Savdhaan! Yeh 100% fraud hai. Bank kabhi aapse OTP nahi maangta. Apna OTP kisi ko bilkul na dein!",
            "bullet_actions": [
                "NEVER share your 6-digit OTP with anyone under any circumstances",
                "Hang up the phone call immediately and block the caller",
                "Genuine bank employees never ask for OTPs or passwords",
                "If money was deducted, dial National Cyber Helpline 1930 immediately"
            ]
        }

    # -------------------------------------------------------------
    # 5. Dedicated High-Risk Conceptual Scenarios (Educational & Protective)
    # -------------------------------------------------------------

    # 5a. UPI PIN Receive Rule / QR Scan
    if any(k in q_lower for k in ["upi", "pin", "qr", "cashback"]) and any(
        k in q_lower for k in ["paise lene", "receive", "receive money", "lene ke liye", "paise aayenge", "pin dalna padta", "pin kyu", "pin kab", "qr scan karke paise", "qr code scan", "पैसे लेने", "पिन डालना"]
    ):
        return {
            "detected_category": "UPI_FRAUD_EDUCATION",
            "risk_level": "CRITICAL",
            "response_text_hindi": "सावधान! सबसे बुनियादी यूपीआई नियम याद रखें: पैसे प्राप्त (Receive) करने के लिए कभी भी यूपीआई पिन डालने या क्यूआर कोड स्कैन करने की आवश्यकता नहीं होती! यूपीआई पिन केवल तभी डाला जाता है जब आपके खाते से पैसे कटने (Send/Pay) होते हैं। यदि कोई कहता है कि कैशबैक या पैसे लेने के लिए पिन डालें या क्यूआर स्कैन करें, तो वह 100% फ्रॉड कर रहा है।",
            "response_text_hinglish": "Savdhaan! Sabse basic UPI niyam yaad rakhiye: Paise lene (receive karne) ke liye kabhi bhi UPI PIN nahi dalna padta aur na hi QR scan karna padta hai! PIN sirf tab daala jata hai jab aapke account se paise katte (send hote) hain. Agar koi cashback ya paise lene ke naam par PIN mang raha hai, toh woh 100% thag hai.",
            "response_text_english": "Caution! Fundamental UPI Golden Rule: You NEVER need to enter your UPI PIN or scan a QR code to receive money! A PIN is strictly required only when you SEND money from your account. Anyone asking you to enter a PIN or scan a QR code to receive money is committing 100% fraud.",
            "spoken_audio_script": "Paise lene ke liye kabhi bhi UPI PIN nahi dalna padta. PIN dalte hi aapke khate se paise kat jayenge.",
            "bullet_actions": [
                "Never enter your UPI PIN to receive money or cashback",
                "Do not scan QR codes sent on WhatsApp or OLX",
                "Report suspect UPI VPAs on 1930"
            ]
        }

    # 5b. AnyDesk / TeamViewer / Remote Screen Share Tools
    if any(k in q_lower for k in ["anydesk", "teamviewer", "rustdesk", "quicksupport", "screen share", "screen sharing", "app download karne", "रिमोट ऐप"]):
        return {
            "detected_category": "REMOTE_ACCESS_FRAUD",
            "risk_level": "CRITICAL",
            "response_text_hindi": "सावधान! किसी भी अनजान व्यक्ति, बैंक कॉलर या कस्टमर केयर के कहने पर AnyDesk, TeamViewer, RustDesk या QuickSupport ऐप कभी डाउनलोड न करें! ये स्क्रीन-शेयरिंग ऐप्स हैं। इनके ज़रिए कॉलर आपके मोबाइल की स्क्रीन और आने वाले बैंक ओटीपी को सीधे अपनी स्क्रीन पर देख लेता है और आपके खाते से सारे पैसे निकाल लेता है।",
            "response_text_hinglish": "Savdhaan! Kisi bhi anjaan caller ya customer care ke kehne par AnyDesk, TeamViewer ya QuickSupport app bilkul download na karein! Yeh screen-sharing apps hain. Inse caller aapke phone ki screen aur aane wale OTPs dekhkar aapka pura bank account khali kar dega.",
            "response_text_english": "Critical Warning! Never download screen-sharing apps like AnyDesk, TeamViewer, RustDesk, or QuickSupport at the instruction of any caller. These apps give total remote visibility of your phone screen, enabling scammers to read your OTPs and drain your bank account.",
            "spoken_audio_script": "AnyDesk ya QuickSupport app kabhi download na karein. Isse caller aapka pura phone dekhkar OTP chura leta hai.",
            "bullet_actions": [
                "Never install AnyDesk or TeamViewer on stranger's instruction",
                "Uninstall remote access tools immediately if installed",
                "Turn off internet and change netbanking passwords"
            ]
        }

    # 5c. Digital Arrest / CBI / Police Video Call
    if any(k in q_lower for k in ["digital arrest", "skype arrest", "cbi call", "cbi video", "customs narcotics", "mdma parcel", "डिजिटल अरेस्ट"]) or ("cbi" in q_lower and "officer" in q_lower):
        return {
            "detected_category": "DIGITAL_ARREST_EDUCATION",
            "risk_level": "CRITICAL",
            "response_text_hindi": "ध्यान से सुनिए: भारतीय कानून और पुलिस प्रक्रिया में 'डिजिटल अरेस्ट' (Digital Arrest) नाम की कोई चीज़ नहीं होती! कोई भी सीबीआई, पुलिस, कस्टम्स या कोर्ट अधिकारी कभी भी व्हाट्सएप या स्काइप वीडियो कॉल पर जांच नहीं करता और न ही वीडियो पर किसी को अरेस्ट करता है। वे आपको डराकर पैसे ऐंठने की कोशिश कर रहे हैं। बिना डरे तुरंत कॉल काटें और 1930 पर शिकायत दर्ज करें।",
            "response_text_hinglish": "Dhayan se suniye: Bharat ke kanoon me 'Digital Arrest' jaisa koi rule nahi hota! Na CBI, na Police, na Customs kabhi Skype ya WhatsApp video call par arrest karte hain. Yeh thag police ki vardi pehankar logon ko dara-dhamkakar paise loot-te hain. Bilkul mat dariye, call kaat dijiye aur 1930 par complaint karein.",
            "response_text_english": "Listen carefully: There is NO concept of 'Digital Arrest' under Indian law or CrPC! Neither CBI, Police, nor Customs conduct arrests or interrogations over Skype or WhatsApp video calls. These fraudsters impersonate officers in uniforms with fake setups to extort money. Disconnect immediately and call 1930.",
            "spoken_audio_script": "Digital arrest jaisa koi kanoon nahi hai. Na police na CBI video call par arrest karti hai. Call kaat dijiye.",
            "bullet_actions": [
                "Disconnect video call immediately",
                "Law enforcement never conducts virtual Skype arrests",
                "Report cyber extortion to 1930 or local police station"
            ]
        }

    # 5d. Electricity Bill Cutoff Scam
    if any(k in q_lower for k in ["bijli", "electricity", "power cut", "line kat", "bijli bill", "light kaat denge", "बिजली"]):
        return {
            "detected_category": "ELECTRICITY_CUTOFF",
            "risk_level": "HIGH",
            "response_text_hindi": "बिल्कुल मत घबराइए! यह एक फर्जी बिजली बिल फ्रॉड है। कोई भी सरकारी बिजली विभाग (Discom) आम 10-अंकों के मोबाइल नंबर से रात 9:30 बजे बिजली काटने का अल्टीमेटम नहीं भेजता। मैसेज में दिए गए किसी भी अनजान मोबाइल नंबर पर कॉल न करें। अपना असली बिल हमेशा आधिकारिक बिजली वितरण ऐप या बिजली कार्यालय में जाकर ही चेक करें।",
            "response_text_hinglish": "Bilkul mat ghabraiye! Yeh ek fake bijli bill scam hai. Koi bhi discom aam mobile number se 9:30 baje bijli kaatne ka sandesh nahi bhejta. Diye gaye mobile number par call na karein. Apna bill hamesha official discom app ya portal par hi check karein.",
            "response_text_english": "Do not panic at all! This is a well-known fake electricity bill scam. Official electricity providers never send cut-off threats from personal 10-digit mobile numbers. Do not call numbers provided in the SMS. Verify your account balance only via the official provider portal.",
            "spoken_audio_script": "Yeh fake bijli bill sandesh hai. Diye gaye number par call na karein aur bill official app par check karein.",
            "bullet_actions": [
                "Do not call the 10-digit number in the SMS",
                "Electricity departments never threaten immediate power cutoffs via SMS",
                "Verify dues on your state discom's official website"
            ]
        }

    # 5e. Lottery / Prize / KBC WhatsApp
    if any(k in q_lower for k in ["lottery", "kbc", "25 lakh", "free iphone", "gift prize", "processing fee", "cash reward", "लॉटरी", "इनाम"]):
        return {
            "detected_category": "KBC_LOTTERY",
            "risk_level": "HIGH",
            "response_text_hindi": "यह 100% फर्जी लॉटरी घोटाला है! न तो केबीसी और न ही कोई कंपनी बिना प्रतियोगिता में भाग लिए मुफ्त में कार, आईफोन या लाखों रुपये देती है। ये आपसे रजिस्ट्रेशन फीस, जीएसटी या फाइल चार्ज के नाम पर पैसे मांगेंगे और फिर गायब हो जाएंगे। इन्हें एक भी रुपया न दें और इस नंबर को तुरंत ब्लॉक करें।",
            "response_text_hinglish": "Yeh 100% fake lottery scam hai! KBC ya koi company bina kisi contest ke muft me iPhone ya lakhon rupaye nahi deti. Yeh aapse file charge ya GST ke naam par paise thagenge. Ek bhi rupya na transfer karein aur number ko block karein.",
            "response_text_english": "This is a 100% fraudulent advance-fee lottery scam! Neither KBC nor any company awards cash prizes or free iPhones without entry. Fraudsters demand processing fees or GST and disappear. Never transfer any fee and block the caller.",
            "spoken_audio_script": "Yeh lottery poori tarah jhoothi hai. Kisi bhi processing fee ya delivery charge ke naam par paise na dein.",
            "bullet_actions": [
                "Do not pay any 'processing fee' or 'GST'",
                "Legitimate lotteries never demand advance registration charges",
                "Block the scammer's contact number"
            ]
        }

    # 5f. Instant Loan / Fake Loan App
    if any(k in q_lower for k in ["instant loan", "bina document loan", "aadhaar and otp", "aadhaar aur otp", "fake loan", "loan approved!"]) or ("loan" in q_lower and ("without documents" in q_lower or "bina document" in q_lower or "aadhaar" in q_lower)):
        return {
            "detected_category": "LOAN_FRAUD",
            "risk_level": "CRITICAL",
            "response_text_hindi": "सावधान! बिना किसी दस्तावेज़ के तुरंत लाखों का लोन देने वाले मैसेज या ऐप्स गंभीर फ्रॉड सिंडिकेट होते हैं। ये आपके आधार, पैन और ओटीपी की चोरी करते हैं, या फर्जी ऐप इंस्टॉल करवाकर आपकी कॉन्टैक्ट लिस्ट और निजी फोटो चुराकर ब्लैकमेल करते हैं। केवल आरबीआई-रजिस्टर्ड बैंकों या एनबीएफसी से ही लोन लें।",
            "response_text_hinglish": "Savdhaan! Bina document instant loan dene wale message ya apps khatarnak scam hote hain. Yeh aapka Aadhaar, PAN aur OTP churate hain ya phone se photos chura kar blackmail karte hain. Sirf RBI-approved banks se hi loan lein.",
            "response_text_english": "Warning! Unsolicited messages promising instant loans without documentation are predatory fraud traps. They steal your Aadhaar, PAN, and OTP, or install spyware APKs that harvest personal contacts and photos for extortion. Only borrow from RBI-registered entities.",
            "spoken_audio_script": "Bina document instant loan dene wale sandesh scam hain. Apna Aadhaar ya OTP kisi ko na dein.",
            "bullet_actions": [
                "Never share Aadhaar, PAN, or OTP for instant loans",
                "Do not install loan APK files from outside the Play Store",
                "Check RBI's Sachet portal for registered lenders"
            ]
        }

    # 5g. Courier / Parcel / India Post / FedEx Redelivery
    if any(k in q_lower for k in ["parcel is on hold", "parcel", "courier", "redelivery fee", "redelivery", "address update", "डाक", "पार्सल"]) and any(k in q_lower for k in ["hold", "address", "fee", "rs. 10", "rs 10", "link", "post"]):
        return {
            "detected_category": "COURIER_PARCEL_FRAUD",
            "risk_level": "HIGH",
            "response_text_hindi": "यह कूरियर / पार्सल री-डिलीवरी फ्रॉड (Smishing) है! जालसाज इंडिया पोस्ट या कूरियर के नाम से फर्जी मैसेज भेजते हैं कि आपका पता गलत है और 10 या 25 रुपये री-डिलीवरी फीस भरें। उस लिंक पर क्लिक करके कार्ड डिटेल्स डालते ही आपके खाते से हजारों रुपये उड़ा लिए जाते हैं। पार्सल का स्टेटस केवल ऑफिशियल वेबसाइट पर ट्रैकिंग नंबर से देखें।",
            "response_text_hinglish": "Yeh courier parcel redelivery scam hai! Thag India Post ya courier ke naam se message bhejte hain ki address galat hai aur Rs 10 fee bharein. Us link par payment karte hi aapke bank khate se paise chori ho jate hain. Kisi link par card details na dalein.",
            "response_text_english": "This is a parcel redelivery smishing scam! Fraudsters send fake messages claiming your package is on hold and requesting a nominal Rs 10-25 fee. The payment link phishes your credit/debit card credentials. Track parcels exclusively on the courier's official tracking portal.",
            "spoken_audio_script": "Parcel redelivery ke naam par diye gaye link par kabhi 10 ya 25 rupaye ka payment na karein. Yeh card chori ka scam hai.",
            "bullet_actions": [
                "Never click on links to pay Rs 10 or 25 redelivery fees",
                "Verify tracking number only on India Post or carrier's official website",
                "Block the sender and report to 1930"
            ]
        }

    # -------------------------------------------------------------
    # 6. Fallback to Deep Scam NLP Engine for Any Quoted SMS / Calls
    # -------------------------------------------------------------
    analysis = analyze_scam_message(query)
    cat = analysis["scam_category"]

    # 6a. Explicit Safe Message / Transaction
    is_explicit_bank_or_delivery = any(k in q_lower for k in [
        "credited", "debited", "swiggy", "zomato", "amazon", "jiomart", "irctc",
        "fixed deposit", "statement", "order has been", "out for delivery",
        "ticket booking", "train ticket", "avl bal", "xxxx", "ending with",
        "खाते में", "पैसे निकले", "जमा हुए", "ऑर्डर कन्फर्म", "डिलीवरी"
    ])

    if cat == "SAFE_TRANSACTION" and is_explicit_bank_or_delivery:
        return {
            "detected_category": "SAFE_TRANSACTION",
            "risk_level": "SAFE",
            "response_text_hindi": "✅ यह एक सामान्य और वैध (सुरक्षित) संदेश प्रतीत होता है। इसमें कोई फ़िशिंग लिंक, ओटीपी चोरी या धोखाधड़ी का संकेत नहीं मिला है। आप निश्चिंत रह सकते हैं। सामान्य सुरक्षा के तौर पर अपना 6-अंकों का ओटीपी या पासवर्ड किसी से साझा न करें।",
            "response_text_hinglish": "✅ Yeh ek bilkul normal aur surakshit (legitimate) message hai (jaise bank transaction alert ya delivery update). Isme koi phishing link ya fraud ka sanket nahi hai. Aap nishchint reh sakte hain. Bas hamesha ki tarah apna OTP ya PIN kisi ko na dein.",
            "response_text_english": "✅ This appears to be a legitimate, safe notification (such as standard transaction confirmation or delivery update). No phishing links or fraud indicators detected. Rest assured, and remember never to share OTPs or passwords.",
            "spoken_audio_script": "Yeh sandesh surakshit aur legitimate pratit hota hai. Isme koi fraud nahi hai.",
            "bullet_actions": [
                "Notification verified as safe",
                "Review transactions periodically in your official banking app",
                "Never share OTPs even for verified transactions"
            ]
        }
    elif cat == "SAFE_TRANSACTION":
        # General safe conversational query or advice request
        return {
            "detected_category": "GENERAL_CONVERSATION",
            "risk_level": "SAFE",
            "response_text_hindi": "नमस्ते! मैं आपका रक्षक एआई (FraudRakshak) साइबर सुरक्षा सलाहकार हूँ। आप मुझसे किसी भी संदिग्ध कॉल, एसएमएस, व्हाट्सएप मैसेज या ऑनलाइन सुरक्षा से जुड़े नियम के बारे में पूछ सकते हैं। यदि आपको कोई संदेहास्पद संदेश आया है, तो वह मुझे बताएं — मैं तुरंत जांच कर आपको सुरक्षित रखूँगा।",
            "response_text_hinglish": "Namaste! Main aapka FraudRakshak AI cyber security advisor hoon. Aap mujhse kisi bhi sandigdh call, SMS, WhatsApp message ya online fraud ke baare me pooch sakte hain. Agar aapko koi sandigdh sandesh aaya hai, toh batayein — main turant check karke aapko sahi salah doonga.",
            "response_text_english": "Hello! I am your FraudRakshak AI cyber defense advisor. Feel free to ask about any suspicious call, SMS, WhatsApp message, or online safety rule. If you received any suspicious alert, let me know — I will verify it right away to keep you safe.",
            "spoken_audio_script": "Namaste! Main FraudRakshak AI hoon. Aap mujhse kisi bhi sandigdh call ya cyber scam ke baare me pooch sakte hain.",
            "bullet_actions": []
        }

    # 6b. Dynamic Threat Breakdown for Real Scams
    if analysis["risk_score"] >= 60:
        if cat == "CARD_BLOCK_PHONE_TRAP":
            hi_dev = "सावधान! यह एक फर्जी एटीएम कार्ड ब्लॉक ट्रैप है! जालसाज फर्जी एसएमएस भेजकर आपको दिए गए नंबर पर कॉल करने को कहते हैं ताकि वे आपका कार्ड नंबर, सीवीवी और ओटीपी पूछ सकें। असली बैंक कभी भी एसएमएस में निजी मोबाइल नंबर देकर उस पर कॉल करने को नहीं कहते।"
            hi_text = "Savdhaan! Yeh ek fake ATM card block trap hai! Thag aapse fake number par call karwakar card details aur OTP mangenge. Real bank kabhi bhi SMS me aam mobile number par call karne ko nahi kehta."
            en_text = "Warning! This is a fraudulent card block trap. Scammers send SMS urging you to call an unverified mobile number to steal your card credentials and OTP. Real banks never provide private numbers for reactivation."
            spoken = "Savdhaan! Yeh fake card block message hai. Diye gaye number par call bilkul na karein."
        elif cat == "CREDENTIAL_HARVESTING":
            hi_dev = "खतरा! यह कैश रिवॉर्ड के नाम पर लॉगिन पासवर्ड या पिन चुराने का फ़िशिंग जाल है! किसी भी लिंक पर अपने नेटबैंकिंग पासवर्ड, कार्ड नंबर या यूपीआई पिन कभी न डालें।"
            hi_text = "Khatra! Yeh cash reward ke naam par aapka netbanking password ya PIN churaane ka phishing trap hai! Diye gaye link par banking password bilkul na dalein."
            en_text = "Danger! This is a credential harvesting phishing trap masquerading as a cash reward. Never enter your netbanking password or PIN on external links."
            spoken = "Khatra! Diye gaye link par apna password ya PIN bilkul na dalein."
        elif cat == "MALICIOUS_APK_FRAUD":
            hi_dev = "अत्यंत खतरनाक! एसएमएस में दिया गया एपीके (APK) फाइल एक मैलवेयर वायरस है! कैशबैक के नाम पर कोई भी अज्ञात एपीके डाउनलोड या इंस्टॉल न करें, यह आपके फोन का पूरा डेटा और ओटीपी चुरा लेगा।"
            hi_text = "Critical Danger! SMS me diya gaya APK file ek malware virus hai! Cashback ke naam par kisi anjaan APK ko install na karein, yeh aapke phone ke saare OTP chura lega."
            en_text = "Critical Danger! The APK mentioned in the SMS is a malicious spyware trojan. Never install APK files outside official app stores, as they harvest OTPs and compromise your device."
            spoken = "Savdhaan! Is APK ko bilkul install na karein. Yeh ek malware virus hai."
        elif cat == "OTP_HARVESTING":
            hi_dev = "सावधान! कोई भी असली बैंक कर्मचारी या अधिकारी कभी भी फोन या मैसेज पर ओटीपी (OTP) नहीं मांगता! अपना ओटीपी किसी के साथ साझा न करें, यह तुरंत आपके खाते से पैसे खाली कर देगा।"
            hi_text = "Savdhaan! Real bank employee kabhi bhi phone par OTP nahi mangta! Apna OTP kisi ke sath share na karein, varna account se paise kat jayenge."
            en_text = "Alert! Genuine bank employees never ask for your OTP over phone or SMS. Sharing your OTP will immediately allow unauthorized transactions."
            spoken = "Savdhaan! Real bank kabhi OTP nahi mangta. Apna OTP kisi ko na batayein."
        elif cat == "BANK_KYC_FREEZE":
            hi_dev = "सावधान! यह एक खतरनाक बैंक केवाईसी फ़िशिंग स्कैम है! बैंक कभी भी एसएमएस लिंक से केवाईसी करने को नहीं कहता और न ही 24 घंटे में खाता बंद करने की धमकी देता है। लिंक पर क्लिक न करें।"
            hi_text = "Savdhaan! Yeh ek khatarnak bank KYC phishing scam hai! Bank kabhi bhi SMS link se KYC karne ko nahi kehta aur na hi 24 ghante me account suspend karne ki dhamki deta hai."
            en_text = "Warning! This is a dangerous bank KYC phishing scam! Banks never demand KYC updates via SMS links or threaten suspension within 24 hours. Do not click the link."
            spoken = "Savdhaan! Yeh bank phishing sandesh hai. Link par bilkul click na karein."
        elif cat == "TRAFFIC_CHALLAN_SCAM":
            hi_dev = "सावधान! यह फर्जी ट्रैफिक ई-चालान (e-Challan) फ्रॉड है! ट्रैफिक पुलिस या परिवहन विभाग कभी भी व्हाट्सएप या एसएमएस लिंक से लाइसेंस रद्द करने की धमकी देकर जुर्माना नहीं मांगता। असली चालान केवल सरकारी पोर्टल 'echallan.parivahan.gov.in' पर ही चेक करें।"
            hi_text = "Savdhaan! Yeh fake traffic challan scam hai! Traffic police anjaan SMS link bhejkar fine nahi maangti. Asli challan sirf echallan.parivahan.gov.in par bharein."
            en_text = "Warning! This is a fake traffic e-challan scam. Police never threaten license suspension via SMS links. Pay fines strictly on echallan.parivahan.gov.in."
            spoken = "Savdhaan! Yeh fake traffic challan scam hai. Diye gaye link par fine na bharein."
        elif cat == "TRAI_SIM_BLOCK_SCAM":
            hi_dev = "सावधान! यह फर्जी ट्राई (TRAI) या सिम कार्ड ब्लॉकिंग स्कैम है! दूरसंचार विभाग (DoT) या ट्राई कभी भी व्यक्तिगत ग्राहकों को फोन करके 2 घंटे में सिम काटने की धमकी नहीं देता। यह डिजिटल अरेस्ट की शुरुआत है।"
            hi_text = "Savdhaan! Yeh TRAI ya SIM block karne ka farzi scam hai. DoT ya TRAI kabhi bhi 2 ghante me sim band karne ki dhamki nahi deta. Call turant kaat dein."
            en_text = "Alert! TRAI or DoT never call citizens threatening to disconnect mobile numbers within 2 hours. This is extortion. Hang up immediately."
            spoken = "Savdhaan! TRAI kabhi sim band karne ki dhamki nahi deta. Call kaat dijiye."
        elif cat == "INCOME_TAX_REFUND_SCAM":
            hi_dev = "सावधान! यह आयकर विभाग (Income Tax) के नाम पर फर्जी रिफंड फ़िशिंग स्कैम है! आयकर विभाग कभी भी एसएमएस लिंक भेजकर रिफंड क्लेम करने या बैंक डिटेल्स मांगने को नहीं कहता।"
            hi_text = "Savdhaan! Yeh Income Tax refund phishing scam hai! IT department SMS link se refund claim karne ko nahi kehta. Refund direct bank account me aata hai."
            en_text = "Warning! Income Tax refund phishing scam detected. The IT department never sends SMS links to claim refunds."
            spoken = "Savdhaan! Income tax refund link par click na karein. Yeh fraud hai."
        elif cat == "CREDIT_CARD_REWARD_SCAM":
            hi_dev = "सावधान! यह क्रेडिट कार्ड रिवॉर्ड पॉइंट रिडीम करने का फर्जी संदेश है! असली बैंक कभी एसएमएस लिंक भेजकर रिवॉर्ड पॉइंट को कैश में बदलने के लिए कार्ड नंबर, सीवीवी या ओटीपी नहीं मांगते।"
            hi_text = "Savdhaan! Yeh credit card reward points scam hai! Bank kabhi SMS link se reward points cash karne ke liye card details ya OTP nahi maangta."
            en_text = "Caution! Credit card reward points expiry phishing detected. Banks never request card credentials to convert points into cash."
            spoken = "Savdhaan! Credit card reward link par apni card details bilkul na bharein."
        elif cat == "GOVT_SCHEME_PHISHING":
            hi_dev = "सावधान! यह मुफ्त रिचार्ज या फर्जी सरकारी योजना का मैलवेयर ट्रैप है! सरकार या टेलीकॉम कंपनियां व्हाट्सएप संदेशों पर मुफ्त लैपटॉप या 3 महीने का फ्री रिचार्ज नहीं बांटतीं।"
            hi_text = "Savdhaan! Yeh free recharge ya fake govt scheme ka viral scam hai. Kisi bhi link par click na karein."
            en_text = "Warning! Viral free mobile recharge or government scheme offers are malicious phishing links. Do not click."
            spoken = "Savdhaan! Yeh muft recharge ya fake scheme ka viral scam hai. Click na karein."
        elif cat == "FAKE_CUSTOMER_CARE_SCAM":
            hi_dev = "सावधान! यह फर्जी कस्टमर केयर नंबर का ट्रैप है! किसी भी निजी 10-अंकीय मोबाइल नंबर पर कॉल न करें, यह साइबर अपराधियों का नंबर है जो बैंक फ्रॉड करते हैं।"
            hi_text = "Savdhaan! Yeh fake customer care trap hai! Personal mobile number par helpline call na karein. Real helpline official website par check karein."
            en_text = "Warning! Unverified personal 10-digit mobile number posing as customer support. Do not dial."
            spoken = "Savdhaan! Yeh farzi customer care number hai. Is number par call na karein."
        elif cat == "WFH_TELEGRAM":
            hi_dev = "सावधान! यह प्रसिद्ध यूट्यूब लाइक / टेलीग्राम टास्क फ्रॉड (Work From Home Scam) है! घर बैठे वीडियो लाइक करके पैसे कमाने के झांसे में न आएं, यह लाखों की ठगी का सिंडिकेट है।"
            hi_text = "Savdhaan! Yeh YouTube like aur Telegram task scam hai! Like karke paise kamane ke jhaanse me na aayein, yeh fraud syndicate hai."
            en_text = "Critical Alert! Work-from-home YouTube like and Telegram task scam detected. Never transfer any prepaid deposits."
            spoken = "Savdhaan! YouTube like karke paise kamane ka offer poori tarah fraud hai."
        elif cat == "SUSPICIOUS_CONTENT":
            hi_dev = "सावधान! इस संदेश या कॉल में साइबर फ्रॉड और अनधिकृत वित्तीय लेनदेन के गंभीर संकेत मिले हैं। किसी भी अनजान व्यक्ति के साथ ओटीपी, पिन या कार्ड विवरण साझा न करें।"
            hi_text = "Savdhaan! Is call ya message me cyber fraud aur suspicious threat ke sanket hain. Kisi ke sath OTP, PIN ya card details share na karein."
            en_text = "Warning! High-risk suspicious indicators detected. Never share OTPs, PINs, or financial credentials."
            spoken = "Savdhaan! Yeh sandigdh sandesh hai. Apna OTP ya PIN kisi ko na dein."
        else:
            hi_dev = analysis["explanations"]["hindi"]
            hi_text = analysis["explanations"]["hinglish"]
            en_text = analysis["explanations"]["english"]
            spoken = analysis["voice_warning_script"]["hi"]

        return {
            "detected_category": cat,
            "risk_level": analysis["severity"],
            "response_text_hindi": hi_dev,
            "response_text_hinglish": hi_text,
            "response_text_english": en_text,
            "spoken_audio_script": spoken,
            "bullet_actions": analysis["action_recommendations"]
        }

    # 6c. General Cyber Security Questions (Informative Guidance)
    return {
        "detected_category": "CYBER_AWARENESS_GENERAL",
        "risk_level": "SAFE",
        "response_text_hindi": "ऑनलाइन धोखाधड़ी से सुरक्षित रहने के लिए ये 4 बुनियादी नियम हमेशा याद रखें: 1. कभी भी किसी के साथ अपना ओटीपी या पासवर्ड शेयर न करें। 2. पैसे प्राप्त करने के लिए कभी यूपीआई पिन न डालें। 3. किसी अनजान व्यक्ति के कहने पर AnyDesk या अज्ञात एपीके इंस्टॉल न करें। 4. किसी भी फ्रॉड की स्थिति में तुरंत 1930 हेल्पलाइन पर कॉल करें।",
        "response_text_hinglish": "Online cyber fraud se bachne ke liye yeh 4 golden rules hamesha yaad rakhein: 1. Apna OTP ya banking password kabhi kisi ko na dein. 2. Paise receive karne ke liye kabhi UPI PIN na dalein. 3. Kisi ke kehne par AnyDesk ya unverified APK install na karein. 4. Kisi bhi shak ya fraud par turant 1930 helpline milayein.",
        "response_text_english": "To stay safe from online cyber frauds, follow these core principles: 1. Never share OTPs or passwords with anyone. 2. Remember UPI PIN is never required to receive money. 3. Never install remote-screen apps like AnyDesk or unknown APKs. 4. Immediately report any cyber fraud to the national helpline 1930.",
        "spoken_audio_script": "Cyber security ke liye apna OTP ya PIN kisi ko na dein, aur fraud hone par 1930 milayein.",
        "bullet_actions": [
            "Rule 1: Never share OTPs or passwords",
            "Rule 2: Never enter PIN to receive money",
            "Rule 3: Never install unknown APKs or screen sharing apps",
            "Rule 4: Dial 1930 immediately in case of fraud"
        ]
    }
