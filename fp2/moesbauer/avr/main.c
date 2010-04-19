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
volatile int cmd_recieved, int1, int2, send, started, num_samples= 0;
volatile unsigned int error_counter, saved_timer, counted_interrupts, interrupts = 0;
volatile unsigned long overflows, saved_overflows=0;
volatile char cmd [10];
volatile char buffer [30];

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
 	DDRD &= ~((1<<DDD3) | (1<<DDD2)); // Set PORTD Pins 2 and 3 as input (external interupt pins)
 	DDRB &= ~(1<<DDB2); // Set PORTD Pins 2 and 3 as input (external interupt pins)
// 	PORTD |= (1<<PORTD3) | (1<<PORTD2); // activate internal pullups
// 	interrupt on change on INT0 and INT1
	MCUCR = (0<<ISC01) |(1<<ISC00) | (0<<ISC11) | (1<<ISC10);
	//interrupt INT2 on rising edge
	MCUCSR |= (1<<ISC2);
	// turn on interrupts!
	GIMSK  |= (1<<INT0)|(1<<INT1)|(1<<INT2);
}

inline void toggle_Int2( void )
{
	GIMSK &= ~(1<<INT2); //disable INT2 see datasheet for info why
	MCUCSR ^= (1<<ISC2); // toggle
	GIFR |= (1<<INTF2); //clear
	GIMSK |= (1<<INT2);  //enable INT2
}

inline void count_interrupt( void )
{
	interrupts++;     //count//
	if (interrupts >= num_samples) {
		saved_timer = TCNT1; //timer auslesen
		saved_overflows = overflows; // overflows auslesen
		counted_interrupts = interrupts;
		TCNT1= 0;
		overflows = 0; //reset
		interrupts = 0;
		send = 1;
	}
}

ISR(INT0_vect)
{
	count_interrupt();
}

ISR(INT1_vect)
{
	count_interrupt();
}

ISR(INT2_vect)
{
	if (started){
		GIMSK  &= ~(1<<INT0)|(1<<INT1); //stop meassuring
		stop_Timer();
		TCNT1 = 0;
		overflows = 0;
		started = 0;
		send = 0;
		uart_puts("stopped\n");
	} else {
		TCNT1 = 0;
		overflows = 0;
		started = 1;
		uart_puts("started\n");
		TCCR1B |= (1<<CS10); // start timer
		GIMSK  |= (1<<INT0)|(1<<INT1); //start meassuring
	}
	toggle_Int2();
}

ISR(TIMER1_OVF_vect)
{
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
	num_samples = 8;
	USART_Init();
	uart_puts("\n#########################################################");
	uart_puts("\n# Welcome to Low Speed Meassuring using a Mouse Sensor. #");
	uart_puts("\n# one overflow means 65535 timer ticks (16 bit) and we  #");
	uart_puts("\n# have no prescaler so one tick means 1/16Mhz           #");
	uart_puts("\n#                     by Tobi and Paul                  #");
	uart_puts("\n#########################################################");
	uart_puts("\n");
	sprintf(buffer, "\n  Auto Meassure on, Sampling %u counts", num_samples);
	uart_puts(buffer);
	uart_puts("\n  [OUTPUT] is <number_of_interrupts number_of_overflows timer_count>");
	sprintf(cmd, "");
	init_Interrupts();
	GIMSK  &= ~(1<<INT0)|(1<<INT1); //but stop meassuring
	start_Timer();
	sei();
	while(1) {
		if (started) {
			if (send) {
				if (counted_interrupts) {
					sprintf(buffer, "%u %u %u\n", saved_timer, saved_overflows, counted_interrupts);
					uart_puts(buffer);
				}
				send = 0;
			}
		}
		if (cmd_recieved) {
			uart_putc('\r');
			if (strcmp(cmd ,"help")==0){ 
				uart_puts("\n[Usage] Enter Command:");
				uart_puts("\n                      help - for this Help");
				uart_puts("\n                     start - start a meassurement. While this i send.");
				uart_puts("\n                      stop - stop a meassurement.");
				uart_puts("\n                   auto_on - start/stop auto on (INT2).");
				uart_puts("\n                  auto_off - start/stop auto off (INT2).");
				uart_puts("\n                    errors - Read error counter");
			} else if (strcmp(cmd, "start") == 0){
				started = 1;
				uart_puts("OK\n");
			} else if (strcmp(cmd, "stop") == 0){
				started = 0;
				uart_puts("OK\n");
			} else if (strcmp(cmd, "auto_on") == 0){
				started = 0;
				GIMSK |= (1<<INT2);
				uart_puts("OK\n");
			} else if (strcmp(cmd, "auto_off") == 0){
				GIMSK &= ~(1<<INT2); //disable INT2
				started = 0;
				uart_puts("OK\n");
			} else if (strcmp(cmd, "errors") == 0) {
				sprintf(buffer, "ErrorCount: %i\n", error_counter);
				uart_puts(buffer);
			} else if (strcmp(cmd, "?") == 0) {
				sprintf(buffer, "Timer was %u ", TCNT1);
				uart_puts(buffer);
			}else {
				uart_puts("[Unknown Command]: ");
				uart_puts(cmd);
			}
			sprintf(cmd, "");
			cmd_recieved = 0;
			uart_putc('\r');
		}
	}
}
