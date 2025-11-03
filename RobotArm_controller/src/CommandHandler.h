#pragma once
#include <Arduino.h>
#include <vector>

class CommandHandler {
public:
    CommandHandler();

    // Process raw string like "[0,0,0,0,0]"
    void processJointState(const String& raw);

    // Get cleaned command string: "ANGLE j0 j1 j2 j3 j4"
    String getCommand() const;

private:
    std::vector<float> joints;
    String command_str;
};
