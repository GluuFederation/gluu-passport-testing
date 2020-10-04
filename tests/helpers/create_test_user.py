from users_helper import TestUser

# CREATES USER

test_user = TestUser()

token = test_user.get_token()
print("Token generated: %s" % token)


created_user = test_user.create_user(token)
