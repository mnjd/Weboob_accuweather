# -*- coding: utf-8 -*-

# Copyright(C) 2012 Manoj D
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals
from datetime import date
from weboob.browser.elements import ItemElement, method, DictElement, ListElement
from weboob.browser.pages import JsonPage, HTMLPage
from weboob.browser.filters.standard import CleanText, CleanDecimal, Regexp
from weboob.browser.filters.json import Dict
from weboob.capabilities.weather import Forecast, Current, City, Temperature


class CityPage(JsonPage):
    ENCODING = 'utf-8'

    @method
    class iter_cities(DictElement):
        ignore_duplicate = True

        class item(ItemElement):
            klass = City

            obj_id = Dict('Key')

            def obj_name(self):
                return '{}, {}, {}'.format(Dict('LocalizedName')(self),
                                           Dict['AdministrativeArea']['LocalizedName'](self),
                                           Dict['Country']['LocalizedName'](self))


class WeatherPage(HTMLPage):
    @method
    class get_current(ItemElement):
        klass = Current

        obj_date = date.today()

        def obj_text(self):

            pressure = CleanDecimal('//*[@id="detail-now"]/div/div[2]/ul/li[4]/strong')(self)
            humidity = CleanDecimal('//*[@id="detail-now"]/div/div[2]/ul/li[3]/strong')(self)
            apparent_temp = CleanDecimal(CleanText('//*[@id="detail-now"]/div/div[1]/div[2]/div/span[2]/text()'))(self)
            description = CleanText('//*[@id="detail-now"]/div/div[1]/div[2]/span')(self)
            unit_temp = Regexp(CleanText('//*[@id="detail-now"]/div/div[2]/ul/li[8]/strong/text()'), u'([A-Z])$')(self)
            unit_pressure = Regexp(CleanText('//*[@id="detail-now"]/div/div[2]/ul/li[4]/strong/text()'), u'([a-z]+)')(self)

            # For US cities temp is sometimes given in fahrenheit
            if unit_temp == 'F':
                apparent_temp = round((float(apparent_temp) - 32) / 1.8)
                unit_temp = 'C'

            # For US cities pressure is given in inch of mercury
            if unit_pressure == 'in': pressure = round(float(pressure) * 33.863886666667)

            return '{} hPa - humidity {}% - feels like {} °{} - {}'.format(pressure,
                                                                           humidity,
                                                                           apparent_temp,
                                                                           unit_temp,
                                                                           description)

        def obj_temp(self):
            temp = CleanDecimal('//*[@id="detail-now"]/div/div[1]/div[2]/div/span[1]')(self)
            unit_temp = Regexp(CleanText('//*[@id="detail-now"]/div/div[2]/ul/li[8]/strong/text()'), u'([A-Z])$')(self)
            if unit_temp == 'F': temp = round((float(temp) - 32) / 1.8); unit_temp = 'C'
            return Temperature(float(temp), unit_temp)

    @method
    class iter_forecast(ListElement):
        ignore_duplicate = True

        item_xpath = '//*[@id="panel-main"]/div[2]/div/div/div[2]/ul/li'

        class item(ItemElement):
            klass = Forecast
            obj_id = CleanText('./div/h4')
            obj_date = CleanText('./div/h4')

            def obj_low(self):
                temp = CleanText('./div/div[2]/div/span[2]/text()')(self)
                unit_temp = Regexp(CleanText('//*[@id="detail-now"]/div/div[2]/ul/li[8]/strong/text()'), u'([A-Z])$')(self)
                if temp != "Lo": # Sometimes there is no low temperature
                    temp = CleanDecimal(Regexp(CleanText('./div/div[2]/div/span[2]/text()'), u'(\d*)\xb0'))(self)
                else:
                    temp = CleanDecimal(Regexp(CleanText('./div/div[2]/div/span[1]/text()'), u'(\d*)\xb0'))(self)
                if unit_temp == 'F': temp = round((float(temp) - 32) / 1.8); unit_temp = 'C'
                return Temperature(float(temp), unit_temp)

            def obj_high(self):
                unit_temp = Regexp(CleanText('//*[@id="detail-now"]/div/div[2]/ul/li[8]/strong/text()'), u'([A-Z])$')(self)
                temp = CleanDecimal(Regexp(CleanText('./div/div[2]/div/span[1]/text()'), u'(\d*)\xb0'))(self)
                if unit_temp == 'F': temp = round((float(temp) - 32) / 1.8); unit_temp = 'C'
                return Temperature(float(temp), unit_temp)

            obj_text = CleanText('./div/div[2]/span')
