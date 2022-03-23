TELNETCONSOLE_ENABLED = False
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
ITEM_PIPELINES = {
    'irado_scrapy.mqtt_pipeline.IradoMQTTPipeline': 100
}
EXTENSIONS = {
    'irado_scrapy.hass_discovery_ext.HassMQTTDiscoveryOnOpen': 100
}
