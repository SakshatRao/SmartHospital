-- Configuration of Wifi & MQTT services
dofile("config.lua")

-- Wifi setup
wifi.setmode(wifi.STATION)
print('\n\nSTATION Mode:',	'mode='..wifi.getmode())
print('MAC Address: ',		wifi.sta.getmac())
print('Chip ID: ',			node.chipid())
print('Heap Size: ',		node.heap(),'\n')
station_cfg={}
station_cfg.ssid=WIFI_SSID
station_cfg.pwd=WIFI_PASS
station_cfg.save=true
wifi.sta.config(station_cfg)

-- Timer for Wifi connection
local mytimer = tmr.create()
mytimer:alarm(1000, tmr.ALARM_AUTO, function()
	if wifi.sta.getip() == nil then
		print("Connecting...\n")
   	else
        ip, nm, gw = wifi.sta.getip()
    	print("\n\nIP Info: \nIP Address: ", ip)
      	print("Netmask: ", nm)
        print("Gateway Addr: ", gw, '\n')
        
        mytimer:unregister()
      	dofile("main.lua")
   	end
end)
