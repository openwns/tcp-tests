# import the WNS module. Contains all sub-classes needed for
# configuration of WNS
import wns.WNS
import wns.Distribution
import ip
from ip.VirtualARP import VirtualARPServer
from ip.VirtualDHCP import VirtualDHCPServer
from ip.VirtualDNS import VirtualDNSServer

from constanze.Constanze import Constanze, CBR;
from constanze.Node import ConstanzeComponent
from ip.BackboneHelpers import Router_10BaseT, Station_10BaseT 
from ip.Address import ipv4Address
from ip.IP import IP
import copper.Copper
import glue
import glue.support.Configuration
import tcp.TCP

import applications

# create an instance of the WNS configuration
# The variable must be called WNS!!!!
WNS = wns.WNS.WNS()
WNS.outputStrategy = wns.WNS.OutputStrategy.DELETE

wire = copper.Copper.Wire("theWire")


client1 = Station_10BaseT(name = "client1",
                         _wire = wire,
                         _domainName = "client1.ap.wns.org",
                         _defaultRouter = "127.0.0.1")

client2 = Station_10BaseT(name = "client",
                         _wire = wire,
                         _domainName = "client2.ap.wns.org",
                         _defaultRouter = "127.0.0.1")

server = Station_10BaseT(name = "server",
                         _wire = wire,
                         _domainName = "server.ap.wns.org",
                         _defaultRouter = "127.0.0.1")

client1UDP = tcp.TCP.UDPComponent(client1, "udp", client1.ip.dataTransmission, client1.ip.notification)
client1appls = applications.Applications.Client(client1, "client1.ap.wns.org", "client1.ap.wns.org", None, client1UDP.service)
# Set different traffic mixes
# CBR, VoIP applications use UDP
client1appls.params.CBR.SessionIat = 0.5
client1appls.params.CBR.ServerIPAddress = server.ip.domainName
client1appls.params.VoIP.SessionIat = 0.5
client1appls.params.VoIP.ServerIPAddress = server.ip.domainName

client2UDP = tcp.TCP.UDPComponent(client2, "udp", client2.ip.dataTransmission, client2.ip.notification)
client2TCP = tcp.TCP.TCPComponent(client2, "tcp", client2.ip.dataTransmission, client2.ip.notification)
client2appls = applications.Applications.Client(client2,  "client2.ap.wns.org", "client2.ap.wns.org", client2TCP.service, client2UDP.service)
# Set different traffic mixes
# Video application uses UDP, WWW_Choi uses TCP
client2appls.params.Video.SessionIat = 0.5
client2appls.params.Video.ServerIPAddress = server.ip.domainName
client2appls.params.WWW_Choi.SessionIat = 0.5
client2appls.params.WWW_Choi.ServerIPAddress = server.ip.domainName
client2appls.params.FTP_Rx.SessionIat = 0.5
client2appls.params.FTP_Rx.ServerIPAddress = server.ip.domainName
#client2appls.params.FTP_Tx.SessionIat = 0.5
#client2appls.params.FTP_Tx.ServerIPAddress = server.ip.domainName

serverUDP = tcp.TCP.UDPComponent(server, "udp", server.ip.dataTransmission, server.ip.notification)
serverTCP = tcp.TCP.TCPComponent(server, "tcp", server.ip.dataTransmission, server.ip.notification)
serverappls = applications.Applications.Server(server, "server.ap.wns.org", "server.ap.wns.org",serverTCP.service, serverUDP.service)

WNS.nodes.append(client1)
WNS.nodes.append(client2)
WNS.nodes.append(server)

# one Virtual ARP Zone
varp = VirtualARPServer("vARP", "theWire")
WNS.nodes.append(varp)
vdhcp = VirtualDHCPServer("vDHCP@",
                          "theWire",
                          "192.168.0.2", "192.168.254.253",
                          "255.255.0.0")

vdns = VirtualDNSServer("vDNS", "ip.DEFAULT.GLOBAL")
WNS.nodes.append(vdns)

WNS.nodes.append(vdhcp)

#WNS.maxSimTime = 1000.0
WNS.maxSimTime = 200.0
