
# coding: utf-8

# In[28]:

import numpy as np
import phonenumbers
from phonenumbers import geocoder
import sys
import os.path
from StringIO import StringIO

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
                outfile.write(names[key_name].decode('utf-8') +',' + key_name.decode('utf-8')                          +',' + numbers1[key_name].decode('utf-8') + ',' + str(geocoding[key_name]).decode('utf-8')                          + '\n')
            except UnicodeDecodeError:
                    print key_name
            
# If we organize all of the desired files in one directory, we can clean them all with one shot with the following 
# function

def clean_numbers_in_directory(directory):
    # This creates a list of filenames that we can loop through
    filenames = os.listdir(directory)
    
    for name in filenames:
        phone_number_cleaner(directory,name)
    
    
    


# In[29]:

my_dir = '/Users/lukemarrinan/Desktop/GiantOak/'
my_file = 'abdoulaye.csv'
my_file2 = 'rhino_horns.csv'
phone_number_cleaner(my_dir,my_file2)


# In[17]:




# In[ ]:



