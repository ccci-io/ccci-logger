/**
 * @file h_SDI-12_slave_implementation.ino
 * @copyright (c) 2013-2020 Stroud Water Research Center (SWRC)
 *                          and the EnviroDIY Development Team
 *            This example is published under the BSD-3 license.
 * @date 2016
 * @author D. Wasielewski
 *
 * @brief Example I:  SDI-12 PC Interface
 *
 *  Arduino-based USB dongle translates serial comm from PC to SDI-12 (electrical and
 * timing)
 *  1. Allows user to communicate to SDI-12 devices from a serial terminal emulator
 * (e.g. PuTTY).
 *  2. Able to spy on an SDI-12 bus for troubleshooting comm between datalogger and
 * sensors.
 *  3. Can also be used as a hardware middleman for interfacing software to an SDI-12
 * sensor. For example, implementing an SDI-12 datalogger in Python on a PC.  Use
 * verbatim mode with feedback off in this case.
 *
 *  Note: "translation" means timing and electrical interface.  It does not ensure
 * SDI-12 compliance of commands sent via it.
 *
 * D. Wasielewski, 2016
 * Builds upon work started by:
 * https://github.com/jrzondagh/AgriApps-SDI-12-Arduino-Sensor
 * https://github.com/Jorge-Mendes/Agro-Shield/tree/master/SDI-12ArduinoSensor
 *
 * Known issues:
 *  - Backspace adds a "backspace character" into the serialMsgStr (which gets sent
 *    out on the SDI-12 interface) instead of removing the previous char from it
 *  - Suceptible to noise on the SDI-12 data line; consider hardware filtering or
 *    software error-checking
 */

#include <SDI12.h>

#define SERIAL_BAUD 9600 /*!< The baud rate for the output serial port */
#define DATA_PIN 7         /*!< The pin of the SDI-12 data bus */

/** Define the SDI-12 bus */
SDI12 mySDI12(DATA_PIN);

void setup() {
  Serial.begin(SERIAL_BAUD);
  while (!Serial)
    ;

  // Initiate serial connection to SDI-12 bus
  mySDI12.begin();
  delay(500);
  mySDI12.forceListen();

}

void loop() {
  static String  serialMsgStr;
  static boolean serialMsgReady = false;

  static String  sdiMsgStr;
  static boolean sdiMsgReady = false;

  // -- READ SERIAL (PC COMMS) DATA --
  // If serial data is available, read in a single byte and add it to
  // a String on each iteration
  if (Serial.available()) {
    char inByte1 = Serial.read();
    if (inByte1 == '\r' || inByte1 == '\n') {
      serialMsgReady = true;
    } else {
      serialMsgStr += inByte1;
    }
  }

  // -- READ SDI-12 DATA --
  // If SDI-12 data is available, keep reading until full message consumed
  // (Normally I would prefer to allow the loop() to keep executing while the string
  //  is being read in--as the serial example above--but SDI-12 depends on very precise
  //  timing, so it is probably best to let it hold up loop() until the string is
  //  complete)
  int avail = mySDI12.available();
  if (avail < 0) {
    mySDI12.clearBuffer();
  }  // Buffer is full; clear
  else if (avail > 0) {
    for (int a = 0; a < avail; a++) {
        char inByte2 = mySDI12.read();
        //Serial.println(inByte2);
        if (inByte2 == '\n') {
            sdiMsgReady = true;
        } else if (inByte2 == '!') {
            sdiMsgStr += "!";
            sdiMsgReady = true;
        } else {
            sdiMsgStr += String(inByte2);
        }
    }
  }


  // Report completed SDI-12 messages back to serial interface
  if (sdiMsgReady) {
    Serial.println(sdiMsgStr);
    // Reset String for next SDI-12 message
    sdiMsgReady = false;
    sdiMsgStr   = "";
  }

  // Send completed Serial message as SDI-12 command
  if (serialMsgReady) {
    Serial.println();
    lowerMsgStr.toLowerCase();
    mySDI12.sendCommand(serialMsgStr);
    // Reset String for next serial message
    serialMsgReady = false;
    serialMsgStr   = "";
  }
}