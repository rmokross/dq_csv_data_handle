from datetime import datetime, timedelta, date
import imp
import json
import os

## ATTENTION
## this code mofified to run with a python 2.x interpreter

def getParameters(path):
    """reads parameters from the parameter file (input.conv)

    Args:
        path (str): full path to the parameter file : input.conv
    Return:
        params: object holding each parameter from the parameter file : input.conv
    """
    with open(path, 'rb') as f:
        params = imp.load_source('data', '', f)
    return(params)

def joadDict(path):
    """reads out all paths from the files.json. Path will be read out of the input.conv

    Args:
        path (str): full path to the files.json
    """
    with open(path, 'rb') as f:
        data = json.load(f)
    return(data)

def checkTimestamp(docs):
    """reads the doc name ending with the timestamp <GENERATED ON(YYYYMMTTHHMMSS)> and returns a date object:
    
~Die Dateien sollen der Namenskonvention  
~<AWS> _<OBJECTINF>_<ULTIMO(YYYYMMTT)>_<GENERATED ON(YYYYMMTTHHMMSS)>.csv

    Args:
        docs (str): name of a document
    """
    smp = docs.split('_')[-2]
    smp = smp.split('.')[0]
    t_stm = datetime.strptime(smp, '%Y%m%d')
    return(t_stm)

def generateUltimo():
    """returns the months ultimo of the previous month
    """
    first_of_this_month = date.today().month
    ultimo = first_of_this_month - timedelta(days=1)
    return(ultimo)

def processInput(data, days_back, ultimo):
    """will check all files within the paths defined in the files.json. If there are files within each directory from the past days 
    defined by the parameter DAYS_BACK from the input.conv, the function will return 1. If there are files missing, it will 
    return 0.

    Args:
        data (dict): dictionary with paths and systems from files.json 
        days_back (int): integer defining how large the timedelta can be in order to accept a file (<GENERATED ON(YYYYMMTTHHMMSS)>)
    """
    acceptance_day = ultimo - timedelta(days=days_back)
    keys = data.keys()
    available_docs = {key : 0 for key in keys}
    for key in data:
        try:
            doc_list = os.listdir(data[key])
            doc_list = [doc for doc in doc_list if checkTimestamp(doc)>=acceptance_day]
            if len(doc_list) != 0:
                available_docs[key] = 1
        except:
            available_docs[key] = 0
            print("Incorrect path: {}".format(data[key]))
    
    if 0 in available_docs.values():
        return(0)
    else:
        return(1)

def main(prof_path):
    
    params = getParameters(prof_path)
    sys_dict = joadDict(params.FILESET)

    processInput(sys_dict, int(params.DAYS_BACK))
if __name__ == '__main__':
    PROFILE = './config/input.conv'     
    main(PROFILE)

