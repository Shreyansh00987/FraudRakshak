from test_voice_query import voice_query_advisor_v2

more_queries = [
    "sab theek hai bhai",
    "how to report a cyber crime",
    "kisi ne mujhe bola ki lottery lagi hai",
    "ATM card blocked call 9000000003",
    "mera phone hack ho gaya",
    "Google Pay cashback lene ke liye pin mang raha hai",
    "SBI YONO account block update kyc http://sbi-fake.com",
    "Swiggy order confirmed Rs 350",
    "OTP for login is 482910. Do not share with anyone.",
    "Bina documents ke loan kaise milega?"
]

print("\n--- RUNNING ADDITIONAL EDGE CASES ---")
for q in more_queries:
    res = voice_query_advisor_v2(q)
    print(f"\n[QUERY]: {q}")
    print(f"  Category : {res.get('detected_category')}")
    print(f"  Risk     : {res.get('risk_level')}")
    print(f"  Hinglish : {res.get('response_text_hinglish')[:80]}...")
