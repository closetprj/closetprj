char p;
int x_1;
int x_2;
int x_3;
int flag;

void setup()
{
 Serial.begin(9600);
 pinMode(2,OUTPUT);
 pinMode(3,OUTPUT);
 pinMode(4,OUTPUT);
 pinMode(5,OUTPUT);
 
 pinMode(6,OUTPUT);
 pinMode(7,OUTPUT);
 pinMode(8,OUTPUT);
 pinMode(9,OUTPUT);

 pinMode(10,OUTPUT);
 pinMode(11,OUTPUT);
 pinMode(12,OUTPUT);
 pinMode(13,OUTPUT);


}
 
void loop()
{
  while(Serial.available())
  { 
     
     //char p;
     
     int c = Serial.read();
       if(c == '1')
       {
        light1();
        light2();
        light3();
        
        Serial.println("Your recommended clothes: ");
        Serial.print(x_1);
        Serial.print(", ");
        Serial.print(x_2);
        Serial.print(" AND ");
        Serial.println(x_3);
        Serial.println("Do you like?");
        flag=1;

        
       }
       /*p = Serial.parseInt();
       Serial.print(p);*/
       else if(flag==1 && c == 'Y')
       {
        digitalWrite(x_1, HIGH);
        digitalWrite(x_2, HIGH);
        digitalWrite(x_3, HIGH);
          delay(3000);
        digitalWrite(x_1, LOW);
        digitalWrite(x_2, LOW);
        digitalWrite(x_3, LOW);
         
          flag=2;
       }
       else if((flag==1 && c == 'N')){
        Serial.println("which cloth would you like to choose? ");
         flag=3;
       }
      else if (flag ==3){
        //p = Serial.parseInt();
        //Serial.println(p);
        //c = Serial.read();
        int num = c-'0';
        //Serial.println(num);
        //int num =3; 
        digitalWrite(num, HIGH);
        delay(1000);
        }
  }
}

void light1(){
      x_1=rand()%4+2;
      //Serial.println(x);
      digitalWrite(x_1, HIGH);
      delay(1000);
      digitalWrite(x_1, LOW);
      delay(1000);
      digitalWrite(x_1, HIGH);
      delay(1000);
      digitalWrite(x_1, LOW);
       delay(1000);
      digitalWrite(x_1, HIGH);
      delay(1000);
      digitalWrite(x_1, LOW);
  }
 void light2(){
      x_2=rand()%4+6;
      //Serial.println(x);
      digitalWrite(x_2, HIGH);
      delay(1000);
      digitalWrite(x_2, LOW);
      delay(1000);
      digitalWrite(x_2, HIGH);
      delay(1000);
      digitalWrite(x_2, LOW);
       delay(1000);
      digitalWrite(x_2, HIGH);
      delay(1000);
      digitalWrite(x_2, LOW);
  }
 void light3(){
      x_3=rand()%4+10;
      //Serial.println(x);
      digitalWrite(x_3, HIGH);
      delay(1000);
      digitalWrite(x_3, LOW);
      delay(1000);
      digitalWrite(x_3, HIGH);
      delay(1000);
      digitalWrite(x_3, LOW);
       delay(1000);
      digitalWrite(x_3, HIGH);
      delay(1000);
      digitalWrite(x_3, LOW);
  }
