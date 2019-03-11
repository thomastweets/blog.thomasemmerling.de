Title: Setting up IPv6 with FritzBox 7530 and EdgeRouter Lite
Date: 2019-03-11
Modified: 2019-03-11
Category: Tech
Tags: IPv6, network, Ubiquiti, EdgeRouter Lite, EdgeOS, Fritzbox 7530, AVM, Double-NAT

I have been running a 'double NAT' setup for some years now: in the beginning because I had to due to my ISP regulations (yes, Ziggo.nl and plusnet, I am looking at you), nowadays as a deliberate choice to segment the network into ISP specific devices (mostly the SIP client) and my own network. On the WAN-facing side I am using a [FritzBox 7530](https://en.avm.de/products/fritzbox/fritzbox-7530/). Behind the FritzBox I use the almighty [EdgeRouter Lite](https://www.ui.com/edgemax/edgerouter-lite/) that gives you a full-fledged [Vyatta](https://en.wikipedia.org/wiki/Vyatta)-based router. However, with great power comes great responsibility so you have to do some digging if you want to configure certain features. Finally, I have a [Unifi AP AC Pro](https://www.ui.com/unifi/unifi-ap-ac-pro/) as my WiFi access point - very recommendable piece of hardware but not the star of this blog post.

Recently, I wanted to set up IPv6 again after having moved to a new place and a new ISP. This turned out to be a little longer journey and I decided to document it here, potentially for my future self ;)

---

Let's start with the FritzBox (sorry for the German menu item names; my FritzBox version does not let me change the language setting). First of all, backup your current configuration (```System```->```Sicherung```)! You obviously want to enable IPv6 at ```Internet``` -> ```Zugangsdaten``` -> ```IPv6```. Make sure that ```IPv6-Unterstützung aktiv``` is checked as well as (if your ISP still offers IPv4) ```Native IPv4-Anbindung verwenden```. ```DHCPv6 Rapid Commit verwenden``` should also be active. This should already give you an IPv6 address that you can see in ```Internet``` -> ```Online-Monitor```.

Next, you want to configure the announcing of IPv6 into the network and, therefore, towards the EdgeRouter. In ```Heimnetz```-> ```Netzwerk```->```Netzwerkeinstellungen``` scroll down and click on ```IPv6-Adressen```. Select ```Unique Local Addresses (ULA) zuweisen, solange keine IPv6-Internetverbindung besteht (empfohlen)```, deselect ```Auch IPv6-Präfixe zulassen, die andere IPv6-Router im Heimnetz bekanntgeben```, select ```Diese FRITZ!Box stellt den Standard-Internetzugang zur Verfügung```, and select ```DNSv6-Server auch über Router Advertisement bekanntgeben (RFC 5006)```.

