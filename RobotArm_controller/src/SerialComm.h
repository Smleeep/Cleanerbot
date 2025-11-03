#pragma once
#include <Arduino.h>
#include "CommandHandler.h"

#define COM_LEN_MAX 128

enum CommState {
    IDLE,
    RECEIVING
};

class SerialComm {
public:
    SerialComm();
    void begin();
    void readCommand();           // Call this in loop()
    String getCleanCommand();     // Get the last processed command
    bool hasCommand() const;      // Returns true if a complete command is available

private:
    CommState commState;
    uint8_t cmdBuffer[COM_LEN_MAX];
    uint8_t cmdIndex;
    String incomingMsg;
    bool commandReady;

    CommandHandler handler;

    void processIncoming();
    void resetBuffer();
};
