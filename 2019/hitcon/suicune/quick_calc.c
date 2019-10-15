/*
 * quick_calc.c
 * Copyright (C) 2019 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdint.h>
#include <string.h>
uint64_t times[0x100];
uint64_t lazy_sort_step[] = {0x0,
    0x0000000000000001-1,0x0000000000000002-1,
    0x0000000000000006-1,0x0000000000000018-1,
    0x0000000000000078-1,0x00000000000002d0-1,
    0x00000000000013b0-1,0x0000000000009d80-1,
    0x0000000000058980-1,0x0000000000375f00-1,
    0x0000000002611500-1,0x000000001c8cfc00-1,
    0x000000017328cc00-1,0x000000144c3b2800-1,
    0x0000013077775800-1,0x0000130777758000-1,
    0x0001437eeecd8000-1,0x0016beecca730000-1,
    0x01b02b9306890000-1,0x21c3677c82b40000-1,
    0xffffffffffffffff,0xffffffffffffffff,
};
uint64_t calc(uint64_t n){
    if(times[n] != 0)
        return times[n];
    uint64_t result = (n-1)*(calc(n-1)+calc(n-2));
    times[n] = result;
    return result;
}
uint64_t bubble_sort(uint8_t* data,int length){
    uint64_t count = 0;
    for(int j=length-2;j>=0;j--){
        if(data[j+1]>data[j]){
            int iter = length-1;
            while(iter>j){
                //find the first bigger than data[j]
                if( data[iter] > data[j])
                    break;
                iter--;
            }
            uint64_t left_dis = iter - j;
            //            printf("left_dis %d sort step %d\n",left_dis,lazy_sort_step[length-j-1]);
            count += left_dis * lazy_sort_step[length-j-1];
            // sort
            uint8_t tmp = data[j];
            memmove(&data[j],&data[j+1],left_dis);
            data[iter] = tmp;
        }
    }
    return count;
}

uint64_t calc_array_status(uint8_t* data,int length,uint64_t count){
    uint64_t cost = 0;
    uint64_t tmp_cost=0;
    for(int j=length-2;count > 0 && j>=0;j--){
        if(data[j+1]>data[j]){
            int iter = length-1;
            while(iter>j){
                //find the first bigger than data[j]
                if( data[iter] > data[j])
                    break;
                iter--;
            }
            for(; count && iter > j;iter--){
                count--;
                cost++;
                uint8_t tmp = data[j];
                data[j] = data[iter];
                data[iter] = tmp;
                if(count > lazy_sort_step[length-j-1]){
                    //ok
                    count -= lazy_sort_step[length-j-1];
                    cost += lazy_sort_step[length-j-1];
                }else{
                    uint8_t ex_buffer[0x100];
                    memcpy(ex_buffer,&data[j+1],length-1-j);
                    for(int tmp_i = 0;tmp_i<length-j-1;tmp_i++){
                        data[tmp_i+j+1] = ex_buffer[length-j-2-tmp_i];
                    }
                    tmp_cost = calc_array_status(&data[j+1],length-j-1,count);
                    cost += tmp_cost;
                    count -= tmp_cost;
                }
            }
        }
    }
    return cost;
}


/*
int main(){
    uint8_t buffer[] = {1,2,3,4,5,6,7,8,9,10};
    uint64_t max = 22;
    uint64_t cost = calc_array_status(buffer,sizeof(buffer),max);
    for(int i=0;i<sizeof(buffer);i++){
        printf("%x ",buffer[i]);
    }
    puts("");
    printf("max %ld \ncost %ld\n",max,cost);
}
*/




uint8_t mallocBuffer[0x1000];
int lazysort(uint8_t *data,int length){
    // return loop rounds
    int times = 0;
    while(1){
        times++;
        int i = length-1;
        int j = i-1;
        while(j>=0){
            if(data[j] < data[i]){
                break;
            }
            j--;
            i--;
        }
        if(j<0)
            return times;
        // locate exchange idx
        int x = length-1;
        for(;x>j;x--){
            // find the last bigger than data[j]
            if(data[x] > data[j])
                break;
        }
        assert(x > j);
        // exchange
        uint8_t exchange = data[j];
        data[j] = data[x];
        data[x] = exchange;
        
        // reverse the left
        uint8_t *buffer = mallocBuffer;
        memcpy(buffer,&data[j+1],length-1-j);
        for(int iter = 0; iter < length-1-j ; iter++){
            data[iter+j+1] = buffer[length-2-j-iter];
        }

    }
}
void lazysortTest(){
    uint8_t data[0x100];
    for(int length = 2;length<9;length++){
        for(int i=0;i<length;i++){
            data[i] = i;
        }
        int rounds = lazysort(data,length);
        printf("rounds(%d):%d\n",length,rounds);
    }
    puts("");
}





