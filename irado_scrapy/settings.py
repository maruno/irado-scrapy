TELNETCONSOLE_ENABLED = False
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
ITEM_PIPELINES = {
    'irado_scrapy.mqtt_pipeline.IradoMQTTPipeline': 100
}
EXTENSIONS = {
    'irado_scrapy.hass_discovery_ext.HassMQTTDiscoveryOnOpen': 100
}
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Edge/79.0.1451.30 Safari/537.36'
