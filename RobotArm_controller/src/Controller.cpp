#include "Controller.h"

Controller::Controller() {
    for (int i = 0; i < 5; i++) joint_angles[i] = 0.0;
}

void Controller::begin() {
    // Initialize serial communication
    // serialComm.begin(115200);

    // Attach servos to pins
    servo_base.attach(23); // Update pins accordingly
    servo_1.attach(22);
    servo_2.attach(19);
    servo_3.attach(25);
    servo_4.attach(26);

    // Initialize serial communication
    serialComm.begin();

    // Write 0 angle to all servos
    servo_base.write(0); // 0 rad = 90 degrees for typical servo
    servo_1.write(0);
    servo_2.write(0);
    servo_3.write(0);
    servo_4.write(0);

    // Update joint_angles array
    for (int i = 0; i < 5; i++) {
        joint_angles[i] = 0.0; // 0 radians
    }

    serialComm.begin();
}

void Controller::update() {
    // Read any incoming serial commands
    serialComm.readCommand();
    if (serialComm.hasCommand()) {
        String cmd = serialComm.getCleanCommand();
        // Serial.println("Received Command: " + cmd);
        parseSerialCommand(cmd);
    }

    // Update servo positions
    writeServos();
}

void Controller::parseSerialCommand(const String& cmd) {
    // Expecting format: "ANGLE j0 j1 j2 j3 j4"
    // Example: "ANGLE -1.047 0.977 1.274 0.384 -0.297"
    if (cmd.startsWith("ANGLE")) {
        int idx = 0;
        int start = cmd.indexOf(' ') + 1;
        for (int i = 0; i < 5; i++) {
            int end = cmd.indexOf(' ', start);
            if (end == -1) end = cmd.length();
            String valueStr = cmd.substring(start, end);
            joint_angles[i] = valueStr.toFloat();
            start = end + 1;
        }
    }
}

void Controller::writeServos() {
    // Convert joint angles from radians to degrees
    Serial.println(joint_angles[1] * -180.0 / PI);
    servo_base.write((joint_angles[0] * 180.0 / PI)+90.0);
    servo_1.write((joint_angles[1] * -180.0 / PI)+90.0);
    servo_2.write((joint_angles[2] * 180.0 / PI)+90.0);
    servo_3.write((joint_angles[3] * 180.0 / PI)+90.0);
    servo_4.write((joint_angles[4] * 180.0 / PI)+90.0);
}
