import os
import django
from pathlib import Path

# Load environment
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings


def test_smtp():
    user = getattr(settings, 'EMAIL_HOST_USER', '')
    pwd = getattr(settings, 'EMAIL_HOST_PASSWORD', '')

    print("=" * 60)
    print("   CareerPulse - Gmail SMTP Real Email Delivery Tester")
    print("=" * 60)
    print(f"Configured Email Address: {user}")
    print(f"Backend in use: {settings.EMAIL_BACKEND}")

    if not pwd:
        print("\n[!] EMAIL_HOST_PASSWORD is currently empty in .env!")
        print("\nTo activate real Gmail delivery in 60 seconds:")
        print("  1. Go to: https://myaccount.google.com/security")
        print("  2. Turn on '2-Step Verification' if not already on.")
        print("  3. Search for 'App passwords' (or go to https://myaccount.google.com/apppasswords).")
        print("  4. Name it 'CareerPulse' and click Create.")
        print("  5. Copy the 16-character code (e.g. 'abcd efgh ijkl mnop').")
        print("  6. Open your .env file and paste it in EMAIL_HOST_PASSWORD=...")
        print("  7. Re-run: python test_gmail_smtp.py\n")
        return False

    print("\nAttempting to connect to smtp.gmail.com:587 and send test email...")
    try:
        sent = send_mail(
            subject="[CareerPulse] Real Gmail SMTP Verified & Working!",
            message=(
                f"Hello Kavya,\n\n"
                f"Congratulations! Your CareerPulse Job Portal is now connected to real Gmail SMTP!\n\n"
                f"From now on, whenever:\n"
                f"  - A candidate applies to any job -> Confirmation email is sent.\n"
                f"  - A recruiter shortlists a resume -> 'Your resume is shortlisted' email is sent.\n\n"
                f"Sender: {settings.DEFAULT_FROM_EMAIL}\n"
                f"Recipient: {user}\n\n"
                f"CareerPulse Portal Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user],
            fail_silently=False,
        )
        if sent:
            print("\n[SUCCESS] Test email was sent successfully to", user)
            print("Check your Gmail inbox (and Spam/Promotions folder) now!")
            return True
        else:
            print("\n[!] Send returned 0. Check your settings.")
            return False
    except Exception as e:
        print(f"\n[ERROR] Failed to send email: {e}")
        print("\nCommon reasons:")
        print("  1. Did you use your normal Gmail password? Google requires an App Password.")
        print("  2. App Password should be 16 characters without spaces.")
        return False


if __name__ == '__main__':
    test_smtp()
