# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

today = datetime.now().strftime('%a %d %b %Y')

# Traditional Chinese news briefing - using concatenation instead of f-string
body = "每日簡報 — " + today + """

世界新聞
1. 全球市場應對地緣政治緊張局勢，各大經濟體實施新的貿易限制措施。投資者對國際爭端升級保持謹慎態度，各國央行考慮調整政策以穩定金融狀況。

2. 聯合國氣候峰會已從190多個國家獲得重大減排承諾。各國承諾加快向可再生能源轉變並增加對發展中國家的氣候融資，在全球環境合作上取得重大進展。

3. 主要經濟體之間繼續進行國際貿易談判，協商關稅協議和市場準入。來自亞洲、歐洲和北美的外交官正在努力建立公平的貿易框架。

4. 地區人道主義危機影響衝突地區的援助分配，國際組織難以接觸易受傷害的人群。需要政府、非政府組織和聯合國機構之間的緊急協調。

5. 國
