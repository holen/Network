#!/bin/bash
IPT=/sbin/iptables

$IPT -F
$IPT -X
$IPT -t nat -F
$IPT -t nat -X
$IPT -t mangle -F
$IPT -t mangle -X
$IPT -P INPUT ACCEPT
$IPT -P OUTPUT ACCEPT

# Drop 10086
$IPT -I INPUT -i eth1 -p tcp --syn --dport 10086 -j DROP

# ACCEPT
$IPT -I INPUT -i eth1 -p tcp --syn --dport 10086 -s 17.25.140.170/32 -j ACCEPT

