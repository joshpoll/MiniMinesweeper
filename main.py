import yaml
import argparse
import os.path
import copy

parser = argparse.ArgumentParser(description='MiniMinesweeper')
parser.add_argument('-d', '--dir', metavar='d', nargs=1, default=[str(os.path.abspath(
    os.path.dirname(__file__)))], help='directory to look for traces folder')
parser.add_argument('trace', metavar='t', type=str, nargs=1,
                    help='trace name. try `sample`')

args = parser.parse_args()
trace = args.trace[0]

# load network and invariants from yaml files
ws_path = os.path.abspath(args.dir[0])


def load_network(ws_path):
    """
    network yaml schema (incomplete):

    Devices: [{Acls, BgpConfig, Interfaces, Name, StaticRoutes}]
    Acls: {DefaultAction, Name, Rules}
    Rules: [{Action, Description, DstIp, DstPort, Protocol, SrcIp, SrcPort}]
    BgpConfig: {AdvertisedRoutes, InboundPolicies, OutboundPolicies}
    OutboundPolicies: [{Name, PolicyClauses}]
    PolicyClauses: [{Matches, Actions}]
    Interfaces: [{InAcl, InBgpPolicy, Name, Neighbor, OutAcl, OutBgpPolicy}]
    StaticRoutes: [{Interface, Prefix}]
    """

    cp_path = os.path.join(ws_path, 'traces/network/'+trace+'.yml')
    with open(cp_path) as f:
        cp = yaml.load(f, Loader=yaml.SafeLoader)

    print(yaml.dump(cp))
    print('=========')
    print(yaml.dump(cp['Devices'][0]))
    print('=========')
    print(yaml.dump(cp['Devices'][0]['StaticRoutes']))
    return copy.deepcopy(cp)


def load_invariants(ws_path):
    """
    invariants yaml schema (incomplete):

    Reachability: [{Ingress, Egress, DstIp, SrcIp, Protocol, DstPort, SrcPort, MaxFailures}]
    """

    iv_path = os.path.join(ws_path, 'traces/invariants/'+trace+'.yml')
    with open(iv_path) as f:
        iv = yaml.load(f, Loader=yaml.SafeLoader)
    return copy.deepcopy(iv)


cp = load_network(ws_path)
iv = load_invariants(ws_path)

# map from device name to device
device_dict = {
    device['Name']: device
    for device in cp['Devices']
}

# map from interface name to interface
interface_dict = {
    interface['Name']: interface
    for device in cp['Devices'] for interface in device['Interfaces']
}

# map from policy name to policy
policy_dict = {}
for device in cp['Devices']:
    for policy in device['BgpConfig']['InboundPolicies']:
        policy_dict[policy['Name']] = policy
    for policy in device['BgpConfig']['OutboundPolicies']:
        policy_dict[policy['Name']] = policy
