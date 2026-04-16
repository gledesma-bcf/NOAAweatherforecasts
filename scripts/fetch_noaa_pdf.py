from playwright.sync_api import sync_playwright
from datetime import datetime
import os

url = "https://www.weather.gov/wrh/print?lat=36.769&lon=-119.7178"
output_file = "weather_forecast.pdf"

try:
    print(f"[{datetime.now()}] Starting NOAA weather PDF generation...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        print(f"[{datetime.now()}] Fetching webpage: {url}")
        page.goto(url, wait_until="networkidle")
        
        print(f"[{datetime.now()}] Converting to PDF...")
        page.pdf(path=output_file)
        browser.close()
    
    # Verify file was created
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"[{datetime.now()}] ✓ PDF saved: {output_file} ({file_size} bytes)")
    else:
        raise Exception("PDF file was not created")
        
except Exception as e:
    print(f"[{datetime.now()}] ✗ Error: {str(e)}")
    raise