-- Setting up MQTT client
m = mqtt.Client(MQTT_CLIENTID, 60, "", "") -- Need to enable password
m:lwt("/lwt", "Last wish", 0, 0)

-- When connection is established
m:on("connect", function(m)
    print ("\nConnected established!")
    
    -- Timer for sending data regularly
	local pub_timer = tmr.create()
	pub_timer:alarm(5000, tmr.ALARM_AUTO, function()
        
        -- Generating random temperature values
        temperature = math.random(37, 39)

        -- Publishing under topic '/mcu/status'
        m:publish("/mcu/status", tostring(temperature), 0, 0, function(m)
            print("Sent data")
        end)

	end)
end)

-- When connection is lost
m:on("offline", function(m)
	print ("\n\nDisconnected from broker")
	print("Heap: ", node.heap())
end)

m:connect(MQTT_HOST, MQTT_PORT, 0, 1)