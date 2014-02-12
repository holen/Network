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

9.ROS -- ADSL聚合

    1.add wan1 wan2
    2.然后添加PPPOE拨号（先添加拨号再手动输入 帐号）：
    [admin@MikroTik] > :for i from=1 to=4 do= {interface pppoe-client add name=("pppoe-out".$i) user=$i password=$i interface=("wan".$i)}
    interfaces --> add --> Name:pppoe-out1 Interfaces:wan1 Max-MTU:1480 Max-MRU:1480 --> Dial-out --> user password
    interfaces --> add --> Name:pppoe-out2 Interfaces:wan2 Max-MTU:1480 Max-MRU:1480 --> Dial-out --> user password
    3.标记从外网进来的连接（因为外pppoe还没有连接，所以这些标记规则暂时是红色）：
    [admin@MikroTik] > :for i from=1 to=4 do={/ip firewall mangle add chain=input action=mark-connection new-connection-mark=("pppoe-out".$i."_conn") in-interface=("pppoe-out".$i)}
    Firewall --> Mangle --> Chain:input in.Interfaces:pppoe-out1 --> Action:mark connection New-Connection-Mark:pppoe-out1_conn
    Firewall --> Mangle --> Chain:input in.Interfaces:pppoe-out2 --> Action:mark connection New-Connection-Mark:pppoe-out2_conn
    4.然后标记路由让从哪个接口进来的数据就从哪个接口出去：
    [admin@MikroTik] >  :for i from=1 to=4 do= {ip firewall mangle add chain=output connection-mark=("pppoe-out".$i."_conn") action=mark-routing new-routing-mark=("to_pppoe-out".$i)}
    Firewall --> Mangle --> Chain:output Connection-Mark:pppoe-out1_conn --> Action:mark routing New-Connection-Mark:to_pppoe-out1
    Firewall --> Mangle --> Chain:output Connection-Mark:pppoe-out2_conn --> Action:mark routing New-Connection-Mark:to_pppoe-out2
    5．然后将所有内网出来的数据通过pcc的both-addresses分成4分并标记连接和路由：
    [admin@MikroTik] > :for i from=1 to=4 do= {/ip firewall mangle add chain=prerouting src-address-list=lan action=mark-connection new-connection-mark=("conn".$i) per-connection-classifier=("both-addresses:4/".$i) comment=$i{... /ip firewall mangle add chain=prerouting src-address-list=lan-add action=mark-routing new-routing-mark=("rout".($i-2)) connection-mark=("conn".$i)}
    Mangle --> Chain:prerouting Dst.Address:!10.10.0.0/24 In.Interface:lan --> Advanced --> Per-connection-classifier:both addresses 4 0  -->  extra  -->  Address-Tyype::local  -->>Action :mark connection New-connection--Mark:pppoe-out1_conn  
    Mangle --> Chain:prerouting In.Interface:lan connection-Mark:pppoe-out1_conn --> Action :mark routing New-connection-Mark:to_pppoe-out1
    6.为每个路由标记添加路由并添加pppoe-out4为默认路由：
    [admin@MikroTik] > :for i from=2 to=41 do= {ip route add dst-address=0.0.0.0/0 gateway=("pppoe-out".$i) routing-mark=("rout".$i)}
    [admin@MikroTik] >ip routed add dst-address=0.0.0.0/0 gateway=pppoe-out41
    ip --> routes --> Dst.Address:0.0.0.0/0 Gateway:pppoe-out1 reachable 
    7．最后做NAT伪装：
    [admin@MikroTik] > ip firewall nat add chain=srcnat action=masquerade 
    NAT --> chain:srcnat out.Address:pppoe-out1 --> Action --> Action:masquerade
    8.MSS设定
    MTU: Maxitum Transmission Unit 最大传输单元
    MSS: Maxitum Segment Size 最大分段大小  MSS=MTU-4
    Firewall --> Mangle --> Chain:forward Protocol:6(tcp) In.Interfaces:pppoe-out2 --> Advanced --> TCP MSS:1441-65535 TCP-Flags:syn --> Action:change  MsSS  New-TCP-MSS:1440  
    Firewall --> Mangle --> Chain:forward Protocol:6(tcp) Out.Interfaces:pppoe-out2 --> Advanced --> TCP MSS:1441-65535 TCP-Flags:syn --> Action:change  MsSS  New-TCP-MSS:1440  
    Test: cmd --> ping www.baidu.com -f -l 1440

