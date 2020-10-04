import arrow
import schedule
import time
import stockdata as sd

def job():
    print(f"START TIME : {arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')}")
    # sd.downloadnsefnostockscurrentprice()
    # sd.downloadnseallindicescurrentprice()
    # sd.downloadnseintradaytoday()
    sd.downloadmysymbolscurrentprice()
    print(f"END TIME   : {arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')}")
    print("----------------<DONE>----------------\n")

def streamnseprices(delay=20, endtime='15:30'):
    endtime  = arrow.get(endtime,'HH:mm').format('HH:mm:ss')
    currtime = arrow.now().format('HH:mm:ss')
    while True:
        job()
        print(f"Next Run   @ {arrow.now().shift(seconds=+delay).format('ddd MMM-DD-YYYY HH:mm:ss')}")
        time.sleep(delay)
        currtime = arrow.now().format('HH:mm:ss')
        day = arrow.now().format('d')
        if day == '6' or day == '7' or currtime >= endtime:
            print(f"# Run Completed for {arrow.now().format('ddd MMM-DD-YYYY')} #")
            print('*****************<END*****************\n')
            break
