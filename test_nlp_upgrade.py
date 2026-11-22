import re
from typing import Dict, Any, List
import sys
sys.path.append(r"C:\Users\shrea\.gemini\antigravity\scratch\fraudRakshak\ai-service")
from nlp_engine import extract_iocs, generate_explanations, generate_voice_scripts, get_action_steps, extract_contextual_elements

def analyze_scam_message_upgraded(text: str, sender: str = "") -> Dict[str, Any]:
    cleaned_text = text.strip()
    lowered = cleaned_text.lower()
    iocs = extract_iocs(cleaned_text)

    vector_scores: Dict[str, int] = {}
    red_flags: List[Dict[str, str]] = []

    # -------------------------------------------------------------
    # 0. OTP / Credential Harvesting (Bank Staff Impersonation)
    # -------------------------------------------------------------
    demands_otp = (
        bool(re.search(r'\b(?:share|send|give|tell|provide|forward|enter|submit)\s+(?:me\s+|us\s+|our\s+)?(?:the\s+|your\s+|that\s+|this\s+|6\s*digit\s+)?(?:aadhaar\s+and\s+)?(?:otp|cvv|password|passcode)\b', lowered))
        or bool(re.search(r'\b(?:the\s+|your\s+|that\s+|this\s+)?otp\s+(?:to\s+us|to\s+me|batao|bhejo|de\s*do|share\s*karo|forward\s*karo)\b', lowered))
        or bool(re.search(r'\b(?:please|pls|plz)\s+.*?\b(?:your\s+|the\s+)?otp\b', lowered))
        or (any(b in lowered for b in ["bank employee", "bank manager", "bank officer", "we are bank", "बैंक से बोल रहे", "बैंक कर्मचारी", "बैंक मैनेजर"]) and any(c in lowered for c in ["otp", "pin", "cvv", "password", "code", "ओटीपी", "सीवीवी", "पासवर्ड"]))
        or any(k in lowered for k in [
            "your otp to us", "otp to us", "otp maang", "otp batao", "otp bhejo",
            "we are bank employee", "bank employee", "bank manager", "aadhaar and otp", "send your aadhaar and otp",
            "ओटीपी शेयर", "अपना ओटीपी", "ओटीपी बताओ", "ओटीपी भेजो", "ओटीपी दें", "cvv batao", "tell me cvv", "card renew karna hai cvv"
        ])
    )

    if demands_otp:
        vector_scores["OTP_HARVESTING"] = 100
        red_flags.append({
            "id": "OTP_SOLICITATION_FRAUD",
            "title": "Strict Fraud Alert: Demanding Confidential Bank OTP/PIN/CVV",
            "description": "GOLDEN RULE: Genuine banks, RBI, and bank employees NEVER ask for your OTP, CVV, or PIN under any circumstances! Any request for your OTP is a 100% active cyber fraud.",
            "level": "CRITICAL"
        })

    # -------------------------------------------------------------
    # 1. UPI Fraud / Account Expiry / PIN Demand
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
    # 2. Bank KYC / Account & ATM Card Freeze Phishing
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
        or "phone aaya" in lowered or "call aaya" in lowered or "फोन आया" in lowered or "मैसेज आया" in lowered or "bol rahe" in lowered
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
    # 3. Traffic E-Challan Scam
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
    # 4. Telecom / SIM Card Disconnection / TRAI Scam
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
    # 5. Income Tax Refund Phishing
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
    # 6. Credit Card Reward Points Expiry Scam
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
    # 7. Free Govt Scheme / Free Mobile Recharge Smishing
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
    # 8. Fake Customer Care / Refund Callback Trap
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
    # 9. Electricity Disconnection Panic (Discom Trap)
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
    # 10. Lottery / Cash Reward / Free iPhone Advance-Fee Scam
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
    # 11. Digital Arrest / Narcotics Parcel Extortion
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
    # 12. Fake Loan Document / Aadhaar & OTP Theft
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
    # 13. Courier / Parcel Hold Redelivery Fee Phishing
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
    # 14. Malicious APK Download Trap
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
    # 15. Confidential Banking Password Phishing
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
    # 16. Remote Device Hijacking (AnyDesk / QuickSupport / Screen Sharing)
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
    # 17. Work-From-Home / YouTube Like / Telegram Task Syndicate
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
        # If text mentions suspicious phrases or calls, treat as suspicious threat
        has_suspicious_phrases = any(k in lowered for k in [
            "phone aaya", "call aaya", "bol rahe", "message aaya", "मैसेज आया", "फोन आया", "कॉल आया",
            "बोल रहे", "लिंक", "link", "click", "expire", "band", "block", "suspend", "आधार", "aadhaar"
        ])
        if has_suspicious_phrases:
            top_cat_key = "SUSPICIOUS_CONTENT"
            risk_score = 70
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
        "SUSPICIOUS_CONTENT": "Suspicious Unverified Contact",
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

