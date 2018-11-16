
/*  OctoWS2811 BasicTest.ino - Basic RGB LED Test
    http://www.pjrc.com/teensy/td_libs_OctoWS2811.html
    Copyright (c) 2013 Paul Stoffregen, PJRC.COM, LLC
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
  Required Connections
  --------------------
    pin 2:  LED Strip #1    OctoWS2811 drives 8 LED Strips.
    pin 14: LED strip #2    All 8 are the same length.
    pin 7:  LED strip #3
    pin 8:  LED strip #4    A 100 ohm resistor should used
    pin 6:  LED strip #5    between each Teensy pin and the
    pin 20: LED strip #6    wire to the LED strip, to minimize
    pin 21: LED strip #7    high frequency ringining & noise.
    pin 5:  LED strip #8
    pin 15 & 16 - Connect together, but do not use
    pin 4 - Do not use
    pin 3 - Do not use as PWM.  Normal use is ok.
  This test is useful for checking if your LED strips work, and which
  color config (WS2811_RGB, WS2811_GRB, etc) they require.
*/

#include <OctoWS2811.h>
#define minimum(a,b)     (((a) < (b)) ? (a) : (b))

#define PACKET_LEN 6

byte databuf[PACKET_LEN];


const int ledsPerStrip = 500;
const int usedStrips = 6;

const int SCREEN_W = usedStrips * 10;
const int SCREEN_H = ledsPerStrip / 10;

DMAMEM int displayMemory[ledsPerStrip * 6];
int drawingMemory[ledsPerStrip * 6];
const int config = WS2811_GRB | WS2811_800kHz;

enum {
  JPEG_BUFLEN = 9000,
  MAGIC1 = 0x11,
  MAGIC2 = 0x22,
  MAGIC3 = 0x33,
  MAGIC4 = 0x44,
  MAGIC5 = 0x55,
  MAGIC6 = 0x66
};
enum {
  CMD_BLANK = 0,
  CMD_SETSOLID = 1,
  CMD_SETFLOOR = 2
};
uint8_t in_data[JPEG_BUFLEN];
uint32_t in_len = 0;
int magic_read = 0;
int len_read = 0;
uint32_t data_read = 0;
byte cmd = CMD_BLANK;
enum {
  STATE_READING_MAGIC,
  STATE_READING_CMD,
  STATE_READING_LEN,
  STATE_READING_DATA
} state = STATE_READING_MAGIC;

OctoWS2811 leds(ledsPerStrip, displayMemory, drawingMemory, config);

boolean frameStarted = false;

void setup() {
  leds.begin();
  leds.show();
  Serial.begin(0);
}


void loop() {
  if (Serial.available()) {
    byte val = Serial.read();
    if (state == STATE_READING_MAGIC) {
      if (magic_read == 0 && val == MAGIC1) {
        ++magic_read;
      } else if (magic_read == 1 && val == MAGIC2) {
        ++magic_read;
      } else if (magic_read == 2 && val == MAGIC3) {
        ++magic_read;
      } else if (magic_read == 3 && val == MAGIC4) {
        ++magic_read;
      } else if (magic_read == 4 && val == MAGIC5) {
        ++magic_read;
      } else if (magic_read == 5 && val == MAGIC6) {
        ++magic_read;
      } else {
        magic_read = 0;
      }
      if (magic_read == 6) {
        state = STATE_READING_CMD;
      }
    } else if (state == STATE_READING_CMD) {
      cmd = val;
      state = STATE_READING_LEN;
      len_read = 0;
      in_len = 0;
    } else if (state == STATE_READING_LEN) {
      in_len |= (((uint32_t)val) << (24 - 8 * len_read));
      ++len_read;
      if (len_read == 4) {
        state = STATE_READING_DATA;
        data_read = 0;
        if (in_len == 0) {
          state = STATE_READING_MAGIC;
          magic_read = 0;
          run_command();
        }
      }
    } else if (state == STATE_READING_DATA) {
      in_data[data_read++] = val;
      if (data_read == len_read || data_read >= JPEG_BUFLEN) {
        state = STATE_READING_MAGIC;
        magic_read = 0;
        run_command();
      }
    }
  }
}

void run_command()
{
  int i;
  if (cmd == CMD_BLANK) {
    for (i = 0; i < SCREEN_H * SCREEN_W; ++i) {
      leds.setPixel(i, 0, 0, 0);
    }
  } else if (cmd == CMD_SETSOLID) {
    for (i = 0; i < SCREEN_H * SCREEN_W; ++i) {
      leds.setPixel(i, in_data[0], in_data[1], in_data[2]);
    }
  } else if (cmd == CMD_SETFLOOR) {
    for (i = 0; i < SCREEN_H * SCREEN_W; ++i) {
      leds.setPixel(i, in_data[3 * i + 0], in_data[3 * i + 1], in_data[3 * i + 2]);
    }
  }
  leds.show();
}
