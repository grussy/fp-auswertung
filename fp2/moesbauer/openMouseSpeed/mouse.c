#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/time.h>
#include <string.h>

void strip(char * ch){
	char *p1 = ch;
	char *p2 = ch;
	p1 = ch;
	while(*p1 != 0) {
		if(ispunct(*p1) || isspace(*p1)) {
			++p1;
		}
		else
			*p2++ = *p1++; 
		}
	*p2 = 0;
}

main(){
        FILE *fmouse;
	FILE *fp;
        char b[3];
        fmouse = fopen("/dev/input/mice","r");
	char filename[20];
  	time_t rawtime;
	time ( &rawtime );
	char *time = ctime(&rawtime);
	strip(time);
	sprintf(filename, "data/%s.dat", time);
	if((fp=fopen(filename, "w")) == NULL) {
		printf("Cannot open file: %s.\n", filename);
		exit(1);
	}
        int xd=0,yd=0; //x/y movement delta
        int xo=0,yo=0; //x/y overflow (out of range -255 to +255)
        int lb=0,mb=0,rb=0,hs=0,vs=0; //left/middle/right mousebutton
	long long unsigned int elapsed, start, stop;
	struct timeval tv;
	time_t startsecs, stopsecs, startusecs, stopusecs, offset;
	gettimeofday(&tv, NULL); 
	stopusecs=tv.tv_usec;
	stopsecs=tv.tv_sec;
	offset=tv.tv_sec;
        int run=0;
        while(!run){
		start = stop;
                fread(b,sizeof(char),3,fmouse);
		gettimeofday(&tv, NULL);
		stopusecs=tv.tv_usec;
		stopsecs=tv.tv_sec;
		stop = stopusecs + 1e6*stopsecs;
                lb=(b[0]&1)>0;
                rb=(b[0]&2)>0;
                mb=(b[0]&4)>0;
                hs=(b[0]&16)>0;
                vs=(b[0]&32)>0;
                xo=(b[0]&64)>0;
                yo=(b[0]&128)>0;
                xd=b[1];
                yd=b[2];
		elapsed = stop - start;
		if (yd) {
			if (yo) {
				printf("[ERROR] Mouse Buffer Overflow - DPI Resolution too High for that Speed, reduce one of it.");
			} else {
				fprintf (fp, "%lu.%.6lu\t%llu\t%i\t%e\n", (long)(stopsecs-offset), (long)stopusecs, elapsed, yd, (double)((yd*1e6)/elapsed));
				printf ("%lu.%.6lu\t%llu\t%i\t%e\n", (long)(stopsecs-offset), (long)stopusecs, elapsed, yd, (double)((yd*1e6)/elapsed));
			}
		}
        }
        fclose(fmouse);
	fclose(fp);
}
