#!/usr/bin/env python3
import optparse
import subprocess
import re


def get_current_mac(interface):
    mac_regex = re.compile(r'(?si)(?:(?:\w{2})[:-]){5}\w{2}')
    ifconfig_output = str(subprocess.check_output(['ifconfig', interface]))
    mac_value_search_result = mac_regex.search(ifconfig_output)
    if mac_value_search_result:
        return mac_value_search_result.group()
    return None


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface to change its MAC address.')
    parser.add_option('-m', '--mac', dest='new_mac', help='New MAC value.')
    (opts, _) = parser.parse_args()
    if not opts.interface:
        parser.error('[-] - Missing -i/--interface parameter.')
    elif not opts.new_mac:
        parser.error('[-] - Missing -m/--mac parameter.')
    else:
        return opts


def change_mac(interface, new_mac):
    old_mac_value_set = get_current_mac(interface)
    print('[+] Changing MAC address from {} to {}'.format(old_mac_value_set, new_mac))
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])
    new_mac_value = get_current_mac(interface)
    if new_mac_value:
        if new_mac_value != new_mac:
            print('[!] ** CAUTION ** MAC address NOT changed')
        else:
            print('[+] MAC value is {}'.format(new_mac_value))
    else:
        print('[-] No MAC address found in "ifconfig {}"'.format(interface))


if __name__ == '__main__':
    options = get_arguments()
    change_mac(options.interface, options.new_mac)
