#include <SPI.h>        

#include <Ethernet2.h>

int sensor0Value = 0; 
int sensor0outputValue = 0;
//MAC Address que usara el arduino (asegurarse de que sea unica)
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
// puerto al cual se envia el paquete  
const int targetPort = 8888;      
// Hostname de destino (opcional) x ej Ubuntu-VCS30

const char* targetHostname = "hostname";
boolean debug = false; 
//Ip de Destino
IPAddress targetIP(192, 168, 1, 255);
// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  if(digitalRead(2)==false){ //DEBUG MODE saltea conexion DHCP para probar mediciones
    Serial.println("DEBUG MODE");
    debug = true ;
    return;
    }
  Serial.println("\n/////////Iniciando/////////\n");
  Serial.print("Conectando con DHCP...");
  boolean bDHCP=Ethernet.begin(mac);
  Serial.println(boolToString2(bDHCP)+"\n");
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
    int sensorVal = digitalRead(2);
    if(debug){
          String sensorString = boolToString(sensorVal);
          String message="{\"Sensor0\" : "+ 
          measureAmps()+" }";
          Serial.println("////////////DEBUG MODE//////////////\n");
          Serial.println(message+"\n");
          Serial.println("////////////////////////////////////\n");
          delay(1000);
          return;
    }

    
    //Comienza a armar el paquete
    Serial.print("1_Iniciando Paquete...");
    //Hostname o IP del servidor, reemplazar por targetIP para usar ip
    boolean bBegin = Udp.beginPacket(targetIP, targetPort); 
    Serial.println(boolToString2(bBegin)+"\n");
    if(bBegin==false){
      return;}
    //Armando Mensaje
    String sensorString = boolToString(sensorVal);
    String message="{ \"Sensor0\" : "+ sensorString+", \"Sensor1\" : "+ 
    measureAmps()+" }";
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
  
  if( ret <= 0.090 ){//with no load sensor oscilates between 0.08 and 0.09 
    ret = 0;
    }
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

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
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
