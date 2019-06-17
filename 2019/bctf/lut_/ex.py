with open('dis') as f:
    dis = f.read()

cons = []
cur = 0
while True:
    pos = dis.find('$0x',cur)
    if pos==-1:
        break
    tmp = dis[cur:pos]
    if tmp.find('movzbl %al,%eax') != -1:
        cons.append(0xff)
    if tmp.find('test   %rax,%rax') != -1:
        cons.append(0)
    end = dis.find(',',pos+1)
    cons.append(int(dis[pos+3:end],16))
    cur = end+1
cons = cons[3:]
d = []
for i in range(8):
    d.append(0xff<<(i*8))

lt = []
for i in range(8):
    lt.append([-1]*256)

cur = 0
res = {}
while cur < len(cons):
    idx = 0
    while cons[cur] > d[idx]:
        idx += 1
    msk = (1<<(8*idx))-1
    assert cons[cur]&msk == 0
    m = cons[cur]>>(8*idx)
    cur += 1
    assert cons[cur]&msk == 0
    val = cons[cur]>>(8*idx)
    cur += 1
    assert val<256
    res[cons[cur]] = (m,val,idx)
    cur += 1

for v in res.values():
    print v[0]
