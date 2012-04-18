import OpenTokSDK
def genSession(): 
	session_address = "https://api.opentok.com/hl" # Replace with the representative URL of your session.
	apiKey = "14260652"
	apiSecret = "4611823556deeea92d01eea637831386e4d50d3d"
	opentok_sdk = OpenTokSDK.OpenTokSDK(apiKey,apiSecret)
	role_constants = OpenTokSDK.RoleConstants
	session = opentok_sdk.create_session(session_address)
	connectionMetadata = "username=Bob,userLevel=4"
	token = opentok_sdk.generate_token(session.session_id, role_constants.PUBLISHER, None, connectionMetadata)
	return session.session_id,token
