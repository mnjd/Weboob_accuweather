# -*- coding: utf-8 -*-

# Copyright(C) 2012 Arno Renevier
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


from weboob.capabilities.weather import CapWeather, CityNotFound
from weboob.tools.backend import Module
from weboob.capabilities.base import find_object
from .browser import AccuWeatherBrowser

__all__ = ['AccuWeatherModule']


class AccuWeatherModule(Module, CapWeather):
    NAME = 'accuweather'
    MAINTAINER = u'Manoj D'
    EMAIL = 'manoj.ducher@gmail.com'
    VERSION = '1.4'
    DESCRIPTION = 'Get forecasts from accuweather.com'
    LICENSE = 'AGPLv3+'
    BROWSER = AccuWeatherBrowser

    def iter_city_search(self, pattern):
        return self.browser.iter_city_search(pattern)

    def get_current(self, city_id):
        return self.browser.get_current(city_id)

    def iter_forecast(self, city_id):
        return self.browser.iter_forecast(city_id)
