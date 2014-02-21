# Gateway on ubuntu
cat /etc/network/interfaces

    auto lo
    iface lo inet loopback
    auto eth0
    iface eth0 inet static
            address 10.1.1.1
            netmask 255.255.255.0
            dns-nameservers 8.8.8.8
            post-up ip route add 10.1.1.0/24 dev eth0
            pre-down ip route del 10.1.1.0/24 dev eth0
    auto eth1
    iface eth1 inet static
        address 125.22.12.19
        netmask 255.255.255.0
        gateway 125.90.88.1
        dns-nameservers 12.96.128.86

开启IP转发

    echo 1 > /proc/sys/net/ipv4/ip_forward

NAT映射

    iptables -t nat -A POSTROUTING -s 10.1.1.0/255.255.255.0 -j MASQUERADE

Test

    ping -I10.1.1.1 8.8.8.8
    mtr -n --address=10.1.1.1 8.8.8.8
    route -n
    ip rule

Log

    cp /etc/profile /etc/profile.bak
    cat << EOF >> /etc/profile
    if [ "\$BASH" ]; then
          PROMPT_COMMAND='history -a >(tee -a ~/.bash_history | logger -p local3.notice -t "\$USER[\$\$] \$SSH_CONNECTION")'
    fi
    EOF
