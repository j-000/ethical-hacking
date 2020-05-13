#!/usr/bin/env python
import os
import netfilterqueue
import argparse


# Ensure we can import scapy
os.sys.path += ['/home/kali/.local/lib/python2.7/site-packages']
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print('[HTTP Req.]')
            if extension in scapy_packet[scapy.RAW].load:
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print('[HTTP Resp.]')
            print(scapy_packet.show())
    packet.accept()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-t', dest='target_website', help='Website address to spoof.', required=True)
    # parser.add_argument('-r', dest='redirect_ip', help='Redirect IP address.', required=True)
    # args = parser.parse_args()
    # target_website = args.target_website
    # redirect_ip = args.redirect_ip
    extension = '.exe'
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)  # 0 is the identifiable number passed as --queue-num param
    queue.run()

