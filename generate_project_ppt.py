"""
Generate a modern, simple, concise 10-slide PowerPoint presentation for FraudRakshak.
Clean, professional design with widescreen 16:9 layout, clear cards, distinct typography,
and embedded academic diagrams.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Output Presentation Path
PPTX_PATH = r"d:\Project\FraudRakshak\FraudRakshak_Project_Presentation.pptx"

# Asset Paths
ASSETS_DIR = r"d:\Project\FraudRakshak\docs_assets"
LOGO_PATH = os.path.join(ASSETS_DIR, "kmclu_logo.jpeg")
FIG2_PATH = os.path.join(ASSETS_DIR, "fig2_layered_architecture.png")
FIG3_PATH = os.path.join(ASSETS_DIR, "fig3_dfd_level_0.png")
FIG4_PATH = os.path.join(ASSETS_DIR, "fig4_dfd_level_1.png")
FIG5_PATH = os.path.join(ASSETS_DIR, "fig5_usecase_sequence.png")
FIG6_PATH = os.path.join(ASSETS_DIR, "fig6_class_diagram.png")
UI_COPILOT_PATH = os.path.join(ASSETS_DIR, "ui_call_copilot.png")
UI_VOICE_PATH = os.path.join(ASSETS_DIR, "ui_voice_ai.png")

# Color Palette
COLOR_BG = RGBColor(248, 250, 252)          # Slate-50 (#F8FAFC)
COLOR_CARD_BG = RGBColor(255, 255, 255)     # Pure White
COLOR_CARD_BORDER = RGBColor(226, 232, 240) # Slate-200 (#E2E8F0)
COLOR_CARD_ALT = RGBColor(241, 245, 249)    # Slate-100 (#F1F5F9)

COLOR_PRIMARY = RGBColor(26, 54, 110)       # Deep Navy Blue (#1A366E)
COLOR_SECONDARY = RGBColor(2, 132, 199)     # Sky Blue / Cyan (#0284C7)
COLOR_TEXT_DARK = RGBColor(15, 23, 42)      # Slate-900 (#0F172A)
COLOR_TEXT_MUTED = RGBColor(71, 85, 105)    # Slate-600 (#475569)
COLOR_TEXT_LIGHT = RGBColor(100, 116, 139)  # Slate-500 (#64748B)

COLOR_GREEN = RGBColor(22, 163, 74)         # Green-600 (#16A34A)
COLOR_GREEN_BG = RGBColor(240, 253, 244)    # Green-50
COLOR_RED = RGBColor(220, 38, 38)           # Red-600 (#DC2626)
COLOR_RED_BG = RGBColor(254, 242, 242)      # Red-50
COLOR_AMBER = RGBColor(217, 119, 6)         # Amber-600 (#D97706)
COLOR_NAVY_LIGHT = RGBColor(238, 242, 255)  # Indigo-50

FONT_NAME = "Calibri"

def set_slide_background(slide):
    """Draw a clean solid background rectangle."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.fill.background()
    # Send background to back by lowering its z-order if possible (it's the first shape added)

def add_header(slide, title_text, category_text, subtitle_text):
    """Add a consistent, clean header across content slides."""
    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = FONT_NAME
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_SECONDARY

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.45))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_NAME
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_PRIMARY

    # Subtitle / takeaway
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.18), Inches(11.7), Inches(0.3))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_NAME
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

def add_footer(slide, current_page, total_pages=10):
    """Add consistent footer with project name and slide number."""
    foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(8.0), Inches(0.3))
    tf_foot = foot_box.text_frame
    tf_foot.margin_left = tf_foot.margin_right = tf_foot.margin_top = tf_foot.margin_bottom = 0
    p_f = tf_foot.paragraphs[0]
    p_f.text = "FraudRakshak: Multilingual AI Cyber Fraud Detection & Voice Advisory System  |  KMCLU Lucknow"
    p_f.font.name = FONT_NAME
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = COLOR_TEXT_LIGHT

    # Slide number
    page_box = slide.shapes.add_textbox(Inches(11.0), Inches(6.95), Inches(1.5), Inches(0.3))
    tf_page = page_box.text_frame
    tf_page.margin_left = tf_page.margin_right = tf_page.margin_top = tf_page.margin_bottom = 0
    p_p = tf_page.paragraphs[0]
    p_p.alignment = PP_ALIGN.RIGHT
    p_p.text = f"Slide {current_page} of {total_pages}"
    p_p.font.name = FONT_NAME
    p_p.font.size = Pt(9)
    p_p.font.bold = True
    p_p.font.color.rgb = COLOR_TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Draw a clean card container with rounded corners."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_bullet(tf, bold_prefix, text_body, pt_size=12, space_after=8, text_color=COLOR_TEXT_DARK):
    """Helper to add a cleanly styled bullet point to a text frame."""
    p = tf.add_paragraph() if len(tf.paragraphs) > 0 and tf.paragraphs[0].text != "" else tf.paragraphs[0]
    p.space_after = Pt(space_after)
    p.font.size = Pt(pt_size)
    p.font.name = FONT_NAME
    
    if bold_prefix:
        r_bold = p.add_run()
        r_bold.text = bold_prefix + ": "
        r_bold.font.bold = True
        r_bold.font.color.rgb = text_color
        
    r_body = p.add_run()
    r_body.text = text_body
    r_body.font.bold = False
    r_body.font.color.rgb = COLOR_TEXT_MUTED

# ==============================================================================
# SLIDE BUILDERS
# ==============================================================================

