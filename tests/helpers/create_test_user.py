from users_helper import TestUser

# CREATES USER


test_user = TestUser()

token = test_user.get_token()


created_user = test_user.create_user(token)


