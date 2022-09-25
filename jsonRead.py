import json
import pprint

with open("jsonFile.json", "r") as data:
    #print(data.read)
    d = data.read()
    print(d)
    #d1 = json.load(d)
    #type(d1)
    #print(d1)
    #pprint.pprint(d1)
    k = json.loads(d)
    #type(k)
    print(k['interface']['description'])
    #print(f' valu of the variable K {k}')
#print(len(d1))
#print(d1[0])

#print(f'Json to dictionary {k}')

#for i in d1:
#    print()

#data = open ("jsonFile.json", "r")
#d = json.load(data)
#print(d)