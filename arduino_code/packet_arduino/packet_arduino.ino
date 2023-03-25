void setup() {
  // 시리얼 통신을 시작합니다.
  Serial.begin(115200);
}

void loop() {
  while (Serial.available() < 8);
  
  // 시리얼 버퍼에서 데이터를 읽어옵니다.
  byte data_bytes[8];
  Serial.readBytes(data_bytes, 8);
  
  // 이진 데이터를 실수 값으로 변환합니다.
  float data1 = *(float*)(data_bytes);
  float data2 = *(float*)(data_bytes + 4);
  
  // 값을 출력합니다.
  Serial.print("data1: ");
  Serial.println(data1);
  Serial.print("data2: ");
  Serial.println(data2);
}

//void serialEvent() {
//  Serial.setTimeout(10);
//  if(Serial.available() > 8)
//  {
//    byte data_bytes[8];
//    Serial.readBytes(data_bytes, 8);
//    Serial.print(*(float*)(data_bytes));
//  }
//  
//}
