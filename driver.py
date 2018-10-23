# for m in range(1, 7):
#     if m in [1, 3, 5, 7]:
#         days = range(1, 32)
#     if m in [4, 6]:
#         days = range(1, 31)
#     if m in [2]:
#         days = range(1, 29)
#     for d in days:
#         if m == 1 and d  <14:
#             continue
#         for h in range(1, 25):
#             if m == 1 and d<15 and h <12:
#                 continue
#             if m == 6 and d == 30 and h > 6:
#                 continue
#             print '{}/{}/2008{}'.format(d, m, h)
from apscheduler.schedulers.background import BackgroundScheduler

def fn():
    print ("Hello, world")


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(fn, trigger='cron', second=59)