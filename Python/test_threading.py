import time
from threading import Thread


def countdown(n):
    while n > 0:
        print 'T-minus{}'.format(n)
        n -= 1
        time.sleep(3)

t = Thread(target=countdown, args=(10,))
# t.daemon = True
t.start()

if t.is_alive():
    print 'Still running'
else:
    print 'Completed'
