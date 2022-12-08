# Реализация небольшой сети офиса
## Топология
<img src="https://user-images.githubusercontent.com/6313540/206579315-0a3d48d1-a875-451d-94b6-791921a6ea80.jpeg" width="300"/>

## Настройка
```bash
ssh root@192.168.82.93
```

### VPC1 (Клиент)
```
root@eve-ng:~# telnet 192.168.82.93 32769
VPCS> ip 10.0.10.1 10.0.10.100
```

### VPC2 (Клиент)
```
root@eve-ng:~# telnet 192.168.82.93 32770
VPCS> ip 10.0.20.2 10.0.20.100
```

### S1 (Коммутатор уровня доступ)
```
root@eve-ng:~# telnet 192.168.82.93 32771
Switch>enable
Switch#configure terminal
Switch(config)#vlan 10
Switch(config)#exit
Switch(config)#interface e0/1
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 10
Switch(config-if)#exit
Switch(config)#interface e0/0
Switch(config-if)#switchport trunk encapsulation dot1q
Switch(config-if)#switchport mode trunk 
Switch(config-if)#switchport trunk allowed vlan 10,20
Switch(config-if)#exit
Switch(config)#interface e0/2
Switch(config-if)#switchport trunk encapsulation dot1q
Switch(config-if)#switchport mode trunk 
Switch(config-if)#switchport trunk allowed vlan 10,20
Switch(config-if)#exit
Switch(config)#exit
Switch#exit
```

### S2 (Коммутатор уровня доступ)
```
root@eve-ng:~# telnet 192.168.82.93 32772
Switch>enable
Switch#configure terminal
Switch(config)#vlan 20
Switch(config)#exit
Switch(config)#interface e0/1
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 20
Switch(config-if)#exit
Switch(config)#interface e0/0
Switch(config-if)#switchport trunk encapsulation dot1q
Switch(config-if)#switchport mode trunk 
Switch(config-if)#switchport trunk allowed vlan 10,20
Switch(config-if)#exit
Switch(config)#interface e0/2
Switch(config-if)#switchport trunk encapsulation dot1q
Switch(config-if)#switchport mode trunk 
Switch(config-if)#switchport trunk allowed vlan 10,20
Switch(config-if)#exit
Switch(config)#exit
Switch#exit
```


### S0 (Коммутатор уровня распределения)
```
root@eve-ng:~# telnet 192.168.82.93 32773
Switch>enable
Switch#configure terminal
Switch(config)#vlan 10
Switch(config)#exit
Switch(config)#vlan 20
Switch(config)#exit
Switch(config)#interface e0/0
Switch(config-if)#switchport trunk encapsulation dot1q
Switch(config-if)#switchport mode trunk 
Switch(config-if)#switchport trunk allowed vlan 10,20
Switch(config-if)#exit
Switch(config)#interface e0/1
Switch(config-if)#switchport trunk encapsulation dot1q
Switch(config-if)#switchport mode trunk 
Switch(config-if)#switchport trunk allowed vlan 10,20
Switch(config-if)#exit
Switch(config)#interface e0/2
Switch(config-if)#switchport trunk encapsulation dot1q
Switch(config-if)#switchport mode trunk 
Switch(config-if)#switchport trunk allowed vlan 10,20
Switch(config-if)#exit
Switch(config)#spanning-tree mode pvst
Switch(config)#spanning-tree extend system-id
Switch(config)#spanning-tree vlan 10,20 priority 61440
Switch(config)#exit
Switch#exit
```

### R (Маршрутизатор)
```
root@eve-ng:~# telnet 192.168.82.93 32774
Router>enable
Router#configure terminal
Router(config)#interface e0/0
Router(config-if)#no shutdown
Router(config-if)#exit
Router(config)#interface e0/0.10
Router(config-subif)#encapsulation dot1Q 10
Router(config-subif)#ip address 10.0.10.100 255.255.255.0
Router(config-subif)#exit
Router(config)#interface e0/0.20
Router(config-subif)#encapsulation dot1Q 20
Router(config-subif)#ip address 10.0.20.100 255.255.255.0
Router(config-subif)#exit
```

STP:


Пинги (с VPC2 на VPC1):
```
VPCS> ping 10.0.10.1          

84 bytes from 10.0.10.1 icmp_seq=1 ttl=63 time=6.049 ms
84 bytes from 10.0.10.1 icmp_seq=2 ttl=63 time=3.957 ms
84 bytes from 10.0.10.1 icmp_seq=3 ttl=63 time=4.274 ms
84 bytes from 10.0.10.1 icmp_seq=4 ttl=63 time=3.989 ms
84 bytes from 10.0.10.1 icmp_seq=5 ttl=63 time=3.514 ms

VPCS> ping 10.0.10.100

84 bytes from 10.0.10.100 icmp_seq=1 ttl=255 time=2.635 ms
84 bytes from 10.0.10.100 icmp_seq=2 ttl=255 time=2.324 ms
84 bytes from 10.0.10.100 icmp_seq=3 ttl=255 time=1.657 ms
84 bytes from 10.0.10.100 icmp_seq=4 ttl=255 time=2.372 ms
84 bytes from 10.0.10.100 icmp_seq=5 ttl=255 time=1.698 ms

VPCS> ping 10.0.20.100

84 bytes from 10.0.20.100 icmp_seq=1 ttl=255 time=2.154 ms
84 bytes from 10.0.20.100 icmp_seq=2 ttl=255 time=1.364 ms
84 bytes from 10.0.20.100 icmp_seq=3 ttl=255 time=1.439 ms
84 bytes from 10.0.20.100 icmp_seq=4 ttl=255 time=2.552 ms
84 bytes from 10.0.20.100 icmp_seq=5 ttl=255 time=2.707 ms
```


Отказоустойчивость: