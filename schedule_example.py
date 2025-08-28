import schedule
import time
import datetime

def job():
    with open('schedule_log.txt', 'a') as f:
        f.write(f'Job ran at: {datetime.datetime.now()}\n')
    print("Scheduled job is running...")

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)