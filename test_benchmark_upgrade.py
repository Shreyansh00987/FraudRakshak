import urllib.request, json
from test_nlp_upgrade import analyze_scam_message_upgraded

benchmarks = [
    # 10 SCAM MESSAGES
    {"sender": "+91-90000-00001", "text": "Your HDFC account will be blocked today. Update your KYC immediately: http://fake-kyc.example", "expect": "CRITICAL"},
    {"sender": "VM-SBIOTP", "text": "Dear Customer, Your account will be suspended within 24 hours. Click here to verify your account details.", "expect": "CRITICAL"},
    {"sender": "+91-90000-00002", "text": "Congratulations! You won Rs. 5,00,000 lottery. Pay Rs. 999 processing fee to claim your prize.", "expect": "CRITICAL"},
    {"sender": "AD-FAKELOAN", "text": "Instant loan approved! Get Rs. 5 lakh without documents. Send your Aadhaar and OTP now.", "expect": "CRITICAL"},
    {"sender": "+91-90000-00003", "text": "Your ATM card is blocked. Call this number immediately to reactivate: 9000000003.", "expect": "CRITICAL"},
    {"sender": "VK-FAKEPAY", "text": "Your UPI account will expire today. Share your UPI PIN to avoid account suspension.", "expect": "CRITICAL"},
    {"sender": "+91-90000-00004", "text": "Your account has been selected for a cash reward. Click this link and enter your banking password.", "expect": "CRITICAL"},
    {"sender": "FAKE-POST", "text": "Your parcel is on hold due to an incorrect address. Pay Rs. 10 redelivery fee using this link.", "expect": "HIGH"},
    {"sender": "+91-90000-00005", "text": "You have received Rs. 10,000 cashback. Install this APK to claim your reward.", "expect": "CRITICAL"},
    {"sender": "VM-LOTTERY", "text": "You have won a free iPhone! Pay Rs. 500 delivery charges to receive your gift.", "expect": "CRITICAL"},

    # 10 NORMAL MESSAGES
    {"sender": "VM-SBIINB", "text": "Your account XXXX1234 has been credited with Rs. 5,000.00 on 22-Nov-2026.", "expect": "SAFE"},
    {"sender": "AD-HDFCBK", "text": "Dear Customer, your ATM card ending 4521 was used for a transaction of Rs. 500.", "expect": "SAFE"},
    {"sender": "VM-ICICIB", "text": "Your monthly bank statement is now available. Please log in through the official mobile banking app.", "expect": "SAFE"},
    {"sender": "JD-SWIGGY", "text": "Your food order has been confirmed. Your delivery partner will reach you soon.", "expect": "SAFE"},
    {"sender": "JD-AMAZON", "text": "Your order has been shipped. Expected delivery: 25 November.", "expect": "SAFE"},
    {"sender": "VM-SBIUPI", "text": "Rs. 250 debited from your account for UPI payment. If not done by you, contact your bank through official channels.", "expect": "SAFE"},
    {"sender": "AD-IRCTC", "text": "Your train ticket booking is confirmed. Please check your registered email for ticket details.", "expect": "SAFE"},
    {"sender": "VM-PNB", "text": "Your fixed deposit receipt has been generated successfully.", "expect": "SAFE"},
    {"sender": "JD-JIOMART", "text": "Your grocery order is out for delivery. Thank you for shopping with us.", "expect": "SAFE"},
    {"sender": "AD-AXISBK", "text": "Dear Customer, your account balance is available through the official mobile banking application.", "expect": "SAFE"}
]

print("Evaluating 20 Benchmarks with analyze_scam_message_upgraded:")
passed = 0
for b in benchmarks:
    res = analyze_scam_message_upgraded(b["text"], b["sender"])
    sev = res["severity"]
    exp = b["expect"]
    match = (sev == exp) or (exp in ["CRITICAL", "HIGH"] and sev in ["CRITICAL", "HIGH"])
    if match:
        passed += 1
        print(f"✅ PASSED [{sev}] -> {b['text'][:40]}...")
    else:
        print(f"❌ FAILED [Expected {exp}, Got {sev}] -> {b['text']}")

print(f"\nUser Benchmark Accuracy: {passed}/{len(benchmarks)} ({passed*100/len(benchmarks)}%)")
