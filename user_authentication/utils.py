def serializer_error_format(error):
    ''' Serializer Error Format '''
    error_message = None
    if error.get('non_field_errors'):
        error_message = error['non_field_errors'][0]
    elif error.get('email'):
        error_message = error['email'][0]
    elif error.get('username'):
        error_message = error['username'][0]
    elif error.get('user_type'):
        error_message = error['user_type'][0]
    return error_message