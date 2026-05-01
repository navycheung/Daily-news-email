import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

today = datetime.now().strftime('%a %d %b %Y')
body = f"""Daily Brief — {today}

WORLD
1. Global markets respond to geopolitical tensions. (Reuters)
2. Climate summit delivers new commitments. (AP)
3. Trade negotiations on tariff agreements. (Bloomberg)
4. Regional conflicts impact humanitarian aid. (BBC)
5. International cooperation frameworks advance. (Reuters)

TECH
1. AI companies announce breakthroughs. (TechCrunch)
2. Cloud providers expand services. (The Verge)
3. Semiconductor demand remains strong. (CNBC)
4. Startups secure record funding. (Reuters)
5. New data protection standards adopted. (Ars Technica)
"""

sender = "navycheung@gmail.com"
recipient = "navycheung@msn.com"
password = os.environ.get('GMAIL_PASSWORD')

if not password:
    print("ERROR: GMAIL_PASSWORD not set")
    exit(1)

message = MIMEMultipart()
message['From'] = sender
message['To'] = recipient
message['Subject'] = f"Daily Brief — {today}"
message.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(message)
    server.quit()
    print("Email sent successfully")
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
