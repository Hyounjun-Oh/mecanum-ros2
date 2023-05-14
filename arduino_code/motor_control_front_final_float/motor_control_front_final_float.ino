//Jeonbuk National University
//Hyounjun Oh 
///////////////////////////////////////
//////////////////////////////////////
//////////////    주의      ///////////
/////////////Front Rear 확인//////////
//////////////////////////////////////
/////////////////////////////////////
#include <MsTimer2.h>
#define ENC_COUNT_REV 1326
#define ENC_IN_1_A 20 //5
#define ENC_IN_2_A 18 //3 original : 20
#define ENC_IN_1_B 21 //4 
#define ENC_IN_2_B 19 //2 original : 21
#define MOT_IN_3 28 //motor driver in1
#define MOT_IN_4 29 //motor driver in2
#define MOT_IN_1 30 //motor driver in3
#define MOT_IN_2 31 //motor driver in4
#define MOT_PWM_PIN_B 6 //motor driver enA
#define MOT_PWM_PIN_A 7 //motor driver enB
// motor value is OK
// PID control is wrong
boolean Direction_motor_1 = true;
boolean Direction_motor_2 = true;
volatile long motor_1_pulse_count = 0;
volatile long motor_2_pulse_count = 0;
float rpm_motor_1 = 0;
float rpm_motor_2 = 0;
float ang_velocity_1 = 0;
float ang_velocity_1_deg = 0;
float ang_velocity_2 = 0;
const float rpm_to_radians = 0.10471975512;
const float rad_to_deg = 57.29578;

// Test
// | Kp | Ki  | Kd  |
// |0.45|0.5  |0.0  | : overshoot, wave
// |0.45|0.2  |0.0  | : more better
// |0.45|0.1  |0.0  | : I_control value is shooting when velocity is changed.
// |0.1 |0.1  |0.0  | : P_control value is too small so entire PID value down too slow.
// -- D_control enable
// |0.3 |0.1  |1.0  | : D_control wave too much.
// |0.3 |0.1  |0.5  | : D_control wave go away.
//
volatile float Kp_1 = 1.15; // wave : 2.3 z_Kp : 0.5*2.3 = 1.15
volatile float Ki_1 = 0.2; // 0.2
volatile float Kd_1 = 0.1; //0.1
volatile float Ks_1 = 1; // slowdown motor
volatile float Kp_2 = 1.15; // wave : 2.3 z_Kp : 0.5*2.3 = 1.15
volatile float Ki_2 = 0.2; // 0.2
volatile float Kd_2 = 0.1; //0.1
volatile float Ks_2 = 1; // slowdown motor
float PID_1 = 0.0;
float PID_2 = 0.0;
float P_control_1 = 0.0;
float P_control_2 = 0.0;
float I_control_1 = 0.0;
float I_control_2 = 0.0;
float D_control_1 = 0.0;
float D_control_2 = 0.0;
float ang_velocity_2_deg = 0;
float control_1 = 0;
float control_2 = 0;
float error_1 = 0;
float error_2 = 0;
float error_pre_1 = 0.0;
float error_pre_2 = 0.0;
float control_1_pre = 0.0;
float control_2_pre = 0.0;
int count = 0;
volatile float targetRPM_1 = 0;
volatile float targetRPM_2 = 0;
volatile float targetRPM_1_old = 0.0;
volatile float targetRPM_2_old = 0.0;
volatile float limit_max_RPM = 122;
volatile float limit_min_RPM = -122;
float maxRPM = 90.0; //172 not loaded, 122 loaded
volatile String slaveData;

void setup() {
  Serial.begin(1000000); //ACM* = 115200
  Serial.setTimeout(0);
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
  MsTimer2::set(50, getRPM);
  MsTimer2::start();
  Serial.flush();
}

