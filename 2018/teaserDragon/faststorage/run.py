from hack import get_name

f=open("names","w+")
for i in range(0,64):
    f.write(get_name(i)+"\n")

f.close()

