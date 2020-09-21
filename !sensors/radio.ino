
//Include Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

//create an RF24 object
RF24 radio(2, 3);  // CE, CSN

//address through which two modules communicate.
const byte address[6] = "ttech";

void setup()
{

  radio.begin();
  radio.setChannel(106);
  radio.setDataRate(RF24_250KBPS);
  
  //set the address
  radio.openWritingPipe(address);
  
  //Set module as transmitter
  radio.stopListening();
}
void loop()
{
  //Send message to receiver
  const char text[] = "RASHKA";
  radio.write(&text, sizeof(text));

  delay(1000);
}




#####

//Include Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

//create an RF24 object
RF24 radio(2, 3);  // CE, CSN

//address through which two modules communicate.
const byte address[6] = "ttech";

void setup()
{
  while (!Serial);
    Serial.begin(9600);
    

  radio.begin();
  radio.setChannel(106);
  radio.setDataRate(RF24_250KBPS);
  
  //set the address
  radio.openReadingPipe(0, address);
  
  //Set module as receiver
  radio.startListening();
}

void loop()
{
  //Read the data if available in buffer
  if (radio.available())
  {
    char text[32] = {0};
    radio.read(&text, sizeof(text));
    Serial.println(text);
  }
}