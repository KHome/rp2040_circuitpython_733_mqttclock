# Controls-Class Description
## Lux
?        self.wait = 0.0
-        self.lux_brigtness = 0.0 # read value by sensor
-        self.lux_automaticclock = True # switch if clock bright is auto

## Clock neopixel settings
?        self.neoclock_enable = True
-        self.neoclock_timestring=""
-        self.neoclock_color_fg = (255,255,255) # white, 255,255,255
-        self.neoclock_task_interval = 100 # has influence on neo_mode==2
-        self.neoclock_brightness = 0.06
-        self.neoclock_outercirle = False
-        self.neoclock_outercirlecolor=(127,0,0)
-        self.neo_mode = 3 #0=off, 1= constant, 2=rainbow animated,3=tile color mix
-        self.neo_mode1_color = (127,0,0)
-        self.neo_mode2_rainbow_cnt = 0
-        self.neo_mode3_color = 0 # 0=red/orange, 1=green/blue, 2=blue/lila

## Audio-Settings
-        self.audio_mp3 = 0
?        self.audio_enable = True
-        self.audio_playtrack = 14
?       self.audio_status_is_playing = False
?        self.audio_do_stop = False
        
 ## Misc
-        self.mqtt_wait = 3000 # reduce time if received something
-       self.watchdog_enable = False
-      self.clock = 0 #rtc.datetime
        
## Display with 7 Segments
?        self.seg7display_enable = True
-        self.seg7display_brightness = 1
-        self.seg7display_blinkrate = 0
-        self.seg7display_string = ""
-        self.seg7display_mode = 4 #0=alarm, 1=clock, 2, lux, 3=inner_rh, 4=innerTemp, 4...
-        self.seg7display_lux_automatic = True
-        self.seg7display_mode_loop = True
       
## SmartHome Feedback
 -       self.house_room_is_present = True
 -       self.house_is_night = False
 
 -self.house_weather_outside_TempC = 0.0
 -       self.house_weather_outside_rH = 0.0
 -       self.house_weather_icon = 0
 -       self.room_status_rH = 0.0
 -       self.room_status_TempC = 0.0
 -       self.room_status_pressure = 0.0
 -       self.room_alarmtime ="1205"


        #https://github.com/KHome/rp2040_circuitpython_733_mqttclock/blob/main/docs/controls_class.md
        self.wait = 0.0
        self.lux_brigtness = 0.0 # read value by sensor
        self.lux_automaticclock = True # switch if clock bright is auto
        # Clock neopixel settings
        self.neoclock_enable = True
        self.neoclock_timestring=""
        self.neoclock_color_fg = (255,255,255) # white, 255,255,255
        self.neoclock_task_interval = 100 # has influence on neo_mode==2
        self.neoclock_brightness = 0.06
        self.neoclock_outercirle = False
        self.neoclock_outercirlecolor=(127,0,0)
        self.neo_mode = 3 #0=off, 1= constant, 2=rainbow animated,3=tile color mix
        self.neo_mode1_color = (127,0,0)
        self.neo_mode2_rainbow_cnt = 0
        self.neo_mode3_color = 0 # 0=red/orange, 1=green/blue, 2=blue/lila
        # Neopixel for clock
        self.neo_all_speed = 60
        self.neo_main_color = (255,0,0)
        self.neo_main_brightness= 0.05
        self.neo_main_copy_to_all = True
        self.neo_main_neo_all = True
        
        self.neo_south_inner_enable = True
        self.neo_south_inner_obj = None #to control pixel
        self.neo_south_inner_nr = 32 #(6*6) #number of pixels
        self.neo_south_inner_rainbow = None #to anmitate comet
        self.neo_south_inner_rb_speed = 0.1
        self.neo_south_inner_rb_size = 5
        self.neo_south_inner_rb_spacing = 3
        self.neo_south_inner_color = (255,0,0,0) # 36px (6 sides, each 6)
        self.neo_south_inner_brightness= 0.1
        self.neo_south_inner_mode=0 # 0=ff, 1=constant, 2=rainbow 3=special
        
        #
        self.neo_south_outer_enable = True
        self.neo_south_outer_obj = None #to control pixel
        self.neo_south_outer_nr = (8*8) # number of pixels
        self.neo_south_outer_rainbow = None #to anmitate comet
        self.neo_south_outer_rb_speed = 0.1
        self.neo_south_outer_rb_size = 5
        self.neo_south_outer_rb_spacing = 3
        self.neo_south_outer_color = (255,0,0,0) # 8x x(hexagon outside, each 8)
        self.neo_south_outer_brightness= 0.05
        self.neo_south_outer_mode=0 # 0=ff, 1=constant, 2=rainbow

        self.neo_east_top_enable = True
        self.neo_east_top_obj = None #to control pixel
        self.neo_east_top_nr = (41+41+27+27) # number of pixels
        self.neo_east_top_rainbow = None #to anmitate comet
        self.neo_east_top_rb_speed = 0.1
        self.neo_east_top_rb_spacing = 3
        self.neo_east_top_color = (255,0,0,0) # 2*x41 +2*26 = 134 
        self.neo_east_top_brightness= 0.05
        self.neo_east_top_mode=0 # 0=ff, 1=constant, 2=rainbow
        
        self.neo_east_table_enable = True
        self.neo_east_table_obj = None #to control pixel
        self.neo_east_table_nr = (57+60) # number of pixels
        self.neo_east_table_rainbow = None #to anmitate comet
        self.neo_east_table_rb_speed = 0.1
        self.neo_east_table_rb_size = 5
        self.neo_east_table_rb_spacing = 3
        self.neo_east_table_color = (255,0,0)
        self.neo_east_table_brightness = 0.05 # 60+57
        self.neo_east_table_mode=0 # 0=ff, 1=constant, 2=rainbow
        # Audio-Settings
        self.audio_mp3 = 0
        self.audio_enable = True
        self.audio_playtrack = 14
        self.audio_status_is_playing = False
        self.audio_do_stop = False
        # Misc
        self.mqtt_wait = 3000 # reduce time if received something
        self.watchdog_enable = False
        self.clock = 0 #rtc.datetime
        # Display with 7 Segments
        self.seg7display_brightness = 1
        self.seg7display_blinkrate = 0
        self.seg7display_string = ""
        self.seg7display_mode = 4 #0=alarm, 1=clock, 2, lux, 3=inner_rh, 4=innerTemp, 4...
        self.seg7display_lux_automatic = True
        self.seg7display_mode_loop = True
        # SmartHome Feedback
        self.house_room_is_present = True
        self.house_is_night = False
        self.house_weather_outside_TempC = 0.0
        self.house_weather_outside_rH = 0.0
        self.house_weather_icon = 0
        self.room_status_rH = 0.0
        self.room_status_TempC = 0.0
        self.room_status_pressure = 0.0
        self.room_alarm_actived = False
        self.room_alarmtime ="1205"
