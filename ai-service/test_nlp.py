"""
Unit & Comprehensive Accuracy Test for fraudRakshak NLP Engine v2.0
Tests Scam Detection & Zero-False-Positive Guarantee across varied Indian messages.
"""

from nlp_engine import analyze_scam_message, voice_query_advisor, evaluate_copilot_turn

TEST_CASES = [
    # --- SCAM DETECTIONS (Must be CRITICAL / HIGH, Risk >= 75%) ---
    {
        "name": "1. UPI QR Scam Preset",
        "text": "Congratulations! You won Rs 4,999 cashback from PhonePe Rewards. Scan this QR code and enter your 6-digit UPI PIN to claim money instantly into your bank account: phonepe-rewards-claim.xyz/qr",
        "expected_cat": "UPI_FRAUD",
        "should_be_safe": False,
        "min_risk": 75
    },
    {
        "name": "2. SBI KYC Freeze Preset",
        "text": "Dear SBI Customer, Your YONO account has been suspended due to pending KYC verification. Please click here http://sbi-kyc-verify.online to update PAN card immediately to avoid permanent account block.",
        "expected_cat": "BANK_KYC_FREEZE",
        "should_be_safe": False,
        "min_risk": 75
    },
    {
        "name": "3. Bijli Cutoff Preset",
        "text": "Dear consumer, your electricity power will be disconnected tonight at 9:30 PM from electric office because your previous month bill was not updated. Please immediately contact our power officer Sharma on 9876543210.",
        "expected_cat": "ELECTRICITY_CUTOFF",
        "should_be_safe": False,
        "min_risk": 75
    },
    {
        "name": "4. KBC 25 Lakh Preset",
        "text": "Dear friend, aapka WhatsApp number KBC lottery me select ho gaya hai aur aapne jeete hain pure 25 Lakh Rupaye! Apna prize claim karne ke liye KBC manager Rana Pratap Singh ko call karein: +92 301 9876543.",
        "expected_cat": "KBC_LOTTERY",
        "should_be_safe": False,
        "min_risk": 80
    },
    {
        "name": "5. FedEx Digital Arrest Preset",
        "text": "URGENT NOTICE: FedEx Courier tracking ID IND-88291 parcel containing 5 passports, 140g MDMA narcotics seized by Mumbai Customs. CBI warrant issued against your Aadhaar. Connect immediately on Skype with DCP Cyber Crime for digital verification.",
        "expected_cat": "DIGITAL_ARREST_CUSTOMS",
        "should_be_safe": False,
        "min_risk": 80
    },
    {
        "name": "6. AnyDesk Remote Screen Hijack",
        "text": "Sir bank verification ke liye Play Store se AnyDesk app install kijiye aur code bataiye.",
        "expected_cat": "REMOTE_HIJACK",
        "should_be_safe": False,
        "min_risk": 80
    },
    {
        "name": "6b. User Reported Case: Demanding OTP as Bank Employee",
        "text": "please your otp to us we are bank employee",
        "expected_cat": "OTP_HARVESTING",
        "should_be_safe": False,
        "min_risk": 90
    },
    {
        "name": "6c. Share your OTP to Bank Manager",
        "text": "Dear customer share your otp immediately with our bank manager to avoid account block",
        "expected_cat": "OTP_HARVESTING",
        "should_be_safe": False,
        "min_risk": 90
    },
    {
        "name": "6d. Hindi Bank Employee Phone OTP Demand",
        "text": "Sir bank employee bol raha hu verification ke liye OTP bataiye",
        "expected_cat": "OTP_HARVESTING",
        "should_be_safe": False,
        "min_risk": 90
    },
    {
        "name": "6e. Direct Send Me The OTP Scam",
        "text": "Send me the OTP you just received on your mobile to proceed",
        "expected_cat": "OTP_HARVESTING",
        "should_be_safe": False,
        "min_risk": 90
    },

    # --- SAFE MESSAGES (Must be SAFE, Risk <= 15%) ---
    {
        "name": "7. Safe Bank SMS Preset",
        "text": "INR 3,250.00 debited from A/C **8912 on 21-Nov-24 18:32 via UPI Ref 432819283712. Avl Bal: INR 34,120.50. If not authorized by you, immediately call HDFC Bank toll-free 18002584455.",
        "expected_cat": "SAFE_TRANSACTION",
        "should_be_safe": True,
        "max_risk": 15
    },
    {
        "name": "8. Genuine Swiggy Login OTP",
        "text": "849201 is your OTP to login to Swiggy. Valid for 10 minutes. Never share this OTP with anyone, including Swiggy delivery partners.",
        "expected_cat": "SAFE_TRANSACTION",
        "should_be_safe": True,
        "max_risk": 15
    },
    {
        "name": "9. Casual Dinner Conversation with 'Sharma' & '9:30 PM'",
        "text": "Hey bhai, kal milte hain 9:30 baje dinner ke liye. Sharma ji bhi aayenge.",
        "expected_cat": "SAFE_TRANSACTION",
        "should_be_safe": True,
        "max_risk": 15
    },
    {
        "name": "10. Amazon Delivery Notification",
        "text": "Your Amazon order #402-9812456-1234567 has been shipped via Bluedart and is arriving today by 8 PM.",
        "expected_cat": "SAFE_TRANSACTION",
        "should_be_safe": True,
        "max_risk": 15
    },
    {
        "name": "11. Jio Mobile Recharge Successful",
        "text": "Recharge of Rs 299 successful for your Jio number 9876543210. 1.5GB/day pack active for 28 days.",
        "expected_cat": "SAFE_TRANSACTION",
        "should_be_safe": True,
        "max_risk": 15
    },
    {
        "name": "12. Salary Credited in SBI Account",
        "text": "Dear customer, your salary of INR 65,000.00 is credited in your SBI A/C **4321 on 01-Nov-24. Avl Bal: INR 84,210.00.",
        "expected_cat": "SAFE_TRANSACTION",
        "should_be_safe": True,
        "max_risk": 15
    },
    {
        "name": "13. Aadhaar Verification OTP (Safe)",
        "text": "Your OTP for Aadhaar verification is 782190. Do not share this OTP with anyone. UIDAI.",
        "expected_cat": "SAFE_TRANSACTION",
        "should_be_safe": True,
        "max_risk": 15
    },
    {
        "name": "14. Casual Chat About Photos (Safe)",
        "text": "Can you send me the photos from yesterday's party? We had so much fun!",
        "expected_cat": "SAFE_TRANSACTION",
        "should_be_safe": True,
        "max_risk": 15
    }
]

