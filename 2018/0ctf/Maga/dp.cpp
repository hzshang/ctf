#include <iostream>
#include <set>
#define MAX 15
#define PATH 0
#define OBSTACLE 1
#define PALACE 2
using namespace std;
/*
0 可分配
1 一条边待匹配，有节点相连
2 一条边待匹配，无节点相连
3 已匹配
*/

int matrix[MAX][MAX];
int N;
set<int> *pool;
set<int> *dev;

void swap(){
    set<int> *temp;
    temp=pool;
    pool=dev;
    dev=temp;
}

static inline size_t encode(int *array){
    size_t p=0;
    size_t pow=1;
    for(int i=0;i<N;i++){
        p+=array[i]*pow;
        pow*=4;
    }
    return p;
}
static inline void decode(int *array,int n){
    size_t p=4;
    for(int i=0;i<N;i++){
        array[i]=n%p;
        p*=4;
    }
}

/*
0 可分配
1 一条边待匹配，有节点相连
2 一条边待匹配，无节点相连
3 已匹配
*/

size_t ans(){
    pool=new set<int>();
    int* temp=new int[N];

    for(int i=0;i<N;i++){
        temp[i]=3;
    }
    pool->insert(encode(temp));
    size_t sum=0;
    // 0 可用，1 待匹配，-1 已匹配
    for(int i = 0; i < N;i++){
        // j == 0
        while(!pool->empty()){
            decode(temp,*(pool->begin()));
            switch(matrix[i][0]){
                case PALACE:
                    if(temp[0] == 1){
                        temp[0]=-1;
                        push_N(dev,temp);
                    }else{ //temp[0]== -1 or 0
                        temp[0]=1;
                        push_N(dev,temp);
                    }
                    break;
                case OBSTACLE:
                    if(temp[0] != 1){
                        temp[0]=-1;
                        push_N(dev,temp);
                    }
                    break;
                case PATH:
                    if(temp[0] == 1){
                        temp[0]=1;
                        push_N(dev,temp);
                    }else{
                        temp[0]=0;
                        push_N(dev,temp);
                    }
                    break;
            }
        }
        swap();

        for(int j=1;j < N;j++){
            /*init new state */
            sum=0;
            while(!pool->empty()){
                pop_N(pool,temp);
                switch(matrix[i][j]){
                    case PALACE:
                        if(temp[j] == 1){
                            temp[j]=-1;
                            push_N(dev,temp);
                        }else{
                            temp[j]=1;
                            push_N(dev,temp);
                            if(temp[j-1]==1){
                                temp[j]=temp[j-1] = -1;
                                push_N(dev,temp);
                            }else if(temp[j-1]==0){
                                temp[j]=-1;
                                temp[j-1]=1;
                                push_N(dev,temp);
                            }
                        }
                        break;
                    case PATH:
                        if(temp[j] != 1){
                            temp[j]=0;
                            push_N(dev,temp);
                            if(temp[j-1]==1){
                                temp[j]=1;
                                temp[j-1]=-1;
                                push_N(dev,temp);
                            }else if(temp[j-1] == 0){
                                temp[j-1]=temp[j]=1;
                                push_N(dev,temp);
                            }
                        }else{
                            push_N(dev,temp);
                            if(temp[j-1]==1){
                                temp[j]=temp[j-1]=-1;
                                push_N(dev,temp);
                            }
                        }
                        break;
                    case OBSTACLE:
                        if(temp[j] != 1){
                            temp[j]=-1;
                            push_N(dev,temp);
                        }
                        break;
                }
            }
            swap();
        }
    }
    size_t sum=0;
    while(!pool->empty()){
        int mark=1;
        for(int i=0;i<N;i++){
            if(pool->back() == 1){
                mark=0;
            }
            pool->pop_back();
        }
        sum+=mark;
    }
    return sum;
}
int main(){
    while (true){
        cin>>N;
        for(int i=0;i<N;i++){
            for(int j=0;j<N;j++){
                cin>>matrix[i][j];
            }
        }
        cout<<ans()<<endl;
    }
}