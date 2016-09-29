import logging
import requests
from basecomponent import BaseComponent


class clavinGeoparser(BaseComponent):


    def initialize(self, parameters):
        self.logger = logging.getLogger('NETS')
        self.url = parameters['clavin']['geoparse']

    def geoparse(self, content):
        try:
            response = requests.post(self.url, data=content.encode("utf-8"))
            return response.json()
        except Exception, e:
            print 'There was an error. Check the log file for more information.'
            self.logger.warning('Problem requesting url: {}. {}'.format(self.url, e))
        return {'resolvedLocations': []}

    def process(self, articles):

        for article in articles:
            if 'geoparse' not in article:
                article['geoparse'] = []

            geocode_doc = self.geoparse(article['content'])

            for location in geocode_doc['resolvedLocations']:
                geocode = { 'source': 'clavin' }
                geocode['matchText'] = location['location']['text']
                geocode['name'] = location['geoname']['asciiName']
                geocode['countryCode'] = location['geoname']['primaryCountryCode']
                geocode['lat'] = location['geoname']['latitude']
                geocode['lon'] = location['geoname']['longitude']
                geocode['adm1'] = location['geoname']['admin1Code']
                geocode['adm2'] = location['geoname']['admin2Code']
                article['geoparse'].append(geocode)
        
        return articles

