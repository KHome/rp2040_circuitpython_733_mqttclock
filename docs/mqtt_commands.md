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
(command_change_17,ascii1,ascii2,ascii3,ascii4) = struct.unpack('bbbbb',message)
- Sets alarmtime for next 24h
- Shows alarmtime in Display-7-seg
- TBD: Sets RTC Alarm2

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
            
