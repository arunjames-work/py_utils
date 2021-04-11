import sys
import names
import random
import threading
import math
import time
import os

import uuid
import csv

import pandas as pd

from faker import Faker

fake = Faker()

main_current = 0


def startProgressBar():
    timer = threading.Thread(
        target=progressBar, args=(main_current, loopCount, 100,))
    timer.start()


def cleanOutputFile(fileName=r'output\HashFileLoad.csv'):
    if os.path.exists(fileName):
        os.remove(fileName)


def progressBar(current, total, barLength=20):
    while True:
        percent = float(main_current) * 100 / total
        arrow = '=' * int(percent/100 * barLength - 1) + '>'
        spaces = ' ' * (barLength - len(arrow))

        print('Progress: [%s%s] %d %%, count: %d' %
              (arrow, spaces, percent, main_current), end='\r')
        if main_current >= total:
            break
        time.sleep(1)


def loadAndWrite(local_loop_Count: int, fileName=r'output\HashFileLoad.csv', mode='a+', lockMode=True):
    global main_current
    with open(fileName, mode, newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        for i in range(local_loop_Count):
            genderId = random.randint(1, 2)

            genderInd = 'male'
            if genderId == 2:
                genderInd = 'female'

            fields = []

            fields.append(str(uuid.uuid4()))
            fields.append(names.get_first_name(gender=genderInd))
            fields.append(names.get_first_name())
            fields.append(names.get_last_name())
            fields.append(fake.date_of_birth(minimum_age=18, maximum_age=60))
            fields.append(random.randint(1001, 9999))
            if genderId == 1:
                fields.append('M')
            else:
                fields.append('F')
            fields.append(random.randint(1111111111, 9999999999))

            if lockMode:
                threadLock.acquire()
                writer.writerow(fields)
                main_current += 1
                threadLock.release()
            else:
                writer.writerow(fields)
                main_current += 1

            # progressBar(main_current, loopCount, 100)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Please insert the count as program argument.')
        exit(1)

    mode = 1

    threadLock = threading.Lock()

    if len(sys.argv) == 3:
        mode = sys.argv[2]

    start = time.time()

    loopCount = int(sys.argv[1])

    if mode == 1:
        cleanOutputFile()
        loadAndWrite(loopCount)
        startProgressBar()
    elif mode == 2:
        cleanOutputFile()
        threadCount = 5

        if(loopCount < 1000):
            threadCount = 1

        divider = math.ceil(loopCount / threadCount)

        threads = []
        for lc in range(threadCount):
            threads.append(threading.Thread(
                target=loadAndWrite, args=(divider,)))
            threads[lc].start()

        startProgressBar()

        for t in threads:
            t.join()

    else:
        cleanOutputFile(r'output\HashFileLoad.csv')
        threadCount = 5

        if(loopCount < 1000):
            threadCount = 1

        divider = math.ceil(loopCount / threadCount)

        threads = []
        for lc in range(threadCount):
            threads.append(threading.Thread(
                target=loadAndWrite, args=(divider, r'temp\temp'+str(lc)+'.csv', 'w', False)))
            threads[lc].start()

        startProgressBar()

        for t in threads:
            t.join()

        for fNum in range(threadCount):
            pd.read_csv(r'temp\temp'+str(fNum)+'.csv').to_csv(r'output\HashFileLoad.csv', sep=',', header=True, index=False, index_label=None, mode='a+', encoding=None, compression='infer', quoting=None, quotechar='"',
                                                              line_terminator=None, chunksize=None, date_format=None, doublequote=True, escapechar=None, decimal='.', errors='strict', storage_options=None)
    end = time.time()
    time.sleep(1)
    print('')
    print(f"Runtime of the program is {end - start}")

    print('Processing Completed Sucessfully.')
