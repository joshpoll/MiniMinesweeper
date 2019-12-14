from collections import namedtuple
import z3

# Figure 2
SymbolicPacket = namedtuple(
    'SymbolicPacket', ['dstIp', 'srcIp', 'dstPort', 'srcPort', 'protocol'])

dstIp, srcIp, dstPort, srcPort, protocol = z3.Ints(
    'dstIp srcIp dstPort srcPort protocol')


def z3Range(exp, low, high):
    return z3.And(low <= exp, exp < high)


# (1)
symbolic_packet = SymbolicPacket(
    z3Range(dstIp, 0, 2**32),
    z3Range(srcIp, 0, 2**32),
    z3Range(dstPort, 0, 2**16),
    z3Range(srcPort, 0, 2**16),
    z3Range(protocol, 0, 2**8)
)
