#include "SerialComm.h"

SerialComm::SerialComm() : commState(IDLE), cmdIndex(0), commandReady(false) {
    resetBuffer();
}

void SerialComm::begin() {
    Serial.begin(115200);
    while (!Serial) {
        // Wait for serial port to be ready
        delay(10);
    }
    Serial.println("SerialComm READY");
}

void SerialComm::readCommand() {
    while (Serial.available()) {
        char data = Serial.read();  // read as char, not uint8_t
        if (commState == IDLE) {
            commState = RECEIVING;
            cmdIndex = 0;
        }

        if (cmdIndex < COM_LEN_MAX - 1) { // leave space for null terminator
            cmdBuffer[cmdIndex++] = data;
        }

        if (data == '\n') {  // end of command
            commState = IDLE;
            cmdBuffer[cmdIndex] = '\0'; // null-terminate

            // Print safely
            // Serial.println((char*)cmdBuffer);

            // Process the cleaned-up message
            processIncoming();

            // Reset buffer after processing
            resetBuffer();
        }
    }
}




void SerialComm::processIncoming() {
    incomingMsg = String((char*)cmdBuffer);
    handler.processJointState(incomingMsg); // Clean up the raw command
    commandReady = true;
}

void SerialComm::resetBuffer() {
    memset(cmdBuffer, 0, COM_LEN_MAX);
    cmdIndex = 0;
    commState = IDLE;
}

String SerialComm::getCleanCommand() {
    if (commandReady) {
        commandReady = false;
        return handler.getCommand();
    }
    return "";
}

bool SerialComm::hasCommand() const {
    return commandReady;
}
