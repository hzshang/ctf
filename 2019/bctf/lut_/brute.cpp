//g++ brute.cpp -lpthread -g -fPIE -no-pie -o brute
#include <iostream>
#include <vector>
#include <map>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

#include <sys/stat.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <stdint.h>
#include <pthread.h>
#include <iterator>
#include "lut.hpp"
#define ELF_ADD 0x100000
#define CORE 3
#define RANGE 95*95*95*95
//#define RANGE 95
uint8_t* print_pool = (uint8_t*)"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ";


uint64_t step = RANGE/CORE;

using namespace std;
struct args{
    uint64_t begin;
    uint64_t end;
};
static inline uint64_t get_value(uint64_t x){
    uint64_t tmp = 0;
    tmp |= (print_pool[x%95]);
    x/=95;
    tmp |= (print_pool[x%95])<<8;
    x/=95;
    tmp |= (print_pool[x%95])<<16;
    x/=95;
    tmp |= print_pool[x%95]<<24;
    return tmp;
}

struct args pool[CORE];
map<uint64_t,uint32_t> *M[CORE];
uint64_t f(uint64_t x){
    //TODO
    uint64_t ret = 0;
    for(int i=0;i<4;i++){
        ret ^=lut[i][x&0xff];
        x>>=8;
    }
    return ret;
}
uint64_t g(uint64_t x){
    //TODO
    uint64_t ret = 0;
    for(int i=4;i<8;i++){
        ret ^=lut[i][x&0xff];
        x>>=8;
    }
    return ret;
}

uint64_t enc(uint64_t x){
    uint64_t ret = 0;
    for(int i=0;i<8;i++){
        ret ^= lut[i][x&0xff];
        x>>=8;
    }
    return ret;
}
int msg[CORE];
int all_done(){
    int ret = 1;
    for(int i=0;ret && i<CORE;i++){
        ret &= msg[i];
    }
    return ret;
}
uint32_t find_hash(uint64_t k){
    std::map<uint64_t,uint32_t>::iterator it;
    for(int i=0;i<CORE;i++){
        it = M[i]->find(k);
        if(it != M[i]->end() ){
            return it->second;
        }
    }
    // bet 0 is not the answer...
    return 0;
}
void* work(void* arg){
    uint64_t idx = (uint64_t)arg;
    uint64_t begin = pool[idx].begin;
    uint64_t end = pool[idx].end;
    uint64_t cnt=0;
    M[idx] = new map<uint64_t,uint32_t>();
    for(uint64_t it = begin;it<end;it++){
        if(idx == 0 && cnt%0x10000 == 0 )
            printf("cnt:%016lx goal:%016lx\n",cnt,step);
        uint64_t value = get_value(it);
        M[idx]->insert(std::make_pair(0xb285ea907ddcdefc^f(value),value));
        cnt++;
    }
    printf("Thread:0x%02lx done!\n",idx);
    msg[idx] = 1;
    while(all_done()){
        sleep(1);
    }
    // now lookup
    for(uint64_t it = begin;it<end;it++){
        uint64_t value = get_value(it);
        uint64_t hash = g(value);
        uint32_t ret = find_hash(hash);
        if(ret != 0){
            printf("find!\n");
            printf("%016lx\n",((uint64_t)ret)|(value<<32));

            exit(0);
        }
    }
    return 0;
}


int mmain(){
    printf("%016lx\n",get_value(1));
}

int main(int argc,char *argv[],char *env[]){
    memset(msg,0,sizeof(msg));
    pthread_t threads[CORE];
    printf("every core step:%016lx\n",step);
    for(uint64_t i=0;i<CORE;i++){
        pool[i].begin = step*i;
        if(i != CORE-1)
            pool[i].end = step*(i+1);
        else
            pool[i].end = RANGE;
        pthread_create(&threads[i],NULL,&work,(void*)i);
    }
    for(int i=0;i<CORE;i++){
        pthread_join(threads[i],NULL);
    }
}


