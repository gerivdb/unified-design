#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MDU Notify — Notifications Discord/Slack/Email pour l'orchestration MDU.

Usage:
    python mdu_notify.py --report /tmp/report.md --channels discord,slack
    python mdu_notify.py --message "MDU Orchestration completed" --channels discord
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from typing: Optional


class MDU_Notifier:
    """Gestionnaire de notifications multi-canaux."""
    
    def __init__(self):
        self.webhooks = {
            "discord": os.environ.get("MDU_DISCORD_WEBHOOK"),
            "slack": os.environ.get("MDU_SLACK_WEBHOOK"),
        }
        self.email_config = {
            "smtp_server": os.environ.get("MDU_SMTP_SERVER"),
            "smtp_port": int(os.environ.get("MDU_SMTP_PORT", "587")),
            "username": os.environ.get("MDU_SMTP_USER"),
            "password": os.environ.get("MDU_SMTP_PASS"),
            "from": os.environ.get("MDU_EMAIL_FROM"),
            "to": os.environ.get("MDU_EMAIL_TO", "").split(",") if os.environ.get("MDU_EMAIL_TO") else [],
        }
    
    def send_discord(self, message: str, report_path: Optional[Path] = None) -> bool:
        """Envoie notification Discord via webhook."""
        webhook = self.webhooks.get("discord")
        if not webhook:
            print("[NOTIFY] Discord webhook not configured")
            return False
        
        try:
            import requests
            
            payload = {
                "content": message[:2000],  # Discord limit
                "username": "MDU Orchestration",
                "avatar_url": "https://raw.githubusercontent.com/gerivdb/unified-design/main/docs/assets/mdu-logo.png",
            }
            
            if report_path and report_path.exists():
                # Ajouter le rapport comme fichier si possible (Discord limite 8MB)
                file_size = report_path.stat().st_size
                if file_size < 8_000_000:
                    with report_path.open("rb") as f:
                        files = {"file": (report_path.name, f, "text/markdown")}
                        response = requests.post(webhook, data={"payload_json": json.dumps(payload)}, files=files, timeout=10)
                else:
                    response = requests.post(webhook, json=payload, timeout=10)
            else:
                response = requests.post(webhook, json=payload, timeout=10)
            
            response.raise_for_status()
            print("[NOTIFY] Discord notification sent")
            return True
            
        except Exception as e:
            print(f"[NOTIFY] Discord error: {e}")
            return False
    
    def send_slack(self, message: str, report_path: Optional[Path] = None) -> bool:
        """Envoie notification Slack via webhook."""
        webhook = self.webhooks.get("slack")
        if not webhook:
            print("[NOTIFY] Slack webhook not configured")
            return False
        
        try:
            import requests
            
            payload = {
                "text": message,
                "username": "MDU Orchestration",
                "icon_emoji": ":gear:",
            }
            
            response = requests.post(webhook, json=payload, timeout=10)
            response.raise_for_status()
            print("[NOTIFY] Slack notification sent")
            return True
            
        except Exception as e:
            print(f"[NOTIFY] Slack error: {e}")
            return False
    
    def send_email(self, subject: str, body: str, report_path: Optional[Path] = None) -> bool:
        """Envoie notification Email via SMTP."""
        if not all([self.email_config["smtp_server"], self.email_config["username"], 
                    self.email_config["password"], self.email_config["from"], self.email_config["to"]]):
            print("[NOTIFY] Email not fully configured")
            return False
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.mime.application import MIMEApplication
            
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = self.email_config["from"]
            msg["To"] = ", ".join(self.email_config["to"])
            
            msg.attach(MIMEText(body, "plain"))
            
            if report_path and report_path.exists():
                with report_path.open("rb") as f:
                    part = MIMEApplication(f.read(), Name=report_path.name)
                    part["Content-Disposition"] = f'attachment; filename="{report_path.name}"'
                    msg.attach(part)
            
            with smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"]) as server:
                server.starttls()
                server.login(self.email_config["username"], self.email_config["password"])
                server.send_message(msg)
            
            print("[NOTIFY] Email sent")
            return True
            
        except Exception as e:
            print(f"[NOTIFY] Email error: {e}")
            return False
    
    def notify(self, message: str, channels: list[str], report_path: Optional[Path] = None, 
               subject: str = "MDU Orchestration Notification") -> dict[str, bool]:
        """Envoie notification sur les canaux spécifiés."""
        results = {}
        
        for channel in channels:
            if channel == "discord":
                results["discord"] = self.send_discord(message, report_path)
            elif channel == "slack":
                results["slack"] = self.send_slack(message, report_path)
            elif channel == "email":
                results["email"] = self.send_email(subject, message, report_path)
            else:
                print(f"[NOTIFY] Unknown channel: {channel}")
                results[channel] = False
        
        return results


def main():
    parser = argparse.ArgumentParser(description="MDU Orchestration Notifier")
    parser.add_argument("--message", help="Message to send")
    parser.add_argument("--report", type=Path, help="Path to report file to attach")
    parser.add_argument("--channels", default="discord,slack", help="Comma-separated channels (discord,slack,email)")
    parser.add_argument("--subject", default="MDU Orchestration Notification", help="Email subject")
    args = parser.parse_args()
    
    if not args.message and not args.report:
        print("Error: --message or --report required")
        return 1
    
    message = args.message or f"MDU Orchestration report: {args.report.name if args.report else 'N/A'}"
    channels = [c.strip() for c in args.channels.split(",") if c.strip()]
    
    notifier = MDU_Notifier()
    results = notifier.notify(message, channels, args.report, args.subject)
    
    print("[NOTIFY] Results:")
    for channel, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {channel}: {status}")
    
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())