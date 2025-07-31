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

## How to run
The service can be run as a container using image `ghcr.io/maruno/irado-scrapy:latest`.

### Docker container
To pass the configuration simply feed the config using the above mentioned environment variables
to docker using an env-file:
`docker run -ti --env-file env.list ghcr.io/maruno/irado-scrapy:latest`

### K8s CronJob
An example CronJob can be found in the `k8s`-folder using the docker image. Just provide
it with a config-map `irado-scrapy-config` with the settings you used for the docker container:

```
$ kubectl create ns scrapy
$ kubectl create configmap -n scrapy irado-scrapy-config --from-env-file=irado-scrapy.env
$ kubectl apply -f k8s/
```
