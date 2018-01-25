/*
  Analog input, analog output, serial output

  Reads an analog input pin, maps the result to a range from 0 to 255 and uses
  the result to set the pulse width modulation (PWM) of an output pin.
  Also prints the results to the Serial Monitor.

  The circuit:
  - potentiometer connected to analog pin 0.
    Center pin of the potentiometer goes to the analog pin.
    side pins of the potentiometer go to +5V and ground
  - LED connected from digital pin 9 to ground

  created 29 Dec. 2008
  modified 9 Apr 2012
  by Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogInOutSerial
*/

// These constants won't change. They're used to give names to the pins used:
const int analogInPin = A0;  
void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}


float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
 return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}


String measureAmps(){
  float sample=0;
  for(int i=0 ; i<150 ; i++){
    sample += takeAmpSample();
    delay(2);
    }
  float ret = sample/150;
  
  return String(ret,3)+ " A";
  }

float takeAmpSample(){
  float sample = analogRead(A0); //read the current from sensor
  float x = mapfloat(sample, 0 , 1023 ,0 ,5 );
  float a= (10.0 * x);
  float y =  a - 25.0 ;
  if ( y < 0){
    
    y = y*(-1);
    }

  return y;
  }


  
void loop() {
  // read the analog in value:
  Serial.print("Amps = "+measureAmps());
  delay(1000);
}
