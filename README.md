# Docker-Lab – Dockerized Pentesting Lab
<pre>
🔎 Overview
Docker-based vulnerable pentesting lab that simulates a realistic web application and system misconfiguration scenario. The lab is designed to demonstrate how web-level weaknesses, insecure automation, and poor privilege management can be chained together to achieve full system compromise.

🎯 Lab Objective
Identify vulnerabilities in a live web application
Exploit insecure automation and cron jobs
Perform lateral movement between users

Escalate privileges to root
Understand both attacker techniques and defensive mistakes

🧨 Attack Surface Summary
User-controlled URL submission in web application
Admin bot visiting attacker-supplied URLs
Group-writable cron-executed Python script
Password-less sudo configuration for vim

🛠️ Technology & Attack Chain
Web Stack: Apache + PHP + MySQL
Automation Abuse: Cron jobs (user & root)
Initial Access: Web exploitation → credential capture
Lateral Movement: SSH access

Privilege Escalation: Cron abuse + sudo misconfiguration

⚙️ Installation & Setup

git clone https://github.com/<your-username>/Docker-Lab.git
cd Docker-Lab
docker build -t vuln-lab .
docker run -d -p 80:80 -p 22:22 --name lab1 vuln-lab </pre>
