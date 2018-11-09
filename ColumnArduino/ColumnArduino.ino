#include "project.h"
#include <FastLED.h>
#include "pins_arduino.h"
#include <util/crc16.h>


#define NUM_LEDS 500
#define DATA_PIN 6
#define MAGIC 36
#define COLUMN 0

#define CHANNELS 3
#define SKIP (COLUMN * NUM_LEDS * CHANNELS)


CRGB leds[NUM_LEDS];
volatile int pos;
volatile boolean new_frame;
volatile boolean reading;
volatile int reads;
volatile uint8_t crc;


void setup (void)
{
  Serial.begin (9600);   // debugging
  
  // have to send on master in, *slave out*
  pinMode(MISO, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  
  // turn on SPI in slave mode
  SPCR |= _BV(SPE);
  
  // turn on interrupts
  SPCR |= _BV(SPIE);
  
  pos = 0;
  new_frame = false;
  reading = false;
  reads = 0;
  init_isrs((uint8_t *)leds);
  
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
}

// SPI interrupt routine
ISR (SPI_STC_vect)
{
  byte c = SPDR;
  if (reading) {
    if ((pos - SKIP) == (NUM_LEDS * CHANNELS)) {
      reading = false;
      ++reads;
      if (crc == c) {
        new_frame = true;
      }
      return;
    }
    if (pos >= SKIP) {
      //leds[(pos - SKIP) / CHANNELS].raw[(pos - SKIP) % CHANNELS] = c;
      *((uint8_t *)(leds) + pos - SKIP) = c;
      crc = _crc_ibutton_update(crc, c);
    }
    ++pos;
  } else if (c == MAGIC) {
    reading = true;
    pos = 0;
    crc = 0;
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
    //Serial.println("RX");
    new_frame = false;
    FastLED.show();   
  }
  delay(1000);
  Serial.println(pos);
  Serial.println(crc);
}  // end of loop

