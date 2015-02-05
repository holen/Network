#!/bin/bash

/sbin/modprobe ip_tables
/sbin/modprobe ip_nat_ftp
iptables -F 
iptables -X
iptables -Z
iptables -A INPUT -s 101.226.102.95 -j DROP 
iptables -A INPUT -s 101.226.102.97 -j DROP
iptables -A INPUT -s 101.226.89.67 -j DROP
iptables -A INPUT -s 101.226.33.0/24 -j DROP
iptables -A INPUT -s 101.226.51.0/24 -j DROP
iptables -A INPUT -s 101.226.52.0/24 -j DROP
iptables -A INPUT -s 101.226.65.0/24 -j DROP
iptables -A INPUT -s 101.226.66.0/24 -j DROP
iptables -A INPUT -s 101.226.89.0/24 -j DROP
iptables -A INPUT -s 111.161.54.0/24 -j DROP
iptables -A INPUT -s 112.64.235.0/24 -j DROP
iptables -A INPUT -s 112.65.193.0/24 -j DROP
iptables -A INPUT -s 112.95.240.189 -j DROP
iptables -A INPUT -s 113.105.95.138 -j DROP
iptables -A INPUT -s 113.89.107.39 -j DROP
iptables -A INPUT -s 113.108.12.0/24 -j DROP
iptables -A INPUT -s 113.108.64.0/24 -j DROP
iptables -A INPUT -s 113.108.81.0/24 -j DROP
iptables -A INPUT -s 113.108.91.0/24 -j DROP
iptables -A INPUT -s 113.142.24.0/24 -j DROP
iptables -A INPUT -s 113.142.8.0/24 -j DROP
iptables -A INPUT -s 113.142.9.0/24 -j DROP
iptables -A INPUT -s 118.123.232.0/24 -j DROP
iptables -A INPUT -s 119.147.193.91 -j DROP
iptables -A INPUT -s 119.147.11.0/24 -j DROP
iptables -A INPUT -s 119.147.14.0/24 -j DROP
iptables -A INPUT -s 119.147.18.0/24 -j DROP
iptables -A INPUT -s 119.147.19.0/24 -j DROP
iptables -A INPUT -s 119.147.21.0/24 -j DROP
iptables -A INPUT -s 119.147.32.0/24 -j DROP
iptables -A INPUT -s 119.147.6.0/24 -j DROP
iptables -A INPUT -s 119.147.7.0/24 -j DROP
iptables -A INPUT -s 121.14.73.0/24 -j DROP
iptables -A INPUT -s 121.14.77.0/24 -j DROP
iptables -A INPUT -s 121.14.94.0/24 -j DROP
iptables -A INPUT -s 121.14.95.0/24 -j DROP
iptables -A INPUT -s 121.14.97.0/24 -j DROP
iptables -A INPUT -s 123.151.42.0/24 -j DROP
iptables -A INPUT -s 124.115.10.0/24 -j DROP
iptables -A INPUT -s 124.115.12.0/24 -j DROP
iptables -A INPUT -s 124.115.14.0/24 -j DROP
iptables -A INPUT -s 124.115.2.0/24 -j DROP
iptables -A INPUT -s 124.115.4.0/24 -j DROP
iptables -A INPUT -s 124.89.31.0/24 -j DROP
iptables -A INPUT -s 180.153.114.0/24 -j DROP
iptables -A INPUT -s 180.153.214.0/24 -j DROP
iptables -A INPUT -s 180.153.206.0/24 -j DROP
iptables -A INPUT -s 180.153.205.0/24 -j DROP
iptables -A INPUT -s 180.153.201.0/24 -j DROP
iptables -A INPUT -s 180.153.212.0/24 -j DROP
iptables -A INPUT -s 180.153.211.0/24 -j DROP
iptables -A INPUT -s 180.153.163.0/24 -j DROP
iptables -A INPUT -s 222.73.77.0/24 -j DROP
iptables -A INPUT -s 222.73.76.0/24 -j DROP
