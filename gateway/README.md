# Gateway on ubuntu
防火墙脚本的一般结构

    1.设置网段、网卡、IP地址等变量
    2.加载包过滤相关的内核模块
        FTP相关：ip_nat_ftp、ip_conntrack_ftp
    3.确认开启路由转发功能
        /sbin/sysctl -w net.ipv4.ip_forward=1
        echo 1 > /proc/sys/net/ipv4/ip_forward

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

Save

    iptables-save > /etc/iptables-script

Restore

    /sbin/iptables-restore /etc/iptables-script # echo > /etc/rc.local

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
