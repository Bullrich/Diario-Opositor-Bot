import redis
from Threader import start_investigation
import time

r = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)

# [... flask routing code, sql queries, etc. ...]

start_investigation()


time.sleep(1)
print('Publishing')
r.publish("sms_replies", "This is a test")

r.set("example", True)

print(r.get("example") == b"True")
print(r.get("example"))
print(str(r.get("example")))
r.delete("example")
print(r.get("example"))

print(r)
for x in range(0, 3):
    time.sleep(2)
    print('Sleeped: ' + str(x))