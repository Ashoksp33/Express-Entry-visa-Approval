"""
CanVisa Decision Support System - Authentication & Email OTP Service
Supports secure 6-digit OTP generation, time-based expiration (10 minutes),
attempt limiting, and real email delivery via SMTP (Gmail, Outlook, Yahoo, Custom).
"""

import os
import time
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

# In-memory store for active OTP codes:
# email -> {"otp": "123456", "expires_at": timestamp, "attempts": 0}
OTP_STORE: Dict[str, Dict[str, Any]] = {}

OTP_EXPIRY_SECONDS = 600  # 10 minutes
MAX_ATTEMPTS = 5

def load_env_file():
    """
    Loads environment variables from .env file in project root if present.
    """
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        key = key.strip()
                        if "#" in val and not (val.startswith('"') or val.startswith("'")):
                            val = val.split("#", 1)[0]
                        val = val.strip().strip("\"'")
                        os.environ[key] = val
        except Exception as e:
            print(f"[CanVisa Auth] Warning reading .env: {e}")

load_env_file()


def get_smtp_config():
    """
    Returns SMTP configuration with intelligent auto-detection for popular email providers.
    """
    load_env_file()
    smtp_user = os.environ.get("SMTP_USER", "").strip()
    smtp_pass = os.environ.get("SMTP_PASSWORD", "").strip()
    smtp_host = os.environ.get("SMTP_HOST", "").strip()
    smtp_port_raw = os.environ.get("SMTP_PORT", "").strip()
    sender_email = os.environ.get("SMTP_FROM", smtp_user or "noreply@canvisa.app").strip()

    lower_user = smtp_user.lower()
    # Remove whitespace from Gmail App Passwords (Google presents them as 4x4 with spaces)
    if "@gmail.com" in lower_user or "smtp.gmail.com" in smtp_host.lower():
        smtp_pass = smtp_pass.replace(" ", "")

    # Intelligent provider auto-detection if host is not specified
    if smtp_user and not smtp_host:
        if "@gmail.com" in lower_user:
            smtp_host = "smtp.gmail.com"
            smtp_port_raw = smtp_port_raw or "587"
        elif "@outlook.com" in lower_user or "@hotmail.com" in lower_user or "@live.com" in lower_user:
            smtp_host = "smtp.office365.com"
            smtp_port_raw = smtp_port_raw or "587"
        elif "@yahoo.com" in lower_user:
            smtp_host = "smtp.mail.yahoo.com"
            smtp_port_raw = smtp_port_raw or "587"

    smtp_port = int(smtp_port_raw) if smtp_port_raw.isdigit() else 587

    return {
        "host": smtp_host,
        "port": smtp_port,
        "user": smtp_user,
        "password": smtp_pass,
        "sender": sender_email,
        "is_configured": bool(smtp_host and smtp_user and smtp_pass)
    }


