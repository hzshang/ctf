#include <vector>
#include <iostream>
#include <utility>
#define MAX 15
#define PATH 0
#define OBSTACLE 1
#define PALACE 2
#define VISITED 3
using namespace std;
typedef struct {
    int **matrix;
    int col;
    int row;
} Matrix;

int power[15][15];
Matrix* mat;

size_t DFS(int x,int y);
size_t calc_num();

void set_power(int x,int y){
    /*assert mat->matrix[x][y] == PALACE*/
    int temp=-1;
    if( x == 0 || y == 0 || mat->matrix[x-1][y-1]!=PATH){
        temp++;
    }
    if( y == 0 || mat->matrix[x][y-1]!= PATH){
        temp++;
    }
    if( x + 1 == mat->row || y==0 || mat->matrix[x+1][y-1]!=PATH){
        temp++;
    }
    if( x == 0 || mat->matrix[x-1][y]!=PATH){
        temp++;
    }
    if( x + 1 == mat->row || mat->matrix[x+1][y] !=PATH){
        temp++;
    }
    if( x == 0 || y+1 == mat->col || mat->matrix[x-1][y+1]!=PATH){
        temp++;
    }
    if( y+1 == mat->col || mat->matrix[x][y+1]!=PATH){
        temp++;
    }
    if( y+1 == mat->col || x+1 == mat->row || mat->matrix[x+1][y+1]!= PATH){
        temp++;
    }
    power[x][y]=temp;
}
void unset_power(int x,int y){
    if( x == 0 || y == 0 || mat->matrix[x-1][y-1]==PALACE){
        power[x-1][y-1]--;
    }
    if( y == 0 || mat->matrix[x][y-1]==PALACE){
        power[x][y-1]--;
    }
    if( x + 1 == mat->row || y==0 || mat->matrix[x+1][y-1]!=PATH){
        power[]
    }
    if( x == 0 || mat->matrix[x-1][y]!=PATH){
        temp++;
    }
    if( x + 1 == mat->row || mat->matrix[x+1][y] !=PATH){
        temp++;
    }
    if( x == 0 || y+1 == mat->col || mat->matrix[x-1][y+1]!=PATH){
        temp++;
    }
    if( y+1 == mat->col || mat->matrix[x][y+1]!=PATH){
        temp++;
    }
    if( y+1 == mat->col || x+1 == mat->row || mat->matrix[x+1][y+1]!= PATH){
        temp++;
    }
}

inline void find_palace(int *x,int *y){
    int p=-1,q=-1,max=-1;
    for(int i=0;i<mat->row;i++){
        for (int j=0;j<mat->col;j++){
            if(mat->matrix[i][j] == PALACE &&power[i][j] > max){
                max=power[i][j];
                p=i;
                q=j;
            }
        }
    }
    *x=p;
    *y=q;
    return;
}
size_t DFS(int x,int y){
    /* assert mat->matrix[x][y]==VISITED*/
    size_t sum=0;
    if(x > 0){
        switch(mat->matrix[x-1][y]){
            case PALACE:
                mat->matrix[x-1][y]=VISITED;
                sum+=calc_num();
                mat->matrix[x-1][y]=PALACE;
                break;
            case PATH:
                mat->matrix[x-1][y]=VISITED;
                sum+=DFS(x-1,y);
                mat->matrix[x-1][y]=PATH;
                break;
            default:
                break;
        }
    }
    if( x<mat->row-1){
        switch(mat->matrix[x+1][y]){
            case PALACE:
                mat->matrix[x+1][y]=VISITED;
                sum+=calc_num();
                mat->matrix[x+1][y]=PALACE;
                break;
            case PATH:
                mat->matrix[x+1][y]=VISITED;
                sum+=DFS(x+1,y);
                mat->matrix[x+1][y]=PATH;
                break;
            default:
                break;
        }
    }
    if( y > 0){
        switch(mat->matrix[x][y-1]){
            case PALACE:
                mat->matrix[x][y-1]=VISITED;
                sum+=calc_num();
                mat->matrix[x][y-1]=PALACE;
                break;
            case PATH:
                mat->matrix[x][y-1]=VISITED;
                sum+=DFS(x,y-1);
                mat->matrix[x][y-1]=PATH;
                break;
            default:
                break;
        }
    }
    if( y < mat->col-1){
        switch(mat->matrix[x][y+1]){
            case PALACE:
                mat->matrix[x][y+1]=VISITED;
                sum+=calc_num();
                mat->matrix[x][y+1]=PALACE;
                break;
            case PATH:
                mat->matrix[x][y+1]=VISITED;
                sum+=DFS(x,y+1);
                mat->matrix[x][y+1]=PATH;
                break;
            default:
                break;
        }
    }
    return sum;
}
size_t calc_num(){
    int x,y;
    find_palace(&x,&y);
    if (x == -1){
        return 1;
    }
    /*assert mat->matrix[x][y]==PALACE*/
    mat->matrix[x][y]=VISITED;
    size_t sum=DFS(x,y);
    mat->matrix[x][y]=PALACE;
    return sum;
}

int main(){
    int m,n;
    mat=new Matrix();
    mat->matrix=new int*[MAX];
    for (int i=0;i< MAX;i++){
        mat->matrix[i]=new int[MAX];
    }
    while(1){
        cin>> m >> n;
        mat->row=m;
        mat->col=n;
        for (int i=0;i<m;i++){
            for (int j=0;j<n;j++){
                cin>>mat->matrix[i][j];
            }
        }
        for( int i=0;i<m;i++){
            for (int j=0;j<n;j++){
                if(mat->matrix[i][j]== PALACE)
                    set_power(i,j);
            }
        }
        cout<<calc_num()<<endl;
    }
}