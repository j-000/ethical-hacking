#!/usr/bin/env python3

import scapy.all as scapy
import optparse


def print_results(results_list):
    print('Devices connected on this network')
    print('IP \t\t\t MAC')
    for response in results_list:
        print('{} \t\t {}'.format(response.get('ip'), response.get('mac')))


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_bdc = broadcast/arp_request
    answered, unanswered = scapy.srp(arp_request_bdc, timeout=1, verbose=False)
    clients_list = []
    for (_, response) in answered:
        client_dict = {'ip': response.psrc, 'mac': response.hwsrc}
        clients_list.append(client_dict)
    print_results(clients_list)
    return clients_list


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-i', '--ip', dest='ip', help='IP address or range.')
    (options, args) = parser.parse_args()
    scan(options.ip)
