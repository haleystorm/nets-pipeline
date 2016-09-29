import logging
import requests
from basecomponent import BaseComponent


class mapzenGeocoder(BaseComponent):


    def initialize(self, parameters):
        self.logger = logging.getLogger('NETS')
        self.url = parameters['mapzen']['geocode']

    def geocode(self, place):
        try:
            payload = {'size':1, 'api_key':'search-6qp3T4u', 'text': place}
            response = requests.get(self.url,  params=payload)
            return response.json()
        except Exception, e:
            print 'There was an error. Check the log file for more information.'
            self.logger.warning('Problem requesting url: {}. {}'.format(self.url, e))
        return {'features':[]}
    
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
                geocode_doc = self.geocode(place)
                feature = self.get_first(geocode_doc['features'])
                if feature:
                    geocode = { 'source': 'mapzen' }
                    geocode['matchText'] = geocode_doc['geocoding']['query']['text']
                    geocode['name'] = feature['properties']['name']
                    geocode['countryCode'] = feature['properties']['country_a']
                    if 'macroregion' in feature['properties']:
                        geocode['state'] = feature['properties']['macroregion']
                    if 'region' in feature['properties']:
                        geocode['city'] = feature['properties']['region']
                    geocode['lat'] = feature['geometry']['coordinates'][1]
                    geocode['lon'] = feature['geometry']['coordinates'][0]
                    article['geocode'].append(geocode)
        
        return articles

