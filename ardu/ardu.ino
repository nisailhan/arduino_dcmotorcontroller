#define echoPin_us1 6
#define trigPin_us1 7
#define echoPin_us2 3
#define trigPin_us2 4
#define gasPin 2
#define motorEnableAPin 9
#define motorEnableBPin 8
#define alarmPin 13

String readString; //main captured String
String sendString; //main string for sending data

bool flag_start_conveyor;
int measurement1, measurement2;

void setup(){

  Serial.begin(9600); // Initialize serial with 9600 baudrate
  //ultrasonic sensor 1
  pinMode(trigPin_us1, OUTPUT);
  pinMode(echoPin_us1, INPUT);
  //ultrasonic sensor 2
  pinMode(trigPin_us2, OUTPUT);
  pinMode(echoPin_us2, INPUT);
  pinMode(gasPin, INPUT);
  pinMode(motorEnableAPin, OUTPUT);
  pinMode(motorEnableBPin, OUTPUT);
  pinMode(alarmPin, OUTPUT);
  flag_start_conveyor= false;
}

void loop(){
    //Serial ComSerial.available()
    
    if (true){
        char c = Serial.read();  //gets one byte from serial buffer
        /*
        if (Serial.available()>0){
          Serial.println("Arrived Command:");
          Serial.println(c);
        }*/
        if (c=='T'){
          flag_start_conveyor= true;
        }
        else if (c=='P'){
          flag_start_conveyor= false;
        }
        sendString+=String(flag_start_conveyor);
        sendString+=","; 
        readString=""; //clears variable for new input
    }
    //Gas Sensor Control
    if (digitalRead(gasPin)==HIGH){
      //Serial.println("GAS DANGER");
      digitalWrite(alarmPin, HIGH);
      sendString+="1,";
    }
    else{
      digitalWrite(alarmPin, LOW);
      sendString+="0,";
    }
    //Serial.println("Conveyor State:");
    //Serial.println(flag_start_conveyor);

    if (flag_start_conveyor){
      digitalWrite(motorEnableAPin, HIGH);
      digitalWrite(motorEnableBPin, LOW);
      //Serial.println("Taking Measurement..");
      delay(10);
      measurement1,measurement2= us_take_measurement();
      //sendData(measurement1,measurement2);
      //Serial.println("Done.");
      //measurement1,measurement2=0,0;
      //debug purpose
      delay(200);
    }
    else{
      digitalWrite(motorEnableAPin, LOW);
      digitalWrite(motorEnableBPin, LOW);
      sendString+="-1,"; // "0,1,-1,-1,"
      sendString+="-1,";
      Serial.println(sendString);
      delay(200);
    }
 sendString="";
 delay(100);
}

int us_take_measurement(){
    /*
    @input: Cofig[int]
            <- 1: Only First ultrasonic sensor measurement
            <- 2: Only Second ultrasonic sensor measurement
            <- 3: Both ultrasonic sensor measurement
    */
    long delta_t, distance_us1, distance_us2;

    digitalWrite(trigPin_us1, LOW);
    delay(2);
    digitalWrite(trigPin_us1, HIGH);
    delay(10);
    digitalWrite(trigPin_us1, LOW);

    delta_t= pulseIn(echoPin_us1,HIGH);
    distance_us1= delta_t/58.2<;
    delay(50);

    
    digitalWrite(trigPin_us2, LOW);
    delay(2);
    digitalWrite(trigPin_us2, HIGH);
    delay(10);
    digitalWrite(trigPin_us2, LOW);

    delta_t= pulseIn(echoPin_us2,HIGH);
    distance_us2= delta_t/58.2;
    delay(50);
    sendString+=String(distance_us1);
    sendString+=",";
    sendString+=String(distance_us2);
    sendString+=",";
    Serial.println(sendString);
    /*Serial.println("Distance1");
    Serial.println(distance_us1);
    Serial.println("Distance2");
    Serial.println(distance_us2);*/
    return distance_us1, distance_us2;
    //configpurpose//return distance_us1;
}

void sendData(int distance1, int distance2){
    Serial.println("Distance1");
    Serial.println(distance1);
    Serial.println("Distance2");
    Serial.println(distance2);
}
