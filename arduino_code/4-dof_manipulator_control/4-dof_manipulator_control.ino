/*******************************************************************************
* Copyright 2016 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

/* Authors: Taehun Lim (Darby) */

/* Editor: Hyounjun Oh 
   E-mail : ohj_980918@naver.com
   Jeonbuk-National University*/
/* [수정사항]
2023. 01. 28. 다이나믹셀 ID1 과 ID2 동시제어 
2023. 02. 05. 다이나믹셀 ID1 ~ ID4 사다리꼴 프로파일 적용. 제어완료.
2023. 02. 06. 조인트 값 파이썬으로부터 Serial2 포트로 받아오기.*/


#include <DynamixelWorkbench.h>
#include <MsTimer2.h>

#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   
#define BAUDRATE  57600
#define JOINT_1    1 //DXL_ID
#define JOINT_2    2
#define JOINT_3    3
#define JOINT_4    4

DynamixelWorkbench dxl_wb;

int joint[3]; //조인트 값 담을 배열 선언.
int32_t get_position[3];
int32_t get_desired_position[3];

void setup() 
{
  Serial.begin(2000000); //다이나믹셀 제어용 UART
  const char *log;
  bool result = false;
  bool joint_1_check = false; //조인트 상태 체크
  bool joint_2_check = false;
  bool joint_3_check = false;
  bool joint_4_check = false;

  int joint_1_ID = JOINT_1;
  int joint_2_ID = JOINT_2;
  int joint_3_ID = JOINT_3;
  int joint_4_ID = JOINT_4;
  volatile float joint_1 = 0.0;
  volatile float joint_2 = 0.0;
  volatile float joint_3 = 0.0;
  volatile float joint_4 = 0.0;
  volatile float joint_1_old = 0.0;
  volatile float joint_2_old = 0.0;
  volatile float joint_3_old = 0.0;
  volatile float joint_4_old = 0.0;
  uint16_t model_number = 0;

  // 모터 상태 초기화.

  result = dxl_wb.init(DEVICE_NAME, BAUDRATE, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to init");
  }
  else
  {
    Serial.print("Succeeded to init : ");
    Serial.println(BAUDRATE);  
  }

  joint_1_check = dxl_wb.ping(joint_1_ID, &model_number, &log);
  joint_2_check = dxl_wb.ping(joint_2_ID, &model_number, &log);
  joint_3_check = dxl_wb.ping(joint_3_ID, &model_number, &log);
  joint_4_check = dxl_wb.ping(joint_4_ID, &model_number, &log);
  if (joint_1_check == false || joint_2_check == false || joint_3_check == false || joint_4_check == false)
  {
    Serial.println(log);
    Serial.println("Failed to ping");
  }
  else
  {
    Serial.println("Succeeded to ping");
  }

  joint_1_check = dxl_wb.jointMode(joint_1_ID, 0, 0, &log);
  joint_2_check = dxl_wb.jointMode(joint_2_ID, 0, 0, &log);
  joint_3_check = dxl_wb.jointMode(joint_3_ID, 0, 0, &log);
  joint_4_check = dxl_wb.jointMode(joint_4_ID, 0, 0, &log);
  if (joint_1_check == false || joint_2_check == false || joint_3_check == false || joint_4_check == false)
  {
    Serial.println(log);
    Serial.println("Failed to change joint mode");
  }
  else
  {
    Serial.println("Succeed to change joint mode");
    Serial.println("Dynamixel is moving...");
  }
  dxl_wb.itemWrite(JOINT_1_ID, "Drive_Mode", 4); //DriveMode Profile Configuration 정의 
  dxl_wb.itemWrite(JOINT_1_ID, "Profile_Acceleration", 4989);
  dxl_wb.itemWrite(JOINT_1_ID, "Profile_Velocity", 3506);

  dxl_wb.itemWrite(JOINT_2_ID, "Drive_Mode", 4); //DriveMode Profile Configuration 정의 
  dxl_wb.itemWrite(JOINT_2_ID, "Profile_Acceleration", 4989);
  dxl_wb.itemWrite(JOINT_2_ID, "Profile_Velocity", 3506); 

  dxl_wb.itemWrite(JOINT_3_ID, "Drive_Mode", 4); //DriveMode Profile Configuration 정의 
  dxl_wb.itemWrite(JOINT_3_ID, "Profile_Acceleration", 4989);
  dxl_wb.itemWrite(JOINT_3_ID, "Profile_Velocity", 3506); 

  dxl_wb.itemWrite(JOINT_4_ID, "Drive_Mode", 4); //DriveMode Profile Configuration 정의 
  dxl_wb.itemWrite(JOINT_4_ID, "Profile_Acceleration", 4989);
  dxl_wb.itemWrite(JOINT_4_ID, "Profile_Velocity", 3506);

  MsTimer2::set(50, position_check);
  MsTimer2::start();
}

void loop() 
{
}

