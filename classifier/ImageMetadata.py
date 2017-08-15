class ImageMetadata:

    def __init__(self, db):
        self.db = db

    """
    Check the database to see if we have an entry for this filename
    @returns: Boolean
    """
    def check_if_image_exists_locally(self, filename):

        filename = self.db.escape(filename).decode('utf-8')
        query = "SELECT 1 FROM images WHERE filename = '{}'".format(filename)

        result = self.db.query(query)
        if result.fetch_row():
            return True
        return False

    def initialize(self):
        pass

    def save_metadata(self):
        pass
