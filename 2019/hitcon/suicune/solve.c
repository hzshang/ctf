#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>


#include "global.h"

size_t hexs2bin(const char *hex, unsigned char **out);
typedef struct Rand_{
    uint64_t append;
    uint64_t value;
} Rand;
int comp(const void * elem1, const void * elem2) 
{
    uint8_t f = *(uint8_t*)elem1;
    uint8_t s = *(uint8_t*)elem2;
    if (f > s) return  1;
    if (f < s) return -1;
    return 0;
}
uint32_t randval(Rand *r){
    uint64_t val = r->value;
    r->value = r->value*0x5851F42D4C957F2D + r->append;
    uint32_t tmp = (val^(val>>18))>>27;
    uint32_t offset = val >> 59;
    return (tmp>>offset) | (((tmp&(1<<offset)-1))<<(32-offset));
}
void init_rand(Rand* r,uint16_t seed){
    r->append = 1;
    r->value = ((uint32_t)seed) * 0x5851F42D4C957F2D + 0x5851F42D4C957F2E;
}
Rand seed;
uint8_t pool[0x10][0x100];
uint64_t rand_table(uint8_t *table,int length){
    for(int i=length-1;i>=1;i--){
        int v = randval(&seed)%(i+1);
        uint8_t tmp = table[v];
        table[v] = table[i];
        table[i] = tmp;
    }
    uint64_t a = randval(&seed);
    uint64_t b = randval(&seed);
    uint64_t counts = (b<<32)|a;
    return counts;//wtf!!!
}
void reverse_array(uint8_t *array,int length);

void decrypt(uint8_t* enc,uint8_t* pt,int length,uint16_t key){
    init_rand(&seed,key);
    for(int i=0;i<0x10;i++){
        memcpy(pool[i],origin,sizeof(origin));
        uint64_t max_cost = rand_table(pool[i],0x100);
        uint8_t wtf[0x100];
        
//        memcpy(wtf,pool[i],0x100);
        calc_array_status(pool[i],length,max_cost);
        reverse_array(pool[i],length);
//        qsort(pool[i],length,1,comp);
//        asm("int $3");
    }
    uint8_t *tmp = malloc(length);
    memcpy(pt,enc,length);
    for(int i=0;i<0x10;i++){
        memcpy(tmp,pt,length);
        for(int j=0;j<length;j++){
            pt[length-1-j] = tmp[j]^pool[0xf-i][j];
        }
    }
    free(tmp);
}
int printable(uint8_t* data,int length){
    for(int i=0;i<length;i++){
        if(!isprint(data[i]))
            return 0;
    }
    return 1;
}


int main(int argc,char* argv[]){
    uint8_t buffer[0x100];
    memset(buffer,0,0x100);
    uint8_t *enc = "04dd5a70faea88b76e4733d0fa346b086e2c0efd7d2815e3b6ca118ab945719970642b2929b18a71b28d87855796e344d8";
    uint8_t* ct;
    int length = strlen(enc)/2;
    hexs2bin(enc,&ct);
    for(uint32_t key=0;key<0x10000;key++){
        memset(buffer,0,0x100);
        decrypt(ct,buffer,length,key);
        printf("%s\n",buffer);
        if(key%0x100 == 0){
            fprintf(stderr,"key 0x%04x\n",key);
        }
    }
}


