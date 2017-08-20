"""This module is a wrapper of the MongoDB database calls."""
from pymongo import MongoClient


class MongoDB(object):
    """"This class is a object of MongoDB calls."""

    def __init__(self, database_name, collection_name):
        """Initializing MongoDB connection to the 'link' collection."""
        self.client = MongoClient()
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    def check_if_entry_exists(self, url):
        """Check if the entry already exists in the collection."""
        count = self.collection.find({"url": url}).count()
        if count > 0:
            return True
        return False

    def put(self, data):
        """Put an entry to the collection."""
        exist = self.check_if_entry_exists(data["url"])
        if exist:
            return False
        else:
            self.collection.insert_one(data)
            return True

    def put_list_of_entries_to_db(self, entry_list):
        """Put a list of entries to the collection."""
        success = 0
        fail = 0
        for obj in entry_list:
            res = self.put(obj)
            if res: success += 1
            else: fail += 1
        print("Added entries to DB::\n Successfully added: " + str(success) + "\n Already was in DB: "+ str(fail))

    def set_entry(self, entry, field_dict):
        return self.collection.update_one({"url" : entry["url"]}, {"$set": field_dict})

    def mark_entry_as_uploaded(self, entry, log_msg):
        """Marks entry as uploaded, logs the date it was uploaded"""
        self.set_entry(entry, {"uploaded": True, "last_status" : log_msg})

    def mark_entry_upload_fail(self, entry, log_msg):
        self.set_entry(entry, {"last_status": log_msg})


    def get_entries_by_subreddit_name(self, subreddit):
        """Get the list of entries that is not uploaded yet by subreddit name."""
        list_of_entries = list()
        cursor = self.collection.find({"subreddit": subreddit, "uploaded": False, "type": {"$in": ['picture', 'video']}})
        for obj in cursor:
            list_of_entries.append(obj)
        return list_of_entries

    def get_entries_of_collection(self):
        """Get the list of entries of the collection"""
        list_of_entries = list()
        cursor = self.collection.find()
        for obj in cursor:
            list_of_entries.append(obj)
        return list_of_entries