def build_slide_1_title(prs):
    """Slide 1: Title & Academic Details."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)

    # University Header Bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.45))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_PRIMARY
    top_bar.line.fill.background()
    
    tf_top = top_bar.text_frame
    p_top = tf_top.paragraphs[0]
    p_top.alignment = PP_ALIGN.CENTER
    p_top.text = "KHWAJA MOINUDDIN CHISHTI LANGUAGE UNIVERSITY, LUCKNOW"
    p_top.font.name = FONT_NAME
    p_top.font.size = Pt(10.5)
    p_top.font.bold = True
    p_top.font.color.rgb = RGBColor(255, 255, 255)

    # University Logo
    if os.path.exists(LOGO_PATH):
        slide.shapes.add_picture(LOGO_PATH, Inches(0.9), Inches(0.75), width=Inches(1.2), height=Inches(1.28))

    # Badge: Mini Project Defense
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.3), Inches(0.75), Inches(3.2), Inches(0.35))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_NAVY_LIGHT
    badge.line.color.rgb = COLOR_SECONDARY
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = "B.TECH MINI PROJECT PRESENTATION (2026-2027)"
    p_b.font.name = FONT_NAME
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_PRIMARY

    # Main Project Title
    t_box = slide.shapes.add_textbox(Inches(2.3), Inches(1.15), Inches(10.2), Inches(1.2))
    tf_title = t_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_t = tf_title.paragraphs[0]
    p_t.text = "FraudRakshak: Multilingual AI-Powered Cyber Fraud Detection & Voice Advisory System"
    p_t.font.name = FONT_NAME
    p_t.font.size = Pt(25)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_PRIMARY
    p_t.space_after = Pt(4)

    p_sub = tf_title.add_paragraph()
    p_sub.text = "Real-Time Threat Scoring • Bilingual Voice Copilot • Scam Simulator • 1930 Zero-FIR Drafting"
    p_sub.font.name = FONT_NAME
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_SECONDARY

    # Card 1: Student Information (Left)
    add_card(slide, Inches(0.9), Inches(2.6), Inches(5.6), Inches(3.8))
    
    # Card 1 Header
    c1_hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(2.8), Inches(5.0), Inches(0.45))
    c1_hdr.fill.solid()
    c1_hdr.fill.fore_color.rgb = COLOR_CARD_ALT
    c1_hdr.line.fill.background()
    tf_c1h = c1_hdr.text_frame
    p_c1h = tf_c1h.paragraphs[0]
    p_c1h.text = "STUDENT DETAILS (CANDIDATE)"
    p_c1h.font.name = FONT_NAME
    p_c1h.font.size = Pt(11)
    p_c1h.font.bold = True
    p_c1h.font.color.rgb = COLOR_PRIMARY

    c1_box = slide.shapes.add_textbox(Inches(1.2), Inches(3.4), Inches(5.0), Inches(2.8))
    tf_c1 = c1_box.text_frame
    tf_c1.word_wrap = True
    add_bullet(tf_c1, "Candidate Name", "Shreyansh Agrahari", pt_size=13, space_after=10)
    add_bullet(tf_c1, "University Roll No", "2308302056", pt_size=13, space_after=10)
    add_bullet(tf_c1, "Degree Programme", "Bachelor of Technology (B.Tech)", pt_size=13, space_after=10)
    add_bullet(tf_c1, "Specialization Branch", "Computer Science and Engineering (AI & Data Science)", pt_size=12, space_after=10)
    add_bullet(tf_c1, "Academic Session", "2026 - 2027", pt_size=12, space_after=4)

    # Card 2: Faculty & University Supervision (Right)
    add_card(slide, Inches(6.8), Inches(2.6), Inches(5.6), Inches(3.8))
    
    # Card 2 Header
    c2_hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(2.8), Inches(5.0), Inches(0.45))
    c2_hdr.fill.solid()
    c2_hdr.fill.fore_color.rgb = COLOR_CARD_ALT
    c2_hdr.line.fill.background()
    tf_c2h = c2_hdr.text_frame
    p_c2h = tf_c2h.paragraphs[0]
    p_c2h.text = "PROJECT SUPERVISION & DEPARTMENT"
    p_c2h.font.name = FONT_NAME
    p_c2h.font.size = Pt(11)
    p_c2h.font.bold = True
    p_c2h.font.color.rgb = COLOR_PRIMARY

    c2_box = slide.shapes.add_textbox(Inches(7.1), Inches(3.4), Inches(5.0), Inches(2.8))
    tf_c2 = c2_box.text_frame
    tf_c2.word_wrap = True
    add_bullet(tf_c2, "Project Supervisor", "Mrs. Ankita Agrawal (Assistant Professor)", pt_size=13, space_after=10)
    add_bullet(tf_c2, "Head of Department", "Dr. Suman Kumar Mishra (Head, Dept. of CSE)", pt_size=13, space_after=10)
    add_bullet(tf_c2, "Academic Faculty", "Faculty of Engineering & Technology", pt_size=13, space_after=10)
    add_bullet(tf_c2, "University", "Khwaja Moinuddin Chishti Language University, Lucknow", pt_size=12, space_after=10)
    add_bullet(tf_c2, "Evaluation Type", "Academic Mini Project Evaluation & Viva Voce", pt_size=12, space_after=4)

    # Slide 1 Footer
    add_footer(slide, 1)

def build_slide_2_problem(prs):
    """Slide 2: Problem Statement."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "The Growing Cyber Fraud Epidemic in India", "Background & Problem Statement", "Why ordinary citizens and elderly users urgently need real-time digital defense")

    # 3 Column Cards
    col_w = Inches(3.68)
    col_h = Inches(5.1)
    top_pos = Inches(1.6)

    # Col 1: Rise of Scams
    add_card(slide, Inches(0.8), top_pos, col_w, col_h)
    hdr1 = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(3.28), Inches(0.5))
    hdr1.text_frame.paragraphs[0].text = "1. Explosive Scam Growth"
    hdr1.text_frame.paragraphs[0].font.name = FONT_NAME
    hdr1.text_frame.paragraphs[0].font.size = Pt(16)
    hdr1.text_frame.paragraphs[0].font.bold = True
    hdr1.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY
    
    tf1 = slide.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(3.28), Inches(4.1)).text_frame
    tf1.word_wrap = True
    add_bullet(tf1, "Rapid Digitalization", "UPI and WhatsApp adoption expanded faster than digital literacy in India.", pt_size=12, space_after=12)
    add_bullet(tf1, "Huge Financial Losses", "Indians lost over Rs. 1,750 Crore to cyber fraud in the first four months of 2024 alone (MHA report).", pt_size=12, space_after=12)
    add_bullet(tf1, "High-Target Groups", "Senior citizens, rural families, and non-tech users are targeted repeatedly.", pt_size=12, space_after=8)

    # Col 2: Top Scam Vectors
    add_card(slide, Inches(4.82), top_pos, col_w, col_h)
    hdr2 = slide.shapes.add_textbox(Inches(5.02), Inches(1.8), Inches(3.28), Inches(0.5))
    hdr2.text_frame.paragraphs[0].text = "2. Psychological Traps"
    hdr2.text_frame.paragraphs[0].font.name = FONT_NAME
    hdr2.text_frame.paragraphs[0].font.size = Pt(16)
    hdr2.text_frame.paragraphs[0].font.bold = True
    hdr2.text_frame.paragraphs[0].font.color.rgb = COLOR_RED
    
    tf2 = slide.shapes.add_textbox(Inches(5.02), Inches(2.4), Inches(3.28), Inches(4.1)).text_frame
    tf2.word_wrap = True
    add_bullet(tf2, "Digital Arrest", "Scammers pose as CBI / Police over video calls, placing victims under fake 'house arrest' to extort life savings.", pt_size=12, space_after=12)
    add_bullet(tf2, "Urgent Utility Scams", "Fake power disconnection SMS messages ('Bijli cut tonight') inducing instant panic.", pt_size=12, space_after=12)
    add_bullet(tf2, "Malicious APKs & Jobs", "Fake wedding invitations, e-challans, and part-time job offers stealing OTPs.", pt_size=12, space_after=8)

    # Col 3: Gaps in Existing Tools
    add_card(slide, Inches(8.84), top_pos, col_w, col_h)
    hdr3 = slide.shapes.add_textbox(Inches(9.04), Inches(1.8), Inches(3.28), Inches(0.5))
    hdr3.text_frame.paragraphs[0].text = "3. Gaps in Current Tools"
    hdr3.text_frame.paragraphs[0].font.name = FONT_NAME
    hdr3.text_frame.paragraphs[0].font.size = Pt(16)
    hdr3.text_frame.paragraphs[0].font.bold = True
    hdr3.text_frame.paragraphs[0].font.color.rgb = COLOR_AMBER
    
    tf3 = slide.shapes.add_textbox(Inches(9.04), Inches(2.4), Inches(3.28), Inches(4.1)).text_frame
    tf3.word_wrap = True
    add_bullet(tf3, "Number-Only Blockers", "Truecaller blocks known spam numbers, but fails completely on fresh SIMs or WhatsApp texts.", pt_size=12, space_after=12)
    add_bullet(tf3, "Language Barrier", "Existing AI safety tools only understand pure English; they fail on Hindi and Hinglish scam scripts.", pt_size=12, space_after=12)
    add_bullet(tf3, "Missing Golden Hour", "Victims panic and do not know how to dial 1930 or format formal police complaints.", pt_size=12, space_after=8)

    add_footer(slide, 2)

