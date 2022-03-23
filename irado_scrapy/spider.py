# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass
from datetime import date
from os import environ

import scrapy

DUTCH_MONTHS = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli',
                'augustus', 'september', 'oktober', 'november', 'december']


def parse_dutch_date(raw_date):
    _, day_raw, month_raw = raw_date.split()
    day = int(day_raw)
    month = DUTCH_MONTHS.index(month_raw) + 1

    today = date.today()
    year = today.year
    if today.month == 12 and month != 12:
        year += 1

    return date(year, month, day)


@dataclass
class IradoNextCollectionDates:
    gft: date
    pmd: date
    papier: date


class IradoSpider(scrapy.Spider):
    name = 'IradoSpider'

    def __init__(self, *args, **kwargs):
        self.zipcode = environ['IRADO_ZIPCODE']
        self.zipcode_suffix = environ['IRADO_ZIPCODE_SUFFIX']
        self.housenumber = environ['IRADO_HOUSENUMBER']
        self.housenumber_suffix = environ.get('IRADO_HOUSENUMBER_SUFFIX', '')
        self.wsa_calendar = "587d45d7c9"

    def start_requests(self):
        return (
            scrapy.FormRequest(
                "https://www.irado.nl/afvalkalender",
                formdata={
                    'appointment_zipcode': self.zipcode,
                    'appointment_zipcode_suffix': self.zipcode_suffix,
                    'appointment_housenumber': self.housenumber,
                    'appointment_housenumber_suffix': self.housenumber_suffix,
                    'wsa_calendar': self.wsa_calendar
                },
                callback=self.parse
            ),
        )

    def parse(self, response):
        next_gft_raw = response.css('.avk-block-row.pickup-type-item-gft::text').get().strip()
        next_pmd_raw = response.css('.avk-block-row.pickup-type-item-kunststof::text').get().strip()
        next_papier_raw = response.css('.avk-block-row.pickup-type-item-papier::text').get().strip()
        self.logger.debug('GFT? %s PMD? %s papier? %s', next_gft_raw, next_pmd_raw, next_papier_raw)

        return IradoNextCollectionDates(parse_dutch_date(next_gft_raw),
                                        parse_dutch_date(next_pmd_raw),
                                        parse_dutch_date(next_papier_raw))


