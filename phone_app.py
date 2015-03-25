#!/home/anaconda/bin/python
import numpy as np
import phonenumbers
from phonenumbers import geocoder
import sys
import os.path
from StringIO import StringIO
import tangelo 
import json
import networkx as nx
from networkx.readwrite import json_graph

# This program will take in a csv file of the following format:
# "Source Name", "Person's phonenumber", "Name of Person" 
# It will return a file of the form 
# "Source Name" " Name of Person" "Person's phonenumber" "country of phonenumber"
# Note, this function can also be used to just loop through all of the files in a directory,
# provided that they are of the correct format

def phone_number_cleaner(directory,filename):
    
    # Grab the phone numbers csv in a three dimensional array
    numbers = np.genfromtxt(directory+filename,dtype=str,delimiter=',')
    
    # Now we need to reformat the numbers for the phonenumbers parser
    for i in range(len(numbers[:,1])):
        numbers[i,1] = ''.join(['+',numbers[i,1]])
    

    # Here we are creating a dictionary of names and phonenumber objects
    numbers1 = {}
    numbers2 = {}
    names = {}
    for i in range(len(numbers[:,1])):
        try:
            numbers2[numbers[i,2]]= phonenumbers.parse(numbers[i,1],region=None)
            numbers1[numbers[i,2]] = numbers[i,1]
            names[numbers[i,2]] = numbers[i,0]
        except:
            print i
            pass

    geocoding = {}    
    for key_name in numbers2.keys():
        geocoding[key_name] = geocoder.description_for_number(numbers2[key_name], "en")
    
    # print numbers2
    # print geocoding

    # Now we need to run through and write to a file 

    with open(directory + 'clean'+filename,'w') as outfile:
        # Now we run through the keynames
        for key_name in numbers2.keys():
            try:
                outfile.write(names[key_name].decode('utf-8') +',' + key_name.decode('utf-8') +',' + numbers1[key_name].decode('utf-8') + ',' + str(geocoding[key_name]).decode('utf-8')                          + '\n')
            except UnicodeDecodeError:
                    print key_name
    return 0
            


def geocode(phone_list):
    dat={}
    g=nx.Graph()
    for pn in phone_list:
        try:
	    g.add_edge(pn[0],pn[1])
            temp=phonenumbers.parse('+'+pn[1],region=None)
            pn.append(geocoder.description_for_number(temp,"en"))
            g.node[pn[1]]['country']=geocoder.description_for_number(temp,"en")		
        except:
            pass

    return json.dumps({'list':phone_list,'graph':json_graph.node_link_data(g)})


post_actions= {
        'geocode':geocode
}


@tangelo.restful
def post(action,*args,**kwargs):
        post_data=json.loads(tangelo.request_body().read())

        def unknown(**kwargs):
                return tangelo.HTTPStatusCode(400,"invalid service call")

        return post_actions.get(action,unknown)(**post_data)






