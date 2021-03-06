#!/bin/bash

##### Usage #####
# Init interfaces: ./set_netns.sh
# IPv4 ping test cmd: sudo ip netns exec $[ns_name] ping $[IP]
# IPv6 ping test cmd: sudo ip netns exec $[ns_name] ping6 $[IP]
##### interface info #####
NS1_NAME=net0
NS1_VID=2
NS1_BASE_IF=eth0
NS1_IP4=192.168.2.29
NS1_MASK4=24
NS1_GW4=192.168.2.254
NS1_IP6=fd53:7cb8:383:2::10f
NS1_MASK6=64
NS1_GW6=fd53:7cb8:383:2::fffe
NS1_GW_MAC=00:e0:4c:00:00:02

NS2_NAME=net1
NS2_VID=5
NS2_BASE_IF=eth1
NS2_IP4=192.168.5.59
NS2_MASK4=24
NS2_GW4=192.168.5.254
NS2_IP6=fd53:7cb8:383:5::e
NS2_MASK6=64
NS2_GW6=fd53:7cb8:383:5::fffe
NS2_GW_MAC=00:e0:4c:00:00:05

sudo ip netns del net0 2>>error.txt
sudo ip netns del net1 2>>error.txt

sudo ip link delete $NS1_NAME.$NS1_VID 2>>error.txt
sudo ip link delete $NS2_NAME.$NS2_VID 2>>error.txt

###### main config ######
# NS1
sudo ip link add link $NS1_BASE_IF name $NS1_NAME.$NS1_VID type vlan id $NS1_VID
sudo ip netns add $NS1_NAME
sudo ip link set $NS1_NAME.$NS1_VID netns $NS1_NAME
sudo ip netns exec $NS1_NAME ip addr add dev $NS1_NAME.$NS1_VID $NS1_IP4/$NS1_MASK4
sudo ip netns exec $NS1_NAME ip -6 addr add dev $NS1_NAME.$NS1_VID $NS1_IP6/$NS1_MASK6
sudo ip netns exec $NS1_NAME ip link set dev $NS1_NAME.$NS1_VID up
sudo ip netns exec $NS1_NAME ip route add $NS2_IP4 via $NS1_GW4
sudo ip netns exec $NS1_NAME ip -6 route add $NS2_IP6 via $NS1_GW6
## For Raspbian
#sudo ip netns exec $NS1_NAME arp -s $NS1_GW4 $NS1_GW_MAC

# NS2
sudo ip link add link $NS2_BASE_IF name $NS2_NAME.$NS2_VID type vlan id $NS2_VID
sudo ip netns add $NS2_NAME
sudo ip link set $NS2_NAME.$NS2_VID netns $NS2_NAME
sudo ip netns exec $NS2_NAME ip addr add dev $NS2_NAME.$NS2_VID $NS2_IP4/$NS2_MASK4
sudo ip netns exec $NS2_NAME ip -6 addr add dev $NS2_NAME.$NS2_VID $NS2_IP6/$NS2_MASK6
sudo ip netns exec $NS2_NAME ip link set dev $NS2_NAME.$NS2_VID up
sudo ip netns exec $NS2_NAME ip route add $NS1_IP4 via $NS2_GW4
sudo ip netns exec $NS2_NAME ip -6 route add $NS1_IP6 via $NS2_GW6
## For Raspbian
#sudo ip netns exec $NS2_NAME arp -s $NS2_GW4 $NS2_GW_MAC