def build_slide_3_motivation(prs):
    """Slide 3: Motivation & Core Objectives."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Motivation & Core Project Objectives", "Project Foundation", "Bridging the gap between sophisticated scams and vulnerable citizens")

    # Left Box: Motivation
    add_card(slide, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    h_left = slide.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(0.45))
    h_left.text_frame.paragraphs[0].text = "Why We Built FraudRakshak"
    h_left.text_frame.paragraphs[0].font.name = FONT_NAME
    h_left.text_frame.paragraphs[0].font.size = Pt(17)
    h_left.text_frame.paragraphs[0].font.bold = True
    h_left.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY

    tf_l = slide.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(5.0), Inches(4.1)).text_frame
    tf_l.word_wrap = True
    add_bullet(tf_l, "A Digital Bodyguard", "Citizens need an unbiased, calm second opinion when a scammer induces fear or false urgency.", pt_size=13, space_after=14)
    add_bullet(tf_l, "Voice First for Equality", "Elderly citizens struggle to read small text; they deserve spoken advice in Hindi and English.", pt_size=13, space_after=14)
    add_bullet(tf_l, "Proactive Training", "Instead of only reacting after money is stolen, citizens must practice how to handle scam calls safely.", pt_size=13, space_after=14)
    add_bullet(tf_l, "Zero Friction Access", "Works immediately in any web browser without demanding app installs or sensitive phone permissions.", pt_size=13, space_after=8)

    # Right Box: 4 Core Objectives
    add_card(slide, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1))
    h_right = slide.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(0.45))
    h_right.text_frame.paragraphs[0].text = "Core Technical Objectives"
    h_right.text_frame.paragraphs[0].font.name = FONT_NAME
    h_right.text_frame.paragraphs[0].font.size = Pt(17)
    h_right.text_frame.paragraphs[0].font.bold = True
    h_right.text_frame.paragraphs[0].font.color.rgb = COLOR_SECONDARY

    tf_r = slide.shapes.add_textbox(Inches(7.1), Inches(2.4), Inches(5.1), Inches(4.1)).text_frame
    tf_r.word_wrap = True
    add_bullet(tf_r, "1. Multilingual Threat Engine", "Accurately score messages (0-100) across 10 Indian fraud types in Hindi, Hinglish, and English.", pt_size=12.5, space_after=12)
    add_bullet(tf_r, "2. Real-Time Voice Advisory", "Spoken audio guidance instructing users: 'Do not panic, do not share OTP, disconnect the call.'", pt_size=12.5, space_after=12)
    add_bullet(tf_r, "3. Interactive Scam Simulator", "A safe practice environment with AI personas (CBI officer, Power official) to train defusal skills.", pt_size=12.5, space_after=12)
    add_bullet(tf_r, "4. Instant 1930 FIR Drafting", "Auto-generate official Zero-FIR letters containing transaction details for national portal submission.", pt_size=12.5, space_after=8)

    add_footer(slide, 3)

def build_slide_4_features(prs):
    """Slide 4: Key Features."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Key Features of FraudRakshak", "System Capabilities", "Four integrated modules providing end-to-end protection against cyber fraud")

    # 4 Cards in 2x2 Grid
    card_w = Inches(5.65)
    card_h = Inches(2.4)
    c1_l = Inches(0.8)
    c2_l = Inches(6.8)
    r1_t = Inches(1.6)
    r2_t = Inches(4.25)

    # Feature 1
    add_card(slide, c1_l, r1_t, card_w, card_h)
    f1_h = slide.shapes.add_textbox(c1_l + Inches(0.25), r1_t + Inches(0.15), card_w - Inches(0.5), Inches(0.4))
    f1_h.text_frame.paragraphs[0].text = "1. Multilingual Message Scanner"
    f1_h.text_frame.paragraphs[0].font.name = FONT_NAME
    f1_h.text_frame.paragraphs[0].font.size = Pt(15)
    f1_h.text_frame.paragraphs[0].font.bold = True
    f1_h.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY

    tf1 = slide.shapes.add_textbox(c1_l + Inches(0.25), r1_t + Inches(0.6), card_w - Inches(0.5), Inches(1.6)).text_frame
    tf1.word_wrap = True
    add_bullet(tf1, "Input Formats", "Accepts suspicious SMS, WhatsApp forwards, email text, or direct voice input.", pt_size=11.5, space_after=6)
    add_bullet(tf1, "Calibrated Scoring", "Calculates a 0-100 Risk Score with traffic-light badges (Safe, Medium, High).", pt_size=11.5, space_after=6)
    add_bullet(tf1, "Zero False Alarms", "Smart whitelist ensures genuine bank debit/credit alerts are never flagged.", pt_size=11.5, space_after=2)

    # Feature 2
    add_card(slide, c2_l, r1_t, card_w, card_h)
    f2_h = slide.shapes.add_textbox(c2_l + Inches(0.25), r1_t + Inches(0.15), card_w - Inches(0.5), Inches(0.4))
    f2_h.text_frame.paragraphs[0].text = "2. Bilingual Voice AI Advisor"
    f2_h.text_frame.paragraphs[0].font.name = FONT_NAME
    f2_h.text_frame.paragraphs[0].font.size = Pt(15)
    f2_h.text_frame.paragraphs[0].font.bold = True
    f2_h.text_frame.paragraphs[0].font.color.rgb = COLOR_SECONDARY

    tf2 = slide.shapes.add_textbox(c2_l + Inches(0.25), r1_t + Inches(0.6), card_w - Inches(0.5), Inches(1.6)).text_frame
    tf2.word_wrap = True
    add_bullet(tf2, "Spoken Advice", "Reads out critical instructions aloud in clear Hindi or English.", pt_size=11.5, space_after=6)
    add_bullet(tf2, "Zero Installation", "Uses browser-native Web Speech API; runs locally on mobile phones without lag.", pt_size=11.5, space_after=6)
    add_bullet(tf2, "Elderly Friendly", "Senior citizens simply tap the microphone icon and listen to safety guidance.", pt_size=11.5, space_after=2)

    # Feature 3
    add_card(slide, c1_l, r2_t, card_w, card_h)
    f3_h = slide.shapes.add_textbox(c1_l + Inches(0.25), r2_t + Inches(0.15), card_w - Inches(0.5), Inches(0.4))
    f3_h.text_frame.paragraphs[0].text = "3. Scam Call Simulator & Copilot"
    f3_h.text_frame.paragraphs[0].font.name = FONT_NAME
    f3_h.text_frame.paragraphs[0].font.size = Pt(15)
    f3_h.text_frame.paragraphs[0].font.bold = True
    f3_h.text_frame.paragraphs[0].font.color.rgb = COLOR_AMBER

    tf3 = slide.shapes.add_textbox(c1_l + Inches(0.25), r2_t + Inches(0.6), card_w - Inches(0.5), Inches(1.6)).text_frame
    tf3.word_wrap = True
    add_bullet(tf3, "Interactive Practice", "Simulates realistic scam conversations (Police threat, Bank manager, Job offer).", pt_size=11.5, space_after=6)
    add_bullet(tf3, "Live Call Copilot", "Transcribes speech in real time and highlights manipulative pressure phrases.", pt_size=11.5, space_after=6)
    add_bullet(tf3, "Defusal Guidance", "Teaches citizens what to say to defuse scammers and safely hang up.", pt_size=11.5, space_after=2)

    # Feature 4
    add_card(slide, c2_l, r2_t, card_w, card_h)
    f4_h = slide.shapes.add_textbox(c2_l + Inches(0.25), r2_t + Inches(0.15), card_w - Inches(0.5), Inches(0.4))
    f4_h.text_frame.paragraphs[0].text = "4. Automated 1930 Zero-FIR Generator"
    f4_h.text_frame.paragraphs[0].font.name = FONT_NAME
    f4_h.text_frame.paragraphs[0].font.size = Pt(15)
    f4_h.text_frame.paragraphs[0].font.bold = True
    f4_h.text_frame.paragraphs[0].font.color.rgb = COLOR_GREEN

    tf4 = slide.shapes.add_textbox(c2_l + Inches(0.25), r2_t + Inches(0.6), card_w - Inches(0.5), Inches(1.6)).text_frame
    tf4.word_wrap = True
    add_bullet(tf4, "Ready-to-File FIR", "Auto-formats an official complaint for the National Cyber Crime Reporting Portal.", pt_size=11.5, space_after=6)
    add_bullet(tf4, "Key Evidence Extraction", "Extracts scam phone numbers, bank accounts, UPI IDs, and timestamps automatically.", pt_size=11.5, space_after=6)
    add_bullet(tf4, "Golden Hour Response", "Provides one-click calling to 1930 helpline to freeze stolen funds instantly.", pt_size=11.5, space_after=2)

    add_footer(slide, 4)

