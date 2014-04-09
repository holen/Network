ip route add 220.120.126.240/28 dev eth0 src 220.120.126.242 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.243 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.244 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.245 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.246 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.247 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.248 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.249 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.250 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.251 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.252 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.253 table ISP1
ip route add 220.120.126.240/28 dev eth0 src 220.120.126.254 table ISP1
ip route add default via 220.120.126.241 dev eth0 table ISP1
ip rule add from 220.120.126.240/28 lookup ISP1 prio 26000

