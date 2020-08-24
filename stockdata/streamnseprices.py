import arrow
import schedule
import time
import stockdata as sd

def job():
    print(f"START TIME : {arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')}")
    sd.downloadnsefnostockscurrentprice()
    sd.downloadnseallindicescurrentprice()
    sd.downloadnseintradaytoday()
    print(f"END TIME   : {arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')}")
    print("*********<DONE>*********\n")

def streamnseprices(delay=60, endtime='15:30'):
    schedule.clear()
    j1 = schedule.every(delay).seconds.do(job)
    j1.run()
    endtime = arrow.get(endtime,'HH:mm').format('HH:mm:ss')
    currtime = arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')
    prev_schedule_time = currtime
    while True:
        schedule.run_pending()
        next_schedule_time = arrow.get(schedule.next_run()).format('ddd MMM-DD-YYYY HH:mm:ss')
        print(f"Last run time       : {prev_schedule_time}\nNext scheduled time : {next_schedule_time}\n")
        prev_schedule_time = next_schedule_time
        time.sleep(delay)
        currtime = arrow.now().format('HH:mm:ss')
        if currtime > endtime: break

if __name__ == '__main__':
    streamnseprices()
    print("<COMPLETED>")
