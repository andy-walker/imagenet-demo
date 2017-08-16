import requests

class ImageProcurer:

    def __init__(self, url):
        self.url = url

    def download_image(self):

        response = requests.get(self.url)

        if response.status_code == 200:
            return response.content

        return None