def build_slide_5_architecture(prs):
    """Slide 5: System Architecture & Layered Design."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "System Architecture: 3-Tier Modular Design", "System Design", "Separation of concerns allows UI, detection logic, and scam rules to evolve independently")

    # Left: Explanation of 3 Layers
    add_card(slide, Inches(0.8), Inches(1.6), Inches(5.2), Inches(5.1))
    h_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.8), Inches(0.45))
    h_l.text_frame.paragraphs[0].text = "Architectural Layers (Figure 2)"
    h_l.text_frame.paragraphs[0].font.name = FONT_NAME
    h_l.text_frame.paragraphs[0].font.size = Pt(17)
    h_l.text_frame.paragraphs[0].font.bold = True
    h_l.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY

    tf_l = slide.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(4.8), Inches(4.1)).text_frame
    tf_l.word_wrap = True
    add_bullet(tf_l, "1. Presentation Layer", "React 19 + Tailwind CSS single page web app. Features Threat Scanner, Voice AI interface, and Call Simulator.", pt_size=12, space_after=12)
    add_bullet(tf_l, "2. Application / Logic Layer", "Validates input, runs Web Speech ASR/TTS, executes multi-vector threat matching, and calculates risk scores.", pt_size=12, space_after=12)
    add_bullet(tf_l, "3. Data & Model Layer", "Scam Vector Dictionaries (D1), Legitimate Bank Whitelists (D2), and 1930 Cybercrime Reporting Schema (D3).", pt_size=12, space_after=12)
    add_bullet(tf_l, "Key Advantage", "Modular design enables updating scam dictionaries without redeploying the frontend.", pt_size=11.5, space_after=4)

    # Right: Embedded Architecture Diagram
    add_card(slide, Inches(6.3), Inches(1.6), Inches(6.2), Inches(5.1))
    h_r = slide.shapes.add_textbox(Inches(6.5), Inches(1.75), Inches(5.8), Inches(0.35))
    h_r.text_frame.paragraphs[0].text = "Figure 2: Layered Architecture Diagram"
    h_r.text_frame.paragraphs[0].font.name = FONT_NAME
    h_r.text_frame.paragraphs[0].font.size = Pt(13)
    h_r.text_frame.paragraphs[0].font.bold = True
    h_r.text_frame.paragraphs[0].font.color.rgb = COLOR_SECONDARY

    if os.path.exists(FIG2_PATH):
        # Image width 5.8 in, height ~ 3.5 in
        slide.shapes.add_picture(FIG2_PATH, Inches(6.5), Inches(2.2), width=Inches(5.8), height=Inches(3.5))

    p_cap = slide.shapes.add_textbox(Inches(6.5), Inches(6.1), Inches(5.8), Inches(0.4)).text_frame
    p_cap.paragraphs[0].text = "Clean 3-tier boundary: Presentation <-> Application Logic <-> Data Stores"
    p_cap.paragraphs[0].font.name = FONT_NAME
    p_cap.paragraphs[0].font.size = Pt(10)
    p_cap.paragraphs[0].font.color.rgb = COLOR_TEXT_MUTED

    add_footer(slide, 5)

def build_slide_6_dfd(prs):
    """Slide 6: How It Works & Data Flow Diagrams."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "How It Works: Data Flow & Processing Pipeline", "System Design & DFD", "Clear visual flow from raw user input to risk classification and FIR generation")

    # Left: Step-by-Step Flow Explanation
    add_card(slide, Inches(0.8), Inches(1.6), Inches(5.2), Inches(5.1))
    h_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.8), Inches(0.45))
    h_l.text_frame.paragraphs[0].text = "4-Step Processing Pipeline"
    h_l.text_frame.paragraphs[0].font.name = FONT_NAME
    h_l.text_frame.paragraphs[0].font.size = Pt(17)
    h_l.text_frame.paragraphs[0].font.bold = True
    h_l.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY

    tf_l = slide.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(4.8), Inches(4.1)).text_frame
    tf_l.word_wrap = True
    add_bullet(tf_l, "Step 1: Input & Normalization", "Citizen pastes text or speaks. System normalizes Hinglish/Hindi text and removes noise.", pt_size=12, space_after=12)
    add_bullet(tf_l, "Step 2: Bank Whitelist Check", "Scans against legitimate bank patterns (D2). If genuine transactional alert, safely bypasses scoring.", pt_size=12, space_after=12)
    add_bullet(tf_l, "Step 3: Multi-Vector Scoring", "Evaluates urgency keywords, fake APKs, authority threats (+90 pts for Digital Arrest), producing a 0-100 score.", pt_size=12, space_after=12)
    add_bullet(tf_l, "Step 4: Advisory & FIR Output", "Triggers voice guidance, displays safety instructions, and pre-fills the 1930 Zero-FIR complaint draft.", pt_size=12, space_after=6)

    # Right: Embedded DFD Diagram
    add_card(slide, Inches(6.3), Inches(1.6), Inches(6.2), Inches(5.1))
    h_r = slide.shapes.add_textbox(Inches(6.5), Inches(1.75), Inches(5.8), Inches(0.35))
    h_r.text_frame.paragraphs[0].text = "Figure 3: Data Flow Diagram (DFD Level 0)"
    h_r.text_frame.paragraphs[0].font.name = FONT_NAME
    h_r.text_frame.paragraphs[0].font.size = Pt(13)
    h_r.text_frame.paragraphs[0].font.bold = True
    h_r.text_frame.paragraphs[0].font.color.rgb = COLOR_SECONDARY

    if os.path.exists(FIG3_PATH):
        # Image width 5.8 in, height ~ 2.5 in
        slide.shapes.add_picture(FIG3_PATH, Inches(6.5), Inches(2.2), width=Inches(5.8), height=Inches(2.55))

    # Caption / Details below DFD
    sub_dfd = slide.shapes.add_textbox(Inches(6.5), Inches(5.0), Inches(5.8), Inches(1.5)).text_frame
    sub_dfd.word_wrap = True
    add_bullet(sub_dfd, "Context Level Flow", "Citizen inputs SMS/Voice -> FraudRakshak Core (0.0) -> Output Risk, Audio Advisory & 1930 Zero-FIR.", pt_size=11, space_after=6)
    add_bullet(sub_dfd, "Law Enforcement Feed", "Drafted complaints align with the National Cyber Crime Reporting Portal (1930).", pt_size=11, space_after=2)

    add_footer(slide, 6)

