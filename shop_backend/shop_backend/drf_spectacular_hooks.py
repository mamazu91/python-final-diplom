def filter_swagger_paths(endpoints):
    filtered_paths = []
    paths_to_exclude = ['/api/v1/common/auth/', '/api/v1/schema/']
    for (path, path_regex, method, callback) in endpoints:
        if path not in paths_to_exclude:
            filtered_paths.append((path, path_regex, method, callback))
    return filtered_paths
