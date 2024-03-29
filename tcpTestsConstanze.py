# import the WNS module. Contains all sub-classes needed for
# configuration of WNS

import openwns
import openwns.logger

import ip.evaluation.default
from ip.VirtualARP import VirtualARPServer
from ip.VirtualDHCP import VirtualDHCPServer
from ip.VirtualDNS import VirtualDNSServer

import constanze.evaluation.default
from constanze.traffic import Poisson
from constanze.node import ConstanzeComponent, Listener, TCPBinding, TCPListenerBinding
from ip.BackboneHelpers import Router_10BaseT, Station_10BaseT 
from ip.IP import IP
import copper.Copper
import glue
import glue.support.Configuration
import tcp.TCP
import tcp.evaluation.default

# create an instance of the WNS configuration
# The variable must be called WNS!!!!
WNS = openwns.Simulator(simulationModel = openwns.node.NodeSimulationModel())
WNS.outputStrategy = openwns.simulator.OutputStrategy.DELETE

wire = copper.Copper.Wire("theWire")

client = Station_10BaseT(name = "client",
                         _wire = wire,
                         _domainName = "client.tcp.wns.org",
                         _defaultRouter = "127.0.0.1")
client.ip.enableTrace()

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

WNS.simulationModel.nodes.append(client)
WNS.simulationModel.nodes.append(server)

# one Virtual ARP Zone
varp = VirtualARPServer("vARP", "theWire")
WNS.simulationModel.nodes.append(varp)

vdhcp = VirtualDHCPServer("vDHCP@",
                          "theWire",
                          "192.168.0.2", "192.168.254.253",
                          "255.255.0.0")

vdns = VirtualDNSServer("vDNS", "ip.DEFAULT.GLOBAL")
WNS.simulationModel.nodes.append(vdns)

WNS.simulationModel.nodes.append(vdhcp)

#WNS.maxSimTime = 1000.0
WNS.maxSimTime = 200.0

tcp.evaluation.default.installEvaluation(WNS)

constanze.evaluation.default.installEvaluation(sim = WNS,
                                               maxPacketDelay = 1.0,
                                               maxPacketSize = 16000,
                                               maxBitThroughput = 100e6,
                                               maxPacketThroughput = 10e6,
                                               delayResolution = 1000,
                                               sizeResolution = 2000,
                                               throughputResolution = 10000)


ip.evaluation.default.installEvaluation(sim = WNS,
                                       maxPacketDelay = 0.5,     # s
                                       maxPacketSize = 2000*8,   # Bit
                                       maxBitThroughput = 10E6,  # Bit/s
                                       maxPacketThroughput = 1E6 # Packets/s
                                       )

openwns.setSimulator(WNS)