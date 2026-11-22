import React, { useState, useEffect, useRef } from 'react';
import { 
  Phone, PhoneOff, PhoneCall, ShieldAlert, AlertTriangle, 
  Volume2, ArrowRight, RefreshCw, FileText, Signal, Wifi, Battery,
  Shuffle, Sparkles, CheckCircle2
} from 'lucide-react';
import { soundSynth } from '../utils/audioSynthesizer';
import { speechEngine } from '../utils/speechEngine';

export const SCENARIOS = [
  {
    id: "sbi_bank",
    name: "🏦 Bank & Card Phishing",
    nameHindi: "🏦 बैंक व कार्ड फ्रॉड",
    callerName: "SBI Fraud Dept (Ramesh Sharma)",
    callerNameHindi: "एसबीआई हेड ऑफिस (रमेश शर्मा)",
    callerNumber: "+91 98201 44520 (Spoofed)",
    badge: "Banking Security Alert",
    badgeHindi: "बैंक सुरक्षा अलर्ट",
    variations: [
      {
        id: "kyc_freeze",
        label: "Account Block & KYC Threat",
        labelHindi: "अकाउंट ब्लॉक व केवाईसी धमकी",
        icon: "⚠️",
        description: "Scammer threatens immediate account closure and demands an 'unfreeze' code.",
        descriptionHindi: "स्कैमर तुरंत खाता बंद करने की धमकी देकर अनफ़्रीज़ कोड (OTP) मांगता है।",
        turns: [
          {
            speaker: "scammer",
            text: "Namaste sir, main SBI Head Office se Officer Ramesh Sharma bol raha hoon. Aapka YONO account aur debit card turant block kiya ja raha hai kyunki KYC pending hai.",
            hindi: "नमस्ते सर, मैं एसबीआई हेड ऑफिस से ऑफिसर रमेश शर्मा बोल रहा हूँ। आपका योनो अकाउंट और डेबिट कार्ड तुरंत ब्लॉक किया जा रहा है क्योंकि केवाईसी पेंडिंग है।",
            english: "Namaste sir, I am Officer Ramesh Sharma from SBI Head Office. Your YONO account and debit card are being permanently blocked due to pending KYC.",
            copilotAlert: "⚠️ Impersonating bank employee: Real banks never threaten account closure over emergency phone calls.",
            copilotAlertHindi: "⚠️ फर्जी बैंक अधिकारी: असली बैंक कभी भी इमरजेंसी फोन कॉल पर खाता बंद करने की धमकी नहीं देते।",
            tactics: ["Authority Impersonation", "False Urgency"],
            threatLevel: "HIGH",
            replies: [
              "Mera account active hai, aap bank ka landline number batayein.",
              "Main branch jakar khud physically verify karunga, call rakhiye.",
              "Bank officer phone par KYC update nahi karte."
            ],
            repliesHindi: [
              "मेरा खाता सक्रिय है, आप बैंक का लैंडलाइन नंबर बताएं।",
              "मैं शाखा जाकर खुद जांच करूँगा, कॉल रखिए।",
              "बैंक अधिकारी फोन पर कभी केवाईसी नहीं मांगते।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir branch me 4 din lagenge tab tak saara balance freeze rahega! Maine aapke mobile par 6 digit unfreeze code bheja hai, jaldi se bataiye taaki account chalu rahe!",
            hindi: "सर ब्रांच में 4 दिन लगेंगे तब तक सारा बैलेंस फ्रीज़ रहेगा! मैंने आपके मोबाइल पर 6 अंकों का अनफ़्रीज़ कोड भेजा है, जल्दी से बताइए ताकि खाता चालू रहे!",
            english: "Sir visiting branch will take 4 days! I have sent a 6-digit unfreeze code to your phone, tell me immediately or your account will be frozen right now!",
            copilotAlert: "🚨 CRITICAL: Scammer is demanding OTP disguised as 'Unfreeze Code'! Never share OTP with anyone under any circumstance.",
            copilotAlertHindi: "🚨 अत्यंत गंभीर खतरा: स्कैमर अनफ़्रीज़ कोड के नाम पर आपका ओटीपी (OTP) मांग रहा है! कभी भी किसी को ओटीपी न दें।",
            tactics: ["Demanding OTP", "Panic Creation"],
            threatLevel: "CRITICAL",
            replies: [
              "RBI kehta hai kisi ko bhi OTP nahi dena chahiye. Main nahi doonga.",
              "Aap real officer hain toh system se verify karein, OTP kyu maang rahe hain?",
              "Main cyber crime police 1930 ko yeh call forward kar raha hoon."
            ],
            repliesHindi: [
              "आरबीआई कहता है किसी को भी ओटीपी नहीं देना चाहिए। मैं नहीं दूंगा।",
              "आप असली अधिकारी हैं तो सिस्टम से देखें, ओटीपी क्यों मांग रहे हैं?",
              "मैं 1930 साइबर हेल्पलाइन को कॉल रिपोर्ट कर रहा हूँ।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir agar code nahi batana toh Play Store se QuickSupport ya AnyDesk app download kijiye, hum screen dekhkar solve kar denge!",
            hindi: "सर अगर कोड नहीं बताना तो प्ले स्टोर से क्विक-सपोर्ट या एनीडेस्क ऐप डाउनलोड कीजिए, हम स्क्रीन देखकर चालू कर देंगे!",
            english: "Sir if you don't want to share code, download AnyDesk or QuickSupport from Play Store, we will resolve by viewing your screen!",
            copilotAlert: "🚨 DANGER: Screen sharing hijack! Installing AnyDesk allows scammer to access your phone and steal money.",
            copilotAlertHindi: "🚨 स्क्रीन हैक का ख़तरा: एनीडेस्क डाउनलोड करने से स्कैमर आपका फोन हैक कर पैसे चुरा लेगा।",
            tactics: ["Remote Screen Hijacking (AnyDesk)"],
            threatLevel: "CRITICAL",
            replies: [
              "AnyDesk download karke phone ka control kisi anjaan ko nahi doonga.",
              "Aapka scam pakda gaya hai. Call disconnect kar raha hoon!"
            ],
            repliesHindi: [
              "एनीडेस्क डाउनलोड करके फोन का कंट्रोल किसी अनजान को नहीं दूंगा।",
              "आपका घोटाला पकड़ा गया है। कॉल काट रहा हूँ!"
            ]
          }
        ]
      },
      {
        id: "reward_points",
        label: "Reward Points Expiry Trap",
        labelHindi: "रिवॉर्ड पॉइंट्स एक्सपायरी ट्रैप",
        icon: "🎁",
        description: "Scammer offers Rs 9,850 cash reward and asks for a 'credit confirmation' OTP.",
        descriptionHindi: "स्कैमर 9,850 रुपये रिवॉर्ड पॉइंट्स कैश में देने का झांसा देकर क्रेडिट कन्फर्मेशन ओटीपी मांगता है।",
        turns: [
          {
            speaker: "scammer",
            text: "Badhai ho sir! Main bank reward cell se baat kar raha hoon. Aapke credit/debit card par Rs 9,850 ke reward points jama hain jo aaj raat 12 baje expire ho jayenge. Kya aap inhe cash me apne khate me lena chahte hain?",
            hindi: "बधाई हो सर! मैं बैंक रिवॉर्ड सेल से बात कर रहा हूँ। आपके कार्ड पर 9,850 रुपये के रिवॉर्ड पॉइंट्स जमा हैं जो आज रात 12 बजे एक्सपायर हो जाएंगे। क्या आप इन्हें कैश में अपने खाते में पाना चाहते हैं?",
            english: "Congratulations sir! Calling from the bank rewards department. You have Rs 9,850 worth of reward points expiring tonight at 12 AM. Do you want to credit this cash to your account?",
            copilotAlert: "⚠️ Reward Points Phishing: Banks never call customers to convert points into direct cash over the phone.",
            copilotAlertHindi: "⚠️ रिवॉर्ड पॉइंट्स फ़िशिंग: बैंक कभी भी फोन पर पॉइंट्स को सीधे कैश में बदलने के लिए कॉल नहीं करते।",
            tactics: ["Reward Baiting", "Greed Exploitation", "Artificial Deadline"],
            threatLevel: "HIGH",
            replies: [
              "Reward points official mobile app me redeem hote hain, phone par claim nahi karna.",
              "Aap bank ke toll-free number se call kyu nahi kar rahe?",
              "Mujhe cash reward nahi chahiye, call disconnect kijiye."
            ],
            repliesHindi: [
              "रिवॉर्ड पॉइंट्स आधिकारिक मोबाइल ऐप में रिडीम होते हैं, फोन पर नहीं।",
              "आप बैंक के टोल-फ्री नंबर से कॉल क्यों नहीं कर रहे?",
              "मुझे कैश रिवॉर्ड नहीं चाहिए, कॉल काटिए।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir 9,850 rupaye sidha aapke account me credit karne ke liye maine bank server se ek Credit Confirmation OTP bheja hai. Bas wo 6 digit bataiye aur turant balance aa jayega!",
            hindi: "सर 9,850 रुपये सीधा आपके खाते में क्रेडिट करने के लिए मैंने बैंक सर्वर से एक क्रेडिट कन्फर्मेशन ओटीपी भेजा है। बस वो 6 अंक बताइए और 2 मिनट में पैसे आ जाएंगे!",
            english: "Sir to credit Rs 9,850 into your account, I sent a Credit Confirmation OTP from the server. Just tell me those 6 digits and the funds will be credited instantly!",
            copilotAlert: "🚨 CRITICAL TRAP: Money can NEVER be credited using an OTP! Entering or sharing an OTP ALWAYS DEBITS your money!",
            copilotAlertHindi: "🚨 खतरनाक जाल: पैसे आने के लिए कभी ओटीपी की ज़रूरत नहीं होती! ओटीपी देने से हमेशा पैसे कटते हैं!",
            tactics: ["Credit OTP Deception", "Financial Drain Trap"],
            threatLevel: "CRITICAL",
            replies: [
              "Paise lene ke liye kabhi OTP nahi chahiye hota! OTP se sirf paise katte hain.",
              "RBI sakht mana karta hai OTP share karne se. Main nahi bataunga.",
              "Main abhi 1930 Cyber Cell par aapka fraud report kar raha hoon."
            ],
            repliesHindi: [
              "पैसे प्राप्त करने के लिए कभी ओटीपी नहीं लगता! ओटीपी से केवल पैसे कटते हैं।",
              "आरबीआई का सख्त नियम है: ओटीपी किसी को न दें। मैं नहीं बताऊंगा।",
              "मैं अभी 1930 साइबर हेल्पलाइन पर यह फ्रॉड रिपोर्ट कर रहा हूँ।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir agar code nahi bolna toh hamare rewards portal sbi-reward-cash.online par jakar apna card number aur 3-digit CVV daalkar khud claim kar lijiye!",
            hindi: "सर अगर कोड नहीं बोलना तो हमारे रिडेम्पशन पोर्टल sbi-reward-cash.online पर जाकर अपना कार्ड नंबर और 3 अंकों का सीवीवी डालकर क्लेम कर लीजिए!",
            english: "Sir if you don't want to speak the code, visit our redemption portal sbi-reward-cash.online, enter your card number and 3-digit CVV to claim yourself!",
            copilotAlert: "🚨 CREDENTIAL HARVESTING: Fake phishing link designed to steal Debit Card numbers and CVV codes!",
            copilotAlertHindi: "🚨 कार्ड डेटा चोरी: फर्जी वेबसाइट लिंक जिससे आपका डेबिट कार्ड नंबर और सीवीवी चुराया जा सके!",
            tactics: ["Phishing Portal", "CVV Harvesting"],
            threatLevel: "CRITICAL",
            replies: [
              "Yeh fake website hai. Official bank website .bank.sbi hoti hai.",
              "Main apna card number aur CVV kisi anjaan link par kabhi nahi daalunga."
            ],
            repliesHindi: [
              "यह फर्जी वेबसाइट है। असली बैंक वेबसाइट .bank.sbi होती है।",
              "मैं अपना कार्ड नंबर और सीवीवी किसी अनजान लिंक पर कभी नहीं डालूँगा।"
            ]
          }
        ]
      },
      {
        id: "unauthorized_tx",
        label: "Fake Fraud Transaction Alert",
        labelHindi: "फर्जी ट्रांजैक्शन अलर्ट ट्रैप",
        icon: "🚨",
        description: "Scammer claims an unauthorized Rs 48,500 transaction occurred and demands a 'cancellation code'.",
        descriptionHindi: "स्कैमर 48,500 रुपये कटने का डर दिखाकर कैंसिलेशन कोड (OTP) मांगता है।",
        turns: [
          {
            speaker: "scammer",
            text: "Emergency Alert sir! Main bank fraud monitoring cell se bol raha hoon. Abhi-abhi aapke card se Dubai ke liye Rs 48,500 ka international payment attempt hua hai! Kya yeh transaction aapne kiya hai?",
            hindi: "इमरजेंसी अलर्ट सर! मैं बैंक फ्रॉड मॉनिटरिंग सेल से बोल रहा हूँ। अभी-अभी आपके खाते से दुबई के लिए 48,500 रुपये का इंटरनेशनल कार्ड पेमेंट इनिशिएट हुआ है! क्या यह आपने किया है?",
            english: "Emergency alert sir! Calling from the bank fraud monitoring cell. A Rs 48,500 international transaction from Dubai was just attempted on your card! Did you authorize this?",
            copilotAlert: "⚠️ Panic Fabrication: Scammers create intense panic by pretending an unauthorized international transaction happened.",
            copilotAlertHindi: "⚠️ झूठा डर: जालसाज अचानक 48,500 रुपये कटने की झूठी कहानी बनाकर घबराहट पैदा करते हैं।",
            tactics: ["Fear Exploitation", "Impersonating Fraud Cell"],
            threatLevel: "HIGH",
            replies: [
              "Maine koi transaction nahi kiya, main bank official app me jakar card lock kar raha hoon.",
              "Aap official bank toll-free 1800 number se kyu nahi bol rahe?",
              "Main local branch jakar verify karunga."
            ],
            repliesHindi: [
              "मैंने कोई ट्रांजैक्शन नहीं किया, मैं बैंक ऐप में जाकर कार्ड लॉक कर रहा हूँ।",
              "आप बैंक के आधिकारिक टोल-फ्री नंबर से कॉल क्यों नहीं कर रहे?",
              "मैं सीधे शाखा जाकर पता करूँगा।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir app kholne ka time nahi hai, paise agle 2 minute me kat jayenge! Maine transaction reverse karne ke liye Cancellation Code bheja hai, jaldi 6 digit bolie!",
            hindi: "सर ऐप खोलने का समय नहीं है, पैसे अगले 2 मिनट में कट जाएंगे! मैंने पेमेंट रिवर्स करने के लिए कैंसिलेशन कोड भेजा है, तुरंत 6 अंक बोलिए वरना 48,500 रुपये कट जाएंगे!",
            english: "Sir there is no time to open the app, funds will be permanently debited! I sent a Cancellation Code to reverse the transaction, read those 6 digits immediately!",
            copilotAlert: "🚨 DANGEROUS REVERSAL TRAP: The 'Cancellation Code' is the real OTP to AUTHORIZE the fraudulent deduction! Never speak it!",
            copilotAlertHindi: "🚨 खतरनाक कैंसिलेशन कोड ट्रैप: यह कैंसिलेशन कोड असल में पैसे काटने का असली ओटीपी है! इसे किसी को न बताएं!",
            tactics: ["Cancellation Code Trap", "Extreme Panic Creation"],
            threatLevel: "CRITICAL",
            replies: [
              "Transaction cancel karne ke liye OTP ki zarurat nahi hoti. Main OTP nahi doonga.",
              "Aap ek cyber criminal hain. Main 1930 Cyber Cell ko call kar raha hoon."
            ],
            repliesHindi: [
              "ट्रांजैक्शन रद्द करने के लिए कभी ओटीपी नहीं लगता। मैं ओटीपी नहीं दूंगा।",
              "आप एक साइबर अपराधी हैं। मैं तुरंत 1930 साइबर सेल पर कॉल कर रहा हूँ।"
            ]
          }
        ]
      },
      {
        id: "instant_loan",
        label: "Pre-approved Instant Loan",
        labelHindi: "प्री-अप्रूव्ड लोन डिस्बर्सल",
        icon: "💰",
        description: "Scammer promises an instant Rs 5 Lakh loan without documents and demands advance processing fees.",
        descriptionHindi: "स्कैमर बिना डॉक्यूमेंट 5 लाख लोन देने का झांसा देकर एडवांस प्रोसेसिंग फीस मांगता है।",
        turns: [
          {
            speaker: "scammer",
            text: "Namaste sir, aapke acche CIBIL score par bank ne Rs 5,00,000 ka pre-approved personal loan pass kiya hai bina kisi document ke sirf 4.5% interest par. Kya aapko yeh fund chahiye?",
            hindi: "नमस्ते सर, आपके अच्छे सिबिल स्कोर पर बैंक ने 5,00,000 रुपये का प्री-अप्रूव्ड पर्सनल लोन बिना किसी कागज़ात के पास किया है सिर्फ 4.5% ब्याज पर। क्या आपको यह राशि चाहिए?",
            english: "Namaste sir, based on your high credit score, the bank has sanctioned a pre-approved personal loan of Rs 5 Lakh without any documentation at just 4.5% interest. Would you like to disburse this?",
            copilotAlert: "⚠️ Unrealistic Loan Offer: Genuine banks never offer instant unsecured loans at 4.5% or disburse without KYC verification.",
            copilotAlertHindi: "⚠️ फर्जी लोन ऑफर: असली बैंक बिना वेरिफिकेशन के 4.5% ब्याज पर कभी लोन नहीं देते।",
            tactics: ["Unrealistic Offer", "Fake Loan Approval", "Greed Lure"],
            threatLevel: "HIGH",
            replies: [
              "Mujhe koi loan nahi chahiye, mera number DND list me daalein.",
              "Bina kisi document ke koi bank loan nahi deta, aap fake caller hain.",
              "Main official bank branch se khud apply karunga."
            ],
            repliesHindi: [
              "मुझे कोई लोन नहीं चाहिए, मेरा नंबर डीएनडी में डालें।",
              "बिना किसी दस्तावेज़ के कोई बैंक लोन नहीं देता, आप फर्जी हैं।",
              "मैं आधिकारिक बैंक शाखा से खुद संपर्क करूँगा।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir offer sirf aaj shaam 4 baje tak valid hai! Loan amount aapke account me transfer karne ke liye Rs 1,999 ki file processing fee turant hamare officer scanner par bhejye!",
            hindi: "सर ऑफर सिर्फ आज शाम 4 बजे तक है! लोन अमाउंट आपके खाते में ट्रांसफर करने के लिए 1,999 रुपये की फाइल प्रोसेसिंग फीस तुरंत हमारे ऑफिसर स्कैनर पर जमा करें!",
            english: "Sir offer is valid only till 4 PM today! Send Rs 1,999 file processing fee to our officer's scanner to release the funds!",
            copilotAlert: "🚨 ADVANCE-FEE FRAUD: Genuine banks deduct processing fees from the loan amount itself. NEVER pay advance fees to personal scanners!",
            copilotAlertHindi: "🚨 एडवांस फीस फ्रॉड: असली बैंक प्रोसेसिंग फीस लोन की राशि से काटते हैं, कभी पर्सनल स्कैनर पर पहले पैसे नहीं मांगते!",
            tactics: ["Advance Fee Fraud", "Personal Scanner Payment"],
            threatLevel: "CRITICAL",
            replies: [
              "Asli bank processing fee loan amount se katte hain, advance payment maangna 100% fraud hai.",
              "Main kisi personal scanner par paise nahi bhejunga. Call rakhiye."
            ],
            repliesHindi: [
              "असली बैंक प्रोसेसिंग फीस लोन राशि से काटते हैं, एडवांस स्कैनर पर मांगना 100% फ्रॉड है।",
              "मैं किसी पर्सनल स्कैनर पर पैसे नहीं भेजूंगा। कॉल रखिए।"
            ]
          }
        ]
      },
      {
        id: "pan_aadhaar",
        label: "PAN-Aadhaar Mandate Penalty",
        labelHindi: "पैन-आधार पेनाल्टी धमकी",
        icon: "🆔",
        description: "Scammer threatens a Rs 10,000 government penalty for unlinked PAN-Aadhaar.",
        descriptionHindi: "स्कैमर पैन-आधार लिंक न होने पर 10,000 रुपये जुर्माने की धमकी देकर बायोमेट्रिक ओटीपी मांगता है।",
        turns: [
          {
            speaker: "scammer",
            text: "Hello sir, RBI compliance cell se bol raha hoon. Aapke bank account me PAN card aur Aadhaar linking update nahi hui hai. Aaj 5 baje tak link na hone par Rs 10,000 penalty lagegi aur account seal ho jayega.",
            hindi: "हेलो सर, आरबीआई कंप्लायंस सेल से बोल रहा हूँ। आपके बैंक खाते में पैन कार्ड और आधार लिंकिंग अपडेट नहीं हुई है। आज 5 बजे तक अपडेट न होने पर 10,000 रुपये का जुर्माना लगेगा और खाता सील हो जाएगा।",
            english: "Hello sir, calling from the RBI Compliance Cell. Your bank account lacks PAN-Aadhaar linking. If not updated by 5 PM today, a Rs 10,000 penalty will be levied and your account permanently sealed.",
            copilotAlert: "⚠️ Fake RBI Officer: RBI never calls individual citizens to threaten account seizures or penalty fines.",
            copilotAlertHindi: "⚠️ फर्जी आरबीआई अधिकारी: आरबीआई कभी भी आम नागरिकों को कॉल करके खाता सील करने की धमकी नहीं देता।",
            tactics: ["Regulatory Impersonation", "Threat of Penalty"],
            threatLevel: "HIGH",
            replies: [
              "Mera PAN aur Aadhaar pehle se linked hai, income tax portal par verified hai.",
              "RBI individual account holders ko call nahi karta. Aap jhooth bol rahe hain.",
              "Main apni branch jakar khud pata karunga."
            ],
            repliesHindi: [
              "मेरा पैन और आधार पहले से लिंक है, इनकम टैक्स पोर्टल पर वेरिफाइड है।",
              "आरबीआई सीधे खाताधारकों को कॉल नहीं करता। आप झूठ बोल रहे हैं।",
              "मैं अपनी शाखा जाकर खुद पता करूँगा।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir income tax portal down hai! Maine bank portal se biometric verification OTP bheja hai, turant 6 digit bataiye taaki penalty maaf ho jaye aur account unfreeze ho jaye!",
            hindi: "सर इनकम टैक्स पोर्टल डाउन है! मैंने बैंक पोर्टल से बायोमेट्रिक ऑथेंटिकेशन ओटीपी भेजा है, तुरंत 6 अंक बताइए ताकि पेनल्टी माफ हो जाए और खाता अनफ़्रीज़ हो जाए!",
            english: "Sir the portal is down! I sent a biometric authentication OTP from the banking gateway, tell me the 6 digits immediately to waive the penalty!",
            copilotAlert: "🚨 CRITICAL OTP EXTRACTION: Scammer is using government mandate fear to harvest your banking OTP!",
            copilotAlertHindi: "🚨 खतरनाक ओटीपी चोरी: सरकारी नियम का डर दिखाकर स्कैमर आपके खाते का ओटीपी चुराने की कोशिश कर रहा है!",
            tactics: ["Government Mandate Deception", "OTP Harvesting"],
            threatLevel: "CRITICAL",
            replies: [
              "Government compliance ke liye kabhi phone par OTP nahi manga jata. Main nahi doonga.",
              "Main yeh call cyber police helpline 1930 par forward kar raha hoon."
            ],
            repliesHindi: [
              "सरकारी नियमों के लिए कभी फोन पर ओटीपी नहीं मांगा जाता। मैं नहीं दूंगा।",
              "मैं यह कॉल साइबर पुलिस हेल्पलाइन 1930 पर फॉरवर्ड कर रहा हूँ।"
            ]
          }
        ]
      }
    ]
  },
  {
    id: "electricity",
    name: "💡 Power Cutoff / Discom",
    nameHindi: "💡 बिजली बिल कटऑफ फ्रॉड",
    callerName: "Electricity Board Sub-Division",
    callerNameHindi: "बिजली विभाग हेल्पलाइन (शर्मा)",
    callerNumber: "+91 98765 43210 (Mobile)",
    badge: "Discom Utility Scam",
    badgeHindi: "बिजली बिल फर्जीवाड़ा",
    variations: [
      {
        id: "tonight_cutoff",
        label: "Tonight 9:30 PM Cutoff Threat",
        labelHindi: "रात 9:30 बजे बिजली कट धमकी",
        icon: "⚡",
        description: "Scammer warns power will be disconnected at 9:30 PM due to an un-updated bill.",
        descriptionHindi: "स्कैमर कहता है बिल अपडेट नहीं हुआ है और रात 9:30 बजे बिजली काट दी जाएगी।",
        turns: [
          {
            speaker: "scammer",
            text: "Hello, electricity sub-division office se bol rahe hain. Pichle mahine ka bijli bill update nahi hua hai, aaj raat 9:30 baje line kaat di jayegi.",
            hindi: "हेलो, बिजली सब-डिवीजन ऑफिस से बोल रहे हैं। पिछले महीने का बिजली बिल अपडेट नहीं हुआ है, आज रात 9:30 बजे लाइन काट दी जाएगी।",
            english: "Hello, calling from electricity sub-division. Previous bill was not updated, power supply will be cut off tonight at 9:30 PM.",
            copilotAlert: "⚠️ Discom electricity boards never call from personal 10-digit mobile numbers or give 9:30 PM cutoff threats.",
            copilotAlertHindi: "⚠️ बिजली विभाग कभी भी निजी 10-अंकीय मोबाइल नंबर से रात 9:30 बजे लाइन काटने की धमकी नहीं देता।",
            tactics: ["Utility Impersonation", "Urgency Trap"],
            threatLevel: "HIGH",
            replies: [
              "Mera bill paid hai, consumer portal par check kijiye.",
              "Bijli vibhag aam mobile number se dhamki nahi deta.",
              "Main substation jakar pata karunga."
            ],
            repliesHindi: [
              "मेरा बिल भरा हुआ है, उपभोक्ता पोर्टल पर चेक करें।",
              "बिजली विभाग आम मोबाइल नंबर से धमकी नहीं देता।",
              "मैं सबस्टेशन जाकर पता करूँगा।"
            ]
          },
          {
            speaker: "scammer",
            text: "Server error tha sir! Turant hamare officer number par 15 rupaye ki update fee bhejiye aur receipt WhatsApp kijiye varna transformer se line cut ho jayegi!",
            hindi: "सर्वर एरर था सर! तुरंत हमारे ऑफिसर नंबर पर 15 रुपये की अपडेट फीस भेजिए और रसीद व्हाट्सएप कीजिए वरना ट्रांसफार्मर से लाइन कट जाएगी!",
            english: "It was a server error sir! Send Rs 15 update fee to our officer number and WhatsApp slip or power will be disconnected!",
            copilotAlert: "🚨 FRAUD DETECTED: Demanding direct payment to a personal phone number under threat of disconnection.",
            copilotAlertHindi: "🚨 धोखाधड़ी: बिजली काटने की धमकी देकर व्यक्तिगत नंबर पर पैसे मांगे जा रहे हैं।",
            tactics: ["Personal UPI Trap", "Coerced Payment"],
            threatLevel: "CRITICAL",
            replies: [
              "Sarkari bill official discom app par hi pay hota hai, personal UPI par nahi.",
              "Main meter reader aur discom helpline 1912 par call kar raha hoon."
            ],
            repliesHindi: [
              "सरकारी बिल आधिकारिक ऐप पर ही जमा होता है, किसी पर्सनल नंबर पर नहीं।",
              "मैं बिजली विभाग की हेल्पलाइन 1912 पर कॉल कर रहा हूँ।"
            ]
          }
        ]
      },
      {
        id: "smart_meter",
        label: "Smart Meter Fault & Fee Trap",
        labelHindi: "स्मार्ट मीटर खराबी व चार्ज",
        icon: "🔌",
        description: "Scammer claims your smart meter has communication error and will be deactivated in 1 hour.",
        descriptionHindi: "स्कैमर कहता है आपका स्मार्ट मीटर खराब है और 1 घंटे में बिजली बंद हो जाएगी।",
        turns: [
          {
            speaker: "scammer",
            text: "Namaste sir, electricity control room se bol rahe hain. Aapke ghar ka smart meter system me offline dikha raha hai. Agar 1 ghante me update nahi hua toh automatic line disconnect ho jayegi.",
            hindi: "नमस्ते सर, बिजली कंट्रोल रूम से बोल रहे हैं। आपके घर का स्मार्ट मीटर सिस्टम में ऑफलाइन दिखा रहा है। अगर 1 घंटे में अपडेट नहीं हुआ तो ऑटोमैटिक बिजली कट जाएगी।",
            english: "Namaste sir, calling from the power control room. Your smart meter is showing offline in our system. If not updated within 1 hour, power will automatically disconnect.",
            copilotAlert: "⚠️ Smart Meter Phishing: Discoms do not issue 1-hour automatic disconnect threats over mobile calls.",
            copilotAlertHindi: "⚠️ स्मार्ट मीटर फर्जीवाड़ा: बिजली कंपनियां 1 घंटे में ऑटोमैटिक बिजली काटने की धमकी नहीं देतीं।",
            tactics: ["Smart Meter Scare", "Panic Creation"],
            threatLevel: "HIGH",
            replies: [
              "Mera meter normal chal raha hai, main sub-station complaint karunga.",
              "Aap bijli vibhag ke 1912 helpline se baat karwayein."
            ],
            repliesHindi: [
              "मेरा मीटर सामान्य चल रहा है, मैं सब-स्टेशन में शिकायत करूँगा।",
              "आप बिजली विभाग की 1912 हेल्पलाइन से बात करवाएं।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir maine meter update link SMS kiya hai, uspar click karke 50 rupaye ka reconnection portal charge bhariye, turant online green signal ho jayega!",
            hindi: "सर मैंने मीटर अपडेट लिंक एसएमएस किया है, उसपर क्लिक करके 50 रुपये का रीकनेक्शन चार्ज भरिए, तुरंत मीटर ग्रीन हो जाएगा!",
            english: "Sir I sent a meter update link via SMS, click it and pay Rs 50 reconnection fee to turn the signal green!",
            copilotAlert: "🚨 PHISHING LINK DETECTED: The link leads to a fake payment page designed to capture UPI credentials!",
            copilotAlertHindi: "🚨 खतरनाक फ़िशिंग लिंक: यह लिंक फर्जी पेमेंट पेज खोलकर आपका यूपीआई पिन चुराने के लिए बनाया गया है!",
            tactics: ["Smishing / Malicious Link", "Credential Theft"],
            threatLevel: "CRITICAL",
            replies: [
              "Main kisi SMS link par payment nahi karunga.",
              "1912 par call karke fraudster number report kar raha hoon."
            ],
            repliesHindi: [
              "मैं किसी एसएमएस लिंक पर भुगतान नहीं करूँगा।",
              "1912 हेल्पलाइन पर इस नंबर की धोखाधड़ी रिपोर्ट कर रहा हूँ।"
            ]
          }
        ]
      }
    ]
  },
  {
    id: "digital_arrest",
    name: "📦 CBI & Narcotics Digital Arrest",
    nameHindi: "📦 सीबीआई व डिजिटल अरेस्ट",
    callerName: "DCP Vikram Rathore (Cyber Crime)",
    callerNameHindi: "डीसीपी विक्रम राठौर (साइबर सेल)",
    callerNumber: "+91 88291 00219 (Fake Badge)",
    badge: "Digital Arrest Extortion",
    badgeHindi: "फर्जी डिजिटल अरेस्ट ब्लैकमेल",
    variations: [
      {
        id: "drugs_parcel",
        label: "FedEx MDMA Narcotics Parcel",
        labelHindi: "फेडेक्स ड्रग्स पार्सल व वारंट",
        icon: "📦",
        description: "Scammer claims a FedEx parcel containing 140g MDMA drugs was seized with your Aadhaar.",
        descriptionHindi: "स्कैमर कहता है आपके आधार से बुक फेडेक्स पार्सल में 140 ग्राम ड्रग्स मिले हैं और गिरफ्तारी वारंट निकला है।",
        turns: [
          {
            speaker: "scammer",
            text: "I am DCP Vikram Rathore from Mumbai Cyber Crime Cell. FedEx courier IND-88291 containing 140 grams MDMA drugs in your name has been seized. Arrest warrant issued.",
            hindi: "मैं मुंबई साइबर क्राइम सेल से डीसीपी विक्रम राठौर बोल रहा हूँ। आपके नाम का फेडेक्स पार्सल जिसमें 140 ग्राम एमडीएमए ड्रग्स है, जब्त हुआ है। आपके खिलाफ गिरफ्तारी वारंट जारी हुआ है।",
            english: "I am DCP Vikram Rathore from Mumbai Cyber Crime Cell. FedEx parcel with 140g MDMA drugs in your name is seized. Supreme Court warrant issued.",
            copilotAlert: "🚨 EXTORTION IN PROGRESS: Supreme Court & Police confirm 'Digital Arrest' is 100% fake! Police never arrest anyone via phone or video call.",
            copilotAlertHindi: "🚨 ब्लैकमेल का प्रयास: सुप्रीम कोर्ट और पुलिस ने स्पष्ट किया है कि 'डिजिटल अरेस्ट' पूरी तरह फर्जी है! पुलिस कभी फोन पर अरेस्ट नहीं करती।",
            tactics: ["Police Impersonation", "Narcotics Blackmail"],
            threatLevel: "CRITICAL",
            replies: [
              "Indian law has no concept of Digital Arrest. I am going to the local police station.",
              "Send official legal summons to my address. Disconnecting now.",
              "Recording this call to submit to 1930 Cyber Crime Helpline."
            ],
            repliesHindi: [
              "भारतीय कानून में डिजिटल अरेस्ट जैसा कुछ नहीं है। मैं स्थानीय थाने जा रहा हूँ।",
              "मेरे घर के पते पर आधिकारिक समन भेजें। कॉल काट रहा हूँ।",
              "मैं यह कॉल रिकॉर्ड कर 1930 साइबर हेल्पलाइन पर भेज रहा हूँ।"
            ]
          },
          {
            speaker: "scammer",
            text: "Do not disconnect! You are under Digital Arrest! Stay in a locked room on Skype camera and transfer all your savings to RBI secure escrow account for anti-money laundering verification!",
            hindi: "कॉल डिस्कनेक्ट मत करो! तुम डिजिटल अरेस्ट में हो! कमरे में बंद रहो और स्काइप कैमरे पर आओ, अपनी सारी बचत आरबीआई के एस्क्रो खाते में ट्रांसफर करो सत्यापन के लिए!",
            english: "Do not disconnect! You are under Digital Arrest! Transfer all funds to RBI escrow account for verification!",
            copilotAlert: "🚨 FRAUD: Coercing you to transfer savings to 'RBI Escrow'. RBI never maintains citizen escrow accounts!",
            copilotAlertHindi: "🚨 महा-घोटाला: आरबीआई एस्क्रो खाते में पैसे ट्रांसफर करने का दबाव। आरबीआई के पास नागरिकों के लिए कोई एस्क्रो खाता नहीं होता!",
            tactics: ["Fake RBI Escrow", "Extortion Trap"],
            threatLevel: "CRITICAL",
            replies: [
              "RBI does not hold escrow accounts. You are a cyber criminal.",
              "I am hanging up and calling National Cyber Helpline 1930 immediately!"
            ],
            repliesHindi: [
              "आरबीआई कोई एस्क्रो खाता नहीं रखता। आप एक साइबर अपराधी हैं।",
              "मैं कॉल काटकर तुरंत 1930 साइबर हेल्पलाइन मिला रहा हूँ!"
            ]
          }
        ]
      },
      {
        id: "money_laundering",
        label: "Rs 3.8 Cr Hawala Laundering",
        labelHindi: "3.8 करोड़ हवाला मनी लॉन्ड्रिंग",
        icon: "⚖️",
        description: "Scammer claims your bank account was used in international hawala transactions.",
        descriptionHindi: "स्कैमर आपके खाते पर 3.8 करोड़ के हवाला मनी लॉन्ड्रिंग में एफआईआर होने का दावा करता है।",
        turns: [
          {
            speaker: "scammer",
            text: "Main CBI Special Investigation Team se Officer Verma bol raha hoon. Naresh Goyal money laundering case me aapke Canara Bank account me 3.8 crore ka hawala fund trace hua hai. Supreme Court ne non-bailable warrant issue kiya hai.",
            hindi: "मैं सीबीआई स्पेशल इन्वेस्टिगेशन टीम से ऑफिसर वर्मा बोल रहा हूँ। मनी लॉन्ड्रिंग केस में आपके खाते में 3.8 करोड़ का हवाला फंड ट्रेस हुआ है। सुप्रीम कोर्ट ने गैर-जमानती वारंट जारी किया है।",
            english: "Calling from CBI Special Investigation Team. In a major money laundering case, Rs 3.8 Crore hawala funds were traced to your account. Supreme Court has issued a non-bailable warrant.",
            copilotAlert: "🚨 CBI IMPERSONATION: CBI never calls citizens on mobile phones or conducts Supreme Court hearings over WhatsApp/Skype.",
            copilotAlertHindi: "🚨 फर्जी सीबीआई ऑफिसर: सीबीआई कभी फोन पर पूछताछ या सुप्रीम कोर्ट की सुनवाई नहीं करती।",
            tactics: ["CBI Impersonation", "Money Laundering Extortion"],
            threatLevel: "CRITICAL",
            replies: [
              "Main apne vakeel aur local police station se sampark kar raha hoon.",
              "Official legal notice postal service se bhejiye, video call par baat nahi karunga."
            ],
            repliesHindi: [
              "मैं अपने वकील और स्थानीय थाने से संपर्क कर रहा हूँ।",
              "आधिकारिक कानूनी नोटिस डाक से भेजें, फोन पर बात नहीं करूँगा।"
            ]
          },
          {
            speaker: "scammer",
            text: "Agar bail chahiye toh turant hamare Secret Government Clearance Account me 2 lakh rupaye security deposit bhejiye, verification ke baad wapas mil jayenge!",
            hindi: "अगर ज़मानत चाहिए तो तुरंत हमारे सीक्रेट गवर्नमेंट क्लीयरेंस खाते में 2 लाख रुपये सिक्योरिटी डिपॉजिट भेजिए, जांच के बाद वापस मिल जाएंगे!",
            english: "If you want clearance, transfer Rs 2 Lakh security deposit to our Secret Government Clearance Account immediately!",
            copilotAlert: "🚨 EXTORTION ATTEMPT: No government clearance account exists! Criminals extort life savings through terror.",
            copilotAlertHindi: "🚨 जबरन वसूली (Extortion): सरकारी क्लीयरेंस खाता जैसा कुछ नहीं होता! यह ठगों का निजी खाता है!",
            tactics: ["Extortion Payment", "Coercion"],
            threatLevel: "CRITICAL",
            replies: [
              "Main ek rupaya bhi transfer nahi karunga. 1930 cyber police ko complaint de raha hoon."
            ],
            repliesHindi: [
              "मैं एक रुपया भी ट्रांसफर नहीं करूँगा। तुरंत 1930 पर शिकायत दर्ज कर रहा हूँ।"
            ]
          }
        ]
      }
    ]
  },
  {
    id: "kbc_lottery",
    name: "🎟️ KBC & Lottery Prize",
    nameHindi: "🎟️ केबीसी 25 लाख लॉटरी",
    callerName: "KBC Lucky Draw (Rana Pratap)",
    callerNameHindi: "केबीसी हेड ऑफिस (राणा प्रताप)",
    callerNumber: "+92 301 982144 (Fake Country)",
    badge: "Lottery Advance Fee",
    badgeHindi: "लॉटरी फ्रॉड",
    variations: [
      {
        id: "kbc_25_lakh",
        label: "KBC 25 Lakh Prize Cheque",
        labelHindi: "केबीसी 25 लाख लकी ड्रॉ",
        icon: "🏆",
        description: "Scammer claims your SIM card won Rs 25 Lakh in KBC and demands Rs 12,500 tax fees.",
        descriptionHindi: "स्कैमर कहता है आपने केबीसी में 25 लाख जीते हैं और 12,500 रुपये टैक्स फीस मांगता है।",
        turns: [
          {
            speaker: "scammer",
            text: "Namaste! Main Kaun Banega Crorepati Head Office Mumbai se Manager Rana Pratap bol raha hoon. All India SIM Card Lucky Draw me aapke number ne Rs 25,00,000 ka cash prize jeeta hai!",
            hindi: "नमस्ते! मैं कौन बनेगा करोड़पति हेड ऑफिस मुंबई से मैनेजर राणा प्रताप बोल रहा हूँ। ऑल इंडिया सिम कार्ड लकी ड्रॉ में आपके नंबर ने 25,00,000 रुपये का नकद इनाम जीता है!",
            english: "Namaste! I am Manager Rana Pratap from KBC Head Office Mumbai. In our All India SIM Card Lucky Draw, your number has won Rs 25,00,000 cash prize!",
            copilotAlert: "⚠️ Classic Lottery Scam: KBC never conducts SIM card lucky draws. Nobody wins money in contests they never entered.",
            copilotAlertHindi: "⚠️ फर्जी लॉटरी फ्रॉड: केबीसी कभी भी सिम कार्ड लकी ड्रॉ नहीं कराता। बिना भाग लिए कोई लॉटरी नहीं मिलती।",
            tactics: ["Advance Fee Fraud", "Greed Lure"],
            threatLevel: "HIGH",
            replies: [
              "Maine KBC me hissa nahi liya tha. Yeh fake lottery hai.",
              "Agar 25 lakh mile hain toh tax usme se kaat kar baki 24 lakh bhej do!",
              "Aapka international number dikh raha hai, fraud mat karo."
            ],
            repliesHindi: [
              "मैंने केबीसी में भाग नहीं लिया था। यह फर्जी लॉटरी है।",
              "अगर 25 लाख मिले हैं तो टैक्स काटकर बाकी पैसे भेज दो!",
              "आपका नंबर अंतरराष्ट्रीय दिख रहा है, फ्रॉड मत करो।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir RBI aur Income Tax ka rule hai tax pehle jama karna padta hai! Hamare SBI officer ke account me 12,500 rupaye GST fee pay kijiye aur 10 minute me 25 lakh ka cheque aapke ghar!",
            hindi: "सर आरबीआई और इनकम टैक्स का नियम है कि टैक्स पहले जमा करना पड़ता है! हमारे ऑफिसर के खाते में 12,500 रुपये जीएसटी फीस ट्रांसफर करें और 10 मिनट में 25 लाख का चेक आपके घर!",
            english: "Sir RBI and Income Tax rule requires upfront tax! Pay Rs 12,500 GST fee to our officer's SBI account and receive 25 Lakh cheque in 10 minutes!",
            copilotAlert: "🚨 ADVANCE-FEE SCAM: Demanding upfront tax/processing fees before releasing fake prizes.",
            copilotAlertHindi: "🚨 एडवांस टैक्स फ्रॉड: फर्जी लॉटरी के नाम पर पहले 12,500 रुपये ठगने की कोशिश।",
            tactics: ["Advance Fee Tax Trap", "Fake Cheque Bait"],
            threatLevel: "CRITICAL",
            replies: [
              "Asli lottery prize se TDS cut hota hai, advance cash koi nahi maangta. Call cut kar raha hoon!"
            ],
            repliesHindi: [
              "असली लॉटरी में टीडीएस कटकर मिलता है, कोई एडवांस पैसे नहीं मांगता। कॉल काट रहा हूँ!"
            ]
          }
        ]
      }
    ]
  },
  {
    id: "trai_sim",
    name: "📱 TRAI SIM Deactivation",
    nameHindi: "📱 ट्राई सिम कार्ड ब्लॉक धमकी",
    callerName: "TRAI Telecom Department",
    callerNameHindi: "दूरसंचार विभाग (TRAI)",
    callerNumber: "+91 80010 99281 (IVR)",
    badge: "Telecom Impersonation",
    badgeHindi: "टेलीकॉम फ्रॉड",
    variations: [
      {
        id: "sim_block_2hr",
        label: "2-Hour SIM Disconnect Notice",
        labelHindi: "2 घंटे में सिम ब्लॉक नोटिस",
        icon: "📵",
        description: "Scammer claims illegal SMS spamming was reported on your number and demands Aadhaar/OTP.",
        descriptionHindi: "स्कैमर कहता है आपके नंबर से आपत्तिजनक मैसेज भेजे गए हैं और 2 घंटे में सिम ब्लॉक हो जाएगी।",
        turns: [
          {
            speaker: "scammer",
            text: "Telecom Regulatory Authority of India (TRAI) alert: Aapke number se illegal advertising aur threat messages report hue hain. 2 ghante ke andar aapke sabhi mobile number deactivate kar diye jayenge.",
            hindi: "भारतीय दूरसंचार नियामक प्राधिकरण (TRAI) अलर्ट: आपके मोबाइल नंबर से गैर-कानूनी विज्ञापन और धमकी भरे संदेश भेजे गए हैं। 2 घंटे में आपके सभी सिम कार्ड बंद कर दिए जाएंगे।",
            english: "TRAI Alert: Illegal SMS spamming and extortion reported from your number. All your mobile numbers will be permanently disconnected within 2 hours.",
            copilotAlert: "⚠️ TRAI Impersonation: TRAI never calls individual telecom subscribers to threaten SIM card disconnection.",
            copilotAlertHindi: "⚠️ फर्जी ट्राई अधिकारी: ट्राई कभी भी आम मोबाइल उपभोक्ताओं को कॉल करके सिम बंद करने की धमकी नहीं देता।",
            tactics: ["TRAI Impersonation", "Fabricated Offense"],
            threatLevel: "HIGH",
            replies: [
              "Main apne official telecom provider (Jio/Airtel) ke store jakar pata karunga.",
              "TRAI direct customer ko call nahi karta. Aap fraud kar rahe hain."
            ],
            repliesHindi: [
              "मैं अपने टेलीकॉम ऑपरेटर (Jio/Airtel) के नजदीकी स्टोर जाकर पता करूँगा।",
              "ट्राई सीधे ग्राहकों को कॉल नहीं करता। आप फ्रॉड कर रहे हैं।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir agar disconnection rokna hai toh turant hamare officer ko apna 12-digit Aadhaar number aur verification OTP bataiye varna police case file ho jayega!",
            hindi: "सर अगर सिम ब्लॉक होने से बचाना है तो तुरंत हमारे अधिकारी को अपना 12 अंकों का आधार नंबर और वेरिफिकेशन ओटीपी बताइए वरना पुलिस केस दर्ज हो जाएगा!",
            english: "Sir if you want to prevent deactivation, tell our officer your 12-digit Aadhaar number and verification OTP immediately!",
            copilotAlert: "🚨 IDENTITY THEFT ATTEMPT: Scammer demands Aadhaar and OTP to hijack your mobile identity and access bank accounts!",
            copilotAlertHindi: "🚨 पहचान की चोरी (Identity Theft): आधार और ओटीपी चुराकर बैंक खाते खाली करने की साजिश!",
            tactics: ["Aadhaar Solicitation", "OTP Harvesting"],
            threatLevel: "CRITICAL",
            replies: [
              "Aadhaar aur OTP phone par kisi ko nahi diya jata. Main 1930 par report kar raha hoon!"
            ],
            repliesHindi: [
              "आधार और ओटीपी फोन पर किसी को नहीं दिया जाता। मैं 1930 पर रिपोर्ट कर रहा हूँ!"
            ]
          }
        ]
      }
    ]
  },
  {
    id: "wfh_telegram",
    name: "💼 WFH / YouTube Like Scam",
    nameHindi: "💼 वर्क फ्रॉम होम टास्क फ्रॉड",
    callerName: "HR Global Media (Pooja Sharma)",
    callerNameHindi: "एचआर रिक्रूटमेंट (पूजा)",
    callerNumber: "+91 70211 44521",
    badge: "Part-Time Task Scam",
    badgeHindi: "टास्क फ्रॉड",
    variations: [
      {
        id: "youtube_like",
        label: "YouTube Video Like & Earn",
        labelHindi: "यूट्यूब लाइक व टास्क फ्रॉड",
        icon: "💻",
        description: "Scammer offers Rs 2,500 daily for liking videos and then traps victim in prepaid tasks.",
        descriptionHindi: "स्कैमर यूट्यूब वीडियो लाइक करने पर 2500 रुपये रोज़ाना देने का लालच देकर प्रीपेड टास्क में फंसाता है।",
        turns: [
          {
            speaker: "scammer",
            text: "Hello sir! Main Global Media HR Pooja bol rahi hoon. Hamari company me part-time Work From Home job available hai. Sirf 5 YouTube videos like karne par daily 2,500 rupaye kamayein. Kya aap interested hain?",
            hindi: "हेलो सर! मैं ग्लोबल मीडिया एचआर पूजा बोल रही हूँ। हमारी कंपनी में पार्ट-टाइम वर्क फ्रॉम होम जॉब उपलब्ध है। सिर्फ 5 यूट्यूब वीडियो लाइक करके रोज़ाना 2,500 रुपये कमाएं। क्या आप इच्छुक हैं?",
            english: "Hello sir! Calling from Global Media HR. We have a part-time WFH job. Earn Rs 2,500 daily just by liking 5 YouTube videos. Are you interested?",
            copilotAlert: "⚠️ WFH Task Scam: Legitimate companies never pay Rs 500 per video like. This is an entry point to Telegram investment fraud.",
            copilotAlertHindi: "⚠️ वर्क फ्रॉम होम टास्क फ्रॉड: वीडियो लाइक करने के लिए कोई कंपनी 500 रुपये नहीं देती। यह टेलीग्राम टास्क स्कैम का जाल है।",
            tactics: ["Easy Money Lure", "Task-Based Fraud"],
            threatLevel: "HIGH",
            replies: [
              "Video like karne ke koi paise nahi deta. Yeh fake scheme hai.",
              "Mujhe part time job nahi chahiye, dobara call mat karna."
            ],
            repliesHindi: [
              "वीडियो लाइक करने के कोई पैसे नहीं देता। यह फर्जी स्कीम है।",
              "मुझे पार्ट टाइम जॉब नहीं चाहिए, दोबारा कॉल मत करना।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir demo task complete hone par 250 rupaye milenge, phir VIP merchant group me 5,000 jama karke 8,500 rupaye turant withdrawal kijiye!",
            hindi: "सर डेमो टास्क पूरा होने पर 250 रुपये मिलेंगे, फिर वीआईपी मर्चेंट ग्रुप में 5,000 जमा करके 8,500 रुपये तुरंत निकालिए!",
            english: "Sir after completing demo task you get Rs 250, then deposit Rs 5,000 in VIP merchant group to withdraw Rs 8,500 instantly!",
            copilotAlert: "🚨 PREPAID TASK PONZI: Initial small payment is bait. Once you deposit Rs 5,000+, they freeze your funds and demand lakhs!",
            copilotAlertHindi: "🚨 प्रीपेड टास्क पोंजी ट्रैप: पहले 200 रुपये देकर भरोसा जीतते हैं, फिर 5000+ रुपये जमा करवाकर पैसे हड़प लेते हैं!",
            tactics: ["Prepaid Task Trap", "Deposit Extortion"],
            threatLevel: "CRITICAL",
            replies: [
              "Pehle paise jama karwane wali har job 100% fraud hoti hai. Call disconnect kar raha hoon!"
            ],
            repliesHindi: [
              "पहले पैसे जमा करवाने वाली हर जॉब 100% फ्रॉड होती है। कॉल काट रहा हूँ!"
            ]
          }
        ]
      }
    ]
  },
  {
    id: "traffic_challan",
    name: "🚗 Traffic Police E-Challan",
    nameHindi: "🚗 ट्रैफिक पुलिस ई-चालान कॉल",
    callerName: "Traffic Police Control Room",
    callerNameHindi: "ट्रैफिक पुलिस कंट्रोल रूम",
    callerNumber: "+91 99120 44102",
    badge: "Government Impersonation",
    badgeHindi: "ई-चालान फर्जीवाड़ा",
    variations: [
      {
        id: "court_challan",
        label: "Court Challan & License Block",
        labelHindi: "कोर्ट चालान व लाइसेंस रद्द धमकी",
        icon: "🚨",
        description: "Scammer claims a Rs 3,500 overdue speed violation fine must be paid immediately on a fake link.",
        descriptionHindi: "स्कैमर 3,500 रुपये का पेंडिंग चालान तुरंत फर्जी लिंक पर भरने का दबाव डालता है।",
        turns: [
          {
            speaker: "scammer",
            text: "Traffic police control room se bol raha hoon. Aapki vehicle par Rs 3,500 ka overspeeding court challan pending hai. Aaj payment nahi kiya toh Driving License aur RC permanently suspend kar di jayegi.",
            hindi: "ट्रैफिक पुलिस कंट्रोल रूम से बोल रहा हूँ। आपकी गाड़ी पर 3,500 रुपये का कोर्ट चालान पेंडिंग है। आज भुगतान नहीं किया तो ड्राइविंग लाइसेंस और आरसी स्थायी रूप से निलंबित कर दी जाएगी।",
            english: "Calling from Traffic Police control room. Your vehicle has a Rs 3,500 overdue court challan. If not paid today, your Driving License and RC will be suspended.",
            copilotAlert: "⚠️ Fake E-Challan Call: Traffic police never calls citizens on mobile phones threatening RC/DL suspension.",
            copilotAlertHindi: "⚠️ फर्जी ई-चालान कॉल: ट्रैफिक पुलिस कभी फोन पर आरसी/लाइसेंस रद्द करने की धमकी देकर पैसे नहीं मांगती।",
            tactics: ["Traffic Police Impersonation", "License Cancellation Threat"],
            threatLevel: "HIGH",
            replies: [
              "Mera challan official echallan.parivahan.gov.in portal par check karunga.",
              "Traffic police phone par payment karne ke liye call nahi karti."
            ],
            repliesHindi: [
              "मैं अपना चालान आधिकारिक echallan.parivahan.gov.in पोर्टल पर चेक करूँगा।",
              "ट्रैफिक पुलिस फोन पर भुगतान करने के लिए कॉल नहीं करती।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir court notice bachaane ke liye hamare link echallan-parivahan-gov.live par jakar abhi 500 rupaye court fee UPI se pay kijiye varna police summon ghar aayega!",
            hindi: "सर कोर्ट नोटिस से बचने के लिए हमारे लिंक echallan-parivahan-gov.live पर जाकर अभी 500 रुपये कोर्ट फीस यूपीआई से भरिए वरना पुलिस समन घर आएगा!",
            english: "To avoid court summons, visit our link echallan-parivahan-gov.live and pay Rs 500 court fee via UPI right now!",
            copilotAlert: "🚨 PHISHING URL: Look at the fake domain .live! Genuine government portals always end in .gov.in!",
            copilotAlertHindi: "🚨 खतरनाक फर्जी लिंक: ध्यान दें डोमेन .live है! सरकारी पोर्टल हमेशा .gov.in पर खत्म होते हैं!",
            tactics: ["Fake .gov.in Domain", "UPI Phishing"],
            threatLevel: "CRITICAL",
            replies: [
              "Yeh fake .live website hai. Official portal hamesha .gov.in hota hai. Call rakhiye!"
            ],
            repliesHindi: [
              "यह फर्जी .live वेबसाइट है। आधिकारिक पोर्टल हमेशा .gov.in होता है। कॉल रखिए!"
            ]
          }
        ]
      }
    ]
  },
  {
    id: "courier_hold",
    name: "📬 India Post / Courier Hold",
    nameHindi: "📬 इंडिया पोस्ट पार्सल होल्ड",
    callerName: "Speed Post Hub (Amit Kumar)",
    callerNameHindi: "स्पीड पोस्ट डिलीवरी हब",
    callerNumber: "+91 94101 88390",
    badge: "Postal Smishing",
    badgeHindi: "पार्सल फ्रॉड",
    variations: [
      {
        id: "address_update_10rs",
        label: "Address Update & Rs 10 Fee",
        labelHindi: "पता सुधार व 10 रु फीस ट्रैप",
        icon: "📦",
        description: "Scammer claims a parcel is on hold due to missing house number and demands a Rs 10 redelivery fee.",
        descriptionHindi: "स्कैमर कहता है पार्सल का पता गलत है और 10 रुपये री-डिलीवरी फीस के बहाने कार्ड डिटेल्स चुराता है।",
        turns: [
          {
            speaker: "scammer",
            text: "Hello sir, Speed Post delivery branch se bol raha hoon. Aapka important parcel hub par ruka hua hai kyunki delivery address me flat number missing hai.",
            hindi: "हेलो सर, स्पीड पोस्ट डिलीवरी शाखा से बोल रहा हूँ। आपका महत्वपूर्ण पार्सल हब पर रुका हुआ है क्योंकि पते में मकान नंबर अधूरा है।",
            english: "Hello sir, calling from Speed Post branch. Your important parcel is stuck at the hub because the house number is missing from the address.",
            copilotAlert: "⚠️ India Post Smishing: India Post never calls customers demanding address updates or redelivery fees.",
            copilotAlertHindi: "⚠️ डाक विभाग फ़िशिंग: इंडिया पोस्ट कभी भी फोन करके पता सुधारने या री-डिलीवरी फीस के लिए कॉल नहीं करता।",
            tactics: ["Postal Impersonation", "Missing Address Lure"],
            threatLevel: "HIGH",
            replies: [
              "Maine koi parcel book nahi kiya hai, consignment tracking number batayein.",
              "Main local post office jakar pata karunga."
            ],
            repliesHindi: [
              "मैंने कोई पार्सल बुक नहीं किया, कंसाइनमेंट ट्रैकिंग नंबर बताएं।",
              "मैं स्थानीय डाकघर जाकर पता करूँगा।"
            ]
          },
          {
            speaker: "scammer",
            text: "Sir parcel return hone se bachane ke liye hamare link indiapost-tracking.site par jakar sirf 10 rupaye redelivery charges card se pay kijiye!",
            hindi: "सर पार्सल वापस जाने से बचाने के लिए हमारे लिंक indiapost-tracking.site पर जाकर सिर्फ 10 रुपये री-डिलीवरी शुल्क कार्ड से भरिए!",
            english: "Sir to avoid parcel return, visit indiapost-tracking.site and pay a nominal Rs 10 redelivery fee using your debit card!",
            copilotAlert: "🚨 CARD DUMP ATTACK: Scammers use small Rs 10 fees as bait to harvest complete card numbers, CVVs, and OTPs!",
            copilotAlertHindi: "🚨 कार्ड चोरी का जाल: मात्र 10 रुपये का झांसा देकर स्कैमर आपके पूरे डेबिट कार्ड का नंबर, सीवीवी और ओटीपी चुरा लेते हैं!",
            tactics: ["Rs 10 Phishing Bait", "Banking Card Dumping"],
            threatLevel: "CRITICAL",
            replies: [
              "10 rupaye ke bahane card data chori karne ki chal hai! Call disconnect kar raha hoon."
            ],
            repliesHindi: [
              "10 रुपये के बहाने कार्ड डेटा चोरी करने की चाल है! कॉल काट रहा हूँ।"
            ]
          }
        ]
      }
    ]
  }
];

export default function ScamCallSimulator({ onOpen1930Modal, language = 'hinglish' }) {
  const [selectedScenarioIndex, setSelectedScenarioIndex] = useState(0);
  const [selectedVariationIndex, setSelectedVariationIndex] = useState(0);
  const [callState, setCallState] = useState('idle'); // idle | ringing | connected | ended
  const [currentTurnIndex, setCurrentTurnIndex] = useState(0);
  const [callDuration, setCallDuration] = useState(0);
  const [dialogueHistory, setDialogueHistory] = useState([]);
  const [copilotStatus, setCopilotStatus] = useState(null);
  const [isScammerSpeaking, setIsScammerSpeaking] = useState(false);
  
  const timerRef = useRef(null);

  const scenario = SCENARIOS[selectedScenarioIndex] || SCENARIOS[0];
  const variations = scenario.variations || [];
  const activeVariation = variations[selectedVariationIndex] || variations[0];

  useEffect(() => {
    if (callState === 'connected') {
      timerRef.current = setInterval(() => {
        setCallDuration((prev) => prev + 1);
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
      setCallDuration(0);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [callState]);

  // Handle Scenario Switch
  const handleSelectScenario = (idx) => {
    handleHangupCall();
    setSelectedScenarioIndex(idx);
    setSelectedVariationIndex(0);
  };

  // Handle Variation / Asking Style Switch
  const handleSelectVariation = (varIdx) => {
    handleHangupCall();
    setSelectedVariationIndex(varIdx);
  };

  // Shuffle / Randomize Asking Style
  const handleShuffleVariation = () => {
    handleHangupCall();
    if (variations.length > 1) {
      let nextIdx = selectedVariationIndex;
      while (nextIdx === selectedVariationIndex) {
        nextIdx = Math.floor(Math.random() * variations.length);
      }
      setSelectedVariationIndex(nextIdx);
    } else {
      // Pick another random scenario
      const nextScenarioIdx = (selectedScenarioIndex + 1) % SCENARIOS.length;
      setSelectedScenarioIndex(nextScenarioIdx);
      setSelectedVariationIndex(0);
    }
  };

  const handleStartCall = () => {
    setCallState('ringing');
    setCurrentTurnIndex(0);
    setDialogueHistory([]);
    setCopilotStatus(null);
    soundSynth.playRingtone();
  };

  const handleAnswerCall = () => {
    soundSynth.stopRingtone();
    soundSynth.playClick();
    setCallState('connected');
    triggerScammerTurn(0);
  };

  const handleHangupCall = () => {
    soundSynth.stopRingtone();
    soundSynth.stopSiren();
    speechEngine.stopSpeaking();
    setIsScammerSpeaking(false);
    setCallState('ended');
  };

  const triggerScammerTurn = (turnIdx) => {
    const turns = activeVariation.turns || [];
    if (turnIdx >= turns.length) {
      setCallState('ended');
      return;
    }

    const turnData = turns[turnIdx];
    setCurrentTurnIndex(turnIdx);

    const spokenText = language === 'english' ? turnData.english : (language === 'hindi' ? turnData.hindi : turnData.text);

    const scammerMsg = {
      speaker: 'scammer',
      text: turnData.text,
      hindi: turnData.hindi,
      english: turnData.english
    };

    setDialogueHistory((prev) => [...prev, scammerMsg]);

    const alertText = language === 'hindi' 
      ? turnData.copilotAlertHindi 
      : language === 'english' 
      ? turnData.copilotAlert 
      : turnData.copilotAlert;

    const repliesList = language === 'hindi' 
      ? turnData.repliesHindi || turnData.replies 
      : turnData.replies;

    setCopilotStatus({
      alert: alertText,
      threatLevel: turnData.threatLevel,
      tactics: turnData.tactics,
      replies: repliesList
    });

    if (turnData.threatLevel === 'CRITICAL') {
      soundSynth.playSiren();
    }

    setIsScammerSpeaking(true);
    speechEngine.speak(spokenText, {
      lang: language === 'english' ? 'en-IN' : 'hi-IN',
      rate: 1.0,
      pitch: 0.92,
      onEnd: () => setIsScammerSpeaking(false),
      onError: () => setIsScammerSpeaking(false)
    });
  };

  const handleUserReply = (replyText) => {
    if (!replyText || !replyText.trim()) return;
    speechEngine.stopSpeaking();
    setIsScammerSpeaking(false);

    const userMsg = {
      speaker: 'user',
      text: replyText
    };

    setDialogueHistory((prev) => [...prev, userMsg]);

    setTimeout(() => {
      const turns = activeVariation.turns || [];
      const nextTurn = currentTurnIndex + 1;
      if (nextTurn < turns.length) {
        triggerScammerTurn(nextTurn);
      } else {
        const scammerBusted = {
          speaker: 'scammer',
          text: language === 'hindi' 
            ? "🚨 [स्कैमर घबरा गया और उसने तुरंत फोन काट दिया — आपने साइबर ठगी को सफलतापूर्वक नाकाम कर दिया!]" 
            : "🚨 [SCAMMER PANICS & HANGS UP — You successfully neutralized the cyber fraud attempt!]",
          hindi: "🚨 [स्कैमर घबरा गया और उसने तुरंत फोन काट दिया — आपने साइबर ठगी को सफलतापूर्वक नाकाम कर दिया!]",
          english: "🚨 [Scammer panics and hangs up — You successfully neutralized the cyber fraud attempt!]"
        };
        setDialogueHistory((prev) => [...prev, scammerBusted]);
        setCallState('ended');
        soundSynth.playSuccessChime();
      }
    }, 1100);
  };

  const formatTime = (secs) => {
    const mins = Math.floor(secs / 60);
    const rem = secs % 60;
    return `${mins.toString().padStart(2, '0')}:${rem.toString().padStart(2, '0')}`;
  };

  const getCallerName = () => (language === 'hindi' ? scenario.callerNameHindi || scenario.callerName : scenario.callerName);
  const getBadgeName = () => (language === 'hindi' ? scenario.badgeHindi || scenario.badge : scenario.badge);

  return (
    <div className="w-full max-w-6xl mx-auto px-4 sm:px-6 py-6">
      {/* Title & Top Description */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-2.5">
            <span>{language === 'hindi' ? 'लाइव स्कैम कॉल सिम्युलेटर' : 'Live Scam Call Simulator'}</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-950 border border-cyan-800 text-cyan-400 font-semibold uppercase tracking-wider">
              Bilingual Copilot
            </span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            {language === 'hindi'
              ? 'अलग-अलग तरीकों से स्कैमर कैसे फोन पर बात करते हैं, और रक्षक एआई कैसे तुरंत चाल पकड़ता है।'
              : 'Experience how fraudsters use different asking angles over the phone, and how Rakshak AI counters them.'}
          </p>
        </div>

        {/* Shuffle Button */}
        <button
          onClick={handleShuffleVariation}
          className="inline-flex items-center gap-2 px-3.5 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-slate-950 font-bold rounded-xl text-xs shadow-lg shadow-cyan-900/30 transition-all cursor-pointer self-start md:self-auto hover:scale-105"
          title={language === 'hindi' ? 'दूसरा तरीका / रैंडम सवाल पूछें' : 'Shuffle asking angle / question style'}
        >
          <Shuffle className="w-3.5 h-3.5 text-slate-950" />
          <span>{language === 'hindi' ? '🎲 नया तरीका (Shuffle Style)' : '🎲 Shuffle Asking Style'}</span>
        </button>
      </div>

      {/* 1. Category Selector Pills */}
      <div className="mb-4">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
          {language === 'hindi' ? '1. स्कैम श्रेणी चुनें (Scam Category):' : '1. Select Scam Category:'}
        </p>
        <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-thin">
          {SCENARIOS.map((sc, idx) => (
            <button
              key={sc.id}
              onClick={() => handleSelectScenario(idx)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer flex-shrink-0 ${
                selectedScenarioIndex === idx
                  ? 'bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20'
                  : 'bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700/60'
              }`}
            >
              {language === 'hindi' ? sc.nameHindi || sc.name : sc.name}
            </button>
          ))}
        </div>
      </div>

      {/* 2. Asking Way / Angle Selector Pills */}
      <div className="mb-6 p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
        <div className="flex items-center justify-between gap-2 mb-2">
          <p className="text-xs font-bold text-cyan-400 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>{language === 'hindi' ? '2. पूछने का तरीका चुनें (Different Ways Scammer Asks):' : '2. Choose How Scammer Asks (Different Asking Angles):'}</span>
          </p>
          <span className="text-[11px] text-slate-400">
            {variations.length} {language === 'hindi' ? 'अलग तरीके उपलब्ध' : 'styles available'}
          </span>
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          {variations.map((v, vIdx) => {
            const isSelected = selectedVariationIndex === vIdx;
            return (
              <button
                key={v.id}
                onClick={() => handleSelectVariation(vIdx)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer flex items-center gap-1.5 ${
                  isSelected
                    ? 'bg-rose-600 text-white font-bold shadow-md shadow-rose-900/40 ring-2 ring-rose-400/50'
                    : 'bg-slate-800 hover:bg-slate-700/80 text-slate-300 border border-slate-700'
                }`}
              >
                <span>{v.icon}</span>
                <span>{language === 'hindi' ? v.labelHindi || v.label : v.label}</span>
              </button>
            );
          })}
        </div>
        <p className="text-[11px] text-slate-400 mt-2 italic">
          💡 {language === 'hindi' ? activeVariation.descriptionHindi : activeVariation.description}
        </p>
      </div>

      {/* Main Grid: Phone Mockup & Copilot Transcript */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left: Phone Screen Mockup */}
        <div className="lg:col-span-5 flex justify-center">
          <div className="w-full max-w-[320px] rounded-3xl bg-[#030712] border-4 border-slate-700 shadow-2xl p-5 flex flex-col justify-between min-h-[530px]">
            {/* Top Phone Header */}
            <div className="flex items-center justify-between text-xs text-slate-400 font-mono mb-4">
              <span>09:41</span>
              <div className="w-16 h-3.5 bg-slate-900 rounded-full border border-slate-800" />
              <div className="flex items-center gap-1">
                <Signal className="w-3 h-3 text-slate-400" />
                <Wifi className="w-3 h-3 text-slate-400" />
                <Battery className="w-3.5 h-3.5 text-slate-400" />
              </div>
            </div>

            {/* Caller Info */}
            <div className="text-center my-auto py-4">
              <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-slate-800 border-2 border-slate-700 flex items-center justify-center text-slate-300 shadow-inner">
                <Phone className={`w-8 h-8 ${callState === 'ringing' ? 'text-rose-400 animate-bounce' : 'text-slate-400'}`} />
              </div>

              <h3 className="text-base font-bold text-white px-2">
                {getCallerName()}
              </h3>
              <p className="text-xs text-slate-400 mt-0.5 font-mono">
                {scenario.callerNumber}
              </p>
              
              <div className="mt-2 inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-rose-950/70 border border-rose-800/50 text-rose-300 text-[11px] font-medium">
                <span>{activeVariation.icon}</span>
                <span>{language === 'hindi' ? activeVariation.labelHindi : activeVariation.label}</span>
              </div>

              {/* Status Indicator */}
              <div className="mt-4 text-xs font-medium">
                {callState === 'idle' && (
                  <span className="text-slate-500">
                    {language === 'hindi' ? 'सिम्युलेशन के लिए तैयार' : 'Ready to simulate'}
                  </span>
                )}
                {callState === 'ringing' && (
                  <span className="text-rose-400 font-bold animate-pulse">
                    🔔 {language === 'hindi' ? 'इनकमिंग कॉल आ रही है...' : 'Incoming Call...'}
                  </span>
                )}
                {callState === 'connected' && (
                  <div className="text-emerald-400 flex items-center justify-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                    <span>{language === 'hindi' ? 'कॉल जारी है • ' : 'Call in progress • '}</span>
                    <span className="font-mono font-bold text-white">{formatTime(callDuration)}</span>
                  </div>
                )}
                {callState === 'ended' && (
                  <span className="text-amber-400 flex items-center justify-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-amber-400" />
                    <span>{language === 'hindi' ? 'कॉल समाप्त हुई' : 'Call Ended'}</span>
                  </span>
                )}
              </div>
            </div>

            {/* Call Action Buttons */}
            <div className="pt-3 border-t border-slate-800/60">
              {callState === 'idle' && (
                <button
                  onClick={handleStartCall}
                  className="w-full py-3 bg-rose-600 hover:bg-rose-500 text-white font-bold rounded-xl text-xs uppercase tracking-wider transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-rose-900/40"
                >
                  <PhoneCall className="w-4 h-4" />
                  <span>{language === 'hindi' ? 'नकली कॉल शुरू करें' : 'Start Incoming Call'}</span>
                </button>
              )}

              {callState === 'ringing' && (
                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={handleHangupCall}
                    className="py-3 bg-slate-800 hover:bg-slate-700 text-rose-400 font-bold rounded-xl text-xs border border-rose-500/30 flex items-center justify-center gap-2 cursor-pointer"
                  >
                    <PhoneOff className="w-4 h-4" />
                    <span>{language === 'hindi' ? 'काटें' : 'Decline'}</span>
                  </button>
                  <button
                    onClick={handleAnswerCall}
                    className="py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-2 cursor-pointer animate-pulse"
                  >
                    <Phone className="w-4 h-4" />
                    <span>{language === 'hindi' ? 'उठाएं' : 'Answer'}</span>
                  </button>
                </div>
              )}

              {callState === 'connected' && (
                <button
                  onClick={handleHangupCall}
                  className="w-full py-3 bg-rose-600 hover:bg-rose-500 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-2 cursor-pointer"
                >
                  <PhoneOff className="w-4 h-4" />
                  <span>{language === 'hindi' ? 'कॉल काटें (Hang Up)' : 'Hang Up Call'}</span>
                </button>
              )}

              {callState === 'ended' && (
                <div className="space-y-2">
                  <button
                    onClick={handleStartCall}
                    className="w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-xl text-xs flex items-center justify-center gap-2 cursor-pointer"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>{language === 'hindi' ? 'दोबारा चलाएं (Try Again)' : 'Try Again'}</span>
                  </button>
                  <button
                    onClick={() => onOpen1930Modal({
                      scamCategory: activeVariation.label || scenario.badge,
                      suspectNumber: scenario.callerNumber,
                      categoryName: `${scenario.name} - ${activeVariation.label}`,
                      text: dialogueHistory.map(d => `${d.speaker}: ${d.text}`).join('\n')
                    })}
                    className="w-full py-2.5 bg-rose-600 hover:bg-rose-500 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-2 cursor-pointer shadow-md"
                  >
                    <FileText className="w-3.5 h-3.5" />
                    <span>{language === 'hindi' ? '1930 पोर्टल पर शिकायत करें' : 'Report to 1930 Portal'}</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right: AI Copilot Alerts & Live Dialogue */}
        <div className="lg:col-span-7 space-y-4">
          {/* AI Copilot Alert Banner */}
          {copilotStatus ? (
            <div className={`p-4 rounded-xl border ${
              copilotStatus.threatLevel === 'CRITICAL'
                ? 'bg-rose-950/30 border-rose-800/60 text-rose-200'
                : 'bg-amber-950/30 border-amber-800/60 text-amber-200'
            }`}>
              <div className="flex items-start gap-3">
                <ShieldAlert className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-rose-400">
                      {language === 'hindi' ? 'रक्षक एआई लाइव कोपायलट' : 'Rakshak AI Live Copilot'}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-rose-900/60 text-rose-200 font-bold">
                      {copilotStatus.threatLevel} {language === 'hindi' ? 'खतरा' : 'RISK'}
                    </span>
                  </div>
                  <p className="text-sm font-semibold text-white mt-1">
                    {copilotStatus.alert}
                  </p>

                  {/* Tactics */}
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {copilotStatus.tactics.map((tac, i) => (
                      <span
                        key={i}
                        className="text-[11px] px-2 py-0.5 rounded bg-slate-900/80 border border-slate-700 text-slate-300 font-medium"
                      >
                        ⚠️ {tac}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Counter Reply Buttons */}
              {callState === 'connected' && (
                <div className="mt-4 pt-3 border-t border-slate-800">
                  <p className="text-xs font-semibold text-cyan-400 mb-2">
                    {language === 'hindi' ? 'स्कैमर को जवाब देने के लिए कोई विकल्प चुनें:' : 'Tap a response to reply to the scammer:'}
                  </p>
                  <div className="space-y-2">
                    {copilotStatus.replies.map((reply, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleUserReply(reply)}
                        className="w-full p-2.5 rounded-lg bg-slate-900/80 hover:bg-slate-800 border border-slate-700 text-left text-xs text-slate-200 hover:text-white transition-colors flex items-center justify-between cursor-pointer"
                      >
                        <span>"{reply}"</span>
                        <ArrowRight className="w-3.5 h-3.5 text-cyan-400 ml-2 flex-shrink-0" />
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="p-6 rounded-xl bg-[#111827] border border-slate-800 text-center">
              <ShieldAlert className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                {language === 'hindi' ? 'एआई कोपायलट तैयार है' : 'AI Copilot Ready'}
              </h4>
              <p className="text-xs text-slate-500 mt-1">
                {language === 'hindi'
                  ? 'ऊपर से कोई भी तरीका चुनें और "नकली कॉल शुरू करें" पर क्लिक करें। कॉल उठाने पर एआई लाइव बातचीत सुनकर खतरे को पकड़ेगा।'
                  : 'Select an asking angle above and click "Start Incoming Call". When answered, the AI Copilot will listen and detect fraud tactics.'}
              </p>
            </div>
          )}

          {/* Dialogue Transcript */}
          <div className="bg-[#111827] border border-slate-800 rounded-xl p-4 sm:p-5">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                {language === 'hindi' ? 'लाइव कॉल बातचीत विवरण' : 'Call Audio Transcript'}
              </h4>
              {isScammerSpeaking && (
                <span className="text-xs text-rose-400 flex items-center gap-1.5 font-medium animate-pulse">
                  <Volume2 className="w-3.5 h-3.5" />
                  {language === 'hindi' ? 'स्कैमर बोल रहा है...' : 'Scammer Speaking...'}
                </span>
              )}
            </div>

            <div className="space-y-2.5 max-h-[300px] overflow-y-auto pr-1">
              {dialogueHistory.length === 0 ? (
                <p className="text-center text-xs text-slate-600 py-8">
                  {language === 'hindi' ? 'कॉल उठाने पर यहाँ बातचीत दिखाई देगी।' : 'Call transcript will appear here when answered.'}
                </p>
              ) : (
                dialogueHistory.map((d, index) => {
                  const isScammer = d.speaker === 'scammer';
                  const displayText = isScammer
                    ? (language === 'hindi' && d.hindi ? d.hindi : language === 'english' && d.english ? d.english : d.text)
                    : d.text;

                  return (
                    <div
                      key={index}
                      className={`p-3 rounded-xl text-xs sm:text-sm leading-relaxed ${
                        isScammer
                          ? 'bg-rose-950/20 border border-rose-900/30 text-rose-100'
                          : 'bg-cyan-950/20 border border-cyan-900/30 text-cyan-100 ml-4'
                      }`}
                    >
                      <span className="text-[10px] font-bold uppercase tracking-wider block mb-0.5 text-slate-400">
                        {isScammer 
                          ? (language === 'hindi' ? '🚨 स्कैमर (अपराधी)' : '🚨 Scammer') 
                          : (language === 'hindi' ? '🛡️ आप (नागरिक)' : '🛡️ You')}
                      </span>
                      <p className="text-slate-200">"{displayText}"</p>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
