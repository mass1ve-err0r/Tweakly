from wsgi import app, lim
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from Utilities.PackagesManager import PackagesManager

CharizMon = PackagesManager("chariz", "https://repo.chariz.com/Packages.bz2")
DynasticMon = PackagesManager("dynastic", "https://repo.dynastic.co/Packages.bz2")
PackixMon = PackagesManager("packix", "https://repo.packix.com/Packages.bz2")
TwickdMon = PackagesManager("twickd", "https://repo.twickd.com/Packages.bz2")


@app.route('/v1/tweakly/lookup', subdomain="api")
@lim.limit("100/minute")
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
