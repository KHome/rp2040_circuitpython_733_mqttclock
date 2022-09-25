from watchdog import WatchDogMode
import time
import neopixel

# wait time to catch a debugging session
time.sleep(10)

w.timeout=8 # Set a timeout of 8 seconds
w.mode = WatchDogMode.RESET
w.feed()
print('feed_wd');
for i = 1 to 7:
    print(i)
    time.sleep(1)
w.feed()
#w.deinit()
print('after 7 sec no reset, ok')
print('No dont feed')
for i = 1 to 10:
    print(i)
    time.sleep(1)
print(' If you can read this, than Watchdog failed to bite')
