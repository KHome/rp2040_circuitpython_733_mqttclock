# MQTT command
## 3, Draw outer cicle
(command_show_text, showthis,red_value,green_value,blue_value) = struct.unpack('bbBBB',message)
- Will be kept for clock updates
- E.g. for use of Room Heat Warning

## 4, Draw Pixel in Clock
(command_show_text,x,timeoffset_x, red_value,green_value,blue_value) = struct.unpack('bbbBBB',message)
- Just written once, will be not taken over for next clock udpate cycle
- Useful for Alarm Signaling

## 7, Draw Fill screen 
(command_show_fill,red_fill,green_fill,blue_fill) = struct.unpack('bBBB',message)
- Just written once, will be not taken over for next clock udpate cycle
- Useful for Alarm Signaling

## 9, Draw Clear screen
(command) = struct.unpack('b',message)
- Just written once, will be not taken over for next clock udpate cycle
- Useful for Alarm Signaling

## 10, Play Audio Track from SD Card
(command_playmp3,songnr,playvolume)=struct.unpack('bbB',message)
- songnr == 1, equals stop
- playvolumne not used yet (TBD?)

## 11, ECU Reset
(command) = struct.unpack('b',message)
- Re-init Microcontroller

## 13, Neoopixel Clock brightness
(command_change_brihtness,controllux,enableautomatic)=struct.unpack('bbb',message)
- Set Brightness or
- Set Automatic Brightness control via Lux-sensor

## 17, Display-7-Segment Alarm update
(command_change_17,ascii1,ascii2,ascii3,ascii4, activate) = struct.unpack('bbbbb',message)
- Bool to activate or deactive output
- Sets alarmtime for next 24h
- Shows alarmtime in Display-7-seg
- TBD: Sets RTC Alarm2

## 18, Display-7-Segment Mode update
(command,newmode,enableautomatic) = struct.unpack('bBb',message)
- Sets the Display mode = Content
- Set, if complete content will be changed / rotated over time

## 21, Display-7-Segment Brightness control
(command21,brightness1,enableautomatic) = struct.unpack('bBb',message)
- Set Brightness or
- Set Automatic Brightness control via Lux-sensor

## 22, Display-7-Segment Blinkrate
(command_change_alarmtime,blinkrate1) = struct.unpack('bB',message)
- Sets Blinkrate for display
- 0=HT16K33_BLINK_OFF       = steady off
- 1=fast=HT16K33_BLINK_2HZ       = 2 Hz blink
- 2=mid=HT16K33_BLINK_1HZ       = 1 Hz blink
- 3=slow=HT16K33_BLINK_HALFHZ    = 0.5 Hz blink

## 23, Audio Sound Stop
(command) = struct.unpack('b',message)
- Stops Audio play

## 30, Show Clock
(command) = struct.unpack('b',message)
- Show Clock "refresh"

## 40, Home-Status - Is Night
(command) = struct.unpack('b',message)
- Sets controls.house_is_night 
- Set Clock background mode to black
- Set Clock foreground to green
- Set Display-7-Seg to Alarm and don't rotate

## 50, NeopixelStrips: Mode
(command_change,position,modevalue)=struct.unpack('bbb',message)
- Position = 0 is all at one time, and 1,2,3,4 are for each
- Mode: 0=off, 1=constant, 2=rainbow 3=special

## 51, NeopixelStrips: Brightness
(command_change,position, x,x2)=struct.unpack('bbbb',message)
- Position = 0 is all at one time, and 1,2,3,4 are for each
- x,x2 = a value for up to 256 = int(x << 8) + int(x2)    
- A brightness from 0-up to 255

## 52, NeopixelStrips - Rainbow Effect (Mode =2) Speed
(command_change,position, x,x2)=struct.unpack('bbbb',message)
- Position = 0 is all at one time, and 1,2,3,4 are for each
- x,x2 = int(x << 8) + int(x2)
- Süeed via = float(newval / (256/4))

## 53, NeopixelStrips - Rainbow Effect (Mode=2) Size
(command_change,position, x,x2)=struct.unpack('bbbb',message)
- Position = 0 is all at one time, and 1,2,3,4 are for each
- x,x2 = int(x << 8) + int(x2)
- Size of equal Neopixel

## 54, NeopixelStrips - Rainbow Effect (Mode=2) Spacing
(command_change,position, x,x2)=struct.unpack('bbbb',message)
- Position = 0 is all at one time, and 1,2,3,4 are for each
- x,x2 = int(x << 8) + int(x2)
- Spacing in Pixel, which keep Black

## 55, NeopixelStrips - Constant (Mode =1)
(command_show_fill,position,red_fill,green_fill,blue_fill,white_fill) = struct.unpack('bbBBBB',message)
- Position = 0 is all at one time, and 1,2,3,4 are for each
- x_fill = from 0..127 (will be muplitplied by two
- For position 4 it's only RGB, otherwise RGBW
      
      
        
       
