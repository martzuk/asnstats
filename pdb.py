#!/usr/bin/env python
import requests
import argparse

# Definte parameters
apiurl = 'https://www.peeringdb.com/api/'

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--asn", help="ASN to lookup")
args = parser.parse_args()
if args.asn:
    asn = str(args.asn)
else:
    print "No ASN specified"

def lookup_net_id(asn):
    url = apiurl + 'net?asn=' + asn
    json = requests.get(url).json()
    net_id = str(json['data'][0]['id'])
    return net_id

def get_statistics(asn):
    url = apiurl + 'net/' + lookup_net_id(asn)
    json = requests.get(url).json()
    print "Name: " + json['data'][0]['name']
    print "Number of IXPs present at: " + str(len(json['data'][0]['netixlan_set']))
    print "IXP port sizes: "
    port_sizes = {}
    for i in json['data'][0]['netixlan_set']:
        if not port_sizes.get(i['speed']):
            port_sizes[(i['speed'])] = 1
        else:
            port_sizes[(i['speed'])] += 1
    keylist = port_sizes.keys()
    keylist.sort()
    for i in keylist:
        if i < 1000:
            speed = str(i) + "M"
        else:
            speed = str(i/1000) + "G"
        print "    " + speed + " " + str(port_sizes[i])
    print "Number of private facilities present at: " + str(len(json['data'][0]['netfac_set']))
get_statistics(asn)
