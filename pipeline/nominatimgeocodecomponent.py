import logging
import requests
from basecomponent import BaseComponent


class nominatimGeocoder(BaseComponent):


    def initialize(self, parameters):
        self.logger = logging.getLogger('NETS')
        self.url = parameters['nominatim']['geocode']

    def geocode(self, place):
        try:
            payload = {'format':'json', 'namedetails':1, 'addressdetails':1, 'limit':1, 'q': place}
            response = requests.get(self.url,  params=payload)
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
            if 'geocode' not in article:
                article['geocode'] = []
            
            for place in article['places']:
                # Take first hit returned
                geocode_doc = self.get_first(self.geocode(place))
                if geocode_doc:
                    geocode = { 'source': 'nominatim' }
                    geocode['matchText'] = place
                    geocode['name'] = geocode_doc['namedetails']['name']
                    if 'name:en' in geocode_doc['namedetails']:
                        geocode['name'] = geocode_doc['namedetails']['name:en']
                    if 'country_code' in geocode_doc['address']:
                        geocode['countryCode'] = geocode_doc['address']['country_code']
                    if 'state' in geocode_doc['address']:
                        geocode['state'] = geocode_doc['address']['state']
                    if 'city' in geocode_doc['address']:
                        geocode['city'] = geocode_doc['address']['city']
                    geocode['lat'] = geocode_doc['lat']
                    geocode['lon'] = geocode_doc['lon']
                    article['geocode'].append(geocode)
        
        return articles