void loop() {
//  Serial.println("target_rpm_1,now_rpm_1,D");
//  Serial.print(targetRPM_2);
//  Serial.print(",");
//  Serial.print(rpm_motor_2);
//  Serial.print(",");
//  Serial.println(error_2*Kp_2);
//  delay(50);
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
  float damp_1 = 0.0; // 급가속을 방지하기위한 댐핑 도
  float damp_2 = 0.0;
  if (control_1_pre >= 7.64){
    damp_1 = 0.5;
  }else if (control_1_pre >= 5.73){
    damp_1 = 3.0;
  }else{
    damp_1 = 4.0;
  }
  if (control_2_pre >= 7.64){
    damp_2 = 0.5;
  }else if (control_2_pre >= 5.73){
    damp_2 = 3.0;
  }else{
    damp_2 = 4.0;
  }
  rpm_motor_1 = (float)(motor_1_pulse_count * 1200 / ENC_COUNT_REV);
  rpm_motor_2 = (float)(motor_2_pulse_count * 1200 / ENC_COUNT_REV);
  error_1 = (targetRPM_1 - rpm_motor_1);
  error_2 = (targetRPM_2 - rpm_motor_2);
  I_control_1 += error_1*1;
  I_control_2 += error_2*1;
  //튀는 오류 잡기
  if (error_1 - error_pre_1 == 0){
    D_control_1 = 0;
  }else{
    D_control_1 = (error_1 - error_pre_1);
  }
  if (error_1 - error_pre_1 == 0){
    D_control_2 = 0;
  }else{
    D_control_2 = (error_2 - error_pre_2);;
  }
  PID_1 = error_1*Kp_1 + I_control_1*Ki_1 + D_control_1*Kd_1;
  PID_2 = error_2*Kp_2 + I_control_2*Ki_2 + D_control_2*Kd_2;
  error_pre_1 = error_1;
  error_pre_2 = error_2;
  control_1 = float(((targetRPM_1*Ks_1 + PID_1)/maxRPM)*255);
  control_2 = float(((targetRPM_2*Ks_2 + PID_2)/maxRPM)*255);
  //타겟 RPM이 0임에도 잔류 토크가 남아있는경우를 방지하기 위해서 입력 토크가 0이면 모든 PID계수가 0이됨.
  if (targetRPM_1 == 0){
    control_1 = 0;
    I_control_1 = 0;
    D_control_1 = 0;
  }
  if(targetRPM_2 == 0){
    control_2 = 0;
    I_control_2 = 0;
    D_control_2 = 0;
  }
  //값이 갑자기 치솟는 현상 방지.
  //1.91 -> 3.82 -> 5.73 -> 7.64 ...
  // x3   ->   x3    -> x2 -> x0.5
  if ((control_1 != 0) and (abs(control_1) > abs(control_1) + abs(control_1_pre)*damp_1)){
    control_1 = control_1_pre;
  }
  if ((control_2 != 0 ) and (abs(control_2) > abs(control_2) + abs(control_2_pre)*damp_2)){
    control_2 = control_2_pre;
  }
  doMotor(MOT_IN_1, MOT_IN_2, MOT_PWM_PIN_A,(control_1>=0)?HIGH:LOW, min(abs(control_1), 255));
  doMotor(MOT_IN_3, MOT_IN_4, MOT_PWM_PIN_B,(control_2>=0)?HIGH:LOW, min(abs(control_2), 255));
  control_1_pre = control_1;
  control_2_pre = control_2;
  motor_1_pulse_count = 0;
  motor_2_pulse_count = 0;
  // 양단 4 테스트 완료
  if (count == 2){
    Serial.println(String(1)+','+String(rpm_motor_1)+','+String(rpm_motor_2));
    count = 0;
  }
  count = count + 1;
}

void Split(String sData, char cSeparator){	
	int nCount = 0;
	int nGetIndex = 0 ;
	String sTemp = "";
	String sCopy = sData;

	nGetIndex = sCopy.indexOf(cSeparator);
	sTemp = sCopy.substring(0, nGetIndex);
  targetRPM_1 = sTemp.toFloat();
	sCopy = sCopy.substring(nGetIndex + 1);
  sTemp = sCopy;
  targetRPM_2 = sTemp.toFloat();
}

void serialEvent() {
  String inputStr = Serial.readStringUntil('\n');
  Split(inputStr,',');
  //noise filter
  if (abs(targetRPM_1 - targetRPM_1_old) > 100){
    targetRPM_1 = targetRPM_1_old;
  }
  if (abs(targetRPM_2 - targetRPM_2_old) > 100){
    targetRPM_2 = targetRPM_2_old;
  }
  targetRPM_1_old = targetRPM_1;
  targetRPM_2_old = targetRPM_2;
  //sireal publish
}
