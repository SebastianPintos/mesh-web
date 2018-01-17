#include <SPI.h>        

#include <Ethernet2.h>

int sensor0Value = 0; 
int sensor0outputValue = 0;
//MAC Address que usara el arduino (asegurarse de que sea unica)
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

//the IP address is dependent on your network
IPAddress ip(192, 168, 2, 100);
//the dns server ip
IPAddress dnServer(192, 168, 2, 1);
// the router's gateway address:
IPAddress gateway(192, 168, 2, 1);
// the subnet:
IPAddress subnet(255, 255, 255, 0);
// Target IP
IPAddress targetIP(192, 168, 2, 1);
// Hostname de destino (opcional)
const char* targetHostname = "hostname"; 
// puerto al cual se envia el paquete  
const int targetPort = 8888;      
// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  Serial.println("\n/////////Iniciando/////////\n");
  //DEBUG MODE saltea conexion para probar mediciones
  boolean debug = !digitalRead(2);
  while(debug){
        String message="{\"Sensor0\" : "+ 
        measureAmps()+" }";
        Serial.println("////////////DEBUG MODE//////////////\n");
        Serial.println(message+"\n");
        Serial.println("////////////////////////////////////\n");
        delay(1000);
  }
  
  Serial.print("Iniciando Ethernet...");
  Ethernet.begin(mac, ip, dnServer, gateway, subnet);
  Serial.println("listo\n");
  //Necesario inicializar el puerto antes de poder transmitir
  Serial.print("Preparando Puerto UDP...");
  boolean bInit=Udp.begin(targetPort);
  Serial.println(boolToString2(bInit)+"\n");
  printIPAddress();  
  Serial.println("\n/////////Iniciado/////////\n");
}



void loop() {
   
    //Mide los sensores
    int stage = 0;
    sensor0Value = (analogRead(A0));
    sensor0outputValue = map(sensor0Value, 0, 1023, 0, 255);
    int sensorVal = digitalRead(2);
    
    //Comienza a armar el paquete
    Serial.print("1_Iniciando Paquete...");
    //IP o Hostname del servidor, reemplazar por targetHostname para usar hostname
    boolean bBegin = Udp.beginPacket(targetIP, targetPort); 
    Serial.println(boolToString2(bBegin)+"\n");
    if(bBegin==false){
      return;}
    //Armando Mensaje
   // String sensorString = boolToString(sensorVal);
    String message="{ \"Sensor0\" : "+measureAmps()+" }";
    //Enviando Paquete
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
    Serial.println("//////////////////////////\n");
    
    delay (2000);

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
