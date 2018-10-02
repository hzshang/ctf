from ubuntu:18.04

run sed -i -e "s/# deb-src/deb-src/" /etc/apt/sources.list
run apt update
run apt install -y qemu-user simh python sudo
run apt install -y xinetd
#run apt install -y vim qemu-user flex simh build-essential qemu-user flex simh build-essential git python sudo curl git bison libmpfr-dev libmpc-dev libgmp-dev gawk
#run apt install -y autoconf automake autotools-dev curl libmpc-dev libmpfr-dev libgmp-dev libusb-1.0-0-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev device-tree-compiler pkg-config libexpat-dev
#run apt install -y python-bitstring
run apt install -y libc6-arm64-cross
run apt install -y libc6-mipsel-cross

# for riscv
run apt install -y device-tree-compiler

# for mix
run apt install -y guile-2.2-libs
#run apt build-dep qemu-user gcc gdb


# COPY service.conf /service.conf
# COPY platforms /platforms
# COPY fucking-mdk /nonexistent/.mdk
# COPY fucking-usr-mdk /usr/share/mdk
# COPY scripts /scripts
run touch /score
CMD ["/usr/sbin/xinetd", "-filelog", "-", "-dontfork", "-f", "/service.conf"]
