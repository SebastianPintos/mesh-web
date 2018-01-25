#include <SPI.h>        

#include <Ethernet2.h>

int sensor0Value = 0; 
int sensor0outputValue = 0;
//MAC Address que usara el arduino (asegurarse de que sea unica)
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
// puerto al cual se envia el paquete  
const int targetPort = 8888;      
// Hostname de destino (opcional) x ej DellXPS12
const char* targetHostname = "hostname"; 
//Ip de Destino
IPAddress targetIP(192, 168, 8, 255);
// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
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
    sensor0Value = (analogRead(A0));
    sensor0outputValue = map(sensor0Value, 0, 1023, 0, 255);
    int sensorVal = digitalRead(2);
    
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
    intTo3Char(sensor0outputValue)+" }";
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
