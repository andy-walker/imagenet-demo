"""
Class to find and retrieve info for random images on Wikimedia Commons
@author: andyw@bbc
"""

import requests
from pyquery import PyQuery as pq


class ImageFinder:

    """
    Find and return a random Wikimedia Commons image
    @return: a dictionary containing the filename, url and description of the image
    """
    def find_random_image(self):

        html = self.get_random_image_page_html()

        if html:
            return self.parse_info_from_html(html)

        return None

    def get_random_image_page_html(self):

        request = requests.get('https://commons.wikimedia.org/wiki/Special:Random/File')

        if request.status_code == 200:
            return request.text

        return ''

    def parse_info_from_html(self, html):

        pyquery = pq(html)

        return {
            'filename':    pyquery('.fullMedia a').attr('title'),
            'url':         pyquery('.fullMedia a').attr('href'),
            'description': pyquery('.description').text()
        }




