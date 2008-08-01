# import the WNS module. Contains all sub-classes needed for
# configuration of WNS
import wns.WNS
import wns.Distribution
import ip
from ip.VirtualARP import VirtualARPServer
from ip.VirtualDHCP import VirtualDHCPServer
from ip.VirtualDNS import VirtualDNSServer

from constanze.Constanze import Constanze, Poisson
from constanze.Node import ConstanzeComponent, Listener, TCPBinding, TCPListenerBinding
from ip.BackboneHelpers import Router_10BaseT, Station_10BaseT 
from ip.IP import IP
import copper.Copper
import glue
import glue.support.Configuration
import tcp.TCP
import tcp.evaluation.default

# create an instance of the WNS configuration
# The variable must be called WNS!!!!
WNS = wns.WNS.WNS()
WNS.outputStrategy = wns.WNS.OutputStrategy.DELETE

wire = copper.Copper.Wire("theWire")

client = Station_10BaseT(name = "client",
                         _wire = wire,
                         _domainName = "client.tcp.wns.org",
                         _defaultRouter = "127.0.0.1")

server = Station_10BaseT(name = "server",
                         _wire = wire,
                         _domainName = "server.tcp.wns.org",
                         _defaultRouter = "127.0.0.1")

clientTCP = tcp.TCP.TCPComponent(client, "tcp", client.ip.dataTransmission, client.ip.notification)

serverTCP = tcp.TCP.TCPComponent(server, "tcp", server.ip.dataTransmission, server.ip.notification)


tcpClientBinding = TCPBinding(client.ip.domainName, server.ip.domainName, 1024)
constanzeClient = ConstanzeComponent(client, str(client.ip.domainName) + ".constanze")
constanzeClient.addTraffic(tcpClientBinding, Poisson())

tcpServerListenerBinding = TCPListenerBinding(1024)
serverListener = Listener(server.ip.domainName + ".listener")
constanzeServer = ConstanzeComponent(server, (server.ip.domainName) + ".constanze")
constanzeServer.addListener(tcpServerListenerBinding, serverListener)

WNS.nodes.append(client)
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

tcp.evaluation.default.installEvaluation(WNS)
