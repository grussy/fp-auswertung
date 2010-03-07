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

volatile int interrupt = 0;
unsigned int error_counter, saved_timer, counted_interrupts = 0;
unsigned long overflows, saved_overflows=0;

 
void USART_Init( void )
{
  /* Set baud rate */
  UBRRH = (unsigned char)(UBRR_VAL>>8);
  UBRRL = (unsigned char)UBRR_VAL;
  /* Enable receiver and transmitter */
  UCSRB = (1<<RXEN)|(1<<TXEN);
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
	// interrupt on change on INT0 and INT1
	MCUCR = (0<<ISC01) |(1<<ISC00) | (0<<ISC11) | (1<<ISC10);
	// turn on interrupts!
	GIMSK  |= (1<<INT0)|(1<<INT1);
}

inline void count_interrupt( void )
{
	counted_interrupts += 1;     //count
}

inline void handle_Interrupt( void )
{
	if (interrupt) {
		error_counter += 1;
	}
	interrupt = 1;	//flag setzen
	TCCR1B &= ~(1<<CS10); // stop timer
	saved_timer = TCNT1; //timer auslesen
	saved_overflows = overflows; // overflows auslesen
	overflows = 0; //reset
	TCNT1= 0;
	TCCR1B |= (1<<CS10); // no prescaler, start timer
}

ISR(INT0_vect)
{
	handle_Interrupt();
}

ISR(INT1_vect)
{
	handle_Interrupt();
}

ISR(TIMER1_OVF_vect)
{
	overflows++;
}

void start_Timer( void )
{
	TIMSK |= (1 << TOIE1); // enable Interrupt on Overlow
	TCCR1A &= ~((1 << COM1A1)|(1<<COM1B1)|(1 << COM1A0)|(1<<COM1B0)); // normal Mode
	TCCR1B |= (1<<CS10); // no prescaler, start timer
}

int main(void)
{
	char buffer [20];
	USART_Init();
	uart_puts("\n#########################################################");
	uart_puts("\n# Welcome to Low Speed Meassuring using a Mouse Sensor. #");
	uart_puts("\n# one overflow means 65535 timer ticks (16 bit) and we  #");
	uart_puts("\n# have no prescaler so one tick means 1/16Mhz           #");
	uart_puts("\n#                     by Tobi and Paul                  #");
	uart_puts("\n#########################################################");
	uart_puts("\n");
	sprintf(buffer, "\n Baudrate is Set to: %i, while its Error is at %f\n", BAUD, (BAUD_ERROR -1000)/10);
	uart_puts(buffer);
	init_Interrupts();
	start_Timer();
	sei();
	while(1) {
		if (interrupt) {
			interrupt = 0;
			sprintf(buffer, "%ut%uo", saved_timer, saved_overflows);
			uart_puts(buffer);
		}
		if (error_counter) {
			sprintf(buffer, "\n[DEBUG] Error Counter was at: %u\n", error_counter);
			uart_puts(buffer);
			error_counter = 0;
		}
// 		if (int2) {
// 			int2 = 0;
// 			sprintf(buffer, " %ut%uo", saved_timer, saved_overflows);
// 			uart_puts(buffer);
// 		}
	}
}
