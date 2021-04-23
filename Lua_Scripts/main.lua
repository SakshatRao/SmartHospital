-- Setting up MQTT client
-- TODO: Need to enable password
m = mqtt.Client(MQTT_CLIENTID, 60, "", "")
m:lwt("/lwt", "Last wish", 0, 0)

-- When connection is established
m:on("connect", function(m)
    print ("\nConnected established!")
end)

-- When connection is lost
m:on("offline", function(m)
	print ("\n\nDisconnected from broker")
	print("Heap: ", node.heap())
end)

-- Setting up UART communication with Arduino
uart.setup(0, 115200, 8, 0, 1)
uart.on("data", '\r', function(data)
    m:publish(MQTT_TOPIC, tostring(ROOM_NUMBER) .. '_' .. tostring(data), 0, 0, function(m)
        print("Sent data - " .. tostring(data))
    end)
end, 0)

m:connect(MQTT_HOST, MQTT_PORT, 0, 1)