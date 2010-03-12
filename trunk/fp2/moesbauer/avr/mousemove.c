#include <fcntl.h>
#include <stdio.h>
#include <termios.h>
#include <stdlib.h>
#include <strings.h>
#include <time.h>
#include <string.h>
#include <sys/time.h>

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

/* Change to the baud rate of the port B2400, B9600, B19200, etc */
#define SPEED B115200

/* Change to the serial port you want to use /dev/ttyUSB0, /dev/ttyS0, etc. */
#define PORT "/dev/ttyS0"

int main( ){
    int fd = open( PORT, O_RDONLY | O_NOCTTY );
    if (fd <0) {perror(PORT); exit(-1); }
    struct termios options;

    bzero(&options, sizeof(options));
    options.c_cflag = SPEED | CS8 | CLOCAL | CREAD | IGNPAR;
    tcflush(fd, TCIFLUSH);
    tcsetattr(fd, TCSANOW, &options);

    int r;
    char buf[255];

    FILE *fp;
    char filename[20];
    time_t rawtime;
    time ( &rawtime );
    char *time = ctime(&rawtime);
    strip(time);
    sprintf(filename, "data/%s.dat", time);
    if((fp=fopen(filename, "w")) == NULL) {
        printf("Cannot open file: %s.\n", filename);
        exit(-1);
    }
    while( 1 ){
        r = read( fd, buf, 255 );
        buf[r]=0;
        printf( "%s", buf );
	fprintf (fp, "%s", buf);
    }
    fclose(fp);
}
