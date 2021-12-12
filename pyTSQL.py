import datetime
import logging
datetimeFormat = "%Y%m%d%H%M%S%f"
path = "/path/to/sqlFiles/"
inputFilename = "{}/Create.sql".format(path)
outputFilename = "{}/Create{}.sql".format(path,datetime.datetime.now().strftime(datetimeFormat))
includeWord = "INCLUDE"

def log(level,location,message):
    global logger
    if logger == None:
        print(f"[{location}][level] {message}") 
    else:
        exec(f"logger.{level}('[{location}] {message}')")

try:
    logger = logging.getLogger("tsql")
    log("info","Logging","Logging Started")
except Exception as e:
    log("error","Logging",f"ERROR Starting Logging: {e}")
    logger = None
    
try:
    inputFile = open(inputFilename, 'r')
    outputFile = open(outputFilename,'w')
except Exception as e:
    log("error","Opening Files",f"ERROR Opening Files {e}")
else:
    lines = inputFile.readlines()
    inputFile.close()
    for line in lines:
        if line.strip().upper().startswith(includeWord.upper()):
            auxFilename = line[len(includeWord):].strip()
            auxPath = "{}/{}".format(path,auxFilename)
            outputFile.writelines([f"/* {includeWord} {auxFilename} */\r\n"])
            log("error","Aux",f"Reading {auxPath}")
            auxFile = open(auxPath, 'r')
            auxLines = auxFile.readlines()
            auxFile.close()
            outputFile.writelines(auxLines)
            outputFile.writelines([f"\r\n"])            
        else:
            outputFile.writelines([line])
    outputFile.close()
    log("error","tsql",f"Wrote `{outputFilename}`")
