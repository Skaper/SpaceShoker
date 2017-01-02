//Battery power

unsigned long timeLastPower;

int timeOn = 250; 
unsigned long  timeLastOn;
int relayState = 0;
int shokerLevel = 1;

int highRelayPin = 9;
int lowRelayPin = 10;
int countShock =  0;
void setup() {
  
  Serial.begin(115200);
  timeLastPower = millis();
  pinMode(highRelayPin, OUTPUT);
  pinMode(lowRelayPin, OUTPUT);
  digitalWrite(lowRelayPin, LOW);
  digitalWrite(highRelayPin, LOW);
  
}

void loop() {
  readVolts(relayState, shokerLevel); //Battery Power 
  if(Serial.available()){
    char comIndicator = Serial.read();
    switch(comIndicator){
      //Set servo position T[shokerLevel]>[relayState]\n
      case 'T':{
        shokerLevel = readValue(); // 1 or 2
        relayState = readValue(); // 0 or 1
        //Serial.print(shokerLevel);Serial.print(" > ");Serial.println(relayState);
        break;
      }
    }
    
    Serial.flush();
  }
}


int readVolts(int state, int shokerLevel){
  if ((millis()-timeLastPower)>500 && state == 1){
    timeLastPower = millis();
    timeLastOn = millis();
    if (shokerLevel ==1){ //ON
      digitalWrite(lowRelayPin, HIGH);
    }else if (shokerLevel ==2){
      digitalWrite(highRelayPin, HIGH);
    }
   
  }
  if(millis()-timeLastOn > timeOn){
    //Off
     digitalWrite(lowRelayPin, LOW);
     digitalWrite(highRelayPin, LOW);
     timeLastOn = millis();
     //shokerLevel = readValue(); // 1 or 2
     //countShock +=1;
     relayState = 0; 
  }
  //if (countShock >3){
  //  relayState = 0; 
  //  countShock = 0;
  //}
  
}

//Read value from Serial port
int readValue(){
  byte namberCount=0;
  char nambers[5];
  char buf;
  while(1){
    if(Serial.available()){
      buf = Serial.read();
      if(buf != '\n' && buf != '>'){
        nambers[namberCount]= buf;
        namberCount++;
      }else return atoi(nambers);  
    }
  }
}

