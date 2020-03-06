def parse_url(url):
    if url[-1] == '/':
        return url.split('/')[-3:-1]
    else:
        return url.split('/')[-2:]
