echo 1 > /proc/sys/net/ipv4/ip_forward

# MASQUERADE
iptables -t nat -A POSTROUTING -s 10.1.1.0/255.255.255.0 -j MASQUERADE

# nat
iptables -t nat -A PREROUTING -p tcp -d 112.127.130.173 --dport 3002 -j DNAT --to-destination 10.1.1.2:22
