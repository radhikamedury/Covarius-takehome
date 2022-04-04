import json
import csv
import pandas as pd
import os

def readFile(fname, oname):
#read json file
    filepath=os.path.abspath(fname)
    f=open(filepath, encoding="utf8")
    data=json.load(f)
    d=data
    f.close()
    mapping=cleanData(d)
    createCSV(mapping, oname)

def cleanData(d):
    mapping=[]
    #clean data
    c=0
    for record in d:
        c+=1
        while ' ' in record['bankName']:
            record['bankName']=record['bankName'].replace(' ','')
        mapping=checkValidity(record, mapping, c)
        mapping=createNewMapping(record, mapping)
    return mapping
    
    
def checkValidity(record, mapping, c):
    r={}
    #assume each record is valid initially and creates new mappings
    if len(record['ibanNumber'])>0:
        r['accountNumber']=record['ibanNumber']
        r['accountNumberType']='iban'
        mapping.append(r)
        return mapping
    else:
        if len(record['sortCode'])>0 and len(record['accountNumber'])>0:
            r['accountNumber']=record['sortCode']+record['accountNumber']
            r['accountNumberType']='gbDomestic'
            mapping.append(r)
            return mapping
        else:
            if len(record['unstructuredAccountNumber'])>0:
                r['accountNumber']=record['unstructuredAccountNumber']
                r['accountNumberType']='unstructured'
                mapping.append(r)
                return mapping
    #write errors to error file
    f=open(r"C:\Users\willi\Documents\errors.txt","w")
    print("Record "+str(c)+" not valid")
    f.write("Record "+str(c)+" not valid")
    f.close()
    return mapping

def createNewMapping(record, mapping):
    #bank name is the same as the input file
    mapping[-1]['bankName']=record['bankName']
    #branchCountry - 2 character ISO country code
    s=record['bankName'].split('-')
    mapping[-1]['branchCountry']=s[-1]
    #name1 mapping - length 30 characters
    if len(record['name1'])>30:
        mapping[-1]['name1']=record['name1'][:30]
    else:
        if len(record['name1'])!=0:
            mapping[-1]['name1']=record['name1']
        else:
            mapping[-1]['name1']='   '
    #name2 mapping -length 20 characters
    if len(record['name2'])>20:
        mapping[-1]['name2']=str(record['name2'][:20])
    else:
        if len(record['name2'])!=0:
            mapping[-1]['name2']=str(record['name2'])
        else:
            mapping[-1]['name2']='   '
    #userComments - remove non ascii characters
    if len(record['notes'])>30:
        s=record['notes'][:30]
    else:
        s=record['notes']
    mapping[-1]['userComments']=str(s.encode('ascii', errors='ignore'))
    mapping[-1]['userComments']=mapping[-1]['userComments'][1:]
    return mapping


def createCSV(mapping, oname):
    #use pandas to write to file, no difference if csv module used.
    result=pd.DataFrame(mapping)
    result.to_csv(oname, index=False, encoding='ascii')





