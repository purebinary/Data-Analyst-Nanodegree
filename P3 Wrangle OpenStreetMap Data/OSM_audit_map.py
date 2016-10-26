# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21

@author: Jerry

Audit OpenStreetMap Dataset
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", 
            "Court", "Place", "Square", "Lane",
            "Road", "Trail", "Parkway", "Commons",
            "Broadway", "Mall", "Way", "Kingsway", 
            "Highway", "Mews","Alley","Crescent",
            "Walk"]


def count_tags(filename):
    """Count total numbers for each tag in OSM file, return dictionary with
    tag name and its count number"""
    tags = {}
    file = open(filename,'r')
    for _, elem in ET.iterparse(file):
        if elem.tag in tags:
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    return tags

#Count total numbers of second level "k" classified
#by "lower", "lower_colon", "problemchars" and "other" 4 groups

def key_type(element, keys):
    if element.tag == "tag":
        
        if lower.search(element.attrib['k']):
            keys["lower"] += 1
        
        elif lower_colon.search(element.attrib['k']):
            keys["lower_colon"] += 1

        elif problemchars.search(element.attrib['k']):
            print element.attrib["k"]            
            keys["problemchars"] += 1

        else:        
            keys["other"] += 1
    return keys

def audit_key(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

#Check if the street type is in expected list
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name.strip())
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

#Audit the second level "k" field with lower_colon in it 
def audit_address(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    other_colon_types = set()
    other_types = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:street":
                    audit_street_type(street_types, tag.attrib["v"])
                elif lower_colon.search(tag.attrib["k"]):
                    other_colon_types.add(tag.attrib["k"])
                else:
                    other_types.add(tag.attrib["k"])
    osm_file.close()
    return street_types, other_colon_types, other_types
    
#Audit phone number's format
def audit_phone(osmfile):
     osm_file = open(osmfile, "r")
     phone = []
     for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node":
            for tag in elem.iter("tag"):
                if tag.attrib["k"] == "phone":
                    phone.append(tag.attrib["v"])
     osm_file.close()     
     return phone

#Audit postcode's format
def audit_postcode(osmfile):
     osm_file = open(osmfile, "r")
     postcode = []
     for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node":
            for tag in elem.iter("tag"):
                if tag.attrib["k"] == "addr:postcode":
                    postcode.append(tag.attrib["v"])
     osm_file.close()     
     return postcode     


DATAFILE = "/Users/Jerry/Documents/nd/Wrangle/p3/sample_k50.osm"

tags = count_tags(DATAFILE)
pprint.pprint(tags)

keys = audit_key(DATAFILE)
pprint.pprint(keys)

street_types, other_colon_types, other_types = audit_address(DATAFILE)
pprint.pprint(street_types)
pprint.pprint(other_colon_types)
pprint.pprint(other_types)

phone = audit_phone(DATAFILE)
pprint.pprint(phone[:10])

postcode = audit_postcode(DATAFILE)
pprint.pprint(postcode[:10])
