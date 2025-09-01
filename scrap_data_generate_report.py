import requests
from bs4 import BeautifulSoup
import pandas as pd

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email_with_attachment(
    sender, recipient, subject, body, file_path, smtp_server, port, username, password
):
    try:
        # Create email
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject

        # Attach body
        msg.attach(MIMEText(body, "plain"))

        # Attach file if provided
        if file_path and os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file_path)}",
            )
            msg.attach(part)

        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(username, password)

        # Send email
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()

        print("✅ Email with attachment sent successfully!")
    except Exception as e:
        print("❌ Failed to send email")
        print("Error:", e)


def setup():
    # Gmail settings
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "masterarpit@gmail.com"
    smtp_pass = "AAAA BBBB CCCC DDDD"  # <-- Use the 16-char App Password

    # Email details
    from_email = smtp_user
    to_email = "priyankarinki86@gmail.com"
    subject = "Books List"
    body = "Hello!\n\nPlease find the list of books in the attache document."

    # File to attach (change path to your file)
    attachment_file = r"books.xlsx"

    send_email_with_attachment(
        from_email,
        to_email,
        subject,
        body,
        attachment_file,
        smtp_host,
        smtp_port,
        smtp_user,
        smtp_pass,
    )


if __name__ == "__main__":
    current = 1
    all_books = []

    while True:
        res = requests.get(f"http://books.toscrape.com/catalogue/page-{current}.html")
        print(res.status_code)
        soup = BeautifulSoup(res.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")
        if not books:
            break

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text[2:]
            rating = book.p["class"][1]
            availability = book.select_one("p.instock.availability").get_text(
                strip=True
            )

            all_books.append(
                {
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Availability": availability,
                }
            )
        print(all_books)
        current = soup.select("li.current")[0].get_text(strip=True).split()[1]
        current = int(current) + 1

    df = pd.DataFrame(all_books)
    df.to_excel("books.xlsx", index=False)
    print("Data saved to books.xlsx")

    setup()
