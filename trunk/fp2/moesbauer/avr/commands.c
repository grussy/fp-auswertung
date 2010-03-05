#include "commands.h"
void identify_command()
{
	char command[17];      // String mit maximal 12 zeichen 
  	if (uart_gets( command, sizeof( command ) )) return;
		
	if( strcmp( command, "TG" ) == 0 )
	{
		uart_puts("TG AVR Testboard v0.0.1\n");
		//uart_puts(command);
	}
	else if	( strcmp( command, "LED1" ) == 0 )
	{
		DDRD |= ( 1 << PD6 );
		PORTD = PIND ^ ( 1 << PD6 );
		uart_puts(command);
	}
	else if	( strcmp( command, "LED2" ) == 0 )
	{
		DDRD |= ( 1 << PD5 );
		PORTD = PIND ^ ( 1 << PD5 );
		uart_puts(command);
	}
	else if	( strcmp( command, "LCDW1" ) == 0 )
	{
		uart_puts("Type...\n");
		char lcdtext[17];      // String mit maximal 16 zeichen 
  		while (uart_gets( lcdtext, sizeof( lcdtext )));
		set_cursor(0,1);
		lcd_string(lcdtext);
	}
		else if	( strcmp( command, "LCDW2" ) == 0 )
	{
		uart_puts("Type...\n");
		char lcdtext[17];      // String mit maximal 16 zeichen 
  		while (uart_gets( lcdtext, sizeof( lcdtext )));
		set_cursor(0,2);
		lcd_string(lcdtext);
	}
	else if (strcmp( command, "HELP" ) == 0 )
	{
		uart_puts("Available commands:\n TG - print Device and Version Info\n LEDx - Turn on/off LED number x\n\n HELP - Print this Info\n");
	}
}