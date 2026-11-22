/**
 * Hackathon Presets Bar
 * 6 authentic Indian scam presets for instant judge testing without typing.
 */

export const HACKATHON_PRESETS = [
  {
    id: "upi-qr",
    name: "⚡ UPI QR Trap",
    nameHindi: "⚡ यूपीआई क्यूआर जाल",
    tag: "CRITICAL",
    category: "UPI_FRAUD",
    sender: "BZ-PHNPAY",
    text: "Congratulations! You won Rs 4,999 cashback from PhonePe Rewards. Scan this QR code and enter your 6-digit UPI PIN to claim money instantly into your bank account: phonepe-rewards-claim.xyz/qr",
    description: "Fake PhonePe cashback asking victim to enter PIN to 'receive' money."
  },
  {
    id: "sbi-kyc",
    name: "🏦 SBI KYC Freeze",
    nameHindi: "🏦 एसबीआई बैंक केवाईसी",
    tag: "CRITICAL",
    category: "BANK_KYC_FREEZE",
    sender: "VM-SBINB",
    text: "Dear SBI Customer, Your YONO account has been suspended due to pending KYC verification. Please click here http://sbi-kyc-verify.online to update PAN card immediately to avoid permanent account block.",
    description: "Account suspension threat with spoofed netbanking link."
  },
  {
    id: "bijli-cut",
    name: "💡 Bijli Cutoff",
    nameHindi: "💡 बिजली बिल कटऑफ",
    tag: "CRITICAL",
    category: "ELECTRICITY_CUTOFF",
    sender: "+91 98765 43210",
    text: "Dear consumer, your electricity power will be disconnected tonight at 9:30 PM from electric office because your previous month bill was not updated. Please immediately contact our power officer Sharma on 9876543210.",
    description: "Manufactured panic of tonight 9:30 PM power cutoff with fake officer."
  },
  {
    id: "kbc-lottery",
    name: "🎟️ KBC ₹25 Lakh",
    nameHindi: "🎟️ केबीसी 25 लाख",
    tag: "CRITICAL",
    category: "KBC_LOTTERY",
    sender: "+92 301 9876543",
    text: "Dear friend, aapka WhatsApp number KBC lottery me select ho gaya hai aur aapne jeete hain pure 25 Lakh Rupaye! Apna prize claim karne ke liye KBC manager Rana Pratap Singh ko call karein: +92 301 9876543.",
    description: "Cross-border WhatsApp lottery fraud from +92 international calling code."
  },
  {
    id: "fedex-arrest",
    name: "📦 FedEx Digital Arrest",
    nameHindi: "📦 डिजिटल अरेस्ट",
    tag: "CRITICAL",
    category: "DIGITAL_ARREST_CUSTOMS",
    sender: "+91 88291 00219",
    text: "URGENT NOTICE: FedEx Courier tracking ID IND-88291 parcel containing 5 passports, 140g MDMA narcotics seized by Mumbai Customs. CBI warrant issued against your Aadhaar. Connect immediately on Skype with DCP Cyber Crime for digital verification.",
    description: "Extortion scam coercing victim into fake Skype interrogation and asset freeze."
  },
  {
    id: "safe-sms",
    name: "✅ Safe Bank SMS",
    nameHindi: "✅ सुरक्षित बैंक एसएमएस",
    tag: "SAFE",
    category: "SAFE_TRANSACTION",
    sender: "AD-HDFCBK",
    text: "INR 3,250.00 debited from A/C **8912 on 21-Nov-24 18:32 via UPI Ref 432819283712. Avl Bal: INR 34,120.50. If not authorized by you, immediately call HDFC Bank toll-free 18002584455.",
    description: "Genuine banking debit notification demonstrating zero false positives."
  }
];