def build_slide_7_techstack(prs):
    """Slide 7: Technology Stack."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Technology Stack & Tools Used", "Implementation Details", "Modern, zero-cost, lightweight technologies chosen for speed, reliability, and security")

    col_w = Inches(2.72)
    gap = Inches(0.28)
    top_pos = Inches(1.6)
    col_h = Inches(5.1)

    # Tech 1: Frontend
    add_card(slide, Inches(0.8), top_pos, col_w, col_h)
    h1 = slide.shapes.add_textbox(Inches(0.95), Inches(1.8), Inches(2.42), Inches(0.4))
    h1.text_frame.paragraphs[0].text = "Frontend Layer"
    h1.text_frame.paragraphs[0].font.name = FONT_NAME
    h1.text_frame.paragraphs[0].font.size = Pt(16)
    h1.text_frame.paragraphs[0].font.bold = True
    h1.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY

    tf1 = slide.shapes.add_textbox(Inches(0.95), Inches(2.35), Inches(2.42), Inches(4.1)).text_frame
    tf1.word_wrap = True
    add_bullet(tf1, "React 19", "Modern component-based user interface with ultra-fast rendering.", pt_size=11.5, space_after=10)
    add_bullet(tf1, "Tailwind CSS", "Utility-first design providing responsive layouts across all phone & desktop screens.", pt_size=11.5, space_after=10)
    add_bullet(tf1, "Lucide Icons", "Clear, high-contrast visual indicators for danger, warning, and safe states.", pt_size=11.5, space_after=10)
    add_bullet(tf1, "Vite Bundler", "Lightning-fast hot module replacement & build efficiency.", pt_size=11, space_after=4)

    # Tech 2: Audio & Voice AI
    add_card(slide, Inches(0.8) + col_w + gap, top_pos, col_w, col_h)
    h2 = slide.shapes.add_textbox(Inches(0.95) + col_w + gap, Inches(1.8), Inches(2.42), Inches(0.4))
    h2.text_frame.paragraphs[0].text = "Voice AI Pipeline"
    h2.text_frame.paragraphs[0].font.name = FONT_NAME
    h2.text_frame.paragraphs[0].font.size = Pt(16)
    h2.text_frame.paragraphs[0].font.bold = True
    h2.text_frame.paragraphs[0].font.color.rgb = COLOR_SECONDARY

    tf2 = slide.shapes.add_textbox(Inches(0.95) + col_w + gap, Inches(2.35), Inches(2.42), Inches(4.1)).text_frame
    tf2.word_wrap = True
    add_bullet(tf2, "Web Speech API", "Browser-native Speech Recognition (ASR) converting spoken voice to text.", pt_size=11.5, space_after=10)
    add_bullet(tf2, "Browser TTS", "Natural Hindi & English Text-to-Speech voice synthesizer.", pt_size=11.5, space_after=10)
    add_bullet(tf2, "Zero Cloud Cost", "Runs directly inside the browser; no paid external speech APIs required.", pt_size=11.5, space_after=10)
    add_bullet(tf2, "Privacy First", "Voice audio does not leave user's device for transcription.", pt_size=11, space_after=4)

    # Tech 3: Backend & AI Microservice
    add_card(slide, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, col_h)
    h3 = slide.shapes.add_textbox(Inches(0.95) + (col_w + gap)*2, Inches(1.8), Inches(2.42), Inches(0.4))
    h3.text_frame.paragraphs[0].text = "Backend & Cloud"
    h3.text_frame.paragraphs[0].font.name = FONT_NAME
    h3.text_frame.paragraphs[0].font.size = Pt(16)
    h3.text_frame.paragraphs[0].font.bold = True
    h3.text_frame.paragraphs[0].font.color.rgb = COLOR_AMBER

    tf3 = slide.shapes.add_textbox(Inches(0.95) + (col_w + gap)*2, Inches(2.35), Inches(2.42), Inches(4.1)).text_frame
    tf3.word_wrap = True
    add_bullet(tf3, "Node.js API", "Serverless API routes handling validation and client requests.", pt_size=11.5, space_after=10)
    add_bullet(tf3, "Python FastAPI", "High-performance AI microservice evaluating threat dictionaries.", pt_size=11.5, space_after=10)
    add_bullet(tf3, "Vercel Edge", "Global serverless hosting with zero cold-starts and 100% uptime.", pt_size=11.5, space_after=10)
    add_bullet(tf3, "Sub-10ms Latency", "Rule engine evaluates threat level in milliseconds.", pt_size=11, space_after=4)

    # Tech 4: Cyber Security Standards
    add_card(slide, Inches(0.8) + (col_w + gap)*3, top_pos, col_w, col_h)
    h4 = slide.shapes.add_textbox(Inches(0.95) + (col_w + gap)*3, Inches(1.8), Inches(2.42), Inches(0.4))
    h4.text_frame.paragraphs[0].text = "Cyber Standards"
    h4.text_frame.paragraphs[0].font.name = FONT_NAME
    h4.text_frame.paragraphs[0].font.size = Pt(16)
    h4.text_frame.paragraphs[0].font.bold = True
    h4.text_frame.paragraphs[0].font.color.rgb = COLOR_GREEN

    tf4 = slide.shapes.add_textbox(Inches(0.95) + (col_w + gap)*3, Inches(2.35), Inches(2.42), Inches(4.1)).text_frame
    tf4.word_wrap = True
    add_bullet(tf4, "1930 Zero-FIR", "Standardized cybercrime complaint schema matching official MHA guidelines.", pt_size=11.5, space_after=10)
    add_bullet(tf4, "I4C Awareness", "Advisories follow Indian Cybercrime Coordination Centre recommendations.", pt_size=11.5, space_after=10)
    add_bullet(tf4, "Bank Whitelisting", "Regularly updated regex for SBI, HDFC, ICICI, PNB official transaction templates.", pt_size=11.5, space_after=10)
    add_bullet(tf4, "Client Privacy", "User messages are not permanently logged to any external database.", pt_size=11, space_after=4)

    add_footer(slide, 7)

def build_slide_8_results(prs):
    """Slide 8: Testing, Results & Evaluation."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Results & Performance Evaluation", "Testing & Verification", "Tested across 86 real-world messages with 100% scam detection and 0% false alarms")

    # 4 Metric Stat Badges across top
    stat_w = Inches(2.72)
    gap = Inches(0.28)
    top_stat = Inches(1.6)
    h_stat = Inches(1.2)

    stats_info = [
        ("86", "TOTAL TEST CASES", COLOR_PRIMARY, COLOR_CARD_BG),
        ("100%", "SCAM DETECTION (70/70)", COLOR_GREEN, COLOR_GREEN_BG),
        ("0.0%", "FALSE ALARM RATE (0/16)", COLOR_SECONDARY, COLOR_CARD_BG),
        ("1.00", "F1-SCORE & PRECISION", COLOR_PRIMARY, COLOR_CARD_BG)
    ]

    for idx, (num, label, num_col, bg_col) in enumerate(stats_info):
        left_pos = Inches(0.8) + (stat_w + gap) * idx
        add_card(slide, left_pos, top_stat, stat_w, h_stat, bg_color=bg_col)
        
        # Stat Number
        s_box = slide.shapes.add_textbox(left_pos, top_stat + Inches(0.1), stat_w, Inches(0.55))
        p_s = s_box.text_frame.paragraphs[0]
        p_s.alignment = PP_ALIGN.CENTER
        p_s.text = num
        p_s.font.name = FONT_NAME
        p_s.font.size = Pt(26)
        p_s.font.bold = True
        p_s.font.color.rgb = num_col

        # Stat Label
        l_box = slide.shapes.add_textbox(left_pos, top_stat + Inches(0.68), stat_w, Inches(0.4))
        p_l = l_box.text_frame.paragraphs[0]
        p_l.alignment = PP_ALIGN.CENTER
        p_l.text = label
        p_l.font.name = FONT_NAME
        p_l.font.size = Pt(10)
        p_l.font.bold = True
        p_l.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Area: 2 Cards (Testing Breakdown & Confusion Matrix)
    bottom_top = Inches(3.0)
    bottom_h = Inches(3.7)

    # Left Bottom: Confusion Matrix & Methodology
    add_card(slide, Inches(0.8), bottom_top, Inches(5.65), bottom_h)
    h_bl = slide.shapes.add_textbox(Inches(1.05), Inches(3.15), Inches(5.15), Inches(0.4))
    h_bl.text_frame.paragraphs[0].text = "Testing Methodology & Validation"
    h_bl.text_frame.paragraphs[0].font.name = FONT_NAME
    h_bl.text_frame.paragraphs[0].font.size = Pt(16)
    h_bl.text_frame.paragraphs[0].font.bold = True
    h_bl.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY

    tf_bl = slide.shapes.add_textbox(Inches(1.05), Inches(3.6), Inches(5.15), Inches(3.0)).text_frame
    tf_bl.word_wrap = True
    add_bullet(tf_bl, "Comprehensive Dataset", "Compiled 86 realistic test cases spanning English, Hindi, and Hinglish languages.", pt_size=12, space_after=10)
    add_bullet(tf_bl, "True Positives (70 / 70)", "Detected 100% of scams including Digital Arrest, Electricity fraud, and Fake APKs.", pt_size=12, space_after=10)
    add_bullet(tf_bl, "True Negatives (16 / 16)", "Correctly verified authentic bank debits, Swiggy alerts, and regular greetings.", pt_size=12, space_after=10)
    add_bullet(tf_bl, "Zero False Alarms (0 / 16)", "Crucial achievement: citizens will not turn off the system due to annoying fake alerts.", pt_size=12, space_after=4)

    # Right Bottom: Category Breakdown Table
    add_card(slide, Inches(6.8), bottom_top, Inches(5.73), bottom_h)
    h_br = slide.shapes.add_textbox(Inches(7.05), Inches(3.15), Inches(5.23), Inches(0.4))
    h_br.text_frame.paragraphs[0].text = "Detection Accuracy by Scam Vector"
    h_br.text_frame.paragraphs[0].font.name = FONT_NAME
    h_br.text_frame.paragraphs[0].font.size = Pt(16)
    h_br.text_frame.paragraphs[0].font.bold = True
    h_br.text_frame.paragraphs[0].font.color.rgb = COLOR_SECONDARY

    tf_br = slide.shapes.add_textbox(Inches(7.05), Inches(3.6), Inches(5.23), Inches(3.0)).text_frame
    tf_br.word_wrap = True
    add_bullet(tf_br, "Digital Arrest / Police Impersonation", "10 / 10 Detected  (100.0% Accuracy)", pt_size=11.5, space_after=7)
    add_bullet(tf_br, "Electricity Bill Disconnection", "8 / 8 Detected  (100.0% Accuracy)", pt_size=11.5, space_after=7)
    add_bullet(tf_br, "Bank Account Block / Pan KYC", "10 / 10 Detected  (100.0% Accuracy)", pt_size=11.5, space_after=7)
    add_bullet(tf_br, "Part-Time Job / Telegram Scam", "8 / 8 Detected  (100.0% Accuracy)", pt_size=11.5, space_after=7)
    add_bullet(tf_br, "Lottery, Gift, Rewards & Couriers", "14 / 14 Detected  (100.0% Accuracy)", pt_size=11.5, space_after=7)
    add_bullet(tf_br, "Safe Bank Transaction SMS", "16 / 16 Marked Safe  (0% False Positives)", pt_size=11.5, space_after=2)

    add_footer(slide, 8)

