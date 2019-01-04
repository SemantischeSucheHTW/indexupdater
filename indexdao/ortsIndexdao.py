from indexdao import IndexDao
from pymongo import MongoClient

class OrtsIndexDao(IndexDao):

    def __init__(self, config):

        '''
        Setup an instance of OrtsIndexDao.
        Keys in config are: host, port, database, collection
        :param config: dict with keys
        '''
        c_copy =  dict(config)
        db = c_copy.pop('db')
        ortsindex_collection = c_copy.pop('ortsindex_collection')
              

        self.client = MongoClient(**c_copy)
        self.db = self.client[db]
        self.ortsindex_collection = self.db[ortsindex_collection]
        
        

    def updateIndex(self,  pagedetails):

        self.ortsindex_collection.update_one({'ort': pagedetails.location}, {'$push': {'urls':  pagedetails.url}})

        print(f"New entry to {pagedetails.location} written")
        return None

    def getUrlfromKey(self, searchKey): 
        temp = self.ortsindex_collection.find({'ort' : searchKey})
        return temp