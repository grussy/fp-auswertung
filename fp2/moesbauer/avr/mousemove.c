#include <fcntl.h>
#include <stdio.h>
#include <termios.h>
#include <stdlib.h>
#include <strings.h>

/* Change to the baud rate of the port B2400, B9600, B19200, etc */
#define SPEED B38400

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
    while( 1 ){
        r = read( fd, buf, 255 );
        buf[r]=0;
        printf( "%s", buf );
    }
}
