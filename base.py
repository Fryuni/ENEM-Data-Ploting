#!/usr/bin/env python3
import threading as thr
import enop
from time import sleep

sLocker = thr.Semaphore(6)
global count
class LocationError(Exception):
    def __init__(self, *args):
        self.args = tuple(map(str, args))

def getYear():
    import os
    dirname = os.path.basename(os.path.abspath('.'))
    if "Microdados ENEM " in dirname:
        year = int(dirname[16:])
        return year
    elif dirname == "ENEM-Data-Ploting":
        print("Program is running in debug mode for developers...")
        return 0
    else:
        raise LocationError("Program is not running in a default INEP directory")

def Logging():
    global count, during, Test
    while during:
        print('''Progress: [%s] %d/*
                \rActive Threads: %d''' % ('='*round(count/200000), count, thr.active_count()), end='\r\033[F\r')
        #print('Progress: [%s] %d/*' % ('='*round(count/200000), count), end='\r')

def Main():
    global count, during, Test
    Test = False
    during = True
    year = getYear()
    import DADOS.reader as rdr
    dataFile = open("DADOS/MICRODADOS_ENEM_"+str(year)+".csv", 'rb')
    data = rdr.Reader(dataFile, dlimit=';')
    ans = {}
    tgts = enop.setTgts(data.values, year, end=True)
    count = 0
    thr.Thread(target=Logging).start()
    for x in data:
    #for c in range(7000000):
        #sLocker.acquire()
        #x = next(data)
        #print(x[data.values[0]], end='\r')
        count += 1
        thr.Thread(target=enop.choice, args=(x, tgts, ans, sLocker)).start()
        #sLocker.release()
    while thr.active_count()>2:
        sleep(2)
    during = False
    from pickle import dump
    with open('dump.txt', 'wb') as fl:
        dump(ans, fl, 4)

if __name__=="__main__":
    Main()
