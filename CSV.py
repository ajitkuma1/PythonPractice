import csv
import pprint

with open('CSVData.txt', 'r') as data:
    print(data.read())

with open ('CSVData.txt', 'a+') as file:
    file.write("\nswitch, 1.1.1.1, Banagalore")
    print(file.read())

f = open('CSVData.txt', 'r')   
dataList = csv.reader(f)
sdata = list(dataList)
print(sdata)
for i in sdata:
    device = sdata[0]
    ipAddress = sdata[1]
    location = sdata[2]
    print (f'{device} is located in {location} and can be reached on {ipAddress}')