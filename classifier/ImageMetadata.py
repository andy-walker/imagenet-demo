class ImageMetadata:

    def __init__(self, db):
        self.db = db

    def exists_locally(self, filename):

        """
        Check the database to see if we have an entry for this filename
        :return bool
        """

        filename = self.db.escape(filename).decode('utf-8')
        query = "SELECT 1 FROM images WHERE filename = '{}'".format(filename)

        result = self.db.query(query)
        if result.fetch_row():
            return True

        return False

    def initialize(self):
        # todo: stuff
        pass

    def save(self, metadata):

        """
        Save metadata + classification info to the database (this is a bit horrible, sorry - I was in a hurry)
        :param metadata (string)
        :return
        """

        filename = metadata['filename']
        image_path = metadata['image_path']
        description = metadata['description']
        classification = metadata['classification']

        for inference in classification:

            human_name, score = inference

            human_name = self.db.escape(human_name).decode('utf-8')

            print("Classification: " + human_name)
            result = self.db.query("SELECT id FROM classes WHERE name = '{}'".format(human_name)).fetch_row()
            if result:
                (row, ) = result
            else:
                print('Adding database entry for ' + human_name)
                self.db.query("INSERT INTO classes (id, name) VALUES (NULL, '{}')".format(human_name))
                (row, ) = self.db.query("SELECT LAST_INSERT_ID() AS class_id").fetch_row()

            class_id = row[0]

            try:
                self.db.query(
                    "INSERT INTO images (id, filename, description, class_id, score, path) VALUES " +
                    "(NULL, '{}', '{}', {}, {}, '{}')".format(
                        self.db.escape(filename).decode('utf-8'),
                        self.db.escape(description).decode('utf-8'),
                        class_id,
                        score,
                        image_path
                    )
                )
            except BaseException as e:
                # can fail on weird characters, but it's just a test at the moment, so
                # let's not lose any sleep over it
                print('Failed to add database entries:')
                print(str(e))
                pass


