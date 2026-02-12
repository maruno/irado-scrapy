# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass
from datetime import date
from os import environ

import scrapy

@dataclass
class IradoNextCollectionDates:
    gft: date
    rest: date
    papier: date


class IradoSpider(scrapy.Spider):
    name = 'IradoSpider'

    def __init__(self, *args, **kwargs):
        self.zipcode = environ['IRADO_ZIPCODE']
        self.zipcode_suffix = environ['IRADO_ZIPCODE_SUFFIX']
        self.housenumber = environ['IRADO_HOUSENUMBER']
        self.housenumber_suffix = environ.get('IRADO_HOUSENUMBER_SUFFIX', '')
        self.wsa_calendar = "bb7addd20d"

    async def start(self):
        yield scrapy.FormRequest(
            "https://www.irado.nl/afvalkalender",
            formdata={
                'appointment_zipcode': self.zipcode,
                'appointment_zipcode_suffix': self.zipcode_suffix,
                'appointment_housenumber': self.housenumber,
                'appointment_housenumber_suffix': self.housenumber_suffix,
                'wsa_calendar': self.wsa_calendar,
                '_wp_http_referer': '/afvalkalender'
            },
            callback=self.parse
        )

    def parse(self, response):
        next_gft_raw = response.css('.avk-block-row.pickup-type-item.pickup-type-item-gft.active').xpath("./time/@datetime").get().strip()
        next_rest_raw = response.css('.avk-block-row.pickup-type-item-rest.active').xpath("./time/@datetime").get().strip()
        next_papier_raw = response.css('.avk-block-row.pickup-type-item-papier.active').xpath("./time/@datetime").get().strip()
        self.logger.debug('GFT? %s Rest? %s papier? %s', next_gft_raw, next_rest_raw, next_papier_raw)

        return IradoNextCollectionDates(date.fromisoformat(next_gft_raw),
                                        date.fromisoformat(next_rest_raw),
                                        date.fromisoformat(next_papier_raw))


