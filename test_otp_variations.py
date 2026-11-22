import re
from typing import Dict, Any

otp_test_queries = [
    "मुझे कल एक जिसमें वो मेरी ओटीपी मांग।",
    "kal ek call aaya jisme wo meri otp mang raha tha",
    "kisi ne phone karke otp manga",
    "otp maang rahe hain kya karu",
    "ek message me otp mang rahe hain",
    "kya bank manager ko otp dena chahiye?",
    "bank se call aaya otp mang rahe hain",
    "meri otp mang raha hai",
    "otp pooch raha tha",
    "otp mangi",
    "otp chahiye bol rahe hain",
    "please your otp to us we are bank employee",
    "send your aadhaar and otp",
    "bhaiya mujhe ek message aaya jisme meri otp mang rahe hain",
    "kisi ne call karke pin manga",
    "मुझे एक कॉल आया जिसमें वो मुझसे ओटीपी मांग रहे थे"
]

def check_voice_otp_rule(q: str):
    q_lower = q.lower()
    has_otp_mention = any(k in q_lower for k in ["otp", "ओटीपी", "one time password", "cvv", "सीवीवी", "password", "पासवर्ड", "pin", "पिन"])
    has_ask_demand = any(k in q_lower for k in [
        "मांग", "मांगा", "मांगी", "मांगते", "पूछ", "पूछा", "पूछी", "बताओ", "भेजो", "दे दो", "शेयर", "चाहिए",
        "mang", "maang", "manga", "maanga", "mangi", "maangi", "puch", "pucha", "pooch", "poocha",
        "ask", "demand", "share", "give", "tell", "send", "chahiye", "dena", "dedo", "batao", "bhejo",
        "bol rahe", "bol raha", "call", "कॉल", "message", "मैसेज", "kal", "कल", "kisi ne", "किसी ने"
    ])
    has_personal_otp = any(k in q_lower for k in ["meri", "mera", "मेरी", "मेरा", "अपना", "apna", "your", "the", "?"])
    
    # Legit transaction check (e.g., standard verified OTP alert)
    is_legit_alert = ("is your otp" in q_lower or "otp for login" in q_lower or "valid for" in q_lower) and ("do not share" in q_lower or "never share" in q_lower)

    if has_otp_mention and (has_ask_demand or has_personal_otp) and not is_legit_alert:
        return {
            "detected_category": "OTP_HARVESTING",
            "risk_level": "CRITICAL",
            "response_text_hindi": "🚨 **अत्यंत गंभीर खतरा (100% साइबर फ्रॉड)**: कोई भी असली बैंक, बैंक कर्मचारी या अधिकारी कभी भी फोन या मैसेज पर आपका ओटीपी (OTP) या पिन नहीं मांगता! अपना ओटीपी किसी के साथ साझा न करें, वरना तुरंत आपके बैंक खाते से सारे पैसे निकाल लिए जाएंगे।",
            "response_text_hinglish": "🚨 **CRITICAL DANGER (100% Cyber Fraud)**: Real bank employee ya officer aapse kabhi bhi phone ya message par OTP ya PIN nahi maangta! Apna OTP kisi ko na dein, varna account se saare paise kat jayenge."
        }
    return None

print("Testing check_voice_otp_rule:")
for q in otp_test_queries:
    res = check_voice_otp_rule(q)
    if res:
        print(f"✅ DETECTED CRITICAL: '{q}' -> {res['detected_category']}")
    else:
        print(f"❌ MISSED: '{q}'")
