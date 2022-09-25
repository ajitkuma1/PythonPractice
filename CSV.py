import csv

with open('CSVData.txt', 'r') as data:
    print(data.read())

with open ('CSVData.txt', 'a+') as file:
    file.write("\nswitch, 1.1.1.1, Banagalore")
    print(file.read())

f = open('CSVData.txt', 'r')   
dataList = csv.reader(f)
sdata = list(dataList)
print(sdata)
f.close()