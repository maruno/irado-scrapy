# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
from distutils.util import strtobool
from os import environ
from ssl import create_default_context

from aiomqtt import Client
from scrapy import signals

class HassMQTTDiscoveryOnOpen:
    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_opened,
                                signal=signals.spider_opened)

        return ext

    async def spider_opened(self, spider):
        logging.debug("Opened spider in %s", self.__class__.__name__)

        tls_context = None
        if strtobool(environ.get('MQTT_TLS', 'false')):
            tls_context = create_default_context()

        async with Client(environ['MQTT_HOSTNAME'],
                          port=int(environ['MQTT_PORT']),
                          username=environ.get('MQTT_USERNAME'),
                          password=environ.get('MQTT_PASSWORD'),
                          tls_context=tls_context) as client:
            await client.publish('homeassistant/sensor/irado_gft/config',
                                 json.dumps({
                                     'name': 'Irado GFT',
                                     'device_class': 'date',
                                     'state_topic': 'irado_scrapy/gft'
                                 }),
                                 retain=True)
            await client.publish('homeassistant/sensor/irado_pmd/config',
                                 json.dumps({
                                     'name': 'Irado PMD',
                                     'device_class': 'date',
                                     'state_topic': 'irado_scrapy/pmd'
                                 }),
                                 retain=True)
            await client.publish('homeassistant/sensor/irado_papier/config',
                                 json.dumps({
                                     'name': 'Irado papier',
                                     'device_class': 'date',
                                     'state_topic': 'irado_scrapy/papier'
                                 }),
                                 retain=True)
