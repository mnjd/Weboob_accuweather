# Accuweather module for weboob
## Description
This module uses accuweather.com weather forecasting website as backend and weather capability for weboob. The module is accessible through wetboobs application.

## Getting started
Download the repository accuweather into your modules folder for weboob. Make sure that the ~/.config/weboob/sources.list file has the path to the module folder. This is important to be able to load this new module in weboob.

## Prerequisites
Install latest development branch of weboob (1.4), follow the instructions provided here:

```
http://weboob.org/install
```

The git can be found here:

```
https://git.weboob.org/weboob/devel.git
```

If you use the latest stable version (1.3), make sure to change the version from '1.4' to '1.3' in module.py.

## Using the module
Install the module in wetboobs:

```
backend add accuweather
```

Search for a city (Paris for instance):

```
cities Paris
```

From the list provided, choose one. To get the current weather for the city ranked "1" in the list provided by the search, type:

```
current 1
```

To get the forecast for the same city, type:

```
forecast 1
```

## Particularities of the module
Accuweather provides some temperatures and pressures in Fahrenhit (°F) and in inches of mercury (inHg) for American cities. For the sake of consistency, all temperatures are given in Celsius (°C) and pressures in hectopascal (hPa).
