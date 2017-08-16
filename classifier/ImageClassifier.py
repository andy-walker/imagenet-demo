from classifier.classify_image import *

class ImageClassifier:

    def classify(self, path_to_image):
        maybe_download_and_extract()
        return run_inference_on_image(path_to_image)

