#include <SPI.h>        
#include <TimerOne.h>
#include <Ethernet.h>
#include <avr/wdt.h>

int sensor0Value = 0; 
int sensor0outputValue = 0;
//MAC Address que usara el arduino (asegurarse de que sea unica)1A-5C-69-6D-36-60
byte mac[] = { 0x1A, 0x5C, 0x69, 0x6D, 0x36, 0x60 };

//the IP address is dependent on your network
IPAddress ip(192, 168, 1, 99);
//the dns server ip
IPAddress dnServer(192, 168, 1, 1);
// the router's gateway address:
IPAddress gateway(192, 168, 1, 1);
// the subnet:
IPAddress subnet(255, 255, 255, 0);
// Target IP
IPAddress targetIP(192, 168, 1, 1);
// Hostname de destino (opcional)
const char* targetHostname = "hostname"; 
// puerto al cual se envia el paquete  
const int targetPort = 8888;
// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;
boolean sendPackageFlag = false;
int retries=0;

void setup() {
  wdt_enable(WDTO_8S);
  pinMode(2, INPUT_PULLUP);
  //DEBUG MODE saltea conexion para probar mediciones
  boolean debugMode = !digitalRead(2);
  Serial.println("v1.0")
  if (debugMode){
    debug();}
  else{
    Serial.begin(9600);
    Serial.println("\n/////////Iniciando/////////\n");
    Serial.println("\n/////////Inicializando Timers/////////\n");  
    Timer1.initialize(1000000);         // initialize timer1, and set a 1/2 second period
    Timer1.attachInterrupt(callback);  // attaches callback() as a timer overflow interrupt
    initializeNetwork();
    }
  
}

boolean initializeNetwork(){
  Udp.stop();
  Serial.print("Iniciando Ethernet...");
  Ethernet.begin(mac, ip, dnServer, gateway, subnet);
  Serial.println("listo\n");
  //Necesario inicializar el puerto antes de poder transmitir
  Serial.print("Preparando Puerto UDP...");
  boolean bInit=Udp.begin(targetPort); 
  Serial.println(boolToString2(bInit)+"\n");     
  printIPAddress();
  Serial.println("\n/////////Iniciado/////////\n"); 
  return bInit;
  }

void callback()
{
  sendPackageFlag=true;
}

void loop() {
  // si flag true, send temppkg
 if(sendPackageFlag == true)
  {
    sendPackage(preparePackage(0));
    sendPackage(preparePackage(1));
    sendPackageFlag = false;
    }
  if(retries>9){
    Serial.println("Reiniciando...");
    while(1){}
    }

    Serial.println("Se ha reseteado el WatchDog");
    wdt_reset();
  
}




String preparePackage(int typeOfPackage){
  String message="";
    if (typeOfPackage == 0)
      message="{ \"type\": 0, \"current\" : "+measureAmps()+" }";
    if (typeOfPackage == 1)
      message = "{ \"type\": 1, \"temperature\" : "+ GetTemp() +" }";

   return message;
  }

void sendPackage(String message){
    boolean init=initializeNetwork();
   /* if(init==false){
      retries+=1;
      Serial.println("Error... Quedan " +String(10-retries)+" \nintentos antes del reinicio automatico");
      return;
      }
    //Comienza a armar el paquete*/
    Serial.print("1_Iniciando Paquete...");
    //IP o Hostname del servidor, reemplazar por targetHostname para usar hostname
    boolean bBegin = Udp.beginPacket(targetIP, targetPort); 
    Serial.println(boolToString2(bBegin)+"\n");
    if(bBegin==false){
      retries+=1;
      Serial.println("Error... Quedan " +String(10-retries)+" \nintentos antes del reinicio automatico");
      return;
      }
      
    //Armando Mensaje
   // String sensorString = boolToString(sensorVal);

      
    Serial.print("2_Escribiendo Paquete...");
    boolean bWrite =Udp.write(message.c_str()); 
    
    Serial.println(boolToString2(bWrite)+"\n");
    if(bWrite==false){
      retries+=1;
       Serial.println("Error... Quedan " +String(10-retries)+" \nintentos antes del reinicio automatico");
      return;}
    Serial.print("3_Enviando... ");
    boolean bEnd = Udp.endPacket();
    Serial.println(boolToString2(bEnd)+"\n");
    if(bEnd==false){
      retries+=1;
      Serial.println("Error... Quedan " +String(10-retries)+" \nintentos antes del reinicio automatico");
      return;}
    Serial.println(message+"\n");
    
  }

