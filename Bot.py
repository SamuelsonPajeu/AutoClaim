import Vars
import time
import schedule
import threading
import random
from datetime import datetime
from Function import simpleRoll, watchMessages
from i18n import get_text

try:
    from icecream import ic
except ImportError:
    ic = lambda *args: print(*args) if args else None

nextMinute = None

lang = Vars.language

def scheduleNextRoll():
    global nextMinute
    lang = Vars.language
    schedule.clear()
    
    if Vars.repeatBetween:
        minMinute = int(Vars.repeatMinute)
        maxMinute = int(Vars.repeatBetween)
        nextMinute = random.randint(minMinute, maxMinute)
    else:
        nextMinute = int(Vars.repeatMinute)
    
    now = datetime.now()
    currentMinute = now.minute
    currentHour = now.hour
    
    nextHour = (currentHour + 1) % 24
    
    timeString = f'{nextHour:02d}:{nextMinute:02d}'
    
    schedule.every().day.at(timeString).do(lambda: [simpleRoll(), scheduleNextRoll()])
    print(get_text('log_next_execution_full', lang, hour=nextHour, minute=nextMinute))
    return nextMinute

print('='*50)
print(get_text('log_bot_started', lang))
print('='*50)
ic(Vars.desiredSeriesMode)
ic(Vars.minCardPowerMode)
ic(Vars.desiredKakerasMode)
ic(Vars.wishlistMode)

if Vars.repeatBetween:
    print(get_text('log_random_execution', lang, min=Vars.repeatMinute, max=Vars.repeatBetween))
else:
    print(get_text('log_fixed_execution', lang, min=Vars.repeatMinute))

print('='*50)

if Vars.runImmediately:
    simpleRoll()

scheduleNextRoll()

watchThread = threading.Thread(target=watchMessages, daemon=True)
watchThread.start()

while True:
    schedule.run_pending()
    time.sleep(1)
