#!/usr/bin/python
import decimal
import sys
import csv

"""
RTP seq no,WiFi seq no,Time,SignalStrength,DataRate
37613,4019,213.464,-93dBm,2
37614,4023,213.652,-93dBm,2
37615,4024,213.658,-95dBm,2
37615,4024,213.659,-94dBm,2
37616,4025,213.661,-93dBm,2
37616,4025,213.669,-94dBm,2
37616,4025,213.694,-94dBm,1
37618,4027,213.703,-91dBm,2
37618,4027,213.705,-95dBm,2
37618,4027,213.708,-94dBm,1
37619,4040,214.045,-93dBm,1
"""

dict={}
topN=int(sys.argv[3])
inFile = sys.argv[1]
outFile = sys.argv[2]
with open(inFile, 'r') as file:
    next(file)
    reader = csv.reader(file)
    list_of_rows = list(reader)

    for row in list_of_rows:
        #print(row)
        if row[0] in dict:
            #print("RTP %s already present"%(row[0]))
            currentValue=dict[row[0]]
            currentValue['objects'].append(row)
            if currentValue['start']>row[2]:
                currentValue['start']=row[2]

            if currentValue['end']<row[2]:
                currentValue['end']=row[2]
        else:
            emptyArray=[row]
            start=row[2]
            end=row[2]
            dict[row[0]] = {'objects':emptyArray,'start':start,'end':end}
            #print(dict[row[0]])

    with open(outFile,'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        rtpSorted=sorted(list_of_rows, key=lambda value: int(value[0]))
        #print(rtpSorted)
        for index,value in enumerate(rtpSorted[:-1]):
            diff = (decimal.Decimal(rtpSorted[index+1][2])) - (decimal.Decimal(rtpSorted[index][2]))
            #print(diff)
            writer.writerow([value[0],diff])

delaySorted=sorted(dict.items(), key=lambda value: decimal.Decimal(value[1]['end'])-decimal.Decimal(value[1]['start']), reverse=True)[:topN]
#print(delaySorted)
print("************** Printing Sorted Delay**************")
for item in delaySorted:
    tmp=item[1]
    total=str(len(tmp['objects']))
    retry=int(total)-1
    delay=str(decimal.Decimal(tmp['end'])-decimal.Decimal(tmp['start']))
    start=str(decimal.Decimal(tmp['start']))
    print("Total=%s,Retry=%s,Delay=%s,RTP=%s"%(total,retry,delay,item[0]))

retrySorted=sorted(dict.items(), key=lambda value: len(value[1]['objects']), reverse=True)[:topN]
#print(retrySorted)
print("************** Printing Sorted Retry**************")
for item in retrySorted:
    tmp=item[1]
    total=str(len(tmp['objects']))
    retry=int(total)-1
    delay=str(decimal.Decimal(tmp['end'])-decimal.Decimal(tmp['start']))
    start=str(decimal.Decimal(tmp['start']))
    print("Total=%s,Retry=%s,Delay=%s,RTP=%s"%(total,retry,delay,item[0]))
