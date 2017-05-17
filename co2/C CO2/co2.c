#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
/* baudrate settings are defined in <asm/termbits.h>, which is
   included by <termios.h> */
#define BAUDRATE B9600   // Change as needed, keep B
/* change this definition for the correct port */
#define MODEMDEVICE "/dev/ttyO1" //Beaglebone Black serial port
#define _POSIX_SOURCE 1 /* POSIX compliant source */
#define FALSE 0
#define TRUE 1

FILE *debugFile = NULL;

typedef struct UM6_packet_struct
   {
    uint8_t   data_length;
    uint8_t   data[30];
   } UM6_packet;

uint8_t parse_serial_data(uint8_t *buf, uint8_t res, UM6_packet *packetFromSensor);

char values[5];
int value;

int main(int argc, char *argv[])
{
    debugFile = fopen("Stuff", "w");
    UM6_packet packetFromSensor;
    int fd, c, res;
    struct termios oldtio, newtio;
    uint8_t buf[20];
    // Load the pin configuration
    // echo BB-UART4 conflicts with cape-universaln used by pwm.
    // assume the cape-universaln has been set up already and configure the pins.
    int ret = system("echo BB-UART1 > /sys/devices/bone_capemgr.9/slots");
    //system("config-pin P9.24 uart");
    //system("config-pin P9.26 uart");

    /* Open modem device for reading and writing and not as controlling tty
       because we don't want to get killed if linenoise sends CTRL-C. */
    fd = open(MODEMDEVICE, O_RDWR | O_NOCTTY );
    if (fd < 0) { perror(MODEMDEVICE); exit(-1); }

    bzero(&newtio, sizeof(newtio)); /* clear struct for new port settings */

    /* BAUDRATE: Set bps rate. You could also use cfsetispeed and cfsetospeed.
       CRTSCTS : output hardware flow control (only used if the cable has
                 all necessary lines. See sect. 7 of Serial-HOWTO)
       CS8     : 8n1 (8bit,no parity,1 stopbit)
       CLOCAL  : local connection, no modem contol
       CREAD   : enable receiving characters */
    newtio.c_cflag = BAUDRATE | CRTSCTS | CS8 | CLOCAL | CREAD;

    /* IGNPAR  : ignore bytes with parity errors
       otherwise make device raw (no other input processing) */
    newtio.c_iflag = IGNPAR;

    /*  Raw output  */
    newtio.c_oflag = 0;

    /* ICANON  : enable canonical input
       disable all echo functionality, and don't send signals to calling program */
    newtio.c_lflag = ICANON;
    /* now clean the modem line and activate the settings for the port */
    tcflush(fd, TCIFLUSH);
    tcsetattr(fd,TCSANOW,&newtio);
    // NMEA command to ouput all sentences
    // Note that this code & format values in manual are hexadecimal
    /* terminal settings done, now handle input*/
    while (TRUE) {     /* loop continuously */
        /*  read blocks program execution until a line terminating character is
            input, even if more than 20 chars are input. If the number
            of characters read is smaller than the number of chars available,
            subsequent reads will return the remaining chars. res will be set
            to the actual number of characters actually read */
    res = read(fd, buf, 20);
    buf[res] = 0;             /* set end of string, so we can printf */
    //printf("%s", buf, res);
    parse_serial_data(&buf[0], (uint8_t)res, &packetFromSensor);
   }
   tcsetattr(fd, TCSANOW, &oldtio);
}

uint8_t parse_serial_data(uint8_t * rx_data,uint8_t rx_length, UM6_packet * packet)
{
   uint8_t index;
   for( index=0; index < (rx_length-2); index++)
   {
    if (rx_data[index] == 'Z' && rx_data[index+1] == ' ')
    {
       break;
    }
   }

   uint8_t packet_index = index;

   uint8_t data_length=5;

   packet->data_length = data_length;

   values [0] = rx_data[3];
   values [1] = rx_data[4];
   values [2] = rx_data[5];
   values [3] = rx_data[6];
   values [4] = rx_data[7];
   
   value = atoi(values);
   if(value>=150)
   {
    printf("CO2 concentration %dppm\n", value);
    printf("\033[2J");
   }
   else
   {
    printf("\033[2J");
   }
}
