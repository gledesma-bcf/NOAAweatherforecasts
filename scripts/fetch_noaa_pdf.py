from playwright.sync_api import sync_playwright
from datetime import datetime
import os

# Add all your NOAA weather URLs with custom names here
urls = [
    {"name": "Fresno Airport", "url": "https://www.weather.gov/wrh/print?lat=36.769&lon=-119.7178"},
    {"name": "Fresno State", "url": "https://www.weather.gov/wrh/print?lat=36.8092&lon=-119.7530"},
    {"name": "COS Visalia", "url": "https://www.weather.gov/wrh/print?lat=36.3217&lon=-119.3147"},
    {"name": "Los Banos HS", "url": "https://www.weather.gov/wrh/print?lat=37.0509&lon=-120.8408"},
    {"name": "Mendota USD Office", "url": "https://www.weather.gov/wrh/print?lat=36.7622&lon=-120.3885"},
    {"name": "Justin Garza HS", "url": "https://www.weather.gov/wrh/print?lat=36.7986&lon=-119.9154"},
    {"name": "Fresno Airport Rain Gauge", "url": "https://forecast.weather.gov/data/obhistory/KFAT.html"}
    # Add more like this:
    # {"name": "Your Location", "url": "https://www.weather.gov/wrh/print?lat=37.000&lon=-120.000"},
]

try:
    print(f"[{datetime.now()}] Starting NOAA weather PDF generation...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for i, location in enumerate(urls, 1):
            location_name = location["name"]
            url = location["url"]
            output_file = f"weather_forecast_{location_name}.pdf"
            
            try:
                page = browser.new_page()
                
                print(f"[{datetime.now()}] Fetching webpage {i}/{len(urls)}: {location_name}")
                page.goto(url, wait_until="networkidle")
                
                print(f"[{datetime.now()}] Converting to PDF (landscape)...")
                page.pdf(
                    path=output_file,
                    landscape=True
                )
                page.close()
                
                # Verify file was created
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    print(f"[{datetime.now()}] ✓ PDF saved: {output_file} ({file_size} bytes)")
                else:
                    raise Exception(f"PDF file {output_file} was not created")
                    
            except Exception as e:
                print(f"[{datetime.now()}] ✗ Error processing {location_name}: {str(e)}")
        
        browser.close()
        print(f"[{datetime.now()}] ✓ All PDFs generated successfully!")
        
except Exception as e:
    print(f"[{datetime.now()}] ✗ Fatal error: {str(e)}")
    raise
