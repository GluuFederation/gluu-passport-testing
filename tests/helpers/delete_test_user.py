from users_helper import TestUser

# DELETE USER TO TEARDOWN
util = TestUser()
token = util.get_token()
deleted = util.delete_user(token)
if deleted is True:
    print("User deleted from idp/oidc provider via API.")
else:
    print("[ERROR] USER NOT DELETED, PLEASE CHECK.")
