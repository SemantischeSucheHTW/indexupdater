from indexdao import IndexDao
from pymongo import MongoClient

import datetime

class ZeitIndexDao(IndexDao):

    def __init__(self, config):

        '''
        Setup an instance of OrtsIndexDao.
        Keys in config are: host, port, database, collection
        :param config: dict with keys
        '''
        c_copy =  dict(config)
        db = c_copy.pop('db')
        zeitindex_collection = c_copy.pop('zeitindex_collection')
              

        self.client = MongoClient(**c_copy)
        self.db = self.client[db]
        self.zeitindex_collection = self.db[zeitindex_collection]
        
        

    def updateIndex(self,  pagedetails):
        datetime = pagedetails.date
        self.zeitindex_collection.update_one({'date': datetime}, {'$push': {'urls':  pagedetails.url}})

        print(f"New entry to {pagedetails.location} written")
        return None

    def getUrlfromKey(self, searchKey): 
        temp = self.zeitindex_collection.find({'date' : searchKey})
        return temp
