from app import app
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from Utilities.PackagesManager import PackagesManager
from threading import Thread

CharizMon = PackagesManager("chariz", "https://repo.chariz.com/Packages.bz2")
DynasticMon = PackagesManager("dynastic", "https://repo.dynastic.co/Packages.bz2")
PackixMon = PackagesManager("packix", "https://repo.packix.com/Packages.bz2")
TwickdMon = PackagesManager("twickd", "https://repo.twickd.com/Packages.bz2")
isRefreshing = False


@app.route('/api/refreshTweaks')
@jwt_required
def refreshBro():
    global isRefreshing
    if isRefreshing:
        return jsonify({"status": "please wait"})
    chariz_refresh = Thread(target=CharizMon.refreshRepo)
    dynastic_refresh = Thread(target=DynasticMon.refreshRepo)
    packix_refresh = Thread(target=PackixMon.refreshRepo)
    twickd_refresh = Thread(target=TwickdMon.refreshRepo)

    chariz_refresh.start()
    dynastic_refresh.start()
    packix_refresh.start()
    twickd_refresh.start()
    isRefreshing = True

    chariz_refresh.join()
    dynastic_refresh.join()
    packix_refresh.join()
    twickd_refresh.join()

    isRefreshing = False
    return jsonify({"status": "success"})


@app.route('/api/lookup')
@jwt_required
def searchTweak():
    if request.args.get('Name') != None:
        tName = request.args['Name']
        rv_d = {}
        rv1 = CharizMon.getPackage(tName)
        rv2 = DynasticMon.getPackage(tName)
        rv3 = PackixMon.getPackage(tName)
        rv4 = TwickdMon.getPackage(tName)
        if rv1 != None:
            rv_d['chariz'] = rv1
        if rv2 != None:
            rv_d['dynastic'] = rv2
        if rv3 != None:
            rv_d['packix'] = rv3
        if rv4 != None:
            rv_d['twickd'] = rv4
        return jsonify(rv_d)
    return jsonify({"status": "error"})
