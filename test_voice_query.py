import re
from typing import Dict, Any

# We import analyze_scam_message
import sys
sys.path.append(r"C:\Users\shrea\.gemini\antigravity\scratch\fraudRakshak\ai-service")
from nlp_engine import analyze_scam_message

def voice_query_advisor_v2(query: str) -> Dict[str, Any]:
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

    is_greeting_devanagari = any(g in q_clean for g in [
        "हाई", "हाय", "हेलो", "नमस्ते", "नमस्कार", "प्रणाम", "राम राम", "सत श्री", "आदाब",
        "क्या हाल", "हाल चाल", "हाल है", "कैसे हो", "कैसी हो", "कैसे हैं", "कैसा है", "सब ठीक", "सब बढ़िया"
    ])
    greeting_latin_regex = r'\b(hi|hey|hello|namaste|namaskar|pranam|kya hal|kya haal|kaise ho|kaise hain|kaisa hai|how are you|how r u|whats up|what\'s up|good morning|good evening|good afternoon|sab theek|sab badhiya|haal chaal|hal chal)\b'
    is_greeting_latin = bool(re.search(greeting_latin_regex, q_lower))

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
    if cat == "SAFE_TRANSACTION":
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


test_queries = [
    "हाई क्या हाल है?",
    "हेलो",
    "नमस्ते रक्षक",
    "आप कौन हो?",
    "Who are you?",
    "1930 क्या है?",
    "complaint kaise kare cyber cell me?",
    "Bhaiya mujhe bijli cut ka message aaya hai, kya karu?",
    "Bank manager bol raha hai turant OTP batao varna account block hoga",
    "PhonePe par Rs 4,999 lene ke liye QR scan karne ko bola hai",
    "kya paise lene ke liye upi pin dalna padta hai?",
    "CBI officer bol raha hai narcotics parcel me mera naam aaya hai",
    "WhatsApp par call aaya hai ki KBC 25 lakh lottery jeeti hai",
    "Your account XXXX1234 has been credited with Rs. 5,000.00 on 22-Nov-2026.",
    "Your food order has been confirmed. Your delivery partner will reach you soon.",
    "Your parcel is on hold due to an incorrect address. Pay Rs. 10 redelivery fee using this link.",
    "Instant loan approved! Get Rs. 5 lakh without documents. Send your Aadhaar and OTP now.",
    "AnyDesk download karne bol rahe hain bank wale, kar lu kya?",
    "Thank you so much",
    "धन्यवाद"
]

print("\n--- RUNNING TEST SUITE ON V2 ---")
for q in test_queries:
    res = voice_query_advisor_v2(q)
    print(f"\n[QUERY]: {q}")
    print(f"  Category : {res.get('detected_category')}")
    print(f"  Risk     : {res.get('risk_level')}")
    print(f"  Actions  : {len(res.get('bullet_actions', []))} items")
    print(f"  Hinglish : {res.get('response_text_hinglish')[:75]}...")
    print(f"  Hindi    : {res.get('response_text_hindi')[:75]}...")
