# irado-scrapy
Scrapy crawler for Irado afvalkalender that sends it's data using MQTT.
The values are autodiscovered as a date sensor for Home Assistant.

## Configuration
All configuraton is passed in as environment variables:

|Environment variable|Description|
|---|---|
|MQTT_HOSTNAME|Hostname of the MQTT server|
|MQTT_PORT|Port of the MQTT server|
|MQTT_TLS|Boolean if the connection needs to use TLS
|MQTT_USERNAME|Username used on MQTT server|
|MQTT_PASSWORD|Password used on MQTT server|
|IRADO_ZIPCODE|The numbers-part of a Dutch zipcode/'postcode'|
|IRADO_ZIPCODE_SUFFIX|The two ending letters of a Dutch zipcode/'postcode'|
|IRADO_HOUSENUMBER|Your house number|
