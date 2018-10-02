#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
int main(){
	for(int c=0;c<256;c++){
		FILE *file=fopen("bin","w+");
		char tmp[2]={c,'c'};
		fwrite(tmp,1,2,file);
		fclose(file);
		char tmp2[]="12";
		FILE *file2=fopen("bin","r");
		fscanf(file2,"%s",tmp2);
		if(tmp2[1]!='c')
			printf("%d ",c);
	}
	return 0;
}
