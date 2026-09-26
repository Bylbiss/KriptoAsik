import smtplib
from email.mime.text import MIMEText

# Konfigurasi Akun Pengirim (Gunakan App Password dari Google Account)
SENDER_EMAIL = "email_kamu@gmail.com"  # Ganti dengan email pengirim
SENDER_PASSWORD = (
    "xxxx xxxx xxxx xxxx"  # Ganti Password Gmail 16 digit
)


def send_otp_email(recipient_email, otp_key, text_length):
    """
    Mengirim kunci Vernam (OTP) ke Gmail penerima.
    """
    subject = "🔑 KUNCI OTP VERNAM CIPHER (SANGAT RAHASIA)"
    body = f"""
    Halo,

    Berikut adalah Kunci OTP (One-Time Pad) Vernam Cipher Anda:

    🔑 KUNCI OTP : {otp_key}
    📏 PANJANG   : {text_length} karakter

    ⚠️ PERHATIAN:
    - Kunci ini HANYA BISA DIPAKAI 1 KALI untuk proses Dekripsi.
    - Setelah digunakan, kunci ini akan otomatis HANGUS / DIHAPUS oleh sistem.

    Salam,
    Tim KriptoAsik
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        return True, "Email OTP berhasil dikirim!"
    except Exception as e:
        return False, f"Gagal mengirim email: {str(e)}"