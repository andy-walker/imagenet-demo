"""
Class to find and retrieve info for random images on Wikimedia Commons
:author andyw@bbc
"""

import requests
from pyquery import PyQuery as pq


class ImageFinder:


    def find_random_image(self):

        """
        Find and return a random Wikimedia Commons image
        :return a dictionary containing the filename, url and description of the image
        """

        html = self.get_random_image_page_html()

        if html:
            return self.parse_info_from_html(html)

    def get_random_image_page_html(self):

        """
        Follow the redirect on the Special:Random/File url, and return the response
        :return string: the response body
        """

        request = requests.get('https://commons.wikimedia.org/wiki/Special:Random/File')

        if request.status_code == 200:
            return request.text

    def parse_info_from_html(self, html):

        """

        :param html:
        :return:
        """

        pyquery = pq(html)

        return {
            'filename':    pyquery('.fullMedia a').attr('title'),
            'url':         pyquery('.fullMedia a').attr('href'),
            'description': pyquery('.description').text()
        }




