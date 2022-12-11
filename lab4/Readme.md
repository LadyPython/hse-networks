# Построение VPN тоннелей между офисами
## Топология
<img width="1000" alt="image" src="https://user-images.githubusercontent.com/6313540/206918984-9c506a13-6ed8-4513-be44-23e503e06ab8.png">

## Настройка
Все команды в продолжение к lab1!

```bash
ssh root@192.168.1.67
```

### R (Маршрутизатор, эмулирующий интернет)
```
root@eve-ng:~# telnet 192.168.1.67 32773
Router>enable
Router#configure terminal
Router(config)#interface e0/0
Router(config-if)#no shutdown
Router(config-if)#ip address 10.0.1.1 255.255.255.0
Router(config-if)#exit
Router(config)#interface e0/1
Router(config-if)#no shutdown
Router(config-if)#ip address 10.0.2.1 255.255.255.0
Router(config-if)#exit
Router(config)#interface e0/2
Router(config-if)#no shutdown 
Router(config-if)#ip address 10.0.3.1 255.255.255.0
Router(config-if)#exit
Router(config)#exit
Router#
```

### R1 (Маршрутизатор)
```
root@eve-ng:~# telnet 192.168.1.67 32772
Router>enable
Router#configure terminal 
Router(config)#interface e0/1
Router(config-if)#no shutdown
Router(config-if)#ip address 10.0.1.100 255.255.255.0
Router(config-if)#exit
Router(config)#interface e0/0
Router(config-if)#no shutdown
Router(config-if)#ip address 10.0.10.10 255.255.255.0 
Router(config-if)#exit
Router(config)#interface tunnel 1
Router(config-if)#ip address 10.0.12.1 255.255.255.0 
Router(config-if)#tunnel source 10.0.1.100
Router(config-if)#tunnel destination 10.0.2.100
Router(config-if)#exit
Router(config)#ip route 0.0.0.0 0.0.0.0 10.0.1.1
Router(config)#ip route 10.0.20.2 255.255.255.255 10.0.12.100
Router(config)#exit
Router#
```


### R2 (Маршрутизатор)
```
root@eve-ng:~# telnet 192.168.1.67 32774
Router>enable
Router#configure terminal
Router(config)#interface e0/1
Router(config-if)#no shutdown
Router(config-if)#ip address 10.0.2.100 255.255.255.0
Router(config-if)#exit
Router(config)#interface e0/0
Router(config-if)#no shutdown
Router(config-if)#ip address 10.0.20.20 255.255.255.0 
Router(config-if)#exit
Router(config)#interface tunnel 1
Router(config-if)#ip address 10.0.12.100 255.255.255.0
Router(config-if)#tunnel source 10.0.2.100
Router(config-if)#tunnel destination 10.0.1.100
Router(config-if)#exit
Router(config)#ip route 0.0.0.0 0.0.0.0 10.0.2.1 
Router(config)#ip route 10.0.10.1 255.255.255.255 10.0.12.1
Router(config)#exit
Router#
```


### R3 (Маршрутизатор)
```
root@eve-ng:~# telnet 192.168.1.67 32775
Router>enable
Router#configure terminal
Router(config)#interface e0/1
Router(config-if)#no shutdown
Router(config-if)#ip address 10.0.3.100 255.255.255.0
Router(config-if)#exit
Router(config)#interface e0/0
Router(config-if)#no shutdown
Router(config-if)#ip address 10.0.30.30 255.255.255.0 
Router(config-if)#exit
Router(config)#exit
Router#
```

### VPC1 (Клиент)
```
root@eve-ng:~# telnet 192.168.1.67 32769
VPCS> ip 10.0.10.1 255.255.255.0 10.0.10.10
```

### VPC2 (Клиент)
```
root@eve-ng:~# telnet 192.168.1.67 32770
VPCS> ip 10.0.20.2 255.255.255.0 10.0.20.20
```

### VPC3 (Клиент)
```
root@eve-ng:~# telnet 192.168.1.67 32771
VPCS> ip 10.0.30.3 255.255.255.0 10.0.30.30
```
