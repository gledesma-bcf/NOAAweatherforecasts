from playwright.sync_api import sync_playwright

url = "https://www.weather.gov/wrh/print?lat=36.769&lon=-119.7178"
output_file = "weather_forecast.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.pdf(path=output_file)
    browser.close()

print(f"✓ PDF saved: {output_file}")