def custom_preprocessing_hook(endpoints):
    path_to_exclude = 'auth'
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if not (path.endswith(path_to_exclude) or path.endswith(path_to_exclude + '/'))
    ]
