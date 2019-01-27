# InkyPhat-Weather-2019

Time & National Weather Service web scrape is displayed on a Pimoroni InkyPhat.

Pimoroni's weather example stopped working on 01/03/2019 -- It relied upon Yahoo Weather, which curtailed its services at that time.

Here is my totally amateur version used to regain functionality.

Design Notions:

1.  Time & weather forecast are updated separately, with individually selectable intervals.

2.  Inky display is updated every 3 minutes.  (Mostly due to the painfully slow refresh rate of E-paper,
    but this may extend service life too. clean.py isn't 100% effective against "burning")

3.  Time is secured from System time, and the display is set to be 3 minutes fast.
    Then it'll be two minutes fast; Then one minute.  Then it updates & leapfrogs the display again.
    So, it's a bit fast sometimes, but never late.  A reasonable compromise?  Good enough for me.

4.  Selected weather provider is United States National Weather Service (weather.gov).
    Some other providers: Meteorologisk Institutt (met.no), OpenWeatherMap.org

5.  Weather info is scraped using BeautifulSoup.

High/Low Temps are garnered from the website's 7-day forecast, with periods labeled, "Today", "Tonight", etc.
Federal holidays & unusual weather conditions (e.g. "High Wind Advisory") can blow-up the BeautifulSoup scrape.
That's because, in addition to Python, I don't understand BeautifulSoup either.  Yet.
So...  There's some kludgery incorporated to account for odd conditions & preserve display formatting.

Anyway, it works & I like it.
