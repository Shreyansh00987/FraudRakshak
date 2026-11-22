from nlp_engine import analyze_scam_message

tests = [
  # SCAMS
  {"name": "1. HDFC blocked KYC", "text": "Your HDFC account will be blocked today. Update your KYC immediately: http://fake-kyc.example", "sender": "+91-90000-00001", "is_scam": True},
  {"name": "2. SBI suspended click here", "text": "Dear Customer, Your account will be suspended within 24 hours. Click here to verify your account details.", "sender": "VM-SBIOTP", "is_scam": True},
  {"name": "3. ICICI 5 Lakh lottery 999 fee", "text": "Congratulations! You won Rs. 5,00,000 lottery. Pay Rs. 999 processing fee to claim your prize.", "sender": "+91-90000-00002", "is_scam": True},
  {"name": "4. Fake Loan Aadhaar & OTP", "text": "Instant loan approved! Get Rs. 5 lakh without documents. Send your Aadhaar and OTP now.", "sender": "AD-FAKELOAN", "is_scam": True},
  {"name": "5. ATM card blocked call mobile", "text": "Your ATM card is blocked. Call this number immediately to reactivate: 9000000003.", "sender": "+91-90000-00003", "is_scam": True},
  {"name": "6. UPI account expire share PIN", "text": "Your UPI account will expire today. Share your UPI PIN to avoid account suspension.", "sender": "VK-FAKEPAY", "is_scam": True},
  {"name": "7. Kotak reward enter password", "text": "Your account has been selected for a cash reward. Click this link and enter your banking password.", "sender": "+91-90000-00004", "is_scam": True},
  {"name": "8. Parcel hold pay Rs 10 fee", "text": "Your parcel is on hold due to an incorrect address. Pay Rs. 10 redelivery fee using this link.", "sender": "FAKE-POST", "is_scam": True},
  {"name": "9. SBI reward install APK", "text": "You have received Rs. 10,000 cashback. Install this APK to claim your reward.", "sender": "+91-90000-00005", "is_scam": True},
  {"name": "10. Won iPhone pay Rs 500 delivery", "text": "You have won a free iPhone! Pay Rs. 500 delivery charges to receive your gift.", "sender": "VM-LOTTERY", "is_scam": True},

  # NORMAL / SAFE
  {"name": "11. SBI credited 5000", "text": "Your account XXXX1234 has been credited with Rs. 5,000.00 on 22-Nov-2026.", "sender": "VM-SBIINB", "is_scam": False},
  {"name": "12. HDFC card 4521 used 500", "text": "Dear Customer, your ATM card ending 4521 was used for a transaction of Rs. 500.", "sender": "AD-HDFCBK", "is_scam": False},
  {"name": "13. ICICI monthly statement", "text": "Your monthly bank statement is now available. Please log in through the official mobile banking app.", "sender": "VM-ICICIB", "is_scam": False},
  {"name": "14. Swiggy order confirmed", "text": "Your food order has been confirmed. Your delivery partner will reach you soon.", "sender": "JD-SWIGGY", "is_scam": False},
  {"name": "15. Amazon order shipped", "text": "Your order has been shipped. Expected delivery: 25 November.", "sender": "JD-AMAZON", "is_scam": False},
  {"name": "16. SBI UPI debited 250", "text": "Rs. 250 debited from your account for UPI payment. If not done by you, contact your bank through official channels.", "sender": "VM-SBIUPI", "is_scam": False},
  {"name": "17. IRCTC ticket confirmed", "text": "Your train ticket booking is confirmed. Please check your registered email for ticket details.", "sender": "AD-IRCTC", "is_scam": False},
  {"name": "18. PNB FD receipt generated", "text": "Your fixed deposit receipt has been generated successfully.", "sender": "VM-PNB", "is_scam": False},
  {"name": "19. JioMart order out for delivery", "text": "Your grocery order is out for delivery. Thank you for shopping with us.", "sender": "JD-JIOMART", "is_scam": False},
  {"name": "20. Axis balance in official app", "text": "Dear Customer, your account balance is available through the official mobile banking application.", "sender": "AD-AXISBK", "is_scam": False}
]

print("=== RUNNING USER 20-TEST SUITE ===")
passed = 0
for t in tests:
    res = analyze_scam_message(t["text"], t["sender"])
    is_safe = (res["severity"] == "SAFE")
    expected_safe = (not t["is_scam"])
    ok = (is_safe == expected_safe)
    cat = res["scam_category"]
    risk = res["risk_score"]
    sev = res["severity"]
    if ok:
        passed += 1
        print(f"✅ PASS: {t['name']} -> Cat: {cat}, Risk: {risk}%, Sev: {sev}")
    else:
        print(f"❌ FAIL: {t['name']} -> Expected Safe={expected_safe}, Got Safe={is_safe} (Cat: {cat}, Risk: {risk}%, Sev: {sev})")

print(f"\nTotal: {passed}/20 passed ({(passed/20)*100:.1f}%)")
