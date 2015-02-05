#H3C S5120-24P-EI 三层交换机  
  
三层交换机限速测试  
内网IP到10.0.0.1限速  
内网到内网不限速  

>## create ACL  
>><switch> system-view  
>>[switch] acl number 2000  
>>[switch-acl-basic-2000] rule permit source 10.0.10.0 0.0.255.255   
>>[switch-acl-basic-2000] quit  
>>[switch] acl number 2001  
>>[switch-acl-basic-2001] rule permit source 10.0.20.0 0.0.255.255  
>>[switch-acl-basic-2001] quit  
>>[switch] acl number 3001  
>>[H3C-acl-adv-3001] rule 1 permit ip source 10.0.0.0 0.0.255.255 destination 10.0.0.2 0  
>>[H3C-acl-adv-3001] quit  
>## 创建流分类  
>>[switch] traffic classifier boss  
>>[switch-classifiter-boss] if-match acl 2000  
>>[switch-classifiter-boss] quit  
>>[switch] traffic classifier cpb  
>>[switch-classifiter-cpb] if-match acl 2001  
>>[switch-classifiter-cpb] quit  
>## 创建流行为 限速值为1024Kbps  
>>[switch] traffic behavior car_boss_cpb  
>>[switch-behavior-car_boss_cpb] car cir 1024   
>>[switch-behavior-car_boss_cpb] quit  
>CBS和EBS的配置方法：  
*CIR：表示向C桶中投放令牌的速率，即C桶允许传输或转发报文的平均速率；  
*CBS：表示C桶的容量，即C桶瞬间能够通过的承诺突发流量；  
*EBS：表示E桶的容量，即E桶瞬间能够通过的超出突发流量。  
>>[H3C-behavior-yw]car cir 2048 cbs 409600 ebs 0 green pass red discard  
>>[H3C-GigabitEthernet1/0/18]qos gts queue 1 cir 2048 cbs 4096  
>推荐配置：  
>>CBS = 200 * CIR  
>## 创建QoS策略car，将流分类boss,cpb与流行为car_boss_cpb进行匹配  
>>[switch] qos policy car  
>>[switch-qospolicy-car] classifier boss behavior car_boss_cpb  
>>[switch-qospolicy-car] classifier cpb behavior car_boss_cpb  
>>[switch-qospolicy-car] quit  
>>[H3C]  interface GigabitEthernet 1/0/1  
>>[H3C-GigabitEthernet1/0/1] qos apply policy car inbound  
2)端口限速  
>8、Qos端口限速  
>配置限速参数，端口进/出速率限制为5120kbps。1024kbps --> 112K/s  
>>[H3C] interface gigabitethernet 1/0/1  
>>[H3C-GigabitEthernet1/0/1] qos lr inbound cir 5120  
>>[H3C-GigabitEthernet1/0/1] qos lr outbound cir 5120  
>  
>H3C S5120 Series SI 二层交换机  
>H3C S5120-28P-SI Software Version Release 1513P15  
>  
#二层交换机网段限制  
>特定vlan中的PC只能绑定许可IP访问外网  
>1)包过滤  
>## 定义ACL，分别为允许源IP为10.0.10.0的报文通过以及拒绝IP地址为任意地址的报文通过  
>[switch] acl number 2000  
>[switch-acl-basic-2000] rule permit source 10.0.80.0 0.0.255.255  
>[switch-acl-basic-2000] rule deny source any  
>[switch-acl-basic-2000] quit  
>[switch] display acl all  
>## 设置包过滤功能  
>[switch] interface gigabitethernet 1/0/1  
>[switch-gigabitethernet1/0/1] packet-filter 2000 inbound  
>[switch-gigabitethernet1/0/1] quit  
>[H3C]display packet-filter interface GigabitEthernet 1/0/1  
>[H3C]display packet-filter interface Vlan-interface 1  
>## 取消规则  
>[H3C-GigabitEthernet1/0/1]undo packet-filter 2000 inbound  
>[H3C-Vlan-interface1]undo packet-filter 3300 inbound  
>2)QoS策略  
>[H3C]acl number 2000  
>[H3C-acl-basic-2000]rule permit source 10.0.80.0 0.0.0.255  
>[H3C-acl-basic-2000]quit  
>[H3C]acl number 2001   
>[H3C-acl-basic-2001]rule deny source any   
>[H3C-acl-basic-2001]quit  
>[H3C]traffic classifier permit_80  
>[H3C-classifier-permit_80]if-match acl 2000  
>[H3C-classifier-permit_80]quit  
>[H3C]traffic behavior behavior_80  
>[H3C-behavior-behavior_80]filter permit  
>[H3C-behavior-behavior_80]quit  
>[H3C]traffic classifier deny_any   
>[H3C-classifier-deny_any]if-match acl 2001  
>[H3C-classifier-deny_any]quit  
>[H3C]traffic behavior deny_any  
>[H3C-behavior-behavior_80]filter deny  
>[H3C-behavior-behavior_80]quit  
>[H3C] qos policy policy_80  
>[H3C-qospolicy-policy_80] classifier permit_80 behaviro behavior_80  
>[H3C-qospolicy-policy_80] classifier deny_any behaviro deny_any  
>[H3C-qospolicy-policy_80] quit  
>[H3C]  interface GigabitEthernet 1/0/1  
>[H3C-GigabitEthernet1/0/1] qos apply policy policy_80 inbound  
>Display qos policy  
>[H3C]display qos policy interface GigabitEthernet 1/0/1  
>  
># DHCP Snooping配置  
>## GigabitEethernet 1/0/1 为连接DHCP服务器的端口  
><H3C> system-view  
>[H3C] dhcp-snooping  
>[H3C] interface  GigabitEthernet 1/0/1  
>[H3C-GigabitEthernet1/0/1] dhcp-snooping trust  
>[H3C-GigabitEthernet1/0/1] quit  

ip bind

    system-view
    interface GigabitEthernet 1/0/18
    display user-bind
    绑定
    user-bind mac-address 0026-1838-97e6
    解绑
    undo user-bind ip-address 10.0.80.33 mac-address  0026-1838-97e6
    最后save

