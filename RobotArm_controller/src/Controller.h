#pragma once
#include <Arduino.h>
#include <ESP32Servo.h>
#include "SerialComm.h"

class Controller {
public:
    Controller();
    void begin();    // Call in setup()
    void setup();
    void update();   // Call in loop()

private:
    Servo servo_base;
    Servo servo_1;
    Servo servo_2;
    Servo servo_3;
    Servo servo_4;

    float joint_angles[5]; // radians

    SerialComm serialComm;

    void parseSerialCommand(const String& cmd);
    void writeServos();
};
