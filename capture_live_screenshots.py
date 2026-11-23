"""
capture_live_screenshots.py
Captures real, live screenshots of FraudRakshak from https://fraudrakshak-q133oj3bu-me-e80d.vercel.app
for inclusion in the academic project report.
"""

from playwright.sync_api import sync_playwright
import time
import os

ASSETS_DIR = r"d:\Project\FraudRakshak\docs_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def capture_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 850})
        page = context.new_page()

        print("Navigating to https://fraudrakshak-q133oj3bu-me-e80d.vercel.app ...")
        page.goto("https://fraudrakshak-q133oj3bu-me-e80d.vercel.app", timeout=30000)
        page.wait_for_timeout(3000)

        # 1. Main Dashboard & Header with Presets
        path1 = os.path.join(ASSETS_DIR, "screenshot_1_dashboard.png")
        page.screenshot(path=path1)
        print("Captured 1:", path1)

        # 2. Trigger Scam Preset Scan (FedEx Digital Arrest)
        try:
            fedex_btn = page.locator("button:has-text('FedEx Digital Arrest')").first
            if fedex_btn.is_visible():
                fedex_btn.click()
                page.wait_for_timeout(1000)
            
            # Click Scan Message button
            scan_btn = page.locator("button:has-text('Scan Message')").first
            if scan_btn.is_visible():
                scan_btn.click()
                page.wait_for_timeout(2000)
            
            path2 = os.path.join(ASSETS_DIR, "screenshot_2_scam_scan.png")
            page.screenshot(path=path2)
            print("Captured 2 (Scam Scan):", path2)
        except Exception as e:
            print("Error capturing Scam Scan:", e)

        # 3. Safe Bank Alert Scan
        try:
            textarea = page.locator("textarea").first
            if textarea.is_visible():
                textarea.fill("Dear SBI Customer, your A/C XX4921 has been debited by Rs. 850.00 on 23-Nov-2026 at POS Transaction. Available Balance: Rs. 24,150.00. - State Bank of India")
                page.wait_for_timeout(500)
                # Click Scan
                scan_btn = page.locator("button:has-text('Scan')").first
                scan_btn.click()
                page.wait_for_timeout(2000)

                path3 = os.path.join(ASSETS_DIR, "screenshot_3_safe_scan.png")
                page.screenshot(path=path3)
                print("Captured 3 (Safe Scan):", path3)
        except Exception as e:
            print("Error capturing Safe Scan:", e)

        # 4. Voice AI Assistant Tab
        try:
            voice_tab = page.locator("button:has-text('Voice AI')").first
            if voice_tab.is_visible():
                voice_tab.click()
                page.wait_for_timeout(2000)
                path4 = os.path.join(ASSETS_DIR, "screenshot_4_voice_assistant.png")
                page.screenshot(path=path4)
                print("Captured 4 (Voice AI):", path4)
        except Exception as e:
            print("Error capturing Voice AI:", e)

        # 5. Call Demo / Simulator Tab
        try:
            call_tab = page.locator("button:has-text('Call Demo')").first
            if call_tab.is_visible():
                call_tab.click()
                page.wait_for_timeout(2000)
                path5 = os.path.join(ASSETS_DIR, "screenshot_5_call_simulator.png")
                page.screenshot(path=path5)
                print("Captured 5 (Call Simulator):", path5)
        except Exception as e:
            print("Error capturing Call Simulator:", e)

        # 6. Zero-FIR Modal
        try:
            # Switch back to Scan Message tab or find 1930 button
            scan_tab = page.locator("button:has-text('Scan Message')").first
            if scan_tab.is_visible():
                scan_tab.click()
                page.wait_for_timeout(1000)
            
            # Find Draft 1930 Complaint button
            fir_btn = page.locator("button:has-text('1930')").first
            if fir_btn.is_visible():
                fir_btn.click()
                page.wait_for_timeout(1500)
                path6 = os.path.join(ASSETS_DIR, "screenshot_6_fir_modal.png")
                page.screenshot(path=path6)
                print("Captured 6 (1930 FIR Modal):", path6)
        except Exception as e:
            print("Error capturing FIR Modal:", e)

        browser.close()
        print("All screenshot captures complete!")

if __name__ == '__main__':
    capture_all()
