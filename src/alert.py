import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()


def send_alert(city, aqi, label):
    sender = os.getenv("ALERT_EMAIL")
    password = os.getenv("ALERT_PASSWORD")
    receiver = os.getenv("ALERT_EMAIL")

    if not sender or not password:
        logger.warning("Email credentials not set — skipping alert")
        return

    subject = f"⚠️ AQI Alert — {city} has reached {aqi} ({label})"

    body = f"""
    🚨 Air Quality Alert

    City: {city}
    AQI Index: {aqi}
    Category: {label}

    This city has crossed the danger threshold of 200.
    Please take necessary precautions.

    — India AQI Pipeline
    """

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        logger.info(f"Alert sent for {city} — AQI {aqi}")
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")


def check_and_alert(df):
    dangerous = df[df["aqi_index"] > 200]
    if len(dangerous) > 0:
        logger.info(f"Found {len(dangerous)} cities above danger threshold")
        for _, row in dangerous.iterrows():
            send_alert(row["city"], row["aqi_index"], row["air_quality_label"])
    else:
        logger.info("All cities below danger threshold — no alerts needed")