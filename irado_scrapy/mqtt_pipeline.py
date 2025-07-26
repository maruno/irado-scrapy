# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from distutils.util import strtobool
from os import environ
from ssl import create_default_context

from aiomqtt import Client

class IradoMQTTPipeline:
    async def process_item(self, item, spider):
        logging.info("Processing item to send over MQTT: %s", item)

        tls_context = None
        if strtobool(environ.get('MQTT_TLS', 'false')):
            tls_context = create_default_context()

        async with Client(environ['MQTT_HOSTNAME'],
                          port=int(environ['MQTT_PORT']),
                          username=environ.get('MQTT_USERNAME'),
                          password=environ.get('MQTT_PASSWORD'),
                          tls_context=tls_context) as client:
            await client.publish('irado_scrapy/gft',
                                item.gft.isoformat(),
                                retain=True)
            await client.publish('irado_scrapy/pmd',
                                item.pmd.isoformat(),
                                retain=True)
            await client.publish('irado_scrapy/papier',
                                item.papier.isoformat(),
                                retain=True)

