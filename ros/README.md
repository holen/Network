# Ros 

1. 设置网卡名

    Interfaces-Interface 
    
    wan  
    lan  
    wan-liantong

2. 设置内外网网卡IP地址

    IP-Address  
    
    Interface: lan  
    Address: 10.0.0.3/16  
    Network: 10.0.0.0  
    
    Interface: wan  
    Address: 110.80.30.203/29  
    Network: 110.80.30.200
    
    Interface: wan-liantong  
    Address: 58.23.30.162/28  
    Network: 58.23.30.160
    
3. 设置伪装

    IP-Firewall-NAT
    
    Chain: srcnat  
    Out.Interface: wan  
    Action: masquerade
    
    Chain: srcnat  
    Out.Interface: wan-liantong  
    Action: masquerade
    
4. 地址列表

    IP-Firewall-Address List
    
    Name: lan
    Address: 10.0.0.0/16
    
    Name: liantong
    Address: 10.0.80.200
    
    Name: dianxin
    Address: 10.0.80.80
    
5. 标记

    IP-Firewall-Mangle
    
    Chain: prerouting  
    Src.Address.List: dianxin  
    Dst.Address.List: !lan  
    Action: mark routing    
    New Routing Mark: 1st_route
    
    Chain: prerouting   
    Src.Address.List: liantong  
    Dst.Address.List: !lan  
    Action: mark routing   
    New Routing Mark: liantong_route
    
6. 路由设置

    IP-Routes-Routes
    
    Dst.Address: 0.0.0.0  
    Gateway: 110.80.33.201  
    Check gateway: ping  
    Routing Mark: 1st_route
    
    Dst.Address: 0.0.0.0  
    Gateway: 58.23.3.161  
    Check gateway: ping  
    Routing Mark: liantong_route
