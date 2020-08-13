#!/usr/bin/python3
from bz2 import BZ2File
from shutil import copyfileobj
from requests import get
from json import dumps
from os import environ as env
from .MongoDBHandlers import MongoDBHandler

agent = env.get('API_IDENTIFIER')


class PackagesManager:
    def __init__(self, RepoName: str, RepoURL: str):
        self.RepoName = RepoName
        self.RepoURL = RepoURL
        self.Mongo = MongoDBHandler(RepoName)
        self.hdr = {"X-Unique-ID": "00000000-800000E",
                    "X-Firmware": "14.0",
                    "X-Machine": "iPhone12,6",
                    "User-Agent": agent,
                    "Connection": "keep-alive",
                    "Accept": "*/*"
                    }

    def refreshPackagesFile(self) -> None:
        r_hdr = self.hdr
        r = get(url=self.RepoURL,
                allow_redirects=True,
                stream=True,
                headers=r_hdr)
        if r.status_code != 200:
            print("[-]: Could NOT download new Packages file for the following:\n \
                            [-]: Repo: {}\n \
                            [-]: URL: {}\n \
                            [-]: Headers: {}".format(self.RepoName,
                                                     self.RepoURL,
                                                     dumps(r_hdr, indent=4)
                                                     )
                  )
            return
        outfile = self.RepoName + '.bz2'
        with open(outfile, 'wb') as f:
            copyfileobj(r.raw, f)

    def extactPackagesFile(self) -> None:
        outfile = self.RepoName + ".txt"
        infile = self.RepoName + ".bz2"
        try:
            with BZ2File(infile) as fr, open(outfile, "wb") as fw:
                copyfileobj(fr, fw)
                return
        except Exception:
            return

    def parsePackages(self) -> None:
        infile = self.RepoName + ".txt"
        with open(infile, 'r') as f:
            entry = {}
            while True:
                line = f.readline()
                if not line:
                    break
                if line == "\n":
                    if entry.get("Tag") == None:
                        entry['is_paid'] = False
                    self.Mongo.addPackage(entry)
                    entry.clear()
                else:
                    s = line.strip().split(":", 1)
                    if len(s) != 2:
                        continue
                    if "Tag" == s[0]:
                        if "cydia::commercial" in s[1]:
                            entry['is_paid'] = True
                        else:
                            entry['is_paid'] = False
                    entry[s[0]] = s[1].strip()

    def refreshRepo(self):
        self.refreshPackagesFile()
        self.extactPackagesFile()
        self.parsePackages()
        return

    def getPackage(self, identifier: str):
        _pkgList = self.Mongo.getPackage(identifier)
        if _pkgList is None:
            return None
        if len(_pkgList) == 0:
            return None
        rv = []
        for _pkg in _pkgList:
            sileoURL = "sileo://package/" + _pkg['Package']
            zbraURL = "zbra://packages/" + _pkg['Package']
            rv_o = {
                "Name": _pkg['Name'],
                "Version": _pkg['Version'],
                "Description": _pkg['Description'],
                "Author": _pkg['Author'],
                "IconURL": _pkg['Icon'],
                "Depiction": _pkg['Depiction'],
                "Size": _pkg['Size'],
                "Paid": _pkg['is_paid'],
                "SileoURL": sileoURL,
                "ZebraURL": zbraURL
            }
            rv.append(rv_o)
        return rv
