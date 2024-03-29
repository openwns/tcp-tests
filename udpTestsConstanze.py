# import the WNS module. Contains all sub-classes needed for
# configuration of WNS
import openwns

import copper

import ip
import ip.evaluation.default
from ip.VirtualARP import VirtualARPServer
from ip.VirtualDHCP import VirtualDHCPServer
from ip.VirtualDNS import VirtualDNSServer
import ip.BackboneHelpers

import tcp.TCP

import constanze
import constanze.node
import constanze.traffic
import constanze.evaluation.default


# create an instance of the WNS configuration
# The variable must be called WNS!!!!
WNS = openwns.Simulator(simulationModel = openwns.node.NodeSimulationModel())
WNS.outputStrategy = openwns.simulator.OutputStrategy.DELETE
WNS.maxSimTime = 20.0

#  A_____wire_____B
# 0.2            0.3
#
# A sends data to B
# B sends data to A

class UdpStation(ip.BackboneHelpers.Station_10BaseT) :

    udp = None

    domainName = None

    def __init__(self, name, _wire, _domainName, _defaultRouter) :
        super(UdpStation, self).__init__(name, _wire, _domainName, _defaultRouter);
        self.domainName = _domainName
        self.udp = tcp.TCP.UDPComponent(self, name + ".udp", self.ip.dataTransmission, self.ip.notification);


wire = copper.Copper.Wire( "theWire" )
station1 = UdpStation( "A", wire, "192.168.0.2", "127.0.0.1" )
station2 = UdpStation( "B", wire, "192.168.0.3", "127.0.0.1" )

# for both stations
destinationPort = 6666
listenPort = 6666

# for station A
destinationDomainName = station2.ip.domainName
binding = constanze.node.UDPBinding( station1.ip.domainName, destinationDomainName, destinationPort )
constanze1 = constanze.node.ConstanzeComponent( station1, "A.constanze" )
constanze1.addTraffic( binding, constanze.traffic.CBR( 0.01, 1024, 100 ) )
listener = constanze.node.Listener( "A.listener" )
binding = constanze.node.UDPListenerBinding( listenPort )
constanze1.addListener( binding, listener )

# for station B
destinationDomainName = station1.ip.domainName
binding = constanze.node.UDPBinding( station2.domainName, destinationDomainName, destinationPort )
constanze2 = constanze.node.ConstanzeComponent( station2, "B.constanze" )
constanze2.addTraffic( binding, constanze.traffic.CBR( 0.01, 1024, 100 ) )
listener = constanze.node.Listener( "B.listener" )
binding = constanze.node.UDPListenerBinding( listenPort )
constanze2.addListener( binding, listener )

# Add nodes to scenario
WNS.simulationModel.nodes = [station1, station2]

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