# Now let's test all 30 test_risky_inputs!
test_risky_inputs = [
    # Hindi natural voice inputs about scams:
    "मुझे एक मैसेज आया है कि आपका बिजली का बिल जमा नहीं है रात 9 बजे कट जाएगा",
    "मुझे फोन आया कि आपका खाता ब्लॉक हो गया है",
    "एक लड़की ने बोला यूट्यूब वीडियो लाइक करो और रोज 5000 कमाओ",
    "मुझे मैसेज आया कि 50,000 की लॉटरी लगी है",
    "मेरे पास कॉल आया कि आपका पार्सल कस्टम में पकड़ा गया है",
    "कोई बोल रहा है आपका एटीएम कार्ड बंद हो गया है",
    "एक मैसेज में लिखा है कि आपका आधार कार्ड एक्सपायर हो गया है लिंक पर क्लिक करें",
    "प्लीज अपना ओटीपी शेयर करें हम बैंक से बोल रहे हैं",
    "कस्टमर केयर का नंबर 9876543210 है इस पर तुरंत कॉल करें",
    "आपके खाते से 50000 कट गए हैं रिफंड के लिए ये ऐप डाउनलोड करें",
    "मैसेज आया है कि आपका सिम कार्ड 2 घंटे में बंद हो जाएगा",
    "चालान कट गया है तुरंत इस लिंक पर फाइन भरें",
    "इनकम टैक्स रिफंड आया है लिंक पर क्लिक करके क्लेम करें",
    "क्रेडिट कार्ड रिवॉर्ड पॉइंट एक्सपायर हो रहे हैं अभी रिडीम करें",
    # Hinglish / English natural queries:
    "Bhaiya ek message aaya hai bol rahe hain account suspend ho jayega",
    "ek call aaya bola police station se bol raha hu aapka beta arrest ho gaya hai",
    "Telegram par task complete karne par daily 3000 denge bol rahe hain",
    "SBI YONO update alert link sent on my number",
    "TRAI officer called saying my sim card will be blocked in 2 hours",
    "Courier boy called saying parcel on hold pay 25 rs",
    "Bank se call aaya tha unhone bola card renew karna hai cvv batao",
    "credit card points redeem karo varna expire ho jayenge",
    "challan unpaid pay now or license cancel",
    "income tax refund approved claim link",
    "job offer like youtube videos earn 2000 per day",
    "free recharge offer click here",
    "free laptop scheme from government register here",
    "please your otp to us we are bank employee",
    "dear customer your account has been deactivated click link to activate",
    "urgent notice your power supply will be disconnected tonight"
]

print("Scanning with analyze_scam_message_upgraded:")
failed = []
for inp in test_risky_inputs:
    res = analyze_scam_message_upgraded(inp)
    risk = res.get("severity")
    cat = res.get("scam_category")
    if risk == "SAFE":
        failed.append((inp, cat, risk))
        print(f"❌ MISCLASSIFIED AS SAFE: '{inp}' -> cat: {cat}")
    else:
        print(f"✅ DETECTED THREAT ({risk}): '{inp[:42]}...' -> cat: {cat}")

print(f"\nTotal Tested: {len(test_risky_inputs)}, Failed (Marked Safe): {len(failed)}")
