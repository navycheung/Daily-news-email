import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

try:
    from googletrans import Translator
except:
    os.system('pip install google-trans-new')
    from googletrans import Translator

today = datetime.now().strftime('%a %d %b %Y')

# Longer news summaries in English
body_en = f"""Daily Brief — {today}

WORLD
1. Global markets respond to geopolitical tensions as major economies implement new trade restrictions. Investors remain cautious amid escalating international disputes, while central banks consider policy adjustments to stabilize financial conditions and support economic growth in uncertain times.

2. The United Nations Climate Summit delivered significant commitments on emissions reductions from over 190 nations. Countries pledged to accelerate their transition to renewable energy and increase climate finance for developing nations, marking a substantial step forward in global environmental cooperation and sustainability efforts.

3. International trade negotiations between major economic powers continue on tariff agreements and market access. Diplomats from Asia, Europe, and North America are working to establish fairer trade frameworks that balance economic interests while promoting long-term stability in global commerce.

4. Regional humanitarian crises impact aid distribution across conflict-affected areas, with international organizations struggling to reach vulnerable populations. The situation demands urgent coordination between governments, NGOs, and UN agencies to ensure critical supplies reach those in need.

5. International security frameworks are being strengthened to address emerging cyber threats and transnational challenges. Countries are collaborating on intelligence sharing and coordinated defense strategies to protect critical infrastructure and citizens from evolving security risks.

TECH
1. Major AI companies announced groundbreaking advances in large language models with improved efficiency and reasoning capabilities. These new models demonstrate superior performance in complex problem-solving tasks while consuming significantly less computational resources, promising more accessible AI technology for businesses and individuals worldwide.

2. Cloud service providers have unveiled enhanced security features and expanded global infrastructure to support enterprise clients. New compliance certifications and disaster recovery capabilities are helping organizations meet regulatory requirements while improving data protection and business continuity across multiple regions.

3. The semiconductor industry reports strong demand for advanced chips as companies invest heavily in AI infrastructure and data centers. Supply chains have stabilized significantly, though
