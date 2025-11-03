#include "Controller.h"

Controller robot;

void setup() {
  Serial.begin(115200);
	delay(1000); // Optional, sometimes helps
	Serial.println("hi"); // report ready

    robot.begin();
}

void loop() {
    robot.update();
}


// #include <ESP32Servo.h>

// // Define servo pins
// const int servoPin1 = 19;
// const int servoPin2 = 22;
// const int servoPin3 = 23;

// // Create servo objects
// Servo servo1;
// Servo servo2;
// Servo servo3;

// void setup() {
//   Serial.begin(115200);

//   // Attach servos to pins
//   servo1.attach(servoPin1);
//   servo2.attach(servoPin2);
//   servo3.attach(servoPin3);

//   Serial.println("Setting all servos to 0 degrees...");
//   servo1.write(0);
//   servo2.write(0);
//   servo3.write(0);
//   delay(2000); // wait 2 seconds

//   // Serial.println("Moving all servos to 180 degrees...");
//   // servo1.write(180);
//   // servo2.write(180);
//   // servo3.write(180);
//   // delay(2000); // wait 2 seconds

//   // Serial.println("Test complete. Looping motion...");
// }

// void loop() {
//   // Move smoothly between 0 and 180 degrees for testing
//   // for (int angle = 0; angle <= 180; angle += 5) {
//   //   servo1.write(angle);
//   //   // servo2.write(angle);
//   //   // servo3.write(angle);
//   //   delay(100);
//   // }

//   // for (int angle = 180; angle >= 0; angle -= 5) {
//   //   servo1.write(angle);
//   //   // servo2.write(angle);
//   //   // servo3.write(angle);
//   //   delay(100);
//   // }
// }

// #include <ESP32Servo.h>

// // Define servo pins
// const int servoPin1 = 19;
// const int servoPin2 = 22;
// const int servoPin3 = 23;

// // Create servo objects
// Servo servo1;
// Servo servo2;
// Servo servo3;

// void setup() {
//   Serial.begin(115200);
  
//   // Attach servos to pins
//   servo1.attach(servoPin1);
//   servo2.attach(servoPin2);
//   servo3.attach(servoPin3);

//   // Move all servos to 0 degrees
//   servo1.write(0);
//   servo2.write(0);
//   servo3.write(0);

//   Serial.println("All servos set to 0 degrees");
// }

// void loop() {
//   // Nothing to do here
// }


// #include <Arduino.h>
// #include <ESP32Servo.h>

// // Define servo objects
// Servo servo1;
// Servo servo2;
// Servo servo3;

// // Servo pins
// const int pin1 = 19;
// const int pin2 = 22;
// const int pin3 = 23;

// // Servo positions
// int pos = 0;  // Start at 0 degrees

// void setup() {
//   Serial.begin(115200);
//   Serial.println("Starting servo test...");

//   // Attach servos
//   servo1.attach(pin1);
//   servo2.attach(pin2);
//   servo3.attach(pin3);

//   // Move all servos to 0 degrees
//   servo1.write(0);
//   servo2.write(0);
//   servo3.write(0);

//   delay(1000); // Give time to reach start position
// }

// void loop() {
//   // Slowly move from 0° to 90°
//   for (pos = 0; pos <= 90; pos++) {
//     servo1.write(pos);
//     servo2.write(pos);
//     servo3.write(pos);
//     Serial.print("Servo position: ");
//     Serial.println(pos);
//     delay(20); // Small delay for smooth motion
//   }

//   delay(1000); // Hold at 90°

//   // Optionally move back to 0°
//   for (pos = 90; pos >= 0; pos--) {
//     servo1.write(pos);
//     servo2.write(pos);
//     servo3.write(pos);
//     Serial.print("Servo position: ");
//     Serial.println(pos);
//     delay(20);
//   }

//   delay(1000); // Hold at 0°, repeat
// }
