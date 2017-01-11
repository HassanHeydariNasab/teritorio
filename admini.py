import random
Parto.update(minajxo=1000, materialo='argxento').where(Parto.id << list(random.sample(range(1,2500),100))).execute()
Parto.update(minajxo=100, materialo='oro').where(Parto.id << list(random.sample(range(1,2500),50))).execute()
