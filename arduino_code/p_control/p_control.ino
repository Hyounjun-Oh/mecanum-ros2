#include <MsTimer2.h>
#define ENC_COUNT_REV 1326
#define ENC_IN_1_A 18 //5
#define ENC_IN_2_A 20 //3
#define ENC_IN_1_B 19 //4
#define ENC_IN_2_B 21 //2
#define MOT_IN_1 28 //motor driver in1
#define MOT_IN_2 29 //motor driver in2
#define MOT_IN_3 30 //motor driver in3
#define MOT_IN_4 31 //motor driver in4
#define MOT_PWM_PIN_A 6 //motor driver enA
#define MOT_PWM_PIN_B 7 //motor driver enB

boolean Direction_motor_1 = true;
boolean Direction_motor_2 = true;
volatile long motor_1_pulse_count = 0;
volatile long motor_2_pulse_count = 0;
int interval = 100;
float rpm_motor_1 = 0;
float rpm_motor_2 = 0;
float ang_velocity_1 = 0;
float ang_velocity_1_deg = 0;
float ang_velocity_2 = 0;
float ang_velocity_2_deg = 0;
float control_1 = 0;
float control_2 = 0;
float error_1 = 0;
float error_2 = 0;
float error_pre_1 = 0.0;
float error_pre_2 = 0.0;
const float rpm_to_radians = 0.10471975512;
const float rad_to_deg = 57.29578;

float Kp = 0.5; // 0.4 ~ 0.5
float Ki = 0.5; // start : 0.5
float Kd = 0.2;
float PID_1 = 0.0;
float PID_2 = 0.0;
float I_control_sum_1 = 0.0;
float I_control_sum_2 = 0.0;
float D_control_1 = 0.0;
float D_control_2 = 0.0;
long currentTime = 0;
long previousTime = 0;
long elapsedTime = 0;

float targetRPM[2] = {0,0};
float maxRPM = 122.0; //172 not loaded, 122 loaded
String slaveData;

void setup() {
  Serial.begin(115200); //ACM* = 115200
  Serial.setTimeout(50);
  pinMode(ENC_IN_1_A , INPUT_PULLUP);
  pinMode(ENC_IN_1_B , INPUT);
  pinMode(ENC_IN_2_A , INPUT_PULLUP);
  pinMode(ENC_IN_2_B , INPUT);
  pinMode(MOT_IN_1, OUTPUT);
  pinMode(MOT_IN_2, OUTPUT);
  pinMode(MOT_IN_3, OUTPUT);
  pinMode(MOT_IN_4, OUTPUT);
  pinMode(MOT_PWM_PIN_A, OUTPUT);
  pinMode(MOT_PWM_PIN_B, OUTPUT);
 
  attachInterrupt(digitalPinToInterrupt(ENC_IN_1_A), motor_1_pulse, RISING);
  attachInterrupt(digitalPinToInterrupt(ENC_IN_2_A), motor_2_pulse, RISING);

  MsTimer2::set(1000, getRPM);
  MsTimer2::start();
}
 
void loop() {
  currentTime = millis();
  elapsedTime = 0.204;//currentTime - previousTime;
  if(Serial.available() > 0)
  {
    String inputStr = Serial.readStringUntil('\n');
    Split(inputStr,',');
  }
  error_1 = (targetRPM[0] - rpm_motor_1)*Kp;
  error_2 = (targetRPM[1] - rpm_motor_2)*Kp;
  I_control_sum_1 += error_1*Ki*elapsedTime;
  I_control_sum_2 += error_2*Ki*elapsedTime;
  D_control_1 = ((error_1 - error_pre_1== 0 || Kd == 0)?0:(error_1 - error_pre_1)/elapsedTime)*Kd;
  D_control_2 = ((error_2 - error_pre_2== 0 || Kd == 0)?0:(error_2 - error_pre_2)/elapsedTime)*Kd;
  PID_1 = float(error_1/maxRPM*255) + float((I_control_sum_1 == 0 || Ki == 0.0)?0:I_control_sum_1/maxRPM*255) + float((D_control_1 == 0 || Kd == 0)?0:D_control_1/maxRPM*255);
  PID_2 = float(error_2/maxRPM*255) + float((I_control_sum_2 == 0 || Ki == 0.0)?0:I_control_sum_2/maxRPM*255) + float((D_control_2 == 0 || Kd == 0)?0:D_control_2/maxRPM*255);
  Serial.println("---------------------");
  control_1 = float(targetRPM[0]/maxRPM)*255 + PID_1;
  control_2 = float(targetRPM[1]/maxRPM)*255 + PID_2;
  Serial.println(targetRPM[0]);
  Serial.println(targetRPM[1]);
  Serial.println(rpm_motor_1);
  Serial.println(rpm_motor_2);
  Serial.println("---------------------");
  doMotor(MOT_IN_1, MOT_IN_2, MOT_PWM_PIN_A,(control_1>=0)?HIGH:LOW, min(abs(control_1), 255));
  doMotor(MOT_IN_3, MOT_IN_4, MOT_PWM_PIN_B,(control_2>=0)?HIGH:LOW, min(abs(control_2), 255));
  delay(100);
  Serial.flush();
  error_pre_1 = error_1;
  error_pre_2 = error_2;
}
 
void motor_1_pulse() {
   
  // Read the value for the encoder for the right wheel
  int val = digitalRead(ENC_IN_1_B);
 
  if(val == LOW) {
    Direction_motor_1 = false; // Reverse
  }
  else {
    Direction_motor_1 = true; // Forward
  }
   
  if (Direction_motor_1) {
    motor_1_pulse_count++;
  }
  else {
    motor_1_pulse_count--;
  }
}

void motor_2_pulse() {
   
  // Read the value for the encoder for the right wheel
  int val = digitalRead(ENC_IN_2_B);
 
  if(val == LOW) {
    Direction_motor_2 = false; // Reverse
  }
  else {
    Direction_motor_2 = true; // Forward
  }
   
  if (Direction_motor_2) {
    motor_2_pulse_count++;
  }
  else {
    motor_2_pulse_count--;
  }
}
void doMotor(int motor_in_A, int motor_in_B, int motor_rpm_pin ,bool dir, int vel){
  digitalWrite(motor_in_A, dir?HIGH:LOW);
  digitalWrite(motor_in_B, dir?LOW:HIGH);
  analogWrite(motor_rpm_pin, vel);
}

void getRPM(){
  rpm_motor_1 = (float)(motor_1_pulse_count * 60 / ENC_COUNT_REV);
  rpm_motor_2 = (float)(motor_2_pulse_count * 60 / ENC_COUNT_REV);
  motor_1_pulse_count = 0;
  motor_2_pulse_count = 0;
}

//void check_motor_status(float control1, float control2){
//  if (control1 || control2 == "nan"){
//    
//    }
//}

void Split(String sData, char cSeparator){	
	int nCount = 0;
	int nGetIndex = 0 ;
	String sTemp = "";
	String sCopy = sData;

	nGetIndex = sCopy.indexOf(cSeparator);
	sTemp = sCopy.substring(0, nGetIndex);
  targetRPM[0] = sTemp.toFloat();
	sCopy = sCopy.substring(nGetIndex + 1);
  sTemp = sCopy;
  targetRPM[1] = sTemp.toFloat();
}
