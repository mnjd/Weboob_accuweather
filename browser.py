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

from weboob.browser import PagesBrowser, URL
from .pages import CityPage, WeatherPage

__all__ = ['AccuWeatherBrowser']


class AccuWeatherBrowser(PagesBrowser):
    BASEURL = 'https://www.accuweather.com'
    API_KEY = 'd41dfd5e8a1748d0970cba6637647d96'

    city_page = URL('https://api\.accuweather\.com/locations/v1/cities/autocomplete\?q=(?P<pattern>.*)&apikey=(?P<api>.*)&language=en-us&get_param=value', CityPage)

    weather_page = URL('en/fr/city/(?P<city_id>.*)/current-weather/(?P<id>.*)', WeatherPage)



    def iter_city_search(self, pattern):
        return self.city_page.go(pattern=pattern, api=self.API_KEY).iter_cities()

    def get_current(self, city_id):
        return self.weather_page.go(city_id=city_id, id=city_id).get_current()

    def iter_forecast(self, city_id):
        return self.weather_page.go(city_id=city_id, id=city_id).iter_forecast()
