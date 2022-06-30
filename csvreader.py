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
    FlagChangeDay = False
    First = True
    Temps = []
    LastDay = 1
    with open('./dump_dati_stazioni_VR.csv', "r") as CsvFile:
        for Line in CsvFile:
            Day = Line.split(",")[0].split("-")[2]
            if LastDay != Day:
                if not First:
                    DeltaT = float(max(Temps))-float(min(Temps))
                    DeltaTDec = float(f'{DeltaT:.2f}')
                    IdStaz = Line.split(',')[13].replace("\n", "")
                    OutString = (f"{Line.split(',')[0]},{IdStaz},{cal_average(Temps)},{max(Temps)},{min(Temps)},{DeltaTDec}\n")
                    WriteCsv(OutString)
                else:
                    First = False
                    WriteCsv("yyyy/mm/dd,IdStaz,average,maxtemp,mintemp,deltatemp\n")
                Temps = []
            LastDay = Line.split(",")[0].split("-")[2]
            Temperature = float(Line.split(",")[2])
            Temps.append(float(f'{Temperature:.2f}'))
            print(Line.split(",")[0])


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
