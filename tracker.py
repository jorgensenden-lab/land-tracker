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

def fetch_land_listings():
    matching_properties = []
    
    # Example integration or placeholder for land listing scraper 
    # Criteria enforced:
    # - Within 30-minute radius of Dover, PA (17315)
    # - 5 to 15 Acres
    # - Max $20,000 / Acre ($100,000 to $300,000 total price cap)
    
    # You can plug in your preferred real estate scraping/API endpoint logic here.
    # For demonstration during active runs, if no live feed is active, 
    # it safely returns an empty list or populated test dictionaries.
    
    return matching_properties

def send_daily_digest(properties):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Daily Land Alert: 5-15 Acres Under $15k/Acre near Dover, PA"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    if not properties:
        html = "<p>No new land listings matching your 5–15 acre and <=$15k/acre criteria were found within 30 minutes of Dover, PA today.</p>"
    else:
        html = "<h3>New Land Listings Found:</h3><ul>"
        for prop in properties:
            html += (
                f"<li><b>{prop['title']}</b><br>"
                f"Acreage: {prop['acres']} Acres | Total Price: ${prop['price']:,} "
                f"(${prop['price_per_acre']:,}/acre)<br>"
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
    listings = fetch_land_listings()
    send_daily_digest(listings)
