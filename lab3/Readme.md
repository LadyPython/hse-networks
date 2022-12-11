# Модернизация сети офиса
## Топология
<img width="300" alt="image" src="https://user-images.githubusercontent.com/6313540/206864399-c65a67c9-2f4d-433a-bbf2-e31eb4f142a7.png">

## Настройка
Все команды в продолжение к lab1!

```bash
ssh root@192.168.1.67
```

### R (Маршрутизатор)
```
root@eve-ng:~# telnet 192.168.1.67 32774
Router>enable
Router#configure terminal
Router(config)#ip dhcp excluded-address 10.0.10.0 10.0.10.10
Router(config)#ip dhcp pool group1
Router(dhcp-config)#network 10.0.10.0 255.255.255.0
Router(dhcp-config)#default-router 10.0.10.100
Router(dhcp-config)#dns-server 8.8.8.8
Router(dhcp-config)#exit
Router(config)#ip dhcp excluded-address 10.0.20.0 10.0.20.10
Router(config)#ip dhcp pool group2
Router(dhcp-config)#default-router 10.0.20.100
Router(dhcp-config)#network 10.0.20.0 255.255.255.0
Router(dhcp-config)#dns-server 8.8.8.8
Router(dhcp-config)#exit
Router(config)#interface e0/0
Router(config-if)#ip nat inside
Router(config-if)#exit
Router(config)#interface e0/0.10
Router(config-subif)#ip nat inside    
Router(config-subif)#exit             
Router(config)#interface e0/0.20
Router(config-subif)#ip nat inside    
Router(config-subif)#exit
Router(config)#interface e0/1
Router(config-if)#no shutdown
Router(config-if)#ip address 10.0.0.100 255.255.255.0
Router(config-if)#ip nat outside
Router(config-if)#exit
Router(config)#ip nat pool pool 10.0.0.100 10.0.0.200 netmask 255.255.255.0
Router(config)#access-list 100 permit ip 10.0.10.0 0.0.0.255 any
Router(config)#access-list 100 permit ip 10.0.20.0 0.0.0.255 any
Router(config)#ip nat inside source list 100 pool pool
Router(config)#exit
```

### R0 (Маршрутизатор)
```
root@eve-ng:~# telnet 192.168.1.67 32775
Router>enable
Router#configure terminal 
Router(config)#interface e0/0
Router(config-if)#no shutdown
Router(config-if)#ip address 10.0.0.1 255.255.255.0 
Router(config-if)#exit
Router(config)#exit
```

### VPC1 (Клиент)
```
root@eve-ng:~# telnet 192.168.1.67 32769
VPCS> ip dhcp
DDORA IP 10.0.10.11/24 GW 10.0.10.100
```

### VPC2 (Клиент)
```
root@eve-ng:~# telnet 192.168.1.67 32770
VPCS> ip dhcp
DDORA IP 10.0.20.11/24 GW 10.0.20.100
```

## Проверка
* Настройка DHCP:
  
  VPC1:
  ```
  VPCS> show ip
  NAME        : VPCS[1]
  IP/MASK     : 10.0.10.11/24
  GATEWAY     : 10.0.10.100
  DNS         : 8.8.8.8  
  DHCP SERVER : 10.0.10.100
  DHCP LEASE  : 71536, 86400/43200/75600
  MAC         : 00:50:79:66:68:01
  LPORT       : 20000
  RHOST:PORT  : 127.0.0.1:30000
  MTU         : 1500
  ```
  
  VPC2:
  ```
  VPCS> show ip
  NAME        : VPCS[1]
  IP/MASK     : 10.0.20.11/24
  GATEWAY     : 10.0.20.100
  DNS         : 8.8.8.8  
  DHCP SERVER : 10.0.20.100
  DHCP LEASE  : 72409, 86400/43200/75600
  MAC         : 00:50:79:66:68:02
  LPORT       : 20000
  RHOST:PORT  : 127.0.0.1:30000
  MTU         : 1500
  ```
  
* Пинги и NAT:
  1. Пинги c VPC1 на R0:
  ```
  VPCS> ping 10.0.0.1

  84 bytes from 10.0.0.1 icmp_seq=1 ttl=254 time=1.684 ms
  84 bytes from 10.0.0.1 icmp_seq=2 ttl=254 time=2.010 ms
  84 bytes from 10.0.0.1 icmp_seq=3 ttl=254 time=4.277 ms
  84 bytes from 10.0.0.1 icmp_seq=4 ttl=254 time=2.571 ms
  84 bytes from 10.0.0.1 icmp_seq=5 ttl=254 time=2.332 ms
  ```
  2. Смотрим в Wireshark на e0/0 у R0, что адрес, с которого роутер их получает, транслирован:
  <img width="1000" alt="image" src="https://user-images.githubusercontent.com/6313540/206865693-8dd6d393-84a0-4678-8ae4-f4595872d9e3.png">
  3. Можно еще посмотреть трансляцию на роутере:
  
  ```
  Router#show ip nat translations 
  Pro Inside global      Inside local       Outside local      Outside global
  --- 10.0.0.100         10.0.10.11         ---                ---
  --- 10.0.0.101         10.0.20.11         ---                ---
  ```
