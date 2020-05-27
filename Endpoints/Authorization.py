from app import JWTManager
from Database.MongoDBHandlers import TokenDBHandler

MongoTokens = TokenDBHandler()


@JWTManager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    rv = MongoTokens.getBlacklistedToken(jti)
    if rv != None:
        return True
    return False


'''
# This route is temporarily disabled because we'll use a token which is indefinitely valid
@app.route("/auth/get")
def cToken():
    access_token = create_access_token(identity="BotAPIAccess", expires_delta=False)
    return jsonify(access_token=access_token)
'''