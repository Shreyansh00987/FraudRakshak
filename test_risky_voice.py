import sys
sys.path.append(r"C:\Users\shrea\.gemini\antigravity\scratch\fraudRakshak\ai-service")
from nlp_engine import voice_query_advisor

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

print("Scanning test risky inputs in voice_query_advisor:")
failed = []
for inp in test_risky_inputs:
    res = voice_query_advisor(inp)
    risk = res.get("risk_level")
    cat = res.get("detected_category")
    if risk == "SAFE":
        failed.append((inp, cat, risk))
        print(f"❌ MISCLASSIFIED AS SAFE: '{inp}' -> cat: {cat}")
    else:
        print(f"✅ DETECTED THREAT ({risk}): '{inp[:40]}...' -> cat: {cat}")

print(f"\nTotal Tested: {len(test_risky_inputs)}, Failed (Marked Safe): {len(failed)}")
