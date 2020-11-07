from pynput.mouse import Listener
import datetime
import csv
from multiprocessing import Process
import shelve
import time
import psutil


Shelf = shelve.open('ClickCounter')
Shelf['leftcounter'] = 0
Shelf['rightcounter'] = 0
Shelf.close

def on_click(x, y, button, pressed):
    if pressed:
        Shelf = shelve.open('ClickCounter')
        leftcounter = Shelf['leftcounter']
        rightcounter = Shelf['rightcounter']
        Shelf.close

        # print ('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
        if str(button) == 'Button.left':
            leftcounter += 1
        elif str(button) == 'Button.right':
            rightcounter += 1

        Shelf = shelve.open('ClickCounter')
        Shelf['leftcounter'] = leftcounter
        Shelf['rightcounter'] = rightcounter
        Shelf.close

        print('Left clicks:', str(leftcounter))
        print('Right clicks:', str(rightcounter))
        print('Total clicks:', str(leftcounter + rightcounter))
        print('__________________________________________________')


def CheckTime():
    while True:
        time.sleep(1)
        #Record every minute how many clicks were made and then resets the counter
        if str(datetime.datetime.now().strftime('%S')) == '58':
            timehour = (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            writefile = csv.writer(open('ClickerInfo.csv', 'a', newline=''))
            Shelf = shelve.open('ClickCounter')
            ProcessList = getListOfProcessSortedByMemory()
            TopProcess = str(ProcessList[0])[10:].split("'")[0]
            writefile.writerow([timehour, Shelf['leftcounter'], Shelf['rightcounter'], Shelf['leftcounter'] + Shelf['rightcounter'], TopProcess])
            Shelf['leftcounter'] = 0
            Shelf['rightcounter'] = 0
            print('Clicks Recorded!')
            Shelf.close



def RunClicker():
    with Listener(on_click=on_click) as listener:
        listener.join()




def getListOfProcessSortedByMemory():
#Thanks to https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/ for this code
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['name'])
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            # Append dict to list
            listOfProcObjects.append(pinfo);
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)

    return listOfProcObjects


#Runs the code in the background and records the number of clicks every min
if __name__ == '__main__':
    Process(target=RunClicker).start()
    Process(target=CheckTime).start()



'''
#To just run the counter in console - Does not record 
while True:
    RunClicker()
'''
