import logging
import requests
from basecomponent import BaseComponent


class geocoder(BaseComponent):


    def initialize(self, parameters):
        self.dummydata = geocodes = [
            {'name': 'Lima', 'lat': 32.345, 'lon': 45.32, 'adm1' : 'PE15', 'adm2' : None},
            {'name': 'Stuebenville', 'lat': 32.345, 'lon': 45.32, 'adm1': 'US21', 'adm2': 'US21.0007'}
        ]
        self.logger = logging.getLogger('scraper_log')

    def geoparse(self, content):
        try:
            url = 'http://localhost:8182/opensextant/extract/geo/json'
            files = {'infile': ('content.txt', content)}
            response = requests.post(url, files=files)
            return response.json()
        except Exception, e:
            print 'There was an error. Check the log file for more information.'
            self.logger.warning('Problem requesting url: {}. {}'.format(url, e))

    def process(self, articles):

        for article in articles:
            article['geocode'] = []
            geocode_doc = self.geoparse(article['content'])

            for anno in geocode_doc['annoList']:
                geocode = { 'source': 'opensextant' }
                geocode['matchText'] = anno['matchText']
                geocode['name'] = anno['features']['place']['placeName']
                geocode['countryCode'] = anno['features']['place']['countryCode']
                geocode['lat'] = anno['features']['place']['latitude']
                geocode['lon'] = anno['features']['place']['latitude']
                geocode['adm1'] = anno['features']['place']['admin1']
                geocode['adm2'] = anno['features']['place']['admin2']
                article['geocode'].append(geocode)
        
        return articles

