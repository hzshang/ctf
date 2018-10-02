#include <stdio.h>
int main(){
	void *t1=malloc(4);
	void *t2=malloc(4);
	void *t3=malloc(4);
	free(t1);
	free(t2);
	free(t3);
	return 0;
}
