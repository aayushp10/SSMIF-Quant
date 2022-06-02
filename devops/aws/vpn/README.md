# vpn setup

- https://unix.stackexchange.com/questions/201946/how-to-define-dns-server-in-openvpn
- https://smartshift.com/guide-setting-up-an-aws-vpc-client-vpn/
- use `169.254.169.253` for aws dns (see https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html)
- look into splitting traffic somehow (so far could not get it to work): https://medium.com/@Dylan.Wang/how-to-split-tunnel-traffic-with-openvpn-6420d1440fa
- use drill / dig to find dns servers: [drill](https://wiki.archlinux.org/index.php/Domain_name_resolution#Lookup_utilities)
- install `openvpn-update-resolv-conf-git` on arch to get openvpn dns updates working. see https://wiki.archlinux.org/index.php/OpenVPN#DNS
- rdm connection to redis with vpn: https://docs.rdm.dev/en/latest/quick-start/
- command to connect: `sudo openvpn --config connect.ovpn`
- check if it works: `ping ip-172-31-15-26.ec2.internal`
- disassociate when done being used (otherwise it costs a lot of money): https://www.reddit.com/r/aws/comments/ejkky9/aws_client_vpn_pricing_disassociate_to_save_money/
