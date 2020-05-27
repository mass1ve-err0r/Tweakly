from bz2 import BZ2File
from shutil import copyfileobj
from requests import get
from json import dumps
from os import environ as env
from Database.MongoDBHandlers import MongoDBHandler

agent = env.get('UAGENT')


class PackagesManager:
    def __init__(self, RepoName: str, RepoURL: str):
        self.RepoName = RepoName
        self.RepoURL = RepoURL
        self.Mongo = MongoDBHandler(RepoName)
        self.hdr = {"X-Unique-ID": "00000000",
                    "X-Firmware": "14.0",
                    "X-Machine": "iPhone12,6",
                    "User-Agent": agent,
                    "Connection": "keep-alive"
                    }

    def refreshPackagesFile(self) -> int:
        print("[+]: refreshing....")
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
            return 1
        outfile = self.RepoName + '.bz2'
        with open(outfile, 'wb') as f:
            copyfileobj(r.raw, f)
            return 0

    def extactPackagesFile(self) -> int:
        print("[+]: extracting...")
        outfile = self.RepoName + ".txt"
        infile = self.RepoName + ".bz2"
        try:
            with BZ2File(infile) as fr, open(outfile, "wb") as fw:
                copyfileobj(fr, fw)
                return 0
        except Exception:
            return 1

    def parsePackages(self) -> None:
        print("[+]: parsing...")
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
                    if "Tag" == s[0]:
                        if "cydia::commercial" in s[1]:
                            entry['is_paid'] = True
                        else:
                            entry['is_paid'] = False
                    entry[s[0]] = s[1].strip()

    def returnPackage(self, identifier: str):
        print("[+]: getting...")
        _pkg = self.Mongo.getPackage(identifier)
        rv = {
            "Name": _pkg['Name'],
            "Version": _pkg['Version'],
            "Description": _pkg['Description'],
            "Author": _pkg['Author'],
            "IconURL": _pkg['Icon'],
            "Depiction": _pkg['Depiction'],
            "Size": _pkg['Size'],
            "Paid": _pkg['is_paid']
        }
        return rv