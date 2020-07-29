@given(u'user already authenticated with another provider')
def check_if_there_is_any_authentication_method_for_user(context):
    raise NotImplementedError(u'STEP: Given user already authenticated with another provider')


@given(u'user has email attribute')
def check_if_user_has_email(context):
    raise NotImplementedError(u'STEP: Given user has email attribute')


@when(u'user authenticates')
def step_impl(context):
    raise NotImplementedError(u'STEP: When user authenticates')


@then(u'user profile should have both authentication methods')
def check_if_user_profile_has_at_least_two_auth_methods(context):
    raise NotImplementedError(u'STEP: Then user profile should have both authentication methods')