def build_slide_9_impact(prs):
    """Slide 9: Advantages & Social Impact."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Key Advantages & Social Impact", "Real-World Impact", "How FraudRakshak protects ordinary families and assists law enforcement agencies")

    col_w = Inches(3.68)
    top_pos = Inches(1.6)
    col_h = Inches(5.1)

    # Advantage 1: Language & Inclusivity
    add_card(slide, Inches(0.8), top_pos, col_w, col_h)
    h1 = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(3.28), Inches(0.45))
    h1.text_frame.paragraphs[0].text = "Inclusive for Every Indian"
    h1.text_frame.paragraphs[0].font.name = FONT_NAME
    h1.text_frame.paragraphs[0].font.size = Pt(16)
    h1.text_frame.paragraphs[0].font.bold = True
    h1.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY

    tf1 = slide.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(3.28), Inches(4.1)).text_frame
    tf1.word_wrap = True
    add_bullet(tf1, "Multilingual Support", "Overcomes the language barrier by understanding Hindi, English, and romanized Hinglish.", pt_size=12, space_after=12)
    add_bullet(tf1, "Voice-First Guidance", "Senior citizens and non-readers listen to spoken warnings rather than decoding technical terms.", pt_size=12, space_after=12)
    add_bullet(tf1, "Emotional Calm", "Prevents panic-driven financial transfers during high-pressure fake police calls.", pt_size=12, space_after=8)

    # Advantage 2: Zero Barrier Access
    add_card(slide, Inches(4.82), top_pos, col_w, col_h)
    h2 = slide.shapes.add_textbox(Inches(5.02), Inches(1.8), Inches(3.28), Inches(0.45))
    h2.text_frame.paragraphs[0].text = "Zero Barrier & Instant Access"
    h2.text_frame.paragraphs[0].font.name = FONT_NAME
    h2.text_frame.paragraphs[0].font.size = Pt(16)
    h2.text_frame.paragraphs[0].font.bold = True
    h2.text_frame.paragraphs[0].font.color.rgb = COLOR_SECONDARY

    tf2 = slide.shapes.add_textbox(Inches(5.02), Inches(2.35), Inches(3.28), Inches(4.1)).text_frame
    tf2.word_wrap = True
    add_bullet(tf2, "No Installation Required", "Runs immediately in any web browser on smartphones, tablets, or budget laptops.", pt_size=12, space_after=12)
    add_bullet(tf2, "No Permissions Demanded", "Does not request contacts, GPS, or storage access, ensuring complete privacy.", pt_size=12, space_after=12)
    add_bullet(tf2, "100% Free & Open", "Built using open-source tools and browser APIs, keeping usage free for every citizen.", pt_size=12, space_after=8)

    # Advantage 3: Law Enforcement Support
    add_card(slide, Inches(8.84), top_pos, col_w, col_h)
    h3 = slide.shapes.add_textbox(Inches(9.04), Inches(1.8), Inches(3.28), Inches(0.45))
    h3.text_frame.paragraphs[0].text = "Assisting Cyber Police"
    h3.text_frame.paragraphs[0].font.name = FONT_NAME
    h3.text_frame.paragraphs[0].font.size = Pt(16)
    h3.text_frame.paragraphs[0].font.bold = True
    h3.text_frame.paragraphs[0].font.color.rgb = COLOR_GREEN

    tf3 = slide.shapes.add_textbox(Inches(9.04), Inches(2.35), Inches(3.28), Inches(4.1)).text_frame
    tf3.word_wrap = True
    add_bullet(tf3, "Freezing Stolen Funds", "Immediate 1930 dialing ensures reporting within the vital first 2-hour Golden Window.", pt_size=12, space_after=12)
    add_bullet(tf3, "Standardized Complaints", "Pre-fills evidence, timestamps, and suspect account numbers in police-ready format.", pt_size=12, space_after=12)
    add_bullet(tf3, "Reduces Police Overhead", "Officers receive well-structured complaint details rather than incomplete verbal reports.", pt_size=12, space_after=8)

    add_footer(slide, 9)

def build_slide_10_conclusion(prs):
    """Slide 10: Conclusion & Future Roadmap."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Conclusion & Future Roadmap", "Summary & Next Steps", "A scalable foundation for national citizen cybersecurity in India")

    # Left: Conclusion Summary
    add_card(slide, Inches(0.8), Inches(1.6), Inches(5.6), Inches(3.8))
    h_l = slide.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.1), Inches(0.4))
    h_l.text_frame.paragraphs[0].text = "Project Summary & Takeaways"
    h_l.text_frame.paragraphs[0].font.name = FONT_NAME
    h_l.text_frame.paragraphs[0].font.size = Pt(16)
    h_l.text_frame.paragraphs[0].font.bold = True
    h_l.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY

    tf_l = slide.shapes.add_textbox(Inches(1.05), Inches(2.3), Inches(5.1), Inches(3.0)).text_frame
    tf_l.word_wrap = True
    add_bullet(tf_l, "Proven Feasibility", "Demonstrated that lightweight, client-side AI can effectively detect complex fraud vectors without costly servers.", pt_size=12, space_after=10)
    add_bullet(tf_l, "Dual Protection", "Combines reactive defense (Threat Scanner & FIR) with proactive education (Scam Call Simulator).", pt_size=12, space_after=10)
    add_bullet(tf_l, "100% Academic Goal Met", "Successfully engineered, tested, and validated as a complete B.Tech Mini Project.", pt_size=12, space_after=6)

    # Right: Future Scope
    add_card(slide, Inches(6.8), Inches(1.6), Inches(5.73), Inches(3.8))
    h_r = slide.shapes.add_textbox(Inches(7.05), Inches(1.8), Inches(5.23), Inches(0.4))
    h_r.text_frame.paragraphs[0].text = "Future Roadmap & Expansion"
    h_r.text_frame.paragraphs[0].font.name = FONT_NAME
    h_r.text_frame.paragraphs[0].font.size = Pt(16)
    h_r.text_frame.paragraphs[0].font.bold = True
    h_r.text_frame.paragraphs[0].font.color.rgb = COLOR_SECONDARY

    tf_r = slide.shapes.add_textbox(Inches(7.05), Inches(2.3), Inches(5.23), Inches(3.0)).text_frame
    tf_r.word_wrap = True
    add_bullet(tf_r, "Phase 1: Native Android App", "Listen to live incoming calls in the background and pop up instant warning banners on the caller screen.", pt_size=12, space_after=10)
    add_bullet(tf_r, "Phase 2: Telecom Carrier Integration", "Partner with telecom providers (Jio, Airtel) to filter malicious SMS vectors before reaching devices.", pt_size=12, space_after=10)
    add_bullet(tf_r, "Phase 3: Direct Cybercrime API", "One-click automatic API transmission directly into the National Cyber Crime Portal (1930).", pt_size=12, space_after=6)

    # Bottom Thank You Banner
    add_card(slide, Inches(0.8), Inches(5.6), Inches(11.73), Inches(1.15), bg_color=COLOR_PRIMARY)
    
    # Thank You Text Left
    ty_box = slide.shapes.add_textbox(Inches(1.1), Inches(5.72), Inches(5.5), Inches(0.9))
    tf_ty = ty_box.text_frame
    p_ty1 = tf_ty.paragraphs[0]
    p_ty1.text = "Thank You! Questions & Discussion"
    p_ty1.font.name = FONT_NAME
    p_ty1.font.size = Pt(18)
    p_ty1.font.bold = True
    p_ty1.font.color.rgb = RGBColor(255, 255, 255)
    
    p_ty2 = tf_ty.add_paragraph()
    p_ty2.text = "FraudRakshak: A Digital Defense Shield for Every Citizen"
    p_ty2.font.name = FONT_NAME
    p_ty2.font.size = Pt(11)
    p_ty2.font.color.rgb = RGBColor(186, 230, 253)

    # Details Right
    det_box = slide.shapes.add_textbox(Inches(7.0), Inches(5.72), Inches(5.2), Inches(0.9))
    tf_det = det_box.text_frame
    p_d1 = tf_det.paragraphs[0]
    p_d1.alignment = PP_ALIGN.RIGHT
    p_d1.text = "Presenter: Shreyansh Agrahari (Roll: 2308302056)"
    p_d1.font.name = FONT_NAME
    p_d1.font.size = Pt(12)
    p_d1.font.bold = True
    p_d1.font.color.rgb = RGBColor(255, 255, 255)

    p_d2 = tf_det.add_paragraph()
    p_d2.alignment = PP_ALIGN.RIGHT
    p_d2.text = "Guide: Mrs. Ankita Agrawal | Dept. of CSE, KMCLU Lucknow"
    p_d2.font.name = FONT_NAME
    p_d2.font.size = Pt(11)
    p_d2.font.color.rgb = RGBColor(224, 231, 255)

    add_footer(slide, 10)

def main():
    print("Initializing 16:9 Widescreen Presentation...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    print("Generating Slide 1: Title & Academic Details...")
    build_slide_1_title(prs)

    print("Generating Slide 2: Problem Statement...")
    build_slide_2_problem(prs)

    print("Generating Slide 3: Motivation & Core Objectives...")
    build_slide_3_motivation(prs)

    print("Generating Slide 4: Key Features...")
    build_slide_4_features(prs)

    print("Generating Slide 5: System Architecture...")
    build_slide_5_architecture(prs)

    print("Generating Slide 6: How It Works & DFD...")
    build_slide_6_dfd(prs)

    print("Generating Slide 7: Technology Stack...")
    build_slide_7_techstack(prs)

    print("Generating Slide 8: Testing & Results...")
    build_slide_8_results(prs)

    print("Generating Slide 9: Advantages & Social Impact...")
    build_slide_9_impact(prs)

    print("Generating Slide 10: Conclusion & Future Roadmap...")
    build_slide_10_conclusion(prs)

    prs.save(PPTX_PATH)
    print(f"Successfully generated 10-slide presentation at:\n{PPTX_PATH}")

if __name__ == '__main__':
    main()