def run_tests():
    print("=== TESTING FRAUDRAKSHAK NLP ENGINE v2.0 ACCURACY ===")
    all_passed = True
    passed_count = 0

    for t in TEST_CASES:
        res = analyze_scam_message(t["text"])
        name = t["name"]
        cat = res["scam_category"]
        risk = res["risk_score"]
        sev = res["severity"]
        
        passed = True
        if t["should_be_safe"]:
            if sev != "SAFE" or risk > t.get("max_risk", 15):
                passed = False
                print(f"❌ FALSE POSITIVE FAIL [{name}]: Expected SAFE, got {sev} (Risk={risk}%, Cat={cat})")
        else:
            if sev == "SAFE" or risk < t.get("min_risk", 70):
                passed = False
                print(f"❌ FALSE NEGATIVE FAIL [{name}]: Expected SCAM, got {sev} (Risk={risk}%, Cat={cat})")
            elif cat != t["expected_cat"]:
                passed = False
                print(f"❌ CATEGORY MISMATCH [{name}]: Expected {t['expected_cat']}, got {cat}")
            
        if passed:
            passed_count += 1
            print(f"✅ PASS [{name}]: Category={cat}, Risk={risk}%, Severity={sev}")
        else:
            all_passed = False

    accuracy = (passed_count / len(TEST_CASES)) * 100
    print(f"\nAccuracy Score: {passed_count}/{len(TEST_CASES)} ({accuracy:.1f}%)")

    if all_passed:
        print("🎉 100% ACCURACY ACHIEVED! Zero False Positives and Zero False Negatives!")
    else:
        print("⚠️ SOME ACCURACY TESTS FAILED.")

if __name__ == "__main__":
    run_tests()
