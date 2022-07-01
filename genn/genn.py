#!python3

import os
import sys
import platform
import datetime

__author__ = "Lorenzo Lugli, riccardo tai huynh"
__license__ = "GPL"
__status__ = "Development"

boold = True
nameprogram = "etl.py"


def LogLog(text: str, last: bool):
    with open("./log/execute.log", "a") as fin:
        fin.write(text)
        if last:
            fin.write(100*"-" + "\n")


def Trace():
    with open("./log/execute.log", "a") as Trace:
        tracemsg = (f'Esecuzione {nameprogram} il {datetime.datetime.now()}\n')
        Trace.write(tracemsg)
        Trace.close()


def Main():
    print("----main----")


def WriteCsv(OutString):
    with open("./output.csv", "a") as CsvOut:
        CsvOut.write(OutString)


def Read():
    with open("../dump_dati_stazioni_VR.csv", "r") as CsvIn:
        Temps = []
        First = True
        for Line in CsvIn:
            if not First:
                Year = Line.split(",")[0].split("-")[1]
                print(Line)
                if Line.split(",")[0].split("-")[1] == "01":
                    print("----GENNAIO----")
                    if Year == LastYear:
                        Temps.append(Line.split(",")[2])
                        print(Line.split(",")[2])
                    else:
                        StazId = Line.split(',')[13].replace('\n','')
                        OutLine = (f"{Line.split(',')[0]},{StazId},{cal_average(Temps)},{max(Temps)},{min(Temps)},{float(max(Temps)) - float(min(Temps))}\n")
                        WriteCsv(OutLine)
                        Temps = []
                LastYear = Line.split(",")[0].split("-")[1]
            else:
                Year = Line.split(",")[0].split("-")[1]
                LastYear = Line.split(",")[0].split("-")[1]
                First = False
                WriteCsv("date,Statid,tmed,tmax,tmin,deltat\n")

def cal_average(num):
    sum = 0
    for e in num:
        if e == "":
            e = 0
        sum = sum + float(e)
    avg = sum/len(num)
    return float(f'{avg:.2f}')

if __name__ == "__main__":

    msg = "Esecuzione " + nameprogram + " con " + sys.version
    if boold:
        print(msg)

    plat = sys.platform
    if "win" in plat:
        os_comp = os.environ.get('COMPUTERNAME')
    if "linux" in plat:
        os_comp = os.environ.get('HOSTNAME')
    if "darwin" in plat:
        os_comp = platform.node()
    computer = os_comp

    humantime = datetime.datetime.now().strftime("%d/%m/%Y;%H:%M:%S")
    msg = computer + ";" + str(humantime) + ";" + msg + "\n"
    LogLog(msg, False)
    Trace()
    Read()
    msg = f"Termine esecuzione {nameprogram}"
    print(msg)
    msg = computer + ";" + str(humantime) + ";" + msg + "\n"
    LogLog(msg, True)