void sendPackage(int typeOfPackage){
      
    //Comienza a armar el paquete
    Serial.print("1_Iniciando Paquete...");
    //IP o Hostname del servidor, reemplazar por targetHostname para usar hostname
    boolean bBegin = Udp.beginPacket(targetIP, targetPort); 
    Serial.println(boolToString2(bBegin)+"\n");
    if(bBegin==false){
      return;}
      
    //Armando Mensaje
   // String sensorString = boolToString(sensorVal);
    String message = "";
    
    if (typeOfPackage == 0)
      message="{ \"type\": 0, \"current\" : "+measureAmps()+" }";
      
    if (typeOfPackage == 1)
      message = "{ \"type\": 1, \"temperature\" : "+ GetTemp() +" }";
      
    Serial.print("2_Escribiendo Paquete...");
    boolean bWrite =Udp.write(message.c_str()); 
    
    Serial.println(boolToString2(bWrite)+"\n");
    if(bWrite==false){
      return;}
    Serial.print("3_Enviando... ");
    boolean bEnd = Udp.endPacket();
    Serial.println(boolToString2(bEnd)+"\n");
    if(bEnd==false){
      return;}
    Serial.println(message+"\n");
    
  }

String measureAmps(){
  float sample=0;
  for(int i=0 ; i<150 ; i++){
    sample += takeAmpSample();
    delay(2);
    }
  float ret = sample/150;
  
  return String(ret,3);
  }

String GetTemp(void)
{
  unsigned int wADC;
  double t;

  // The internal temperature has to be used
  // with the internal reference of 1.1V.
  // Channel 8 can not be selected with
  // the analogRead function yet.

  // Set the internal reference and mux.
  ADMUX = (_BV(REFS1) | _BV(REFS0) | _BV(MUX3));
  ADCSRA |= _BV(ADEN);  // enable the ADC

  delay(20);            // wait for voltages to become stable.

  ADCSRA |= _BV(ADSC);  // Start the ADC

  // Detect end-of-conversion
  while (bit_is_set(ADCSRA,ADSC));

  // Reading register "ADCW" takes care of how to read ADCL and ADCH.
  wADC = ADCW;

  // The offset of 324.31 could be wrong. It is just an indication.
  t = (wADC - 324.31 ) / 1.22;

  // The returned temperature is in degrees Celsius.
  return String(t, 3);
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

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}


String intTo3Char(int n){
  if(n>99){
    return String(n);}
  if(n>9){
    return "0"+String(n);}
  if(n<10&&n>=0){
    return "00"+String(n);}
  else{  
    return String(n);
  }
  Serial.println();
  Serial.println(n);
  }


String boolToString2(boolean b){
  if(b==true)
  {
    return "listo";
    }
   else{
    return "error";} 
 
  }

String boolToString(boolean b){
  if(b==true)
  {
    return "0";
    }
   else{
    return "1";} 
 
  }

void debug(){
   while(true){
        String message="{\"Sensor0\" : "+ 
        measureAmps()+" }";
        Serial.println("////////////DEBUG MODE//////////////\n");
        Serial.println(message+"\n");
        Serial.println("////////////////////////////////////\n");
        delay(1000);
  }
  }
void printIPAddress()
{
  Serial.print("IP address: ");
  for (byte thisByte = 0; thisByte < 4; thisByte++) {
    // print the value of each byte of the IP address:
    Serial.print(Ethernet.localIP()[thisByte], DEC);
    if(thisByte<3){
      Serial.print(".");
    }
  }

  Serial.println();
}
