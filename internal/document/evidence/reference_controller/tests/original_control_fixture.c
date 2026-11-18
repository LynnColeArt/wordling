/* Authored CONTROL-only tool. Apache-2.0. No private media or original software.
 * WP104 owns prepare/foreground lifetime; semantic readiness/export is WP105.
 */
#define _GNU_SOURCE
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

static void die(void) { _exit(91); }
static void write_all(int fd, const char *p, size_t n) {
    while (n) { ssize_t k=write(fd,p,n); if (k<=0) die(); p+=k; n-=(size_t)k; }
}
static int regular(const char *name, int flags) {
    int fd=open(name,flags|O_NOFOLLOW|O_CLOEXEC); struct stat st;
    if (fd<0 || fstat(fd,&st) || !S_ISREG(st.st_mode) || st.st_nlink!=1 || st.st_size>65536) die();
    return fd;
}
int main(int argc, char **argv) {
    if (argc==4 && !strcmp(argv[1],"mutate")) {
        if (!strcmp(argv[3],"late")) usleep(3000000); /* real bounded child deadline fault */
        else if (strcmp(argv[3],"healthy") && strcmp(argv[3],"early-exit") && strcmp(argv[3],"daemon")) die();
        int fd=regular(argv[2],O_RDWR|O_APPEND);
        write_all(fd,"PREPARED\n",9); if (fsync(fd)) die(); close(fd); return 0;
    }
    if (argc==5 && !strcmp(argv[1],"serve")) {
        if (strcmp(argv[3],"qmp.sock") || (strcmp(argv[4],"healthy") && strcmp(argv[4],"early-exit") && strcmp(argv[4],"daemon"))) die();
        int fd=regular(argv[2],O_RDONLY); close(fd);
        if (!strcmp(argv[4],"early-exit")) return 7;
        if (!strcmp(argv[4],"daemon")) { pid_t p=fork(); if (p<0) die(); if (p>0) return 0; }
        int listener=socket(AF_UNIX,SOCK_STREAM|SOCK_CLOEXEC,0);
        struct sockaddr_un address; memset(&address,0,sizeof address); address.sun_family=AF_UNIX;
        memcpy(address.sun_path,"qmp.sock",9);
        if (listener<0 || bind(listener,(struct sockaddr*)&address,sizeof address) || listen(listener,1)) die();
        /* No readiness or normal-stop claim in WP104. Real foreground persists
         * until actual retained P containment; no detached helper authority. */
        for (;;) pause();
    }
    return 92;
}
