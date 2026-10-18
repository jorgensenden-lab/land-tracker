import os
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration loaded securely from GitHub Repository Secrets
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECEIVER_EMAIL = "jorgensen.den@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Search Criteria Constants (No price limit applied)
MIN_ACRES = 5.0
MAX_ACRES = 15.0

def fetch_land_listings():
    matching_properties = []
    
    # Example integration or placeholder for land listing scraper / API
    # Criteria enforced:
    # - Within 30-minute radius of Dover, PA (17315)
    # - 5 to 15 Acres (All Prices)
    
    # Example structure for scraped or queried items:
    # {
    #     "title": "Example Land Parcel",
    #     "acres": 7.5,
    #     "price": 85000,
    #     "link": "https://example.com/listing"
    # }
    
    return matching_properties

def filter_listings(raw_properties):
    matching_properties = []
    for prop in raw_properties:
        acres = prop.get('acres', 0)
        
        # Only check the acreage criteria; no price ceiling applied
        if MIN_ACRES <= acres <= MAX_ACRES:
            matching_properties.append(prop)
                
    return matching_properties

def send_daily_digest(properties):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Daily Land Alert: 5-15 Acres near Dover, PA (All Prices)"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    if not properties:
        html = "<p>No new land listings matching your 5–15 acre criteria (All Prices) were found within 30 minutes of Dover, PA today.</p>"
    else:
        html = "<h3>New Land Listings Found:</h3><ul>"
        for prop in properties:
            price_val = prop.get('price', 0)
            html += (
                f"<li><b>{prop['title']}</b><br>"
                f"Acreage: {prop['acres']} Acres | Total Price: ${price_val:,}<br>"
                f"<a href='{prop['link']}'>View Listing</a></li><br>"
            )
        html += "</ul>"

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Daily land alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    raw_listings = fetch_land_listings()
    listings = filter_listings(raw_listings)
    send_daily_digest(listings)
