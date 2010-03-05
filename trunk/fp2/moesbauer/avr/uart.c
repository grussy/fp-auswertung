#include "uart.h"

void USART_Init( void )
{
  /* Set baud rate */
  UBRRH = (unsigned char)(UBRR_VAL>>8);
  UBRRL = (unsigned char)UBRR_VAL;
  /* Enable receiver and transmitter */
  UCSRB = (1<<RXEN)|(1<<TXEN);
  UCSRC |= (1<<URSEL)|(1 << UCSZ1)|(1 << UCSZ0); // Asynchron 8N1 

	uart_puts("\n#########################################################");
	uart_puts("\n# Welcome to AVR Testboard, not much implemented so far #");
	uart_puts("\n# for a list of commands type HELP and press RETURN     #");
	uart_puts("\n#                     by Tobi (and Paul)                #");
	uart_puts("\n#########################################################");
	uart_puts("\n");
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

/* Zeichen empfangen */
uint8_t uart_getc(void)
{
    while (!(UCSRA & (1<<RXC)))   // warten bis Zeichen verfuegbar
        ;
    return UDR;                   // Zeichen aus UDR an Aufrufer zurueckgeben
}
 
int uart_gets( char* Buffer, uint8_t MaxLen )
{
  uint8_t NextChar;
  uint8_t StringLen = 0;
 
  NextChar = uart_getc();   
	if ( NextChar == '\n' || NextChar == '\r') return 1;      // Warte auf und empfange das nächste Zeichen
 
                                  // Sammle solange Zeichen, bis:
                                  // * entweder das String Ende Zeichen kam
                                  // * oder das aufnehmende Array voll ist
  while( NextChar != '\n' && NextChar != '\r' && StringLen < MaxLen - 1 ) {
    *Buffer++ = NextChar;
    StringLen++;
    NextChar = uart_getc();
  }
 
                                  // Noch ein '\0' anhängen um einen Standard
                                  // C-String daraus zu machen
  *Buffer = '\0';
	return 0;
}