Select ```DHCPv6-Server in der FRITZ!Box für das Heimnetz aktivieren:``` and ```DNS-Server, Präfix (IA_PD) und IPv6-Adresse (IA_NA) zuweisen``` (see also [here](https://web.nettworks.org/wiki/pages/viewpage.action?pageId=35651587) as a reference). Finally click ```OK```.

As the last step on the FritzBox, you want to expose the EdgeRouter. Go to ```Internet```->```Freigaben```->```Portfreigaben```. Click on ```Gerät für Freigaben hinzufügen```. Select the hostname of the EdgeRouter (e.g. ```ubnt```). Activate all checkmarks on this page (```Selbstständige Portfreigaben für dieses Gerät erlauben.```, ```Dieses Gerät komplett für den Internetzugriff über IPv4 freigeben (Exposed Host).```, ```PING6 freigeben.```, ```Firewall für delegierte IPv6-Präfixe dieses Gerätes öffnen.```, ```Dieses Gerät komplett für den Internetzugriff über IPv6 freigeben (Exposed Host).```). These settings will ensure that all IPv6 tests can pass making your network devices fully IPv6 compliant (see also [here](https://www.bjoerns-techblog.de/2017/06/ipv6-icmp-filtered-an-fritzbox-beheben/)) - and also completely exposed to the internet! So we will need to take care of configuring the firewall on the EdgeRouter.

---

On to the EdgeRouter Lite. A great set of helpful articles by Logan Marchione about setting up the EdgeRouter Lite can be found [here](https://loganmarchione.com/2016/04/ubiquiti-edgerouter-lite-setup/). Again, as a first step you should backup your configuration, either via the GUI or via SSH using ```show configuration commands```. Then, it is a good idea to start fresh an run the ```Basic Setup``` Wizard. Please note that this wipes your current configuration!

It is not necessary to set autoconf for IPv6 interfaces when IA_PD and IA_NA are served by the FritzBox (see above). You also do not need to explicitly set Router Advertisement (RA) when SLAAC is active on the WAN interface as the EdgeRouter is creating the RA automatically (see [here](https://community.ubnt.com/t5/EdgeRouter/IPv6-Setup/m-p/1833655/highlight/true#M150102) for a more detailed explanation). Finally, you need to set up a firewall rule to allow incoming ICMPv6 packages (see also [here](https://community.ubnt.com/t5/EdgeRouter/Filtered-ICMP-on-ipv6-test-com/m-p/2093368/highlight/true#M180948)).

As a reference, I am posting part of my configuration below (created with ```show configuration commands```). Please adapt to your needs before running it on your EdgeRouter.
```bash
set firewall all-ping enable
set firewall broadcast-ping disable
set firewall ipv6-name WANv6_IN default-action drop
set firewall ipv6-name WANv6_IN description 'WAN inbound traffic forwarded to LAN'
set firewall ipv6-name WANv6_IN enable-default-log
set firewall ipv6-name WANv6_IN rule 10 action accept
set firewall ipv6-name WANv6_IN rule 10 description 'Allow established/related sessions'
set firewall ipv6-name WANv6_IN rule 10 state established enable
set firewall ipv6-name WANv6_IN rule 10 state related enable
set firewall ipv6-name WANv6_IN rule 20 action drop
set firewall ipv6-name WANv6_IN rule 20 description 'Drop invalid state'
set firewall ipv6-name WANv6_IN rule 20 state invalid enable
set firewall ipv6-name WANv6_IN rule 30 action accept
set firewall ipv6-name WANv6_IN rule 30 description 'Allow IPv6 icmp'
set firewall ipv6-name WANv6_IN rule 30 protocol ipv6-icmp
set firewall ipv6-name WANv6_LOCAL default-action drop
set firewall ipv6-name WANv6_LOCAL description 'WAN inbound traffic to the router'
set firewall ipv6-name WANv6_LOCAL enable-default-log
set firewall ipv6-name WANv6_LOCAL rule 10 action accept
set firewall ipv6-name WANv6_LOCAL rule 10 description 'Allow established/related sessions'
set firewall ipv6-name WANv6_LOCAL rule 10 state established enable
set firewall ipv6-name WANv6_LOCAL rule 10 state related enable
set firewall ipv6-name WANv6_LOCAL rule 20 action drop
set firewall ipv6-name WANv6_LOCAL rule 20 description 'Drop invalid state'
set firewall ipv6-name WANv6_LOCAL rule 20 state invalid enable
set firewall ipv6-name WANv6_LOCAL rule 30 action accept
set firewall ipv6-name WANv6_LOCAL rule 30 description 'Allow IPv6 icmp'
set firewall ipv6-name WANv6_LOCAL rule 30 protocol ipv6-icmp
set firewall ipv6-name WANv6_LOCAL rule 40 action accept
set firewall ipv6-name WANv6_LOCAL rule 40 description 'allow dhcpv6'
set firewall ipv6-name WANv6_LOCAL rule 40 destination port 546
set firewall ipv6-name WANv6_LOCAL rule 40 protocol udp
set firewall ipv6-name WANv6_LOCAL rule 40 source port 547
set firewall ipv6-receive-redirects disable
set firewall ipv6-src-route disable
set firewall ip-src-route disable
set firewall log-martians enable
set firewall name WAN_IN default-action drop
set firewall name WAN_IN description 'WAN to internal'
set firewall name WAN_IN rule 10 action accept
set firewall name WAN_IN rule 10 description 'Allow established/related'
set firewall name WAN_IN rule 10 state established enable
set firewall name WAN_IN rule 10 state related enable
set firewall name WAN_IN rule 20 action drop
set firewall name WAN_IN rule 20 description 'Drop invalid state'
set firewall name WAN_IN rule 20 state invalid enable
set firewall name WAN_LOCAL default-action drop
set firewall name WAN_LOCAL description 'WAN to router'
set firewall name WAN_LOCAL rule 10 action accept
set firewall name WAN_LOCAL rule 10 description 'Allow established/related'
set firewall name WAN_LOCAL rule 10 state established enable
set firewall name WAN_LOCAL rule 10 state related enable
set firewall name WAN_LOCAL rule 20 action drop
set firewall name WAN_LOCAL rule 20 description 'Drop invalid state'
set firewall name WAN_LOCAL rule 20 state invalid enable
set firewall receive-redirects disable
set firewall send-redirects enable
set firewall source-validation disable
set firewall syn-cookies enable
set interfaces ethernet eth0 address dhcp
set interfaces ethernet eth0 description Internet
set interfaces ethernet eth0 dhcpv6-pd pd 0 interface eth1 host-address '::1'
set interfaces ethernet eth0 dhcpv6-pd pd 0 interface eth1 prefix-id ':1'
set interfaces ethernet eth0 dhcpv6-pd pd 0 interface eth1 service slaac
set interfaces ethernet eth0 dhcpv6-pd pd 0 interface eth2 host-address '::1'
set interfaces ethernet eth0 dhcpv6-pd pd 0 interface eth2 prefix-id ':2'
set interfaces ethernet eth0 dhcpv6-pd pd 0 interface eth2 service slaac
set interfaces ethernet eth0 dhcpv6-pd pd 0 prefix-length /60
set interfaces ethernet eth0 dhcpv6-pd rapid-commit enable
set interfaces ethernet eth0 duplex auto
set interfaces ethernet eth0 firewall in ipv6-name WANv6_IN
set interfaces ethernet eth0 firewall in name WAN_IN
set interfaces ethernet eth0 firewall local ipv6-name WANv6_LOCAL
set interfaces ethernet eth0 firewall local name WAN_LOCAL
set interfaces ethernet eth0 speed auto
set interfaces ethernet eth1 address 192.168.40.1/24
set interfaces ethernet eth1 description Local
set interfaces ethernet eth1 duplex auto
set interfaces ethernet eth1 speed auto
set interfaces ethernet eth2 address 192.168.2.1/24
set interfaces ethernet eth2 description 'Local 2'
set interfaces ethernet eth2 duplex auto
set interfaces ethernet eth2 speed auto
set interfaces loopback lo
set port-forward auto-firewall enable
set port-forward hairpin-nat enable
set port-forward lan-interface eth1
set port-forward wan-interface eth0
set service dhcp-server disabled false
set service dhcp-server hostfile-update disable
set service dhcp-server shared-network-name LAN1 authoritative enable
set service dhcp-server shared-network-name LAN1 subnet 192.168.40.0/24 default-router 192.168.40.1
set service dhcp-server shared-network-name LAN1 subnet 192.168.40.0/24 dns-server 192.168.40.1
set service dhcp-server shared-network-name LAN1 subnet 192.168.40.0/24 lease 86400
set service dhcp-server shared-network-name LAN1 subnet 192.168.40.0/24 start 192.168.40.20 stop 192.168.40.200
set service dhcp-server shared-network-name LAN2 authoritative enable
set service dhcp-server shared-network-name LAN2 subnet 192.168.2.0/24 default-router 192.168.2.1
set service dhcp-server shared-network-name LAN2 subnet 192.168.2.0/24 dns-server 192.168.2.1
set service dhcp-server shared-network-name LAN2 subnet 192.168.2.0/24 lease 86400
set service dhcp-server shared-network-name LAN2 subnet 192.168.2.0/24 start 192.168.2.38 stop 192.168.2.243
set service dhcp-server static-arp disable
set service dhcp-server use-dnsmasq disable
set service dns forwarding cache-size 150
set service dns forwarding listen-on eth1
set service dns forwarding listen-on eth2
set service gui http-port 80
set service gui https-port 443
set service gui older-ciphers enable
set service nat rule 5010 description 'masquerade for WAN'
set service nat rule 5010 outbound-interface eth0
set service nat rule 5010 type masquerade
set service ssh port 22
set service ssh protocol-version v2
set service unms disable
set system gateway-address 192.168.178.1
set system host-name ubnt
set system ntp server 0.ubnt.pool.ntp.org
set system ntp server 1.ubnt.pool.ntp.org
set system ntp server 2.ubnt.pool.ntp.org
set system ntp server 3.ubnt.pool.ntp.org
set system syslog global facility all level notice
set system syslog global facility protocols level debug
set system time-zone Europe/Berlin
```

I found some helpful commands for debugging in [this article](https://kazoo.ga/dhcpv6-pd-for-native-ipv6/) describing the IPv6 setup for the EdgeRouter Lite. Also a tcpdump command for ICMPv6 packets on the EdgeRouter itself can help a lot when debugging:
```bash
sudo tcpdump -n -i eth1 icmp6 and ip6[40]==133 or ip6[40]==134
```

If you made it this far you are hopefully ready to enjoy a full 20/20 score on [ipv6-test.com](http://ipv6-test.com/). Congratulations!
