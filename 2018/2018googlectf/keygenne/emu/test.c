#include <asm/unistd.h>
#include <errno.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/types.h>
#include <sys/xattr.h>
#include <unistd.h>
#define LENGTH 0x18
#define BUF_SIZE 0x18

//BPF system call filter.
const struct sock_filter execve_filter[] = {

    BPF_STMT(BPF_LD | BPF_ABS, offsetof(struct seccomp_data, nr)),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_umask, 1, 0),
    // Permit this system call.
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO),
};

const struct sock_fprog execve_filter_program = {
    .len = sizeof(execve_filter) / (sizeof(execve_filter[0])),
    .filter = (struct sock_filter*)execve_filter
};

// Install the seccomp filter.
static void disable_execve(void) {
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0) {
        abort();
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &execve_filter_program) != 0) {
        abort();
    }
}

#include <stdio.h>
#include <stdlib.h>
int main(){
	disable_execve();

    printf("%s\n",getenv("PWD"));
	return 0;
}
