#include <FastLED.h>
#include "pins_arduino.h"

#define NUM_LEDS 500
#define DATA_PIN 6
#define MAGIC '$'
#define COLUMN 0

#define CHANNELS 3
#define SKIP (COLUMN * NUM_LEDS * CHANNELS)


CRGB leds[NUM_LEDS];
volatile int pos;
volatile boolean new_frame;
volatile boolean reading;
volatile boolean checking;
volatile int reads;

void setup (void)
{
  Serial.begin (9600);   // debugging
  
  // have to send on master in, *slave out*
  pinMode(MISO, OUTPUT);
  
  // turn on SPI in slave mode
  SPCR |= _BV(SPE);
  
  // turn on interrupts
  SPCR |= _BV(SPIE);
  
  pos = 0;
  new_frame = false;
  reading = false;
  checking = false;
  reads = 0;
  
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
}


// SPI interrupt routine
ISR (SPI_STC_vect)
{
  byte c = SPDR;
  if (c == MAGIC) {
    reading = true;
    pos = 0;
  } else if (reading) {
    if (pos >= SKIP) {
      leds[(pos - SKIP) / CHANNELS].raw[(pos - SKIP) % CHANNELS] = c;
    }
    ++pos;
    if ((pos - SKIP) == NUM_LEDS) {
      reading = false;
      ++reads;
      new_frame = true;
    }
  }

  /*
  byte c = SPDR;
  if (c == MAGIC) {
    checking = true;
  } else if (checking) {
    checking = false;
    if (c == DEVICE_ID) {
      reading = true;
      pos = 0;
    }
  } else if (reading) {
    leds[pos / 3].raw[pos % 3] = c;
    ++pos;
    if (pos == NUM_LEDS) {
      reading = false;
      ++reads;
      new_frame = true;
    }
  }
   */
}

// main loop - wait for flag set in interrupt routine
void loop (void)
{
  if (new_frame) {
    new_frame = false;
    FastLED.show();   
  }
}  // end of loop

