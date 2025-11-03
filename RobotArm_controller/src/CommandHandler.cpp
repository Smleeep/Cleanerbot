#include "CommandHandler.h"

CommandHandler::CommandHandler() {
    joints.resize(5, 0.0);
    command_str = "";
}

void CommandHandler::processJointState(const String& raw) {
    // Remove brackets
    String s = raw;
    // Serial.println("Raw input: " + s);
    s.replace("[", "");
    s.replace("]", "");

    // Split by comma and store in joints
    int start = 0;
    int idx = 0;
    while (idx < 5) {
        int comma = s.indexOf(',', start);
        if (comma == -1) comma = s.length();
        String valueStr = s.substring(start, comma);
        joints[idx] = valueStr.toFloat();
        start = comma + 1;
        idx++;
    }

    // Convert to ANGLE format string
    command_str = "ANGLE";
    for (int i = 0; i < 5; i++) {
        command_str += " " + String(joints[i], 6);
    }
}

String CommandHandler::getCommand() const {
    return command_str;
}
