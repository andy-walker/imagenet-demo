"""
MySQL connector class
"""

import _mysql

class Database:

    def __init__(self):
        self.db = _mysql.connect(host="localhost", user="root", passwd="", db="imagenet")

    def escape(self, string):
        return self.db.escape_string(string)

    def query(self, query):
        self.db.query(query)
        return self.db.store_result()