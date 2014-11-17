#include <aJSON.h>
#include <SPI.h>

#define NO_ERROR 0
#define READING_ERROR 1
#define WRITING_ERROR 2
#define INCREMENT_ERROR 3
#define DECREMENT_ERROR 4
#define VALUE_ERROR 5
#define UNKNOWN_COMMAND 6

// set pin 10 and 11 as the slave select for the digital potis:
const int poti1SelectPin = 4;
const int poti2SelectPin = 5;

// establish a filter so we store only the information we're interested in
char* jsonFilter[] = {"command", "value"};
// set of error messages
char* gErrorMessage[]={"no error","reading failed","writing failed","increment failed","decrement failed","given value not valid for writing","unknown command"};
// serial buffer
char incomingMessage[100];

void setup() {
  // set the slaveSelectPin as an output:
  pinMode (poti1SelectPin, OUTPUT);
  pinMode (poti2SelectPin, OUTPUT);
  // deselect both pins
  digitalWrite(poti1SelectPin,HIGH);
  digitalWrite(poti2SelectPin,HIGH);
  // initialize SPI:
  SPI.begin();
  SPI.setDataMode(SPI_MODE0);
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV16);
  // initialize Serial:
  Serial.begin(9600);
}

void loop() {
}

void serialEvent() {
  // variables for the results
  int value=0;
  // no error = 0
  int error=0;
  int errorMessage=0;
  
  // string for storing serial command
  int numbytes;
  numbytes=Serial.readBytes(incomingMessage,sizeof(incomingMessage)-1);
  *(incomingMessage+numbytes)='\0';
  aJsonObject* received = aJson.parse(incomingMessage);
  aJsonObject* commandObject = aJson.getObjectItem(received, "command");
  String command = String(commandObject->valuestring);

  
  // interpret the command and call the appropriate function
  if (command.equals("read1")) {
      if (!poti1Read(&value)){
        error=1;
        errorMessage=READING_ERROR;
      }  
  }
  else if (command.equals("write1")){
      value = aJson.getObjectItem(received, "value")->valueint;
      if (String(incomingMessage).indexOf("value") == -1 || value < 0 || value > 256){
        error=1;
        errorMessage=VALUE_ERROR;
      }
      else {
        if (!poti1Write(&value)){
          error=1;
          errorMessage=WRITING_ERROR;
        }
      }
  }
  else if (command.equals("inc1")){
      if (!poti1Increment()){
        error=1;
        errorMessage=INCREMENT_ERROR;
      }
  }
  else if (command.equals("dec1")){
      if (!poti1Decrement()){
        error=1;
        errorMessage=DECREMENT_ERROR;
      }
  }
  else if (command.equals("read2")) {
      if (!poti2Read(&value)){
        error=1;
        errorMessage=READING_ERROR;
      }  
  }
  else if (command.equals("write2")){
      value = aJson.getObjectItem(received, "value")->valueint;
      if (String(incomingMessage).indexOf("value") == -1 || value < 0 || value > 256){
        error=1;
        errorMessage=VALUE_ERROR;
      }
      else {
        if (!poti2Write(&value)){
          error=1;
          errorMessage=WRITING_ERROR;
        }
      }
  }
  else if (command.equals("inc2")){
      if (!poti2Increment()){
        error=1;
        errorMessage=INCREMENT_ERROR;
      }
  }
  else if (command.equals("dec2")){
      if (!poti2Decrement()){
        error=1;
        errorMessage=DECREMENT_ERROR;
      }
  }
  else {
      error=1;
      errorMessage=UNKNOWN_COMMAND;
  }
  aJson.deleteItem(received);
  
  aJsonObject* sending=aJson.createObject();
  // creating root again, now for sending it to the PC
  aJson.addNumberToObject(sending, "value", value);
  aJson.addNumberToObject(sending, "error", error);
  aJson.addStringToObject(sending, "errorMessage", gErrorMessage[errorMessage]);
  char* returnString=aJson.print(sending);
  Serial.print(returnString);
  aJson.deleteItem(sending);
  free(returnString);
}
 
  
int poti1Read(int *value){
  int rd=0;
  // take the selectPin low to select the chip:
  digitalWrite(poti1SelectPin,LOW);
  // required delay after chip select
  delay(10);
  // send read command and check if an error occurred
  rd = SPI.transfer(12);
  if ( rd < 254) {
    digitalWrite(poti1SelectPin,HIGH);
    return 0;  
  }
  *value = SPI.transfer(0);
  if (rd == 255) {
    *value+=256;
  }
  digitalWrite(poti1SelectPin,HIGH);
  // no error so return 1
  return 1;
}

