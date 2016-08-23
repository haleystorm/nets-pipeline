import logging
import requests
from basecomponent import BaseComponent


class geocoder(BaseComponent):


    def initialize(self, parameters):
        self.logger = logging.getLogger('scraper_log')
        self.url = parameters['clavin']['base']

    def geocode(self, place):
        try:
            payload = {'text': place}
            response = requests.get(self.url,  params=payload)
            if response.status_code == 404:
                # Place was not found
                return []
            return response.json()
        except Exception, e:
            print 'There was an error. Check the log file for more information.'
            self.logger.warning('Problem requesting url: {}. {}'.format(self.url, e))
        return []

    def get_first(self, iterable, default=None):
        if iterable:
            for item in iterable:
                return item
        return default

    def process(self, articles):

        for article in articles:
            article['geocode'] = []
            
            for place in article['places']:
                # Take first hit returned
                geocode_doc = self.get_first(self.geocode(place))
                if geocode_doc:
                    geocode = { 'source': 'clavin' }
                    geocode['name'] = geocode_doc['asciiName']
                    geocode['countryCode'] = geocode_doc['primaryCountryCode']
                    geocode['lat'] = geocode_doc['latitude']
                    geocode['lon'] = geocode_doc['longitude']
                    geocode['adm1'] = geocode_doc['admin1Code']
                    geocode['adm2'] = geocode_doc['admin2Code']
                    article['geocode'].append(geocode)
        
        return articles

