#include <Streaming.h>
#include <DS3231.h>
#include <Wire.h>
#include <avr/sleep.h>

DS3231  rtc(SDA, SCL);
Time t;
int INTERRUPT_PIN = 2;        // Interrupt från RTC - används för alarm
volatile int flag = 0;        // Interruptflagga

bool debug=false;              // Anger om debugutskrifter ska visas

// Portar
const int LED1 = 4;
const int LED2 = 5;
const int LED3 = 6;
const int ldrPin = 0;         // LDR ansluten till A0
const int anaRes = 1;         // A1 - ena sidan på LED resistor för att mäta ström
const int anaLed = 2;         // A2 - andra sidan på LED resistor för att mäta ström

// Commands
String COMMAND_DEBUG = "debug";
String COMMAND_ECHO = "echo";
String COMMAND_LDR = "ldr";
String COMMAND_LED = "led";
String COMMAND_LED_INFO = "getledinfo";
String COMMAND_TIME_GET = "gettime";
String COMMAND_TIME_SET = "settime";
String COMMAND_TEMP_GET = "gettemp";

// LED commands
String COMMAND_LED_ON = "on";
String COMMAND_LED_OFF = "off";


void setup()
{
  pinMode(INTERRUPT_PIN, INPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);

  //pull up the interrupt pin
  digitalWrite(INTERRUPT_PIN, HIGH);

  // make sure LEDs are off
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);

  Serial.begin(9600);
  Serial.println("Initierad");
  rtc.begin();

}

void loop()
{
  if (Serial.available())
  {
    bool handled=false;
    String cmd = readSerial();
    if (
    if (cmd.equals(COMMAND_DEBUG)) {
      activateDebug();
      handled=true;
    }
    if (cmd.equals(COMMAND_LDR)) {
      measureLight();
      handled=true;
    }
    if (cmd.equals(COMMAND_LED_INFO)) 
    {
      getledinfo();
      handled=true;
    }
    if (cmd.startsWith(COMMAND_LED))
    {
      handleLed(cmd);
      handled=true;
    }
    if (cmd.equals(COMMAND_TIME_GET)) 
    {
      getTime();
      handled=true;
    }
    if (cmd.startsWith(COMMAND_TIME_SET))
    {
      setTime(cmd);
      handled=true;
    }
    
    if (!handled) 
    {
      Serial << "Förstår inte kommando " << cmd << endl;
    }
  }
  delay(20);
}

void setTime(String str)
{
    int l = COMMAND_TIME_SET.length();
    String dateStr = str.substring(l+1);
    debugPrint("Tolkat datum : " + dateStr);
    String yearStr = dateStr.substring(0, 4);
    String monthStr = dateStr.substring(5, 7);
    String dayStr = dateStr.substring(8, 10);
    String hourStr = dateStr.substring(11, 13);
    String minStr = dateStr.substring(14, 16);
    String secStr = dateStr.substring(17,19);
    if (isValidNumber(yearStr) && isValidNumber(monthStr) && isValidNumber(dayStr) && isValidNumber(hourStr) && isValidNumber(minStr) && isValidNumber(secStr) )
    {
      rtc.setDate(dayStr.toInt(), monthStr.toInt(), yearStr.toInt());
      rtc.setTime(hourStr.toInt(), minStr.toInt(), secStr.toInt());
    }
    else
    {
      Serial << "Ogiltigt datum" << endl;
    }
}

void activateDebug()
{
  debug = !debug;
  Serial << "Debugutskrifter " <<  (debug ? "pa" : "av") << endl;
}

void getTemp()
{
  //float t = rtc.GetTemperature();
  //RtcTemperature rtcTemp = rtc.GetTemperature();
  //float temp = rtcTemp.AsFloat();
  Serial << "Not implemented yet" << endl;
}

void getTime()
{
  t = rtc.getTime();
  String rawDate = rtc.getDateStr();
  String formattedDate = rawDate.substring(6, 10) + "-" + rawDate.substring(3, 5) + "-" + rawDate.substring(0, 2) + " ";
  Serial << formattedDate << rtc.getTimeStr() << endl;
//  Serial << rtc.getTimeStr() << endl;
}

void getledinfo()
{
  int v1 = analogRead(anaRes);
  int v2 = analogRead(anaLed);
  Serial << "Returned values : " << v1 << " " << v2 << endl;
}

void handleLed(String str)
{
    int l = COMMAND_LED.length();
    String led = str.substring(l+1, l+2);
    debugPrint("Led number '" + led + "'");
    if (led.length() > 0 && isValidNumber(led)) 
    {
      int lednumber = led.toInt();
      String ledcommand = str.substring(l+3);
      debugPrint("Led command : " + ledcommand);
      bool ledstate = false;
      if (ledcommand.equals(COMMAND_LED_ON) || ledcommand.equals(COMMAND_LED_OFF)) 
      {
        if (ledcommand.equals(COMMAND_LED_ON)) {
          ledstate = true;
        }
        setLed(lednumber, ledstate);
      }
      else
      {
        Serial.println(ledcommand + " : Ogiltigt kommando till LED");
      }
    }
    else
    {
      Serial.println("Ogiltig lysdiod : " + led);
    }
}

void setLed(int led, bool onoff)
{
  byte wantedled;
  byte wantedstate=LOW;
  switch(led) {
    case 1: wantedled=LED1;
            break;
    case 2: wantedled=LED2;
            break;
    case 3: wantedled=LED3;
            break;
    deafult: wantedled=99;
            break;
  }
  if (wantedled==99)
  {
    Serial.println("Okänd LED");
  }
  else
  {
    if (onoff) {
      wantedstate=HIGH;
    }
    digitalWrite(wantedled, wantedstate);
  }
}

String readSerial() 
{
    String s = Serial.readString();
    int crpos = s.indexOf('\r');
    if (crpos > 0) {
      s = s.substring(0, crpos);
    }
    int lfpos = s.indexOf('\n');
    if (lfpos > 0) {
      s = s.substring(0, lfpos);
    }
    debugPrint("Mottaget : " + s + "(" + s.length() + " tecken)");
    return s;
}

void measureLight() 
{
    int ldrval;
    ldrval = analogRead(ldrPin);
    Serial.print("Ljus : <");
    Serial.print(ldrval);
    Serial.println(">");
}

void debugPrint(String str)
{
  if (debug)
  {
    Serial.println(str);
  }
}

boolean isValidNumber(String str){
  if (str.length() == 0) return false;
  for(byte i=0;i<str.length();i++)
  {
      if(!isDigit(str.charAt(i))) return false;
  }
  return true;
} 
