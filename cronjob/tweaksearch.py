#!/usr/bin/python3
import os
from .PackagesManager import PackagesManager

CharizMon = PackagesManager("chariz", "https://repo.chariz.com/Packages.bz2")
DynasticMon = PackagesManager("dynastic", "https://repo.dynastic.co/Packages.bz2")
PackixMon = PackagesManager("packix", "https://repo.packix.com/Packages.bz2")
TwickdMon = PackagesManager("twickd", "https://repo.twickd.com/Packages.bz2")


if __name__ == '__main__':
    print("[TWEAKLY]: CRON STARTED")
    print("[TWEAKLY]: fetching chariz...")
    os.system("curl https://repo.chariz.com/Packages.bz2 --output chariz.bz2")
    os.system("bunzip2 -fd chariz.bz2")
    print("[TWEAKLY]: fetching dynastic...")
    os.system("curl -H \"X-Machine: iPhone12,8\" -H \"X-Unique-ID: 00000000-80000000E\" -H \"X-Firmware: 14.0\" https://repo.dynastic.co/Packages.bz2 --output dynastic.bz2")
    os.system("bunzip2 -fd dynastic.bz2")
    print("[TWEAKLY]: fetching twickd...")
    os.system("curl https://repo.twickd.com/Packages.bz2 --output twickd.bz2")
    os.system("bunzip2 -fd twickd.bz2")
    print("[TWEAKLY]: fetching packix...")
    os.system("curl https://repo.packix.com/Packages.bz2 --output packix.bz2")
    os.system("bunzip2 -fd packix.bz2")
    print("[TWEAKLY]: processing...")
    CharizMon.parsePackages()
    DynasticMon.parsePackages()
    TwickdMon.parsePackages()
    PackixMon.parsePackages()
    print("[TWEAKLY]: FINISHED DATA REFESH")