int poti1Write(int *value){
  int wr=0;
  int rd;
  // for writing values greater than 255 we have to set the last bit of the first byte
  if (*value > 255){
    wr=1;
    *value-=256;
  }
  // check if value is actually valid for writing
  if (*value > 255){
    return 0;
  }
  // take the selectPin low to select the chip:
  digitalWrite(poti1SelectPin,LOW);
  // required delay after chip select
  delay(10);
  // send write command and check if an error occurred
  rd = SPI.transfer(wr);
  if ( rd != 255) {
    digitalWrite(poti1SelectPin,HIGH);
    return 0;  
  }
  // send value for writing and check for error
  rd = SPI.transfer(*value);
  // deselect poti
  digitalWrite(poti1SelectPin,HIGH);
  // check for error
  if ( rd != 255) {
    return 0;  
  }  
  // no error so return 1
  return 1;
}

int poti1Increment(){
  int rd;
  digitalWrite(poti1SelectPin,LOW);
  // required delay after chip select
  delay(10);
  // send increment command 0000 0100
  rd=SPI.transfer(4);
  digitalWrite(poti1SelectPin,HIGH);
  if ( rd != 255) {
    return 0;  
  }  
  return 1;
}

int poti1Decrement(){
  int rd;
  digitalWrite(poti1SelectPin,LOW);
  // required delay after chip select
  delay(10);
  // send decrement command 0000 1000
  rd=SPI.transfer(8);
  digitalWrite(poti1SelectPin,HIGH);
  if ( rd != 255) {
    return 0;  
  }  
  return 1;
}

int poti2Read(int *value){
  byte rd=B00000000;
  // take the selectPin low to select the chip:
  digitalWrite(poti2SelectPin,LOW);
  // required delay after chip select
  delay(10);
  // send read command 0000 1100 and check if an error occurred
  rd = SPI.transfer(B00001100);
  if ( rd < 254) {
    digitalWrite(poti2SelectPin,HIGH);
    return 0;  
  }
  *value = SPI.transfer(0);
  if (rd == 255) {
    *value+=256;
  }
  digitalWrite(poti2SelectPin,HIGH);
  // no error so return 1
  return 1;
}

int poti2Write(int *value){
  int wr=0;
  int rd;
  // for writing values greater than 255 we have to set the last bit of the first byte
  if (*value > 255){
    wr=1;
    *value-=256;
  }
  // check if value is actually valid for writing
  if (*value > 255){
    return 0;
  }
  // take the selectPin low to select the chip:
  digitalWrite(poti2SelectPin,LOW);
  // required delay after chip select
  delay(10);
  // send write command and check if an error occurred
  rd = SPI.transfer(wr);
  if ( rd != 255) {
    digitalWrite(poti2SelectPin,HIGH);
    return 0;  
  }
  // send value for writing and check for error
  rd = SPI.transfer(*value);
  // deselect poti
  digitalWrite(poti2SelectPin,HIGH);
  // check for error
  if ( rd != 255) {
    return 0;  
  }  
  // no error so return 1
  return 1;
}

int poti2Increment(){
  int rd;
  digitalWrite(poti2SelectPin,LOW);
  // required delay after chip select
  delay(100);
  // send increment command 0000 0100
  rd=SPI.transfer(B00000100);
  digitalWrite(poti2SelectPin,HIGH);
  if ( rd != 255) {
    return 0;  
  }  
  return 1;
}

int poti2Decrement(){
  int rd;
  digitalWrite(poti2SelectPin,LOW);
  // required delay after chip select
  delay(10);
  // send decrement command 0000 1000
  rd=SPI.transfer(8);
  digitalWrite(poti2SelectPin,HIGH);
  if ( rd != 255) {
    return 0;  
  }  
  return 1;
}