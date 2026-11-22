"""
generate_system_design_diagrams.py
Generates the exact 5 academic diagrams matching the user's reference format:
1. Figure 2: Layered architecture of the system
2. Figure 3: Data flow diagram, level 0
3. Figure 4: Data flow diagram, level 1
4. Figure 5: (a) Use case diagram; (b) sequence diagram
5. Figure 6: Class diagram

All diagrams are styled in clean, professional academic grayscale/B&W.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ASSETS_DIR = r"d:\Project\FraudRakshak\docs_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. FIGURE 2: LAYERED ARCHITECTURE OF THE SYSTEM
# -------------------------------------------------------------
def create_fig2_architecture(output_path):
    fig, ax = plt.subplots(figsize=(9.5, 5.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # Border style
    BOX_BG = "#F3F4F6"
    BOX_EDGE = "#1F2937"

    # Helper: Layer Box with dashed border
    def draw_layer_container(y_bottom, height, label):
        layer_box = patches.Rectangle((0.5, y_bottom), 9.0, height,
                                      linewidth=1.2, linestyle='--',
                                      edgecolor="#4B5563", facecolor="white", zorder=1)
        ax.add_patch(layer_box)
        ax.text(0.7, y_bottom + height - 0.25, label, fontsize=8.5, fontweight='bold',
                fontfamily='serif', color="#111827")

    # Helper: Inner components
    def draw_component(x, y, w, h, text):
        comp = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                      linewidth=1.2, edgecolor=BOX_EDGE,
                                      facecolor=BOX_BG, zorder=2)
        ax.add_patch(comp)
        ax.text(x + w/2, y + h/2, text, fontsize=8.5, fontweight='bold',
                fontfamily='serif', color="#111827", ha='center', va='center')

    # 1. Presentation Layer
    draw_layer_container(4.4, 1.8, "PRESENTATION LAYER")
    draw_component(0.9, 4.7, 2.4, 1.0, "Message Threat Scanner\n(SMS / WhatsApp UI)")
    draw_component(3.8, 4.7, 2.4, 1.0, "Voice AI Advisor UI\n(Hindi & English Audio)")
    draw_component(6.7, 4.7, 2.4, 1.0, "Call Simulator & Copilot\n(1930 Zero-FIR Form)")

    # Downward arrows between layers
    for x in [2.1, 5.0, 7.9]:
        ax.annotate("", xy=(x, 4.2), xytext=(x, 4.7),
                    arrowprops=dict(arrowstyle="->", color="#1F2937", lw=1.2))

    # 2. Application / Logic Layer
    draw_layer_container(2.3, 1.8, "APPLICATION / LOGIC LAYER")
    draw_component(0.9, 2.6, 2.4, 1.0, "Input Validation &\nSpeech Preprocessor")
    draw_component(3.8, 2.6, 2.4, 1.0, "Multi-Vector Threat\n& Whitelist Evaluator")
    draw_component(6.7, 2.6, 2.4, 1.0, "Risk Scoring &\nVoice Advisory Engine")

    # Downward arrows between layers
    for x in [2.1, 5.0, 7.9]:
        ax.annotate("", xy=(x, 2.1), xytext=(x, 2.6),
                    arrowprops=dict(arrowstyle="->", color="#1F2937", lw=1.2))

    # 3. Data & Model Layer
    draw_layer_container(0.2, 1.8, "DATA & MODEL LAYER")
    draw_component(0.9, 0.5, 2.4, 1.0, "Scam Vector Dictionaries\n(10 Threat Rules)")
    draw_component(3.8, 0.5, 2.4, 1.0, "Legitimate Bank Patterns\n(Whitelist D2)")
    draw_component(6.7, 0.5, 2.4, 1.0, "1930 Cybercrime Schema\n(National Portal Draft)")

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Created:", output_path)


# -------------------------------------------------------------
# 2. FIGURE 3: DATA FLOW DIAGRAM, LEVEL 0
# -------------------------------------------------------------
def create_fig3_dfd0(output_path):
    fig, ax = plt.subplots(figsize=(9.0, 4.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    BOX_BG = "#F3F4F6"
    EDGE = "#1F2937"

    # Left Entity: Citizen / User
    user_box = patches.Rectangle((0.6, 1.3), 2.0, 1.8, linewidth=1.4, edgecolor=EDGE,
                                 facecolor=BOX_BG, zorder=2)
    ax.add_patch(user_box)
    ax.text(1.6, 2.2, "Citizen /\nUser", fontsize=10.5, fontweight='bold',
            fontfamily='serif', ha='center', va='center')

    # Center Process: FraudRakshak Core (Oval)
    center_oval = patches.Ellipse((5.0, 2.2), width=2.8, height=2.2, linewidth=1.4,
                                  edgecolor=EDGE, facecolor="white", zorder=2)
    ax.add_patch(center_oval)
    ax.text(5.0, 2.2, "FraudRakshak\nAI Scam Shield\nSystem", fontsize=10, fontweight='bold',
            fontfamily='serif', ha='center', va='center')

    # Right Entity: Cyber Crime Helpline (1930)
    portal_box = patches.Rectangle((7.4, 1.3), 2.0, 1.8, linewidth=1.4, edgecolor=EDGE,
                                   facecolor=BOX_BG, zorder=2)
    ax.add_patch(portal_box)
    ax.text(8.4, 2.2, "1930 Helpline /\nCyber Cell", fontsize=10.5, fontweight='bold',
            fontfamily='serif', ha='center', va='center')

    # Curved Arrow 1: User -> Process (Top)
    ax.annotate("", xy=(3.6, 2.7), xytext=(2.6, 2.7),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2,
                                connectionstyle="arc3,rad=-0.15"))
    ax.text(3.1, 3.2, "suspicious SMS & call audio", fontsize=8, fontfamily='serif',
            ha='center', va='center')

    # Curved Arrow 2: Process -> User (Bottom)
    ax.annotate("", xy=(2.6, 1.7), xytext=(3.6, 1.7),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2,
                                connectionstyle="arc3,rad=-0.15"))
    ax.text(3.1, 1.25, "risk score, voice advice, copilot", fontsize=8, fontfamily='serif',
            ha='center', va='center')

    # Curved Arrow 3: Process -> 1930 Portal (Top)
    ax.annotate("", xy=(7.4, 2.7), xytext=(6.4, 2.7),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2,
                                connectionstyle="arc3,rad=-0.15"))
    ax.text(6.9, 3.2, "formatted FIR draft", fontsize=8, fontfamily='serif',
            ha='center', va='center')

    # Curved Arrow 4: 1930 Portal -> Process (Bottom)
    ax.annotate("", xy=(6.4, 1.7), xytext=(7.4, 1.7),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2,
                                connectionstyle="arc3,rad=-0.15"))
    ax.text(6.9, 1.25, "threat guidelines & status", fontsize=8, fontfamily='serif',
            ha='center', va='center')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Created:", output_path)


# -------------------------------------------------------------
# 3. FIGURE 4: DATA FLOW DIAGRAM, LEVEL 1
# -------------------------------------------------------------
def create_fig4_dfd1(output_path):
    fig, ax = plt.subplots(figsize=(9.2, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    BOX_BG = "#F3F4F6"
    EDGE = "#1F2937"

    # Left Entity: Citizen / User
    user_box = patches.Rectangle((0.6, 2.5), 1.6, 1.6, linewidth=1.4, edgecolor=EDGE,
                                 facecolor=BOX_BG, zorder=2)
    ax.add_patch(user_box)
    ax.text(1.4, 3.3, "Citizen /\nUser", fontsize=10, fontweight='bold',
            fontfamily='serif', ha='center', va='center')

    # Center 3 Ovals (Processes 1.0, 2.0, 3.0)
    p1 = patches.Ellipse((4.4, 5.0), width=2.4, height=1.3, linewidth=1.3,
                         edgecolor=EDGE, facecolor="white", zorder=2)
    ax.add_patch(p1)
    ax.text(4.4, 5.0, "1.0\nValidate &\nPreprocess", fontsize=8.5, fontweight='bold',
            fontfamily='serif', ha='center', va='center')

    p2 = patches.Ellipse((4.4, 3.3), width=2.4, height=1.3, linewidth=1.3,
                         edgecolor=EDGE, facecolor="white", zorder=2)
    ax.add_patch(p2)
    ax.text(4.4, 3.3, "2.0\nDetect Threat &\nPredict Risk", fontsize=8.5, fontweight='bold',
            fontfamily='serif', ha='center', va='center')

    p3 = patches.Ellipse((4.4, 1.5), width=2.4, height=1.3, linewidth=1.3,
                         edgecolor=EDGE, facecolor="white", zorder=2)
    ax.add_patch(p3)
    ax.text(4.4, 1.5, "3.0\nVoice Advisory &\n1930 Escalation", fontsize=8.5, fontweight='bold',
            fontfamily='serif', ha='center', va='center')

    # Right 3 Data Stores (D1, D2, D3)
    def draw_dstore(y, d_label, d_text):
        box = patches.Rectangle((7.0, y), 2.5, 0.7, linewidth=1.2, edgecolor=EDGE,
                                facecolor="white", zorder=2)
        ax.add_patch(box)
        # open left
        ax.plot([7.0, 7.0], [y, y+0.7], color="white", lw=2.0, zorder=3)
        ax.text(8.25, y+0.35, f"{d_label} {d_text}", fontsize=8, fontweight='bold',
                fontfamily='serif', ha='center', va='center')

    draw_dstore(4.65, "D1", "Threat Vectors")
    draw_dstore(2.95, "D2", "Bank Whitelist")
    draw_dstore(1.15, "D3", "1930 FIR Template")

    # Flow arrows:
    # User -> 1.0
    ax.annotate("", xy=(3.3, 4.6), xytext=(2.2, 3.7),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2))
    ax.text(2.6, 4.4, "raw text / audio", fontsize=7.5, fontfamily='serif', ha='center')

    # 1.0 -> 2.0
    ax.annotate("", xy=(4.4, 4.0), xytext=(4.4, 4.35),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2))
    ax.text(4.9, 4.15, "clean tokens", fontsize=7.5, fontfamily='serif')

    # D1 -> 1.0 / 2.0
    ax.annotate("", xy=(5.6, 5.0), xytext=(7.0, 5.0),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2))
    ax.text(6.3, 5.2, "rules", fontsize=7.5, fontfamily='serif', ha='center')

    # D2 -> 2.0
    ax.annotate("", xy=(5.6, 3.3), xytext=(7.0, 3.3),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2))
    ax.text(6.3, 3.5, "patterns", fontsize=7.5, fontfamily='serif', ha='center')

    # 2.0 -> User (Risk score)
    ax.annotate("", xy=(2.2, 3.3), xytext=(3.2, 3.3),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2))
    ax.text(2.7, 3.5, "risk score", fontsize=7.5, fontfamily='serif', ha='center')

    # 2.0 -> 3.0
    ax.annotate("", xy=(4.4, 2.2), xytext=(4.4, 2.65),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2))
    ax.text(4.9, 2.4, "threat level", fontsize=7.5, fontfamily='serif')

    # D3 -> 3.0
    ax.annotate("", xy=(5.6, 1.5), xytext=(7.0, 1.5),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2))
    ax.text(6.3, 1.7, "schema", fontsize=7.5, fontfamily='serif', ha='center')

    # 3.0 -> User (Advice & Complaint)
    ax.annotate("", xy=(2.2, 2.8), xytext=(3.3, 1.9),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.2))
    ax.text(2.6, 2.2, "voice advice & draft", fontsize=7.5, fontfamily='serif', ha='center')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Created:", output_path)


# -------------------------------------------------------------
# 4. FIGURE 5: (A) USE CASE DIAGRAM; (B) SEQUENCE DIAGRAM
# -------------------------------------------------------------
def create_fig5_usecase_sequence(output_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 5.0), dpi=300, gridspec_kw={'width_ratios': [1, 1.3]})
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')

    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')

    EDGE = "#1F2937"

    # --- (A) USE CASE DIAGRAM (Left) ---
    # System boundary box
    sys_box = patches.Rectangle((2.0, 0.5), 6.0, 9.0, linewidth=1.2, edgecolor=EDGE,
                                facecolor="white", zorder=1)
    ax1.add_patch(sys_box)
    ax1.text(5.0, 9.15, "FraudRakshak Scam Shield", fontsize=9, fontweight='bold',
             fontfamily='serif', ha='center')

    # Stick Figure Helper
    def draw_actor(x, y, label):
        # head
        head = patches.Circle((x, y+0.9), radius=0.3, linewidth=1.2, edgecolor=EDGE, facecolor="white", zorder=3)
        ax1.add_patch(head)
        # body
        ax1.plot([x, x], [y+0.6, y], color=EDGE, lw=1.2, zorder=3)
        # arms
        ax1.plot([x-0.4, x+0.4], [y+0.4, y+0.4], color=EDGE, lw=1.2, zorder=3)
        # legs
        ax1.plot([x, x-0.35], [y, y-0.6], color=EDGE, lw=1.2, zorder=3)
        ax1.plot([x, x+0.35], [y, y-0.6], color=EDGE, lw=1.2, zorder=3)
        ax1.text(x, y-0.9, label, fontsize=8, fontweight='bold', fontfamily='serif', ha='center')

    # Left Actor: Citizen / User
    draw_actor(0.9, 4.8, "Citizen /\nUser")
    # Right Actor: Cyber Officer / 1930
    draw_actor(9.1, 4.8, "Cyber Cell /\n1930 Officer")

    # Use Cases (Ellipses)
    ucs = [
        (3.5, 7.8, "Scan message / SMS"),
        (3.5, 5.8, "Listen to Voice advice"),
        (3.5, 3.8, "Practice in Call Simulator"),
        (3.5, 1.8, "Generate 1930 FIR draft"),
        (6.5, 7.0, "Update threat rules"),
        (6.5, 4.8, "View live threat radar"),
        (6.5, 2.6, "Receive incident complaint")
    ]

    for ux, uy, utext in ucs:
        uc_el = patches.Ellipse((ux, uy), width=2.6, height=1.3, linewidth=1.1,
                                edgecolor=EDGE, facecolor="#F9FAFB", zorder=2)
        ax1.add_patch(uc_el)
        ax1.text(ux, uy, utext, fontsize=7.2, fontfamily='serif', ha='center', va='center')

    # Lines from Left Actor to its use cases
    for i in range(4):
        ax1.plot([1.2, ucs[i][0] - 1.2], [4.8, ucs[i][1]], color=EDGE, lw=0.9, zorder=2)

    # Lines from Right Actor to its use cases
    for i in range(4, 7):
        ax1.plot([8.8, ucs[i][0] + 1.2], [4.8, ucs[i][1]], color=EDGE, lw=0.9, zorder=2)

    # --- (B) SEQUENCE DIAGRAM (Right) ---
    lifelines = [
        (0.8, "Citizen"),
        (2.8, "UI"),
        (4.8, "Preprocessor"),
        (6.8, "Threat Engine"),
        (8.8, "Advisor / FIR")
    ]

    # Draw Lifeline Boxes
    for lx, ltext in lifelines:
        lbox = patches.FancyBboxPatch((lx-0.7, 8.8), 1.4, 0.7, boxstyle="round,pad=0.04",
                                      linewidth=1.1, edgecolor=EDGE, facecolor="#F3F4F6", zorder=2)
        ax2.add_patch(lbox)
        ax2.text(lx, 9.15, ltext, fontsize=8, fontweight='bold', fontfamily='serif', ha='center', va='center')
        # Dashed Lifeline down
        ax2.plot([lx, lx], [0.6, 8.8], color="#9CA3AF", linestyle='--', lw=1.0, zorder=1)

    # Sequence Message Arrows:
    # 1. enter text (Citizen -> UI)
    ax2.annotate("", xy=(2.8, 8.0), xytext=(0.8, 8.0), arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.0))
    ax2.text(1.8, 8.15, "enter text / voice", fontsize=7, fontfamily='serif', ha='center')

    # 2. validate() (UI -> Preprocessor)
    ax2.annotate("", xy=(4.8, 7.1), xytext=(2.8, 7.1), arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.0))
    ax2.text(3.8, 7.25, "validate & clean()", fontsize=7, fontfamily='serif', ha='center')

    # 3. clean tokens (Preprocessor -> Threat Engine)
    ax2.annotate("", xy=(6.8, 6.2), xytext=(4.8, 6.2), arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.0))
    ax2.text(5.8, 6.35, "clean tokens", fontsize=7, fontfamily='serif', ha='center')

    # 4. threat match (Threat Engine self loop)
    ax2.annotate("", xy=(6.8, 5.0), xytext=(6.8, 5.5),
                 arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.0, connectionstyle="arc3,rad=-0.5"))
    ax2.text(7.6, 5.25, "calc_risk()", fontsize=7, fontfamily='serif', ha='left')

    # 5. score + category (Threat Engine -> Advisor / FIR)
    ax2.annotate("", xy=(8.8, 4.0), xytext=(6.8, 4.0), arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.0))
    ax2.text(7.8, 4.15, "score + category", fontsize=7, fontfamily='serif', ha='center')

    # 6. advice + draft (Advisor / FIR -> UI)
    ax2.annotate("", xy=(2.8, 2.6), xytext=(8.8, 2.6), arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.0))
    ax2.text(5.8, 2.75, "voice advice & draft complaint", fontsize=7, fontfamily='serif', ha='center')

    # 7. show report & speak (UI -> Citizen)
    ax2.annotate("", xy=(0.8, 1.4), xytext=(2.8, 1.4), arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.0))
    ax2.text(1.8, 1.55, "show alert & speak", fontsize=7, fontfamily='serif', ha='center')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Created:", output_path)


# -------------------------------------------------------------
# 5. FIGURE 6: CLASS DIAGRAM
# -------------------------------------------------------------
def create_fig6_class_diagram(output_path):
    fig, ax = plt.subplots(figsize=(9.2, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    EDGE = "#1F2937"
    HEADER_BG = "#E5E7EB"

    # Helper: UML 3-part box
    def draw_class(x, y, w, h, class_name, attributes, methods):
        # Outer box
        box = patches.Rectangle((x, y), w, h, linewidth=1.3, edgecolor=EDGE,
                                facecolor="white", zorder=2)
        ax.add_patch(box)
        # Header box
        header = patches.Rectangle((x, y + h - 0.7), w, 0.7, linewidth=1.3,
                                   edgecolor=EDGE, facecolor=HEADER_BG, zorder=3)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.35, class_name, fontsize=9.5, fontweight='bold',
                fontfamily='serif', ha='center', va='center')

        # Mid divider line
        divider_y = y + h - 0.7 - len(attributes)*0.28 - 0.2
        ax.plot([x, x+w], [divider_y, divider_y], color=EDGE, lw=1.0, zorder=3)

        # Attributes text
        curr_y = y + h - 1.0
        for attr in attributes:
            ax.text(x + 0.15, curr_y, attr, fontsize=7.5, fontfamily='monospace', va='top')
            curr_y -= 0.28

        # Methods text
        curr_y = divider_y - 0.25
        for m in methods:
            ax.text(x + 0.15, curr_y, m, fontsize=7.5, fontfamily='monospace', va='top')
            curr_y -= 0.28

    # 1. Class: MessageInput
    draw_class(0.6, 0.6, 2.5, 3.2, "MessageInput",
               ["+raw_text: str", "+audio_stream: bytes", "+language: str", "+timestamp: datetime"],
               ["+validate()", "+clean_text()", "+extract_tokens()"])

    # Arrow 1: MessageInput -> ThreatDetector
    ax.annotate("", xy=(3.8, 2.2), xytext=(3.1, 2.2),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.3))
    ax.text(3.45, 2.4, "input", fontsize=8, fontstyle='italic', fontfamily='serif', ha='center')

    # 2. Class: ThreatDetector
    draw_class(3.8, 0.6, 2.5, 3.2, "ThreatDetector",
               ["-scam_rules: dict", "-bank_whitelist: list", "-urgency_weights: dict", "-threshold: int"],
               ["+match_vectors()", "+check_whitelist()", "+compute_score()", "+classify_risk()"])

    # Arrow 2: ThreatDetector -> AdvisoryGenerator
    ax.annotate("", xy=(7.0, 2.2), xytext=(6.3, 2.2),
                arrowprops=dict(arrowstyle="->", color=EDGE, lw=1.3))
    ax.text(6.65, 2.4, "score", fontsize=8, fontstyle='italic', fontfamily='serif', ha='center')

    # 3. Class: AdvisoryGenerator
    draw_class(7.0, 0.6, 2.5, 3.2, "AdvisoryGenerator",
               ["-voice_synth: WebSpeech", "-language_mode: str", "-helpline_schema: dict"],
               ["+speak_advice()", "+get_defensive_replies()", "+generate_fir_draft()", "+export_pdf()"])

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Created:", output_path)

if __name__ == '__main__':
    create_fig2_architecture(os.path.join(ASSETS_DIR, "fig2_layered_architecture.png"))
    create_fig3_dfd0(os.path.join(ASSETS_DIR, "fig3_dfd_level_0.png"))
    create_fig4_dfd1(os.path.join(ASSETS_DIR, "fig4_dfd_level_1.png"))
    create_fig5_usecase_sequence(os.path.join(ASSETS_DIR, "fig5_usecase_sequence.png"))
    create_fig6_class_diagram(os.path.join(ASSETS_DIR, "fig6_class_diagram.png"))
