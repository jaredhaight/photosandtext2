def clean_response_data(res):
    """
    Cleans a dict so that it can be sent out through Restful.
    """
    for key, value in res.iteritems():
        if isinstance(key, datetime.datetime):
            stringKey = key.strftime("%Y-%m-%d %H:%M:%S")
            res[stringKey] = value
            del(res[key])
        if isinstance(value, datetime.datetime):
            res[key] = value.strftime("%Y-%m-%d %H:%M:%S")
    return res