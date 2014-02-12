# ROS 
1.ROS -- Lan

    admin --> enter
    命令行下 int  --> print	#打印网络接口信息
    en 0
    en 1
    set 0 name=Lan
    set 1 name=Wan
    /	#回到根目录
    setup
    a	#设置网络
    a	#add ip address
    Lan
    192.168.0.254/24
    g	#设置网关
    0.0.0.0
    x

2.ROS -- Wan

    Interfaces --> 修改wan名称
    ip --> address --> add --> Address/Network/Interface #外网IP地址与子网掩码

3.ROS -- NAT

    ip --> firewall --> nat --> add --> chain:srcnat Out.Interface:wan--> action:maquerade --> apply #设置完后就可以上网了

4.ROS -- vpn(pptp)

    PPP --> Profiles --> Name:pptp Local Address:192.168.3.2
    IP --> firewall --> nat --> add --> chain:srcnat src.Address:192.168.3.2/24 --> Action:masquerade #设置client通过VPN网关来上网
    ppp --> Secrets --> add --> name password service:pptp Profile:pptp RemoteAddress:192.168.3.10 #设置vpn client

5.ROS -- ipip

    Interfaces --> ip tunnel --> add --> Name:ipip1 Type:IP tunnel Local-Address:110.80.12.123(wan) Remote-Address:117.28.18.123 #建立IP虚拟通道
    IP --> address List --> add --> address:192.168.1.2/24 network:192.168.1.0 interface:ipip1 #为虚拟网卡添加IP地址，不能与内网IP相同
    routes --> route --> add --> Dst.address:10.10.10.0/24 Gateway:ipip1 reachable

6.ROS -- route

    IP --> routes --> add --> Dst.address:0.0.0.0/0 Gateway:110.80.12.1(wan gateway) reachable wan1 Check-Gateway:ping Distance:10 Scope:30 Target-Starge cope:10  #默认路由

7.ROS -- 分流

    firewall --> mangle --> add --> Chain:prerouting --> Advanced src-address-list:scb Dst.Address-list:!lan --> Action action:mark routing New-Routeing-Mark:scb  
    firewall --> mangle --> add --> Chain:prerouting --> Advanced src-address-list:zq Dst.Address-list:!lan --> Action action:mark routing New-Routeing-Mark:zq 
    routes --> add --> Dst.address:0.0.0.0/0 Gateway:10.0.0.1 reachable lan Check-Gateway:ping Routing Mark:scb
    routes --> add --> Dst.address:0.0.0.0/0 Gateway:58.23.23.122 reachable lan Check-Gateway:ping Routing Mark:zq

8.ROS -- 查看流量

    Tools --> Torch --> start
