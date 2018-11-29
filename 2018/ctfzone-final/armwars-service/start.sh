docker build -t armwars .
docker run -d -p 24311:80 -e HOSTIP=`ip addr | grep "100.100" | awk '{print$ 2}'` armwars