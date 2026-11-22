"""
create_dfd_diagrams.py
Generates professional, high-resolution DFD Level 0 and DFD Level 1 diagrams
for academic submission using standard DFD notations.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_dfd_level_0(output_path):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Color Palette
    ENTITY_COLOR = "#E0F2FE"       # Light Sky Blue
    ENTITY_BORDER = "#0284C7"      # Sky Blue border
    PROCESS_COLOR = "#FEF3C7"      # Light Amber / Gold
    PROCESS_BORDER = "#D97706"     # Amber border
    PORTAL_COLOR = "#DCFCE7"       # Light Green
    PORTAL_BORDER = "#16A34A"      # Green border
    ARROW_COLOR = "#1E293B"        # Slate Dark
    TEXT_COLOR = "#0F172A"

    # Title
    ax.text(5, 5.7, "DFD Level 0: Context Level Data Flow Diagram (FraudRakshak)",
            fontsize=13, fontweight='bold', ha='center', color=TEXT_COLOR, fontfamily='serif')

    # 1. Left External Entity: User / Citizen
    entity_user = patches.Rectangle((0.6, 2.0), 2.2, 2.0, linewidth=2, edgecolor=ENTITY_BORDER,
                                    facecolor=ENTITY_COLOR, zorder=2)
    ax.add_patch(entity_user)
    ax.text(1.7, 3.2, "External Entity\n[ USER / CITIZEN ]", fontsize=10, fontweight='bold',
            ha='center', va='center', color=TEXT_COLOR, fontfamily='serif')
    ax.text(1.7, 2.4, "(Mobile User / Senior Citizen\nUPI Consumer)", fontsize=8,
            ha='center', va='center', color="#334155", fontfamily='serif')

    # 2. Center Process: 0.0 FraudRakshak Core System
    process_core = patches.Circle((5.0, 3.0), radius=1.3, linewidth=2.5, edgecolor=PROCESS_BORDER,
                                  facecolor=PROCESS_COLOR, zorder=2)
    ax.add_patch(process_core)
    ax.text(5.0, 3.5, "0.0", fontsize=11, fontweight='bold', ha='center', va='center', color=PROCESS_BORDER, fontfamily='serif')
    ax.text(5.0, 3.0, "FraudRakshak\nAI Scam Shield\nSystem", fontsize=11, fontweight='bold',
            ha='center', va='center', color=TEXT_COLOR, fontfamily='serif')
    ax.text(5.0, 2.2, "(Heuristic + Voice AI)", fontsize=8, ha='center', va='center', color="#78350F", fontfamily='serif')

    # 3. Right External Entity: 1930 Cyber Crime Portal
    entity_gov = patches.Rectangle((7.4, 2.0), 2.1, 2.0, linewidth=2, edgecolor=PORTAL_BORDER,
                                   facecolor=PORTAL_COLOR, zorder=2)
    ax.add_patch(entity_gov)
    ax.text(8.45, 3.2, "External Entity\n[ 1930 HELPLINE ]", fontsize=10, fontweight='bold',
            ha='center', va='center', color=TEXT_COLOR, fontfamily='serif')
    ax.text(8.45, 2.4, "National Cyber Crime\nReporting Portal\n(cybercrime.gov.in)", fontsize=8,
            ha='center', va='center', color="#14532D", fontfamily='serif')

    # Directed Arrows (User -> Process)
    # Arrow 1: Suspicious SMS / WhatsApp Text
    ax.annotate("", xy=(3.7, 3.5), xytext=(2.8, 3.5),
                arrowprops=dict(arrowstyle="->", color=ARROW_COLOR, lw=1.8))
    ax.text(3.25, 3.75, "Suspicious SMS / Text\n& Call Transcripts", fontsize=8, fontweight='bold',
            ha='center', va='center', color=ARROW_COLOR, fontfamily='serif',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))

    # Arrow 2: Voice Question / Mic input
    ax.annotate("", xy=(3.7, 2.7), xytext=(2.8, 2.7),
                arrowprops=dict(arrowstyle="->", color=ARROW_COLOR, lw=1.8))
    ax.text(3.25, 2.4, "Spoken Hindi/English\nVoice Inquiries", fontsize=8, fontweight='bold',
            ha='center', va='center', color=ARROW_COLOR, fontfamily='serif',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))

    # Directed Arrows (Process -> User)
    # Arrow 3: Risk Score & Warning Tags
    ax.annotate("", xy=(2.8, 3.9), xytext=(4.1, 4.1),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.8))
    ax.text(3.3, 4.4, "Risk Score (0-100)\n& Threat Warning Tags", fontsize=8, fontweight='bold',
            ha='center', va='center', color="#B91C1C", fontfamily='serif',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))

    # Arrow 4: Voice Advisory & Copilot Replies
    ax.annotate("", xy=(2.8, 1.9), xytext=(4.1, 1.9),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.8))
    ax.text(3.4, 1.5, "Spoken Audio Advice\n& Defense Responses", fontsize=8, fontweight='bold',
            ha='center', va='center', color="#0369A1", fontfamily='serif',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))

    # Directed Arrows (Process -> 1930 Portal)
    # Arrow 5: Pre-filled Zero FIR complaint
    ax.annotate("", xy=(7.4, 3.0), xytext=(6.3, 3.0),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=2.0))
    ax.text(6.85, 3.4, "Pre-formatted\n1930 Zero-FIR\nComplaint Draft", fontsize=8, fontweight='bold',
            ha='center', va='center', color="#15803D", fontfamily='serif',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated DFD Level 0 at: {output_path}")


def generate_dfd_level_1(output_path):
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    ENTITY_COLOR = "#E0F2FE"       # Light Sky
    ENTITY_BORDER = "#0284C7"
    PROCESS_COLOR = "#FEF3C7"      # Light Amber
    PROCESS_BORDER = "#D97706"
    DATASTORE_COLOR = "#F1F5F9"    # Slate Light
    DATASTORE_BORDER = "#475569"
    PORTAL_COLOR = "#DCFCE7"       # Green
    PORTAL_BORDER = "#16A34A"
    ARROW_COLOR = "#1E293B"
    TEXT_COLOR = "#0F172A"

    # Title
    ax.text(5.5, 8.1, "DFD Level 1: Detailed Functional Data Flow Diagram (FraudRakshak)",
            fontsize=13, fontweight='bold', ha='center', color=TEXT_COLOR, fontfamily='serif')

    # Helper: draw process (rounded box)
    def draw_process(x, y, w, h, p_num, p_title):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                     linewidth=1.8, edgecolor=PROCESS_BORDER, facecolor=PROCESS_COLOR, zorder=3)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.25, p_num, fontsize=9, fontweight='bold', ha='center', va='center', color=PROCESS_BORDER, fontfamily='serif')
        ax.text(x + w/2, y + h/2 - 0.1, p_title, fontsize=8.5, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, fontfamily='serif')

    # Helper: draw datastore (open rectangle)
    def draw_datastore(x, y, w, h, d_num, d_title):
        box = patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor=DATASTORE_BORDER,
                                facecolor=DATASTORE_COLOR, zorder=2)
        ax.add_patch(box)
        # open left/right by redrawing white borders or simple open lines
        ax.plot([x, x+w], [y, y], color=DATASTORE_BORDER, lw=1.8)
        ax.plot([x, x+w], [y+h, y+h], color=DATASTORE_BORDER, lw=1.8)
        ax.plot([x, x], [y, y+h], color="white", lw=2.2) # open left
        ax.text(x + 0.35, y + h/2, d_num, fontsize=8.5, fontweight='bold', ha='center', va='center', color="#0369A1", fontfamily='serif')
        ax.text(x + w/2 + 0.2, y + h/2, d_title, fontsize=8, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, fontfamily='serif')

    # 1. External Entity: User (Left)
    entity_user = patches.Rectangle((0.4, 4.5), 1.8, 2.2, linewidth=2, edgecolor=ENTITY_BORDER,
                                    facecolor=ENTITY_COLOR, zorder=3)
    ax.add_patch(entity_user)
    ax.text(1.3, 5.8, "USER / CITIZEN", fontsize=9.5, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, fontfamily='serif')
    ax.text(1.3, 5.1, "SMS Text /\nVoice Input /\nCall Simulator", fontsize=8, ha='center', va='center', color="#334155", fontfamily='serif')

    # 2. Process 1.0: Input Pre-processing & Normalization
    draw_process(2.8, 5.0, 2.2, 1.2, "1.0", "Text & Audio\nPre-processing")

    # 3. Process 2.0: Multi-Vector Threat Analysis
    draw_process(5.8, 5.0, 2.4, 1.2, "2.0", "Multi-Vector Threat\n& Keyword Matcher")

    # Data Store D1: Threat Dictionaries
    draw_datastore(5.8, 6.8, 2.4, 0.7, "D1", "10 Scam Vectors & Regex\n(Digital Arrest, Cutoff, KYC)")

    # 4. Process 3.0: Safe Bank Whitelist Filter
    draw_process(5.8, 3.0, 2.4, 1.2, "3.0", "Legitimate Bank\nWhitelist Filter")

    # Data Store D2: Legitimate Bank Patterns
    draw_datastore(5.8, 1.7, 2.4, 0.7, "D2", "Genuine Bank Syntax\n(SBI, HDFC, ICICI alerts)")

    # 5. Process 4.0: Risk Scoring & Decision Engine
    draw_process(8.8, 4.0, 2.0, 1.4, "4.0", "Risk Scoring &\nClassification Engine\n(Score: 0 - 100)")

    # 6. Process 5.0: Voice Advisory & Copilot
    draw_process(2.8, 2.6, 2.2, 1.2, "5.0", "Voice AI Advisor &\nCall Simulator Copilot")

    # 7. Process 6.0: 1930 Zero-FIR Generator
    draw_process(2.8, 0.6, 2.2, 1.2, "6.0", "1930 Zero-FIR\nComplaint Formatter")

    # 8. External Entity: 1930 National Portal (Bottom Right)
    entity_gov = patches.Rectangle((8.8, 0.6), 2.0, 1.2, linewidth=2, edgecolor=PORTAL_BORDER,
                                   facecolor=PORTAL_COLOR, zorder=3)
    ax.add_patch(entity_gov)
    ax.text(9.8, 1.3, "1930 HELPLINE", fontsize=9.5, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, fontfamily='serif')
    ax.text(9.8, 0.9, "Cyber Crime Portal\n(cybercrime.gov.in)", fontsize=7.5, ha='center', va='center', color="#14532D", fontfamily='serif')

    # ==================== DATA FLOW ARROWS ====================
    # User -> 1.0
    ax.annotate("", xy=(2.8, 5.6), xytext=(2.2, 5.6),
                arrowprops=dict(arrowstyle="->", color=ARROW_COLOR, lw=1.5))
    ax.text(2.5, 5.9, "Raw Text / Voice", fontsize=7.5, fontweight='bold', ha='center', va='center', color=ARROW_COLOR)

    # 1.0 -> 2.0
    ax.annotate("", xy=(5.8, 5.6), xytext=(5.0, 5.6),
                arrowprops=dict(arrowstyle="->", color=ARROW_COLOR, lw=1.5))
    ax.text(5.4, 5.9, "Cleaned Tokens", fontsize=7.5, fontweight='bold', ha='center', va='center', color=ARROW_COLOR)

    # D1 -> 2.0 (Bidirectional read)
    ax.annotate("", xy=(7.0, 6.2), xytext=(7.0, 6.8),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.5))
    ax.text(7.6, 6.5, "Pattern Rules", fontsize=7.5, color="#0284C7", fontfamily='serif')

    # 2.0 -> 3.0
    ax.annotate("", xy=(7.0, 4.2), xytext=(7.0, 5.0),
                arrowprops=dict(arrowstyle="->", color=ARROW_COLOR, lw=1.5))
    ax.text(7.7, 4.6, "Matched Scam Indicators", fontsize=7.5, fontweight='bold', ha='center', va='center', color=ARROW_COLOR)

    # D2 -> 3.0
    ax.annotate("", xy=(7.0, 3.0), xytext=(7.0, 2.4),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.5))
    ax.text(7.6, 2.7, "Whitelist Rules", fontsize=7.5, color="#0284C7", fontfamily='serif')

    # 3.0 -> 4.0
    ax.annotate("", xy=(8.8, 4.7), xytext=(8.2, 4.0),
                arrowprops=dict(arrowstyle="->", color=ARROW_COLOR, lw=1.5))
    ax.text(8.4, 4.7, "Evaluated Attributes", fontsize=7.5, fontweight='bold', ha='center', va='center', color=ARROW_COLOR)

    # 4.0 -> User (Risk Report)
    ax.annotate("", xy=(2.2, 6.2), xytext=(8.8, 5.2),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.6, connectionstyle="arc3,rad=-0.15"))
    ax.text(5.5, 6.4, "Instant Risk Score (Safe / Medium / High)", fontsize=8, fontweight='bold',
            ha='center', va='center', color="#B91C1C", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9))

    # 4.0 -> 5.0 (Advisory trigger)
    ax.annotate("", xy=(5.0, 3.2), xytext=(8.8, 4.3),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.5, connectionstyle="arc3,rad=0.15"))
    ax.text(6.4, 3.6, "Safety Guidance Data", fontsize=7.5, color="#0369A1", fontfamily='serif')

    # 5.0 -> User (Audio output)
    ax.annotate("", xy=(2.2, 4.8), xytext=(2.8, 3.4),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.5))
    ax.text(2.0, 3.8, "Spoken Voice\nAdvisory (TTS)", fontsize=7.5, fontweight='bold', ha='center', va='center', color="#0369A1")

    # 4.0 -> 6.0 (High risk triggers FIR generator)
    ax.annotate("", xy=(5.0, 1.2), xytext=(8.8, 4.1),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.5, connectionstyle="arc3,rad=0.25"))
    ax.text(6.8, 1.1, "Scam Evidence & Offender Details", fontsize=7.5, color="#15803D", fontfamily='serif')

    # 6.0 -> 1930 Portal
    ax.annotate("", xy=(8.8, 1.2), xytext=(5.0, 1.2),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=2.0))
    ax.text(6.9, 0.7, "Formatted 1930 Zero-FIR Complaint Draft", fontsize=8, fontweight='bold',
            ha='center', va='center', color="#15803D", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9))

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated DFD Level 1 at: {output_path}")

if __name__ == '__main__':
    assets_dir = r"d:\Project\FraudRakshak\docs_assets"
    os.makedirs(assets_dir, exist_ok=True)
    dfd0_path = os.path.join(assets_dir, "dfd_level_0.png")
    dfd1_path = os.path.join(assets_dir, "dfd_level_1.png")
    generate_dfd_level_0(dfd0_path)
    generate_dfd_level_1(dfd1_path)