void move_joints(joint_1, joint_2, joint_3, joint_4){
  dxl_wb.goalPosition(JOINT_1_ID, desired_position_2[0]);
  dxl_wb.goalPosition(JOINT_2_ID, desired_position_2[1]);
  dxl_wb.goalPosition(JOINT_3_ID, desired_position_2[2]);
  dxl_wb.goalPosition(JOINT_4_ID, desired_position_2[3]);
}

void delay_motor(int joint_ID){
  while ((abs(get_desired_position[joint_ID-1] - get_position[joint_ID-1])) > 1){
    dxl_wb.itemRead(joint_ID, "Goal_Position", &get_desired_position[joint_ID-1]);
    dxl_wb.itemRead(joint_ID, "Present_Position", &get_position[joint_ID-1]);
    delay(1);
  };
};

int maximum_calculation(){
  //get goal position 
  dxl_wb.itemRead(JOINT_1, "Goal_Position", &get_desired_position[0]);
  dxl_wb.itemRead(JOINT_1, "Present_Position", &get_position[0]);
  dxl_wb.itemRead(JOINT_2, "Goal_Position", &get_desired_position[1]);
  dxl_wb.itemRead(JOINT_2, "Present_Position", &get_position[1]);
  dxl_wb.itemRead(JOINT_3, "Goal_Position", &get_desired_position[2]);
  dxl_wb.itemRead(JOINT_3, "Present_Position", &get_position[2]);
  dxl_wb.itemRead(JOINT_4, "Goal_Position", &get_desired_position[3]);
  dxl_wb.itemRead(JOINT_4, "Present_Position", &get_position[3]);
  Serial.print("desired position : [");
  Serial.print(get_desired_position[0]);
  Serial.print(", ");
  Serial.print(get_desired_position[1]);
  Serial.print(", ");
  Serial.print(get_desired_position[2]);
  Serial.print(", ");
  Serial.print(get_desired_position[3]);
  Serial.println("]");

  Serial.print("present position : [");
  Serial.print(get_position[0]);
  Serial.print(", ");
  Serial.print(get_position[1]);
  Serial.print(", ");
  Serial.print(get_position[2]);
  Serial.print(", ");
  Serial.print(get_position[3]);
  Serial.println("]");
  int arr[4] = {abs(get_desired_position[0]-get_position[0]),abs(get_desired_position[1]-get_position[1]),abs(get_desired_position[2]-get_position[2]),abs(get_desired_position[3]-get_position[3])};
  int max = 0;
  int index = 0;
  for(int i = 0;i<4;i++)
  {
    if(arr[i] > max ){
      max = arr[i];
      index = i+1;
    };

  };
  if (index == 0){index = 1;};
  Serial.println(max);
  Serial.println(index);
  return index;
};

void position_check(){
  dxl_wb.itemRead(JOINT_1, "Goal_Position", &get_desired_position[0]);
  dxl_wb.itemRead(JOINT_1, "Present_Position", &get_position[0]);
  dxl_wb.itemRead(JOINT_2, "Goal_Position", &get_desired_position[1]);
  dxl_wb.itemRead(JOINT_2, "Present_Position", &get_position[1]);
  dxl_wb.itemRead(JOINT_3, "Goal_Position", &get_desired_position[2]);
  dxl_wb.itemRead(JOINT_3, "Present_Position", &get_position[2]);
  dxl_wb.itemRead(JOINT_4, "Goal_Position", &get_desired_position[3]);
  dxl_wb.itemRead(JOINT_4, "Present_Position", &get_position[3]);
}

void serialEvent() {
  String inputStr = Serial.readStringUntil('\n');
  Split(inputStr,',');
  //noise filter
  if (abs(joint_1 - joint_1_old) > 100){
    joint_1 = joint_1_old;
  }
  if (abs(joint1_2 - joint_2_old) > 100){
    joint_2 = joint_2_old;
  }
  if (abs(joint_3 - joint_3_old) > 100){
    joint_3 = joint_3_old;
  }
  if (abs(joint1_4 - joint_4_old) > 100){
    joint_4 = joint_4_old;
  }
  joint_1_old = joint_1;
  joint_2_old = joint_2;
  joint_3_old = joint_3;
  joint_4_old = joint_4;
}

void Split(String sData, char cSeparator)
{	
	int nCount = 0;
	int nGetIndex = 0 ;
 
	//임시저장
	String sTemp = "";
 
	//원본 복사
	String sCopy = sData;
  int i = 0;
	while(true)
	{
		//구분자 찾기
		nGetIndex = sCopy.indexOf(cSeparator);
 
		//리턴된 인덱스가 있나?
		if(-1 != nGetIndex)
		{
			//있다.
 
			//데이터 넣고
			sTemp = sCopy.substring(0, nGetIndex);
      joint[i] = sTemp.toInt();
		
			//뺀 데이터 만큼 잘라낸다.
			sCopy = sCopy.substring(nGetIndex + 1);
		}
		else
		{
			//없으면 마무리 한다.
      joint[i] = sCopy.toInt();
			break;
		}
 
		//다음 문자로~
		++nCount;
    ++i;
	}
 
}
