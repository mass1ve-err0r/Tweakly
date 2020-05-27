import urllib.parse
import pymongo
from os import environ as env

mdbuser = urllib.parse.quote_plus(env.get('MNG_USER'))
mdbpass = urllib.parse.quote_plus(env.get('MNG_PASS'))
mdbaddress = env.get('MNG_ADDR')
mdbTargetDB = env.get('MNG_DB')


class MongoDBHandler:
    def __init__(self, repoName: str):
        self.client = pymongo.MongoClient("mongodb://" + mdbuser \
                                          + ":" + mdbpass \
                                          + "@" + mdbaddress \
                                          + "/?authSource=" + mdbTargetDB \
                                          + "&authMechanism=SCRAM-SHA-256")
        self.dbHandle = self.client['tweakservice']
        self.pkgHandler = self.dbHandle[repoName]

    def addPackage(self, _obj: dict):
        querty_t = {"Package": _obj['Package']}
        self.pkgHandler.replace_one(querty_t, _obj, upsert=True)
        return

    def deleteAllPackagesByID(self, identifier: str):
        query_t = {"Package": identifier}
        self.pkgHandler.delete_many(query_t)
        return

    def deleteEntireCollection(self, are_you_sure: bool):
        if are_you_sure:
            self.pkgHandler.drop()
        return

    def getPackage(self, identifier: str):
        # rgx = "^" + identifier
        # query_t = {"Name": {"$regex": rgx}}
        query_t = {"Name": identifier}
        rv = self.pkgHandler.find_one(query_t)
        return rv


class TokenDBHandler:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://" + mdbuser \
                                          + ":" + mdbpass \
                                          + "@" + mdbaddress \
                                          + "/?authSource=" + mdbTargetDB \
                                          + "&authMechanism=SCRAM-SHA-256")
        self.dbHandle = self.client['tweakservice']
        self.vtokenHandler = self.dbHandle["vtokens"]
        self.btokenHandler = self.dbHandle["btokens"]

    def addBlacklistedToken(self, jwt_id: str):
        query_t = {"jti": jwt_id}
        self.btokenHandler.insert_one(query_t)
        self.vtokenHandler.delete_one(query_t)
        return

    def addValidToken(self, jwt_id: str):
        query_t = {"jti": jwt_id}
        self.vtokenHandler.insert_one(query_t)
        return

    def getBlacklistedToken(self, jwt_id: str):
        query = {"jti": jwt_id}
        rv = self.btokenHandler.find_one(query)
        return rv

    def getValidToken(self, jwt_id: str):
        query = {"jti": jwt_id}
        rv = self.vtokenHandler.find_one(query)
        return rv
