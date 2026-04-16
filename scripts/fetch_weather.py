import subprocess
from pathlib import Path

# Install browser for Playwright
subprocess.run(["playwright", "install", "chromium"], check=True)

from playwright.sync_api import sync_playwright
from onedrive_integration import upload_to_onedrive  # You'll need this

def save_webpage_as_pdf(url, pdf_filename):
    """Convert a webpage to PDF using Playwright"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.pdf(path=pdf_filename)
        browser.close()
    print(f"✓ Saved: {pdf_filename}")

# Example usage
# save_webpage_as_pdf("https://weather.gov", "weather_page.pdf")