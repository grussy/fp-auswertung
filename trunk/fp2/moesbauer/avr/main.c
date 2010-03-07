#include <avr/io.h>
#include <stdio.h>
#include <stdint.h>
#include <avr/interrupt.h>
#ifndef F_CPU
#warning "F_CPU war noch nicht definiert, wird nun nachgeholt mit 16000000"
#define F_CPU 16000000UL  // Systemtakt in Hz - Definition als unsigned long beachten
#endif
#include <util/delay.h>
#define BAUD 115200UL
#define UBRR_VAL ((F_CPU+BAUD*8)/(BAUD*16)-1)   // clever runden
#define BAUD_REAL (F_CPU/(16*(UBRR_VAL+1)))     // Reale Baudrate
#define BAUD_ERROR ((BAUD_REAL*1000)/BAUD) // Fehler in Promille, 1000 = kein Fehler.
// #if ((BAUD_ERROR<990) || (BAUD_ERROR>1010))
//   #error Systematischer Fehler der Baudrate grösser 1% und damit zu hoch! 
// #endif

/* Variable Declaration */
volatile int cmd_recieved, int1, int2, send = 0;
volatile unsigned int error_counter, saved_timer, counted_interrupts = 0;
volatile unsigned long overflows, saved_overflows=0;
volatile char cmd [10];
char buffer [20];

void append(char* s, char c)
{
        int len = strlen(s);
        s[len] = c;
        s[len+1] = '\0';
}

void USART_Init( void )
{
  /* Set baud rate */
  UBRRH = (unsigned char)(UBRR_VAL>>8);
  UBRRL = (unsigned char)UBRR_VAL;
  /* Enable receiver and transmitter, Enable the USART Recieve Complete interrupt (USART_RXC) */
  UCSRB = (1<<RXEN)|(1<<TXEN)|(1 << RXCIE);
  UCSRC |= (1<<URSEL)|(1 << UCSZ1)|(1 << UCSZ0); // Asynchron 8N1 
}
 
// bei neueren AVRs andere Bezeichnung fuer die Statusregister, hier ATmega16:
int uart_putc(unsigned char c)
{
    while (!(UCSRA & (1<<UDRE)))  /* warten bis Senden moeglich */
	;
    UDR = c;                      /* sende Zeichen */
    return 0;
}
 
 
/* puts ist unabhaengig vom Controllertyp */
void uart_puts (char *s)
{
    while (*s)
    {   /* so lange *s != '\0' also ungleich dem "String-Endezeichen" */
        uart_putc(*s);
        s++;
    }
}

void init_Interrupts( void )
{
	DDRD |= (1<<DDD3) | (1<<DDD2); // Set PORTD Pins 2 and 3 as input (external interupt pins)
	PORTD |= (1<<PORTD3) | (1<<PORTD2); // activate internal pullups
	// interrupt on change on INT0 and INT1
	MCUCR = (0<<ISC01) |(1<<ISC00) | (0<<ISC11) | (1<<ISC10);
	// turn on interrupts!
	GIMSK  |= (1<<INT0)|(1<<INT1);
}

inline void count_interrupt( void )
{
	counted_interrupts += 1;     //count
}

ISR(INT0_vect)
{
// 	count_interrupt();
	if (int1) {
		error_counter += 1;
	}
	int1 = 1;	//flag setzen
	saved_timer = TCNT1; //timer auslesen
	saved_overflows = overflows; // overflows auslesen
	overflows = 0; //reset
	TCNT1= 0;
}

ISR(INT1_vect)
{
// 	count_interrupt();
	if (int2) {
		error_counter += 1;
	}
	int2 = 1;	//flag setzen
	saved_timer = TCNT1; //timer auslesen
	saved_overflows = overflows; // overflows auslesen
	overflows = 0; //reset
	TCNT1= 0;
}

ISR(TIMER1_OVF_vect)
{
// 	if (overflows == 1000) {
// 		send = 1;
// 	}
	overflows++;
}

ISR(USART_RXC_vect)
{
	char ReceivedByte;
	ReceivedByte = UDR;
	if (ReceivedByte == '\r'){
		cmd_recieved = 1;
	} else {
	UDR = ReceivedByte;
        int len = strlen(cmd);
        cmd[len] = ReceivedByte;
        cmd[len+1] = '\0';
	}
} 

inline void start_Timer( void )
{
	TIMSK |= (1 << TOIE1); // enable Interrupt on Overlow
	TCCR1A &= ~((1 << COM1A1)|(1<<COM1B1)|(1 << COM1A0)|(1<<COM1B0)); // normal Mode
	TCCR1B |= (1<<CS10); // no prescaler, start timer
}

inline void stop_Timer( void )
{
	TCCR1B &= ~(1<<CS10); // stop timer
}

int main(void)
{
	USART_Init();
	uart_puts("\n#########################################################");
	uart_puts("\n# Welcome to Low Speed Meassuring using a Mouse Sensor. #");
	uart_puts("\n# one overflow means 65535 timer ticks (16 bit) and we  #");
	uart_puts("\n# have no prescaler so one tick means 1/16Mhz           #");
	uart_puts("\n#                     by Tobi and Paul                  #");
	uart_puts("\n#########################################################");
	uart_puts("\n");
	sprintf(cmd, "");
	init_Interrupts();
	start_Timer();
	sei();
	while(1) {
		if (int1) {
			int1 = 0;
			sprintf(buffer, "%ut%uo", saved_timer, saved_overflows);
			uart_puts(buffer);
		}
		if (int2) {
			int2 = 0;
			sprintf(buffer, "%ut%uo", saved_timer, saved_overflows);
			uart_puts(buffer);
		}
		if (error_counter) {
			sprintf(buffer, "\n[DEBUG] Error Counter was at: %u\n", error_counter);
			uart_puts(buffer);
			error_counter = 0;
		}
		if (send) {
			sprintf(buffer, "%ut%uo%ui", TCNT1, overflows, counted_interrupts);
			TCNT1 = 0;
			overflows = 0;
			counted_interrupts = 0;
			uart_puts(buffer);
		}
		if (cmd_recieved) {
			uart_putc('\r');
			if (strcmp(cmd ,'help')==0){ 
				uart_puts("\n[Usage] Enter Command. While meassuring command means stop.");
				uart_puts("\n Commands are:");
				uart_puts("\n                      help - for this Help");
				uart_puts("\n                     start - start a meassurement. While this i send.");
			} else if (cmd == 'easteregg'){
			} else {
				uart_puts("[Unknown Command]: ");
				uart_puts(cmd);
			}
			sprintf(cmd, "");
			cmd_recieved = 0;
			uart_putc('\r');
		}
	}
}
