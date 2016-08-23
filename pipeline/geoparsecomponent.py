import logging
import requests
from basecomponent import BaseComponent


class geoparser(BaseComponent):


    def initialize(self, parameters):
        self.logger = logging.getLogger('scraper_log')
        self.url = parameters['opensextant']['base'] + '/extract/geo/json'

    def geoparse(self, content):
        try:
            files = {'infile': ('content.txt', content)}
            response = requests.post(self.url, files=files)
            return response.json()
        except Exception, e:
            print 'There was an error. Check the log file for more information.'
            self.logger.warning('Problem requesting url: {}. {}'.format(self.url, e))
        return {'annoList': []}

    def process(self, articles):

        for article in articles:
            article['geoparse'] = []

            geocode_doc = self.geoparse(article['content'])

            for anno in geocode_doc['annoList']:
                geocode = { 'source': 'opensextant' }
                geocode['matchText'] = anno['matchText']
                geocode['name'] = anno['features']['place']['placeName']
                geocode['countryCode'] = anno['features']['place']['countryCode']
                geocode['lat'] = anno['features']['place']['latitude']
                geocode['lon'] = anno['features']['place']['longitude']
                geocode['adm1'] = anno['features']['place']['admin1']
                geocode['adm2'] = anno['features']['place']['admin2']
                article['geoparse'].append(geocode)
        
        return articles

