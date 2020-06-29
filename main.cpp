#include "mbed.h"
#include "arm_math.h"
#include "FXOS8700CQ.h"
#include "bbcar.h"
#include <math.h>
#include <stdlib.h>

#define bound 0.9
#define go_straight_1 116
#define go_straight_2 40
#define go_straight_3 45
#define go_straight_4 102
#define go_straight_5 45
#define go_straight_6 40
#define go_straight_7 120
#define turn_left_90_1 0.77
#define turn_left_90_2 0.79
#define turn_right_90_1 0.7
#define turn_right_90_2 0.7
#define turn_right_90_3 0.7
#define turn_right_90_4 0.7
#define turn_right_90_5 0.7
#define turn_right_90_6 0.7

Serial pc(USBTX, USBRX);
Serial uart(D1,D0); // tx,rx OpenMV
Serial xbee(D12, D11); // Xbee
DigitalOut led1(LED1);
DigitalOut led2(LED2);
Ticker servo_ticker;
Ticker encoder_ticker;
PwmOut pin9(D9), pin8(D8);
DigitalInOut pin4(D4);
DigitalIn pin10(D10);
BBCar car(pin8, pin9, servo_ticker);
parallax_encoder encoder0(pin10, encoder_ticker);

void ping(float distance);
void straight(int distance);
void left(float turn_left_90);
void right(float turn_rightt_90);
void left1(void);

int main() {

    float log[50];
    parallax_ping  ping1(pin4);
    
    
    led1 = 1;
    led2 = 1;

    straight(go_straight_1);

    left(turn_left_90_1);

    // mission1
    straight(go_straight_2);
    car.goStraight(100);
    ping(45.0);
        
    right(turn_right_90_1);

    car.goStraight(-100);               // back
    wait(1.5);
    car.stop();
    wait(1.0);

    car.goStraight(100);
    ping(18.0);

    // left + straight + right + back
    left(0.8);
    straight(15);
    right(1.1);
    car.goStraight(-80);               // back
    wait(0.8);
    car.stop();
    wait(1.0);

    // take picture
    wait(1);
    char s[21];
    sprintf(s,"image_classification"); // sent the command to OpenMV for taking picture
    uart.puts(s); // sent the command by UART
    wait(3);
    // straight adjust after

    car.goStraight(100);
    ping(18.0);
    right(turn_right_90_2);

    straight(go_straight_3);;

    right(turn_right_90_3);

    straight(go_straight_4);
    right(0.72);

    straight(go_straight_5);

    right(turn_right_90_5);
    car.goStraight(100);
    ping(25.0);

    left(0.25); 

    //read data matrix
    // save the ping data
    for(int i=0;i<5;i++)
    {
        right(0.4);
        left(0.35);
        for (int j=0; j<10;j++) {
            log[i*10 + j] = ping1;
            wait(0.02);
        }
    }

    car.goStraight(-100);               // back
    wait(1.5);
    car.stop();
    wait(1.0);

    left(turn_left_90_2);

    straight(go_straight_6);

    right(turn_right_90_6);

    straight(go_straight_7);

    int flag = 0;
    float a[50];

    if((a[10] <= a[25]) && (a[25] <= a[40])){
        flag = 0;  
    }
    else if((a[10] >= a[25]) && (a[25] <= a[40])){
        if (a[25] - a[10] > 3) flag = 1;
        else falg = 3;
    }
    else flag = 2;

    if(flag == 0){
        xbee.printf("right triangle");
    }
    else if(flag = 1){
        xbee.printf("triangle");
    }
    else if(flag == 2){
        xbee.printf("other");
    }
    else{
        xbee.printf("rectangle");
    }
}

void ping(float distance) {
    led1 = 1;
    parallax_ping  ping1(pin4);
    // ping
        while(1) { 
            if((float)ping1>distance) led1 = 1;
            else{
                led1 = 0;
                car.stop();
                break;
            }
            wait(.01);
        }
        wait(1.0);
}

void straight(int distance) {
    encoder0.reset();
    car.goStraight(100);
    while (encoder0.get_cm() < distance)
        wait_ms(50);
    car.stop();
    wait(0.5);
}

void left(float turn_left_90){
    car.turn(93,0.1);                 // turn left
    wait(turn_left_90);               // adjust angle through lasting time
    car.stop();
    wait(0.5);
}

void right(float turn_right_90){
    car.turn(100,-0.1);                 // turn right
    wait(turn_right_90);                // adjust angle through lasting time
    car.stop();
    wait(1);
}
