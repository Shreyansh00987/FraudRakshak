"""
generate_system_design_diagrams.py
Generates 5 highly detailed, professional academic diagrams specifically tailored to FraudRakshak:
1. Figure 2: Layered architecture of FraudRakshak
2. Figure 3: Data flow diagram, level 0 (Context Level)
3. Figure 4: Data flow diagram, level 1 (Functional Decomposition)
4. Figure 5: (a) Use case diagram; (b) Sequence diagram
5. Figure 6: UML Class diagram

All diagrams strictly adhere to academic conventions (clean B&W / grayscale palette, 300 DPI,
standard UML / DFD notations, and clear text labels tailored 100% to FraudRakshak).
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ASSETS_DIR = r"d:\Project\FraudRakshak\docs_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

FONT_FAMILY = 'sans-serif'
EDGE_COLOR = "#1E293B"       # Slate-800
FILL_BG = "#F8FAFC"          # Slate-50
BOX_HEADER_BG = "#E2E8F0"    # Slate-200
DASH_BORDER = "#64748B"      # Slate-500

# ==============================================================================
# 1. FIGURE 2: LAYERED ARCHITECTURE OF FRAUDRAKSHAK
# ==============================================================================
def create_fig2_architecture(output_path):
    fig, ax = plt.subplots(figsize=(9.8, 6.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.6)
    ax.axis('off')

    def draw_layer_container(y_bottom, height, label):
        layer_box = patches.Rectangle((0.4, y_bottom), 9.2, height,
                                      linewidth=1.3, linestyle='--',
                                      edgecolor=DASH_BORDER, facecolor="white", zorder=1)
        ax.add_patch(layer_box)
        # Layer Header Tab
        tab = patches.Rectangle((0.4, y_bottom + height - 0.35), 3.2, 0.35,
                                linewidth=1.0, edgecolor=DASH_BORDER, facecolor=BOX_HEADER_BG, zorder=2)
        ax.add_patch(tab)
        ax.text(0.55, y_bottom + height - 0.22, label, fontsize=8.5, fontweight='bold',
                fontfamily=FONT_FAMILY, color="#0F172A")

    def draw_component(x, y, w, h, title, subtext):
        comp = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                                      linewidth=1.2, edgecolor=EDGE_COLOR,
                                      facecolor=FILL_BG, zorder=3)
        ax.add_patch(comp)
        ax.text(x + w/2, y + h - 0.28, title, fontsize=8.5, fontweight='bold',
                fontfamily=FONT_FAMILY, color="#0F172A", ha='center', va='center')
        ax.text(x + w/2, y + 0.32, subtext, fontsize=7.2,
                fontfamily=FONT_FAMILY, color="#475569", ha='center', va='center')

    # Layer 1: Presentation Layer
    draw_layer_container(4.5, 1.9, "PRESENTATION LAYER (REACT 19)")
    draw_component(0.7, 4.7, 2.65, 1.3, "Message Threat Scanner", "SMS / WhatsApp Input UI\n0-100 Risk Speedometer Gauge")
    draw_component(3.68, 4.7, 2.65, 1.3, "Voice AI Assistant UI", "Speech Input & Audio Waveform\nHindi & English Voice TTS")
    draw_component(6.65, 4.7, 2.65, 1.3, "Simulator & 1930 Portal", "Scam Call Defusal Training UI\nPre-filled Zero-FIR Modal")

    # Downward Inter-Layer Arrows (Presentation -> Application)
    for x in [2.02, 5.0, 7.98]:
        ax.annotate("", xy=(x, 4.3), xytext=(x, 4.7),
                    arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2))

    # Layer 2: Application / Logic Layer
    draw_layer_container(2.35, 1.9, "APPLICATION / LOGIC LAYER (FASTAPI & NODE.JS)")
    draw_component(0.7, 2.55, 2.65, 1.3, "Input & Normalizer", "Speech-to-Text (ASR) Engine\nHinglish & Hindi Tokenizer")
    draw_component(3.68, 2.55, 2.65, 1.3, "Scam Detection Engine", "10-Vector Pattern Matcher\nBank Whitelist (0% False Alarm)")
    draw_component(6.65, 2.55, 2.65, 1.3, "Voice & FIR Generator", "Bilingual Spoken Advisory\n1930 Legal Complaint Formatter")

    # Downward Inter-Layer Arrows (Application -> Data)
    for x in [2.02, 5.0, 7.98]:
        ax.annotate("", xy=(x, 2.15), xytext=(x, 2.55),
                    arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2))

    # Layer 3: Data & Intelligence Layer
    draw_layer_container(0.2, 1.9, "DATA & INTELLIGENCE LAYER")
    draw_component(0.7, 0.4, 2.65, 1.3, "Scam Threat Dictionaries (D1)", "10 Indian Scam Vector Rules\nUrgency & Fear Penalty Store")
    draw_component(3.68, 0.4, 2.65, 1.3, "Bank & Sender Whitelist (D2)", "Verified Bank Sender Headers\nOfficial Institution Domains")
    draw_component(6.65, 0.4, 2.65, 1.3, "1930 FIR & Personas (D3/D4)", "National Cyber Portal Schema\nSimulated Scam Call Personas")

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated Fig 2 Architecture:", output_path)


# ==============================================================================
# 2. FIGURE 3: DATA FLOW DIAGRAM, LEVEL 0 (CONTEXT LEVEL)
# ==============================================================================
def create_fig3_dfd0(output_path):
    fig, ax = plt.subplots(figsize=(9.2, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    # Left Entity: Citizen / User
    user_box = patches.Rectangle((0.5, 1.2), 2.1, 2.0, linewidth=1.4, edgecolor=EDGE_COLOR,
                                 facecolor=FILL_BG, zorder=2)
    ax.add_patch(user_box)
    ax.text(1.55, 2.35, "Citizen /\nUser", fontsize=10.5, fontweight='bold',
            fontfamily=FONT_FAMILY, ha='center', va='center')
    ax.text(1.55, 1.6, "(Victim / Target)", fontsize=7.5, fontstyle='italic',
            fontfamily=FONT_FAMILY, color="#64748B", ha='center', va='center')

    # Center Process: FraudRakshak Core (Oval 0.0)
    center_oval = patches.Ellipse((5.0, 2.2), width=3.2, height=2.3, linewidth=1.5,
                                  edgecolor=EDGE_COLOR, facecolor="white", zorder=2)
    ax.add_patch(center_oval)
    ax.text(5.0, 2.7, "0.0", fontsize=9, fontweight='bold', fontfamily=FONT_FAMILY,
            color="#64748B", ha='center', va='center')
    ax.text(5.0, 2.25, "FraudRakshak\nAI Scam Shield\nSystem", fontsize=10, fontweight='bold',
            fontfamily=FONT_FAMILY, ha='center', va='center')
    ax.text(5.0, 1.45, "(Multilingual Cyber Defense)", fontsize=7, fontstyle='italic',
            fontfamily=FONT_FAMILY, color="#64748B", ha='center', va='center')

    # Right Entity: 1930 Cybercrime Helpline / National Portal
    portal_box = patches.Rectangle((7.4, 1.2), 2.1, 2.0, linewidth=1.4, edgecolor=EDGE_COLOR,
                                   facecolor=FILL_BG, zorder=2)
    ax.add_patch(portal_box)
    ax.text(8.45, 2.35, "1930 Helpline /\nCyber Cell", fontsize=10.5, fontweight='bold',
            fontfamily=FONT_FAMILY, ha='center', va='center')
    ax.text(8.45, 1.6, "(cybercrime.gov.in)", fontsize=7.5, fontstyle='italic',
            fontfamily=FONT_FAMILY, color="#64748B", ha='center', va='center')

    # Flow 1: Citizen -> FraudRakshak (Suspicious Input)
    ax.annotate("", xy=(3.4, 2.75), xytext=(2.6, 2.75),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2, connectionstyle="arc3,rad=-0.12"))
    ax.text(3.0, 3.25, "suspicious SMS, WhatsApp\ntext, or call audio", fontsize=7.5,
            fontfamily=FONT_FAMILY, ha='center', va='center')

    # Flow 2: FraudRakshak -> Citizen (Safety Advice & Score)
    ax.annotate("", xy=(2.6, 1.65), xytext=(3.4, 1.65),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2, connectionstyle="arc3,rad=-0.12"))
    ax.text(3.0, 1.15, "0-100 risk score, danger tags\nspoken voice advice (Hindi/Eng)", fontsize=7.5,
            fontfamily=FONT_FAMILY, ha='center', va='center')

    # Flow 3: FraudRakshak -> 1930 Cyber Cell (Complaint Escalation)
    ax.annotate("", xy=(7.4, 2.75), xytext=(6.6, 2.75),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2, connectionstyle="arc3,rad=-0.12"))
    ax.text(7.0, 3.25, "formatted 1930 Zero-FIR\nincident complaint draft", fontsize=7.5,
            fontfamily=FONT_FAMILY, ha='center', va='center')

    # Flow 4: 1930 Cyber Cell -> FraudRakshak (Advisory & Threat Intel)
    ax.annotate("", xy=(6.6, 1.65), xytext=(7.4, 1.65),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2, connectionstyle="arc3,rad=-0.12"))
    ax.text(7.0, 1.15, "I4C scam threat advisories\n& reporting guidelines", fontsize=7.5,
            fontfamily=FONT_FAMILY, ha='center', va='center')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated Fig 3 DFD Level 0:", output_path)


# ==============================================================================
# 3. FIGURE 4: DATA FLOW DIAGRAM, LEVEL 1 (FUNCTIONAL DECOMPOSITION)
# ==============================================================================
def create_fig4_dfd1(output_path):
    fig, ax = plt.subplots(figsize=(9.5, 6.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.8)
    ax.axis('off')

    # Left Entity: Citizen / User
    user_box = patches.Rectangle((0.4, 2.4), 1.6, 2.0, linewidth=1.4, edgecolor=EDGE_COLOR,
                                 facecolor=FILL_BG, zorder=2)
    ax.add_patch(user_box)
    ax.text(1.2, 3.5, "Citizen /\nUser", fontsize=9.5, fontweight='bold',
            fontfamily=FONT_FAMILY, ha='center', va='center')
    ax.text(1.2, 2.8, "(SMS / Call\nTarget)", fontsize=7, fontstyle='italic',
            fontfamily=FONT_FAMILY, color="#64748B", ha='center', va='center')

    # Central Processes (Vertical 3 Ovals)
    # Process 1.0: Preprocess & Normalize
    p1 = patches.Ellipse((4.4, 5.3), width=2.6, height=1.35, linewidth=1.3,
                         edgecolor=EDGE_COLOR, facecolor="white", zorder=2)
    ax.add_patch(p1)
    ax.text(4.4, 5.3, "1.0\nValidate &\nPreprocess Input", fontsize=8.5, fontweight='bold',
            fontfamily=FONT_FAMILY, ha='center', va='center')

    # Process 2.0: Threat Detection & Risk Scoring
    p2 = patches.Ellipse((4.4, 3.4), width=2.6, height=1.35, linewidth=1.3,
                         edgecolor=EDGE_COLOR, facecolor="white", zorder=2)
    ax.add_patch(p2)
    ax.text(4.4, 3.4, "2.0\nDetect Threat &\nCompute Risk Score", fontsize=8.5, fontweight='bold',
            fontfamily=FONT_FAMILY, ha='center', va='center')

    # Process 3.0: Voice Advisory & 1930 Escalation
    p3 = patches.Ellipse((4.4, 1.4), width=2.6, height=1.35, linewidth=1.3,
                         edgecolor=EDGE_COLOR, facecolor="white", zorder=2)
    ax.add_patch(p3)
    ax.text(4.4, 1.4, "3.0\nGenerate Voice Advice\n& 1930 Zero-FIR", fontsize=8.5, fontweight='bold',
            fontfamily=FONT_FAMILY, ha='center', va='center')

    # Right Data Stores (D1, D2, D3)
    def draw_dstore(y, d_label, d_title, d_sub):
        box = patches.Rectangle((7.0, y), 2.6, 0.85, linewidth=1.2, edgecolor=EDGE_COLOR,
                                facecolor="white", zorder=2)
        ax.add_patch(box)
        # Open left border style
        ax.plot([7.0, 7.0], [y, y+0.85], color="white", lw=2.2, zorder=3)
        ax.text(7.35, y+0.42, d_label, fontsize=8.5, fontweight='bold',
                fontfamily=FONT_FAMILY, ha='center', va='center', color="#1E293B")
        ax.text(8.4, y+0.52, d_title, fontsize=8, fontweight='bold',
                fontfamily=FONT_FAMILY, ha='center', va='center', color="#0F172A")
        ax.text(8.4, y+0.25, d_sub, fontsize=6.5, fontfamily=FONT_FAMILY,
                ha='center', va='center', color="#64748B")

    draw_dstore(4.9, "D1", "Scam Threat Vectors", "(10 Indian scam patterns)")
    draw_dstore(3.0, "D2", "Bank SMS Whitelist", "(SBI, HDFC, ICICI regex)")
    draw_dstore(1.0, "D3", "1930 FIR Template", "(MHA Cybercrime schema)")

    # Data Flows & Arrows:
    # 1. Citizen -> 1.0 (Raw Input)
    ax.annotate("", xy=(3.15, 5.0), xytext=(2.0, 4.0),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2))
    ax.text(2.35, 4.85, "raw text / voice audio", fontsize=7, fontfamily=FONT_FAMILY, ha='center')

    # 2. 1.0 -> 2.0 (Clean Tokens)
    ax.annotate("", xy=(4.4, 4.08), xytext=(4.4, 4.62),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2))
    ax.text(4.85, 4.35, "clean tokens", fontsize=7, fontfamily=FONT_FAMILY)

    # 3. D1 -> 2.0 (Scam Rules)
    ax.annotate("", xy=(5.7, 3.65), xytext=(7.0, 5.1),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.1))
    ax.text(6.4, 4.4, "threat vectors", fontsize=7, fontfamily=FONT_FAMILY)

    # 4. D2 -> 2.0 (Bank Whitelist)
    ax.annotate("", xy=(5.7, 3.4), xytext=(7.0, 3.4),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.1))
    ax.text(6.35, 3.6, "bank patterns", fontsize=7, fontfamily=FONT_FAMILY, ha='center')

    # 5. 2.0 -> Citizen (Immediate Risk Score)
    ax.annotate("", xy=(2.0, 3.4), xytext=(3.1, 3.4),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2))
    ax.text(2.55, 3.6, "0-100 risk score", fontsize=7, fontfamily=FONT_FAMILY, ha='center')

    # 6. 2.0 -> 3.0 (Calibrated Threat Level)
    ax.annotate("", xy=(4.4, 2.08), xytext=(4.4, 2.72),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2))
    ax.text(4.85, 2.4, "threat category", fontsize=7, fontfamily=FONT_FAMILY)

    # 7. D3 -> 3.0 (Complaint Schema)
    ax.annotate("", xy=(5.7, 1.4), xytext=(7.0, 1.4),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.1))
    ax.text(6.35, 1.6, "FIR schema", fontsize=7, fontfamily=FONT_FAMILY, ha='center')

    # 8. 3.0 -> Citizen (Spoken Guidance & Pre-filled FIR)
    ax.annotate("", xy=(2.0, 2.7), xytext=(3.15, 1.8),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.2))
    ax.text(2.35, 2.05, "voice advisory &\nZero-FIR draft", fontsize=7, fontfamily=FONT_FAMILY, ha='center')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated Fig 4 DFD Level 1:", output_path)


# ==============================================================================
# 4. FIGURE 5: (A) USE CASE DIAGRAM; (B) SEQUENCE DIAGRAM
# ==============================================================================
def create_fig5_usecase_sequence(output_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 5.0), dpi=300, gridspec_kw={'width_ratios': [1, 1.35]})
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')

    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')

    # --- (A) USE CASE DIAGRAM (Left) ---
    # System boundary box
    sys_box = patches.Rectangle((2.0, 0.5), 6.0, 9.0, linewidth=1.2, edgecolor=EDGE_COLOR,
                                facecolor="white", zorder=1)
    ax1.add_patch(sys_box)
    ax1.text(5.0, 9.15, "FraudRakshak Scam Shield System", fontsize=8.5, fontweight='bold',
             fontfamily=FONT_FAMILY, ha='center')

    def draw_actor(x, y, label):
        head = patches.Circle((x, y+0.85), radius=0.28, linewidth=1.2, edgecolor=EDGE_COLOR, facecolor="white", zorder=3)
        ax1.add_patch(head)
        ax1.plot([x, x], [y+0.57, y], color=EDGE_COLOR, lw=1.2, zorder=3)
        ax1.plot([x-0.35, x+0.35], [y+0.38, y+0.38], color=EDGE_COLOR, lw=1.2, zorder=3)
        ax1.plot([x, x-0.3], [y, y-0.55], color=EDGE_COLOR, lw=1.2, zorder=3)
        ax1.plot([x, x+0.3], [y, y-0.55], color=EDGE_COLOR, lw=1.2, zorder=3)
        ax1.text(x, y-0.85, label, fontsize=7.5, fontweight='bold', fontfamily=FONT_FAMILY, ha='center')

    draw_actor(0.9, 4.8, "Citizen /\nUser")
    draw_actor(9.1, 4.8, "Cyber Cell /\n1930 Officer")

    ucs = [
        (3.5, 7.8, "Scan SMS / WhatsApp Text"),
        (3.5, 5.8, "Listen to Spoken Voice Advice"),
        (3.5, 3.8, "Practice in Call Simulator"),
        (3.5, 1.8, "Generate 1930 Zero-FIR Draft"),
        (6.5, 7.0, "Update Scam Threat Rules"),
        (6.5, 4.8, "Monitor Live Threat Radar"),
        (6.5, 2.6, "Receive Standardized Complaint")
    ]

    for ux, uy, utext in ucs:
        uc_el = patches.Ellipse((ux, uy), width=2.65, height=1.3, linewidth=1.1,
                                edgecolor=EDGE_COLOR, facecolor=FILL_BG, zorder=2)
        ax1.add_patch(uc_el)
        ax1.text(ux, uy, utext, fontsize=6.8, fontfamily=FONT_FAMILY, ha='center', va='center')

    for i in range(4):
        ax1.plot([1.2, ucs[i][0] - 1.25], [4.8, ucs[i][1]], color=EDGE_COLOR, lw=0.9, zorder=2)

    for i in range(4, 7):
        ax1.plot([8.8, ucs[i][0] + 1.25], [4.8, ucs[i][1]], color=EDGE_COLOR, lw=0.9, zorder=2)

    # --- (B) SEQUENCE DIAGRAM (Right) ---
    lifelines = [
        (0.8, "Citizen"),
        (2.8, "React UI"),
        (4.8, "Preprocessor"),
        (6.8, "Scam Engine"),
        (8.8, "Voice & FIR")
    ]

    for lx, ltext in lifelines:
        lbox = patches.FancyBboxPatch((lx-0.75, 8.8), 1.5, 0.7, boxstyle="round,pad=0.04",
                                      linewidth=1.1, edgecolor=EDGE_COLOR, facecolor=BOX_HEADER_BG, zorder=2)
        ax2.add_patch(lbox)
        ax2.text(lx, 9.15, ltext, fontsize=7.5, fontweight='bold', fontfamily=FONT_FAMILY, ha='center', va='center')
        ax2.plot([lx, lx], [0.6, 8.8], color="#94A3B8", linestyle='--', lw=1.0, zorder=1)

    # Sequence Lifeline Messages
    # 1. Citizen -> React UI
    ax2.annotate("", xy=(2.8, 8.0), xytext=(0.8, 8.0), arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.0))
    ax2.text(1.8, 8.15, "enter text / mic audio", fontsize=6.8, fontfamily=FONT_FAMILY, ha='center')

    # 2. React UI -> Preprocessor
    ax2.annotate("", xy=(4.8, 7.1), xytext=(2.8, 7.1), arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.0))
    ax2.text(3.8, 7.25, "clean & tokenize()", fontsize=6.8, fontfamily=FONT_FAMILY, ha='center')

    # 3. Preprocessor -> Scam Engine
    ax2.annotate("", xy=(6.8, 6.2), xytext=(4.8, 6.2), arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.0))
    ax2.text(5.8, 6.35, "normalized tokens", fontsize=6.8, fontfamily=FONT_FAMILY, ha='center')

    # 4. Scam Engine self-calc
    ax2.annotate("", xy=(6.8, 5.0), xytext=(6.8, 5.5),
                 arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.0, connectionstyle="arc3,rad=-0.5"))
    ax2.text(7.6, 5.25, "match_10_vectors()", fontsize=6.8, fontfamily=FONT_FAMILY, ha='left')

    # 5. Scam Engine -> Voice & FIR
    ax2.annotate("", xy=(8.8, 4.0), xytext=(6.8, 4.0), arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.0))
    ax2.text(7.8, 4.15, "score + danger tags", fontsize=6.8, fontfamily=FONT_FAMILY, ha='center')

    # 6. Voice & FIR -> React UI
    ax2.annotate("", xy=(2.8, 2.6), xytext=(8.8, 2.6), arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.0))
    ax2.text(5.8, 2.75, "spoken voice audio & 1930 draft", fontsize=6.8, fontfamily=FONT_FAMILY, ha='center')

    # 7. React UI -> Citizen
    ax2.annotate("", xy=(0.8, 1.4), xytext=(2.8, 1.4), arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.0))
    ax2.text(1.8, 1.55, "display gauge & speak advice", fontsize=6.8, fontfamily=FONT_FAMILY, ha='center')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated Fig 5 Use Case & Sequence:", output_path)


# ==============================================================================
# 5. FIGURE 6: UML CLASS DIAGRAM
# ==============================================================================
def create_fig6_class_diagram(output_path):
    fig, ax = plt.subplots(figsize=(9.5, 4.3), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.6)
    ax.axis('off')

    def draw_class(x, y, w, h, class_name, attributes, methods):
        box = patches.Rectangle((x, y), w, h, linewidth=1.3, edgecolor=EDGE_COLOR,
                                facecolor="white", zorder=2)
        ax.add_patch(box)
        header = patches.Rectangle((x, y + h - 0.65), w, 0.65, linewidth=1.3,
                                   edgecolor=EDGE_COLOR, facecolor=BOX_HEADER_BG, zorder=3)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.32, class_name, fontsize=9, fontweight='bold',
                fontfamily=FONT_FAMILY, ha='center', va='center')

        divider_y = y + h - 0.65 - len(attributes)*0.28 - 0.15
        ax.plot([x, x+w], [divider_y, divider_y], color=EDGE_COLOR, lw=1.0, zorder=3)

        curr_y = y + h - 0.95
        for attr in attributes:
            ax.text(x + 0.12, curr_y, attr, fontsize=7.2, fontfamily='monospace', va='top')
            curr_y -= 0.28

        curr_y = divider_y - 0.22
        for m in methods:
            ax.text(x + 0.12, curr_y, m, fontsize=7.2, fontfamily='monospace', va='top')
            curr_y -= 0.28

    # Class 1: ThreatScanner (Input Processing)
    draw_class(0.5, 0.5, 2.65, 3.4, "ThreatScanner",
               ["+raw_text: string", "+audio_buffer: bytes", "+language: string", "+timestamp: datetime"],
               ["+capture_input()", "+clean_hinglish()", "+extract_urls_and_phones()", "+get_normalized_tokens()"])

    # Arrow 1: ThreatScanner -> ScamDetectionEngine
    ax.annotate("", xy=(3.8, 2.2), xytext=(3.15, 2.2),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.3))
    ax.text(3.48, 2.4, "tokens", fontsize=7.5, fontstyle='italic', fontfamily=FONT_FAMILY, ha='center')

    # Class 2: ScamDetectionEngine (Core AI)
    draw_class(3.8, 0.5, 2.65, 3.4, "ScamDetectionEngine",
               ["-scam_rules: dict[10]", "-bank_whitelist: list", "-urgency_weights: dict", "-risk_score: int"],
               ["+match_scam_vectors()", "+verify_bank_whitelist()", "+compute_risk_score()", "+get_danger_flags()"])

    # Arrow 2: ScamDetectionEngine -> VoiceAndFIRAdvisor
    ax.annotate("", xy=(7.1, 2.2), xytext=(6.45, 2.2),
                arrowprops=dict(arrowstyle="->", color=EDGE_COLOR, lw=1.3))
    ax.text(6.78, 2.4, "score", fontsize=7.5, fontstyle='italic', fontfamily=FONT_FAMILY, ha='center')

    # Class 3: VoiceAndFIRAdvisor (Actionable Output)
    draw_class(7.1, 0.5, 2.65, 3.4, "VoiceAndFIRAdvisor",
               ["-tts_synth: WebSpeech", "-language_mode: str", "-fir_schema: dict", "-helpline: str = '1930'"],
               ["+synthesize_voice_advice()", "+get_simulator_replies()", "+format_1930_fir_draft()", "+export_complaint_pdf()"])

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated Fig 6 Class Diagram:", output_path)

def main():
    create_fig2_architecture(os.path.join(ASSETS_DIR, "fig2_layered_architecture.png"))
    create_fig3_dfd0(os.path.join(ASSETS_DIR, "fig3_dfd_level_0.png"))
    create_fig4_dfd1(os.path.join(ASSETS_DIR, "fig4_dfd_level_1.png"))
    create_fig5_usecase_sequence(os.path.join(ASSETS_DIR, "fig5_usecase_sequence.png"))
    create_fig6_class_diagram(os.path.join(ASSETS_DIR, "fig6_class_diagram.png"))

if __name__ == '__main__':
    main()
