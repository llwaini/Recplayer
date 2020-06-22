
const int ledPin =  22;// the number of the LED pin

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);
  
  // set the digital pin as output:
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin,HIGH);
}

unsigned long delay_time = 100;

void loop() {
  // put your main code here, to run repeatedly:
  for(int i=0;i<100;i++){
    
    String cmd = "record ";
    cmd = cmd + String(i) + ".wav";
    Serial.println(cmd);
    delay(delay_time);
    
    cmd = "stop";
    Serial.println(cmd);
    delay(delay_time);
    
    cmd = "play ";
    cmd = cmd + String(i) + ".wav";
    Serial.println(cmd);
    delay(delay_time);
  
  }

}
