#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Tue Jun 21

@author: Jerry

Clean OpenStreetMap Dataset
"""
import xml.etree.cElementTree as ET
import re
import codecs
import json
import time


"""
Wrangle the data and transform the shape of the data
into a json file. The output is a list of dictionaries
that looks like this:

{
  "type": "node", 
  "id": "505751513"  
  "amenity": "restaurant", 
  "name": "Steamworks", 
  "created": {
    "uid": "12859", 
    "changeset": "26757833", 
    "version": "6", 
    "user": "pbryan", 
    "timestamp": "2014-11-13T15:01:17Z"
  }, 
  "pos": [
    49.2848448, 
    -123.1105906
  ], 
  "contact": {
    "website": "http://www.steamworks.com/", 
    "phone": "1-604-689-2739"
  }, 
  "address": {
    "city": "Vancouver", 
    "street": "Water Street", 
    "housenumber": "375"
  }, 
  
}


The following things will be done:
- process 3 types of top level tags: "node", "way" and "relation".
- selected attributes of above three top level tags will be turned into regular key/value paires, except:
    - attributes in the CREATED array will be added under a key "created"
    - attributes for latitude and longitude will be added to a "pos" array.
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address".
- if the second level tag "k" value starts with "contact:", it should be added to a dictionary "contact"
- all other types of tag "k" from the second level will be ignored, which will not be used for this project.
 
- for "way" and "relation" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

will be turned into "node_refs" or "way_refs", like this: ["305896090", "1719825889"]      
"""

#define reglar expression for searching lower, lower_colon, problemchars strings
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#define reglar expression for searching street types
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#a list of attributes under a key "created"
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

#a list of attributes will add into top level of the dictinaries
K_FIELDS = ["shop", "name", "amenity", "cuisine", "maxspeed"]

#a list of expected street type will use for indexing the street types
expected = ["Street", "Avenue", "Boulevard", "Drive", 
            "Court", "Place", "Square", "Lane",
            "Road", "Trail", "Parkway", "Commons",
            "Broadway", "Mall", "Way", "Kingsway", 
            "Highway", "Mews","Alley","Crescent",
            "South", "Walk","East"]
            
# a dictinary of abbrivation and misspell street type mappings will use 
# to format the street names
mapping = { "St": "Street",
            "St.":"Street",
            "Steet": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "Blvd": "Boulevard",
            "Blvd,": "Boulevard",
            "W.": "West",
            "west": "West",
            "E.": "East",
            "Venue": "Avenue",
            "Broughton": "Broughton Street", 
            "Esplanade": "Esplanade Avenue", 
            "Terminal": "Terminal Avenue",
            "Jarvis": "Jervis Street",
            "Jervis": "Jervis Street",
            "2nd": "2nd Avenue" # only has 2nd Avenue, no 2nd Street in Vancouver
           }
           
# Format street tpye
def street_format(street):
    m = street_type_re.search(street)
    if m:
        street_type = m.group()
        if street_type in expected:
            return street
        elif mapping.has_key(street_type):
            street = re.sub(street_type_re, mapping[street_type], street)           
            return street
        else:
            street = re.sub(street_type_re, "", street).strip()            
            return street_format(street)
    else:
        return None

# Format US/CANADA Phone number to "1-123-456-7890" 
def phone_format(n): 
    n = re.sub('[^0-9]+','', n)    
    if len(n) == 10:
        n = "1" + n                                                                                                                                
    return format(int(n[:-1]), ",").replace(",", "-") + n[-1] 

    
#Format postcode to "V7J 2C1"(letter with uppercae and a space in the middle) 
def postcode_format(zip):
    """Format postcode like "V7J 2C1": letter with uppercae 
    and a space in the middle """    
    zip = re.sub('\W','', zip).upper()
    substrings = re.findall(r'([A-Z]\d[A-Z])(\d[A-Z]\d)', zip)
    if substrings: 
        clean_postcode = ' '.join(substrings[0])
        return clean_postcode
    else:
        return None

def process_colon(tag, contact, address):

#format phone number     
    if tag.attrib["k"] == "phone":
        contact["phone"] = phone_format(tag.attrib["v"])
                            
    elif tag.attrib["k"] =="website":
        contact["website"] = tag.attrib["v"]
                                
    elif lower_colon.search(tag.attrib["k"]):
        m = tag.attrib["k"].split(":", 1)
#processing attribute with "addr:xxxx"                                
        if m[0] == "addr":
            
            if m[1] == "postcode":
                zip = postcode_format(tag.attrib["v"])
                if zip != None:
                    address[m[1]] = zip

            if m[1] == "street":
                street = street_format(tag.attrib["v"])
                if street != None:
                    address[m[1]] = street
                    
            elif m[1] == "housenumber":
                address[m[1]] = tag.attrib["v"]
            
            elif m[1] == "city":
                address[m[1]] = tag.attrib["v"]
#processing attribute with "contact:xxxx" and add them to a "contact" array.                             
        elif m[0] == "contact":
            if m[1] == "phone":
                contact["phone"] = phone_format(tag.attrib["v"])
            else:
                contact[m[1]] = tag.attrib["v"]
    return contact, address

#read and shape all the elements that we need for this project    
def shape_element(element):
    node = {}
    created = {}
    address = {}
    contact = {}
    node_refs = []
    way_refs = []
    if element.tag == "node" or element.tag == "way" or element.tag == "relation":
        for elem in element.iter():
            node["type"] = element.tag
            
#add attribues of CREATED into "created" arrary             
            for key in CREATED:
                 if elem.get(key):
                    created[key] = elem.get(key)           
            if created != {}:
                node["created"] = created 
                
            if elem.get("id"):
                node["id"] = elem.get("id")
                
#add latitude and longitude to a "pos" array.            
            if elem.get("lat") and elem.get("lon"):
                node["pos"] = [float(elem.get("lat")), float(elem.get("lon"))]
            
            if elem.tag == "tag":
                for tag in elem.iter("tag"):
                    if not problemchars.search(tag.attrib["k"]):  
                        for k in K_FIELDS:
                            if tag.attrib["k"] == k:
                                node[k] = tag.attrib["v"]
                        contact, address = process_colon(tag, contact, address)
                                       
#if there is not street field in the address dictionary, then ignore the housenumber field     
                if "street" not in address.keys() and "housenumber" in address.keys():
                    del address["housenumber"]
                if address != {}:
                    node["address"] = address

#add "contact" array into node                    
                if contact != {}:
                    node["contact"] = contact

#add "node_refs" array into node            
            if elem.tag == "nd":
                for nd in elem.iter("nd"):
                    if nd.attrib["ref"]:
                        node_refs.append(nd.attrib["ref"])
                    if node_refs != []:
                        node["node_refs"] = node_refs

#add "way_refs" array into node            
            if elem.tag == "member":
                for mem in elem.iter("member"):
                    if mem.attrib["ref"]:
                        way_refs.append(mem.attrib["ref"])
                if way_refs != []:
                    node["way_refs"] = way_refs

        return node
    else:
        return None

#Iterating the osm file, shaping the data, then save them to json file 
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w", "utf-8") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def main():    
    start = time.clock()
    DATAFILE = "/Users/Jerry/Documents/nd/Wrangle/p3/vancouver_canada.osm"
    process_map(DATAFILE, False)
    end = time.clock()
    print "read: %f s" % (end - start)
    
#cleaning the OpenStreetMap dataset!
main()
   