def send_email_via_smtp(to_email: str, otp_code: str) -> Dict[str, Any]:
    """
    Attempts to send OTP email via SMTP to a real inbox.
    Returns {"success": bool, "error": str | None}.
    """
    cfg = get_smtp_config()

    if not cfg["is_configured"]:
        return {
            "success": False,
            "error": "SMTP credentials are not yet configured in .env file (SMTP_USER and SMTP_PASSWORD required)."
        }

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Your CanVisa Verification Code: {otp_code}"
        msg["From"] = f"CanVisa Global <{cfg['sender']}>"
        msg["To"] = to_email

        text_body = (
            f"Hello,\n\n"
            f"Your one-time verification code (OTP) for CanVisa is:\n\n"
            f"  {otp_code}\n\n"
            f"This code will expire in 10 minutes. If you did not request this login code, please ignore this message.\n\n"
            f"Best regards,\n"
            f"CanVisa Decision Support System"
        )

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0b1329; color: #f1f5f9; padding: 24px 12px; margin: 0; }}
            .container {{ max-width: 520px; margin: 0 auto; background: #0f1c3d; border: 1px solid #1e3a8a; border-radius: 16px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            .brand {{ font-size: 19px; font-weight: 800; letter-spacing: 2px; color: #38bdf8; text-transform: uppercase; margin-bottom: 24px; }}
            .title {{ font-size: 20px; font-weight: 700; color: #ffffff; margin-bottom: 12px; }}
            .desc {{ font-size: 14.5px; color: #cbd5e1; line-height: 1.55; margin-bottom: 20px; }}
            .otp-box {{ background: linear-gradient(135deg, rgba(37,99,235,0.22), rgba(6,182,212,0.22)); border: 2px dashed #38bdf8; border-radius: 14px; padding: 20px; text-align: center; margin: 24px 0; }}
            .otp-code {{ font-size: 36px; font-weight: 800; letter-spacing: 10px; color: #38bdf8; font-family: Consolas, monospace; }}
            .expire-note {{ font-size: 12.5px; color: #f59e0b; margin-top: 10px; font-weight: 600; }}
            .footer {{ font-size: 12px; color: #64748b; margin-top: 28px; border-top: 1px solid #1e293b; padding-top: 16px; text-align: center; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="brand">🍁 CANVISA DECISION SYSTEM</div>
            <div class="title">Your Login Verification Code</div>
            <p class="desc">You requested to sign in to the CanVisa Decision Support System. Use the 6-digit code below to verify your email address:</p>
            <div class="otp-box">
              <div class="otp-code">{otp_code}</div>
              <div class="expire-note">⏱ Code expires in 10 minutes</div>
            </div>
            <p class="desc">If you did not initiate this sign-in request, you can safely ignore this email.</p>
            <div class="footer">🔒 Secure Session Verification • CanVisa Global Support</div>
          </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        if cfg["port"] == 465:
            # SSL Connection
            with smtplib.SMTP_SSL(cfg["host"], cfg["port"], timeout=14) as server:
                server.login(cfg["user"], cfg["password"])
                server.sendmail(cfg["sender"], to_email, msg.as_string())
        else:
            # STARTTLS Connection (port 587)
            with smtplib.SMTP(cfg["host"], cfg["port"], timeout=14) as server:
                server.starttls()
                server.login(cfg["user"], cfg["password"])
                server.sendmail(cfg["sender"], to_email, msg.as_string())

        print(f"[CanVisa Auth] [OK] Email delivered successfully via SMTP to {to_email}")
        return {"success": True, "error": None}

    except (smtplib.SMTPAuthenticationError, smtplib.SMTPServerDisconnected) as auth_err:
        err_msg = (
            f"Gmail SMTP rejected credentials (535 Bad Credentials / connection closed). "
            f"The Google App Password in .env is invalid or revoked. "
            f"Please generate a fresh 16-character App Password at https://myaccount.google.com/apppasswords"
        )
        print(f"[CanVisa Auth] [AUTH ERROR] {err_msg} ({auth_err})")
        return {"success": False, "error": err_msg}

    except Exception as err:
        err_msg = f"Failed to deliver email via SMTP ({err})"
        print(f"[CanVisa Auth] [ERROR] {err_msg}")
        return {"success": False, "error": err_msg}


def request_otp(email: str) -> Dict[str, Any]:
    """
    Generates a fresh 6-digit OTP, stores it with expiration, and sends it to the real inbox.
    """
    clean_email = email.strip().lower()
    if not clean_email or "@" not in clean_email:
        return {"success": False, "message": "Please provide a valid email address."}

    # Generate secure 6-digit OTP code (100000 - 999999)
    code = str(secrets.randbelow(900000) + 100000)
    now = time.time()

    OTP_STORE[clean_email] = {
        "otp": code,
        "expires_at": now + OTP_EXPIRY_SECONDS,
        "attempts": 0
    }

    # Dispatch real email to user's inbox
    delivery_res = send_email_via_smtp(clean_email, code)
    sent_smtp = delivery_res["success"]

    # Server console audit log
    print(f"\n==================================================")
    print(f"[CanVisa Auth OTP] Target: {clean_email}")
    print(f"[CanVisa Auth OTP] Code:   {code}")
    print(f"[CanVisa Auth OTP] Expiry: 10 minutes ({int(OTP_EXPIRY_SECONDS)}s)")
    print(f"[CanVisa Auth OTP] Status: {'Delivered to Mailbox' if sent_smtp else 'SMTP Delivery Failed (Demo Fallback Active)'}")
    if delivery_res.get("error"):
        print(f"[CanVisa Auth OTP] Error:  {delivery_res['error']}")
    print(f"==================================================\n")

    cfg = get_smtp_config()

    if sent_smtp:
        return {
            "success": True,
            "message": f"A 6-digit verification code has been sent to your email ({clean_email}). Please check your inbox or spam folder.",
            "email": clean_email,
            "expires_in": OTP_EXPIRY_SECONDS,
            "smtp_delivered": True
        }
    else:
        err = delivery_res.get("error") or "SMTP email service is not configured."
        return {
            "success": True,
            "message": "Verification code generated successfully.",
            "email": clean_email,
            "expires_in": OTP_EXPIRY_SECONDS,
            "smtp_delivered": False,
            "smtp_error": err,
            "dev_otp": code
        }


def verify_otp(email: str, entered_otp: str) -> Dict[str, Any]:
    """
    Verifies user-provided OTP code against stored active record sent to their email.
    """
    clean_email = email.strip().lower()
    clean_otp = entered_otp.strip()

    if not clean_email or not clean_otp:
        return {"success": False, "message": "Email and OTP code are required."}

    record = OTP_STORE.get(clean_email)
    if not record:
        return {
            "success": False,
            "message": "No verification code requested for this email. Please click 'Send OTP' first."
        }

    now = time.time()
    if now > record["expires_at"]:
        OTP_STORE.pop(clean_email, None)
        return {
            "success": False,
            "message": "Verification code has expired. Please request a new OTP."
        }

    if record["attempts"] >= MAX_ATTEMPTS:
        OTP_STORE.pop(clean_email, None)
        return {
            "success": False,
            "message": "Too many failed attempts. Please request a fresh OTP."
        }

    if record["otp"] != clean_otp:
        record["attempts"] += 1
        remaining = MAX_ATTEMPTS - record["attempts"]
        return {
            "success": False,
            "message": f"Invalid verification code. {remaining} attempt(s) remaining."
        }

    # OTP is verified! Consume it so it cannot be re-used
    OTP_STORE.pop(clean_email, None)

    token = f"jwt_{secrets.token_hex(16)}"
    return {
        "success": True,
        "message": "Email verified successfully!",
        "email": clean_email,
        "token": token
    }
