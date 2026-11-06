/* Source-owned bounded TEST fixture. No guest, VM, private resource or original. */
#define _GNU_SOURCE
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static void die(const char *s){perror(s);exit(71);}
static int same(const char *a,const char *b){return strcmp(a,b)==0;}
static void pause_ms(long ms){struct timespec t={ms/1000,(ms%1000)*1000000};while(nanosleep(&t,&t)<0&&errno==EINTR){}}
static void write_all(int fd,const void *raw,size_t size){const char *p=raw;while(size){ssize_t n=write(fd,p,size);if(n<=0)die("write");p+=n;size-=(size_t)n;}}
static void append(const char *path,const char *raw){int fd=open(path,O_WRONLY|O_APPEND|O_NOFOLLOW|O_CLOEXEC);if(fd<0)die("append");write_all(fd,raw,strlen(raw));if(fsync(fd))die("fsync");if(close(fd))die("close");}
static void output_file(const char *path,const char *input,int corrupt){int out=open(path,O_WRONLY|O_TRUNC|O_NOFOLLOW|O_CLOEXEC);if(out<0)die("output");if(input){int in=open(input,O_RDONLY|O_NOFOLLOW|O_CLOEXEC);if(in<0)die("input");char buf[4096];size_t total=0;for(;;){ssize_t n=read(in,buf,sizeof(buf));if(n<0)die("read");if(!n)break;total+=(size_t)n;if(total>65536)exit(72);if(corrupt)buf[0]^=1;write_all(out,buf,(size_t)n);}close(in);}if(fsync(out))die("fsync");close(out);}
static void send_text(int fd,const char *s){write_all(fd,s,strlen(s));}
static int listener(const char *name){int s=socket(AF_UNIX,SOCK_STREAM|SOCK_CLOEXEC,0);if(s<0)die("socket");struct sockaddr_un a;memset(&a,0,sizeof(a));a.sun_family=AF_UNIX;if(strlen(name)>=sizeof(a.sun_path))exit(73);strcpy(a.sun_path,name);if(bind(s,(struct sockaddr *)&a,sizeof(a))||listen(s,1))die("bind/listen");return s;}
static int inherited_listener(const char *name){
 int pair[2];if(socketpair(AF_UNIX,SOCK_DGRAM|SOCK_CLOEXEC,0,pair))die("socketpair");
 pid_t child=fork();if(child<0)die("fork inherited");
 char value='F';struct iovec io={&value,1};char control[CMSG_SPACE(sizeof(int))];memset(control,0,sizeof(control));struct msghdr m;memset(&m,0,sizeof(m));m.msg_iov=&io;m.msg_iovlen=1;m.msg_control=control;m.msg_controllen=sizeof(control);
 if(child==0){close(pair[0]);int fd=listener(name);struct cmsghdr *c=CMSG_FIRSTHDR(&m);c->cmsg_level=SOL_SOCKET;c->cmsg_type=SCM_RIGHTS;c->cmsg_len=CMSG_LEN(sizeof(int));memcpy(CMSG_DATA(c),&fd,sizeof(fd));if(sendmsg(pair[1],&m,0)!=1)die("sendfd");close(fd);close(pair[1]);pause_ms(200);_exit(0);}
 close(pair[1]);if(recvmsg(pair[0],&m,0)!=1)die("recvfd");struct cmsghdr *c=CMSG_FIRSTHDR(&m);if(!c||c->cmsg_level!=SOL_SOCKET||c->cmsg_type!=SCM_RIGHTS||c->cmsg_len!=CMSG_LEN(sizeof(int)))exit(78);int fd;memcpy(&fd,CMSG_DATA(c),sizeof(fd));close(pair[0]);return fd;
}
static int serve(const char *working,const char *name,const char *mode){
 if(same(mode,"early-exit"))return 0;
 if(same(mode,"foreign-peer")){
  pid_t child=fork();if(child<0)die("fork");if(child>0){int status;while(waitpid(child,&status,0)<0&&errno==EINTR){}return 0;}
 }
 int s=same(mode,"inherited-peer")?inherited_listener(name):listener(name);
 int fd=accept4(s,NULL,NULL,SOCK_CLOEXEC);if(fd<0)die("accept");
 if(same(mode,"late-greeting"))pause_ms(4000);
 if(same(mode,"long-line")){char spaces[4096];memset(spaces,' ',sizeof(spaces));write_all(fd,spaces,sizeof(spaces));send_text(fd," {\"QMP\":{}}\n");}
 else if(same(mode,"bad-greeting"))send_text(fd,"{\"return\":{}}\n");
 else if(same(mode,"no-lf")){send_text(fd,"{\"QMP\":{}}");close(fd);close(s);return 0;}
 else {
  if(same(mode,"events-65"))for(int i=0;i<65;i++)send_text(fd,"{\"event\":\"TEST\"}\n");
  const char *g="{\"QMP\":{\"version\":{\"qemu\":{\"major\":0}},\"capabilities\":[]}}\n";
  if(same(mode,"partial-progress")){for(size_t i=0;i<strlen(g);i++){write_all(fd,g+i,1);pause_ms(1);}}
  else send_text(fd,g);
 }
 char line[4096];size_t used=0;int quit=0;
 for(size_t attempts=0;attempts<12288;attempts++){
  char byte;ssize_t n=read(fd,&byte,1);if(n<0)die("command read");if(!n)break;if(used>=sizeof(line)-1)return 74;line[used++]=byte;if(byte!='\n')continue;line[used]=0;
  if(strstr(line,"qmp_capabilities"))send_text(fd,"{\"return\":{}}\n");
  else if(strstr(line,"query-test-stage"))send_text(fd,same(mode,"bad-stage")?"{\"return\":{\"stage\":\"WRONG\"}}\n":"{\"return\":{\"stage\":\"WORDLING_TEST_READY\"}}\n");
  else if(strstr(line,"quit")){
   append(working,"STOPPED\n");quit=1;
   if(same(mode,"quit-eof")){close(fd);close(s);return 0;}
   send_text(fd,same(mode,"bad-quit")?"{\"return\":{\"unexpected\":true}}\n":"{\"return\":{}}\n");
   if(same(mode,"quit-exit-race")){close(fd);close(s);return 0;}
   /* Defined TEST recipe: stay alive until the verified channel closes. This
      gives completed-reply identity proof, not provider measurement grace. */
   char extra;ssize_t end=read(fd,&extra,1);if(end!=0)return 75;break;
  }else{send_text(fd,"{\"error\":\"unsupported TEST command\"}\n");return 76;}
  used=0;
 }
 close(fd);close(s);return quit?0:77;
}
int main(int argc,char **argv){
 alarm(20);
 if(argc==3&&same(argv[1],"mutate")){append(argv[2],"PREPARED\n");pause_ms(100);return 0;}
 if(argc==5&&same(argv[1],"serve"))return serve(argv[2],argv[3],argv[4]);
 if(argc==7&&same(argv[1],"derive")){
  const char *mode=argv[6];if(same(mode,"helper-failure"))return 42;
  if(same(mode,"changed-input")){if(chmod(argv[2],0600))die("chmod");append(argv[2],"BAD\n");}
  if(!same(mode,"missing-output"))output_file(argv[3],argv[2],same(mode,"wrong-output"));
  output_file(argv[4],NULL,0);
  if(same(mode,"unexpected-absence")){int fd=open(argv[5],O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW,0600);if(fd<0)die("unexpected");write_all(fd,"BAD",3);close(fd);}
  pause_ms(100);return 0;
 }
 return 64;
}
