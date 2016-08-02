"""
functions to fetch general info about all node packages from npmjs.org
"""
import http.client
import json
import os
import pickle

# save_destination - where pickled information is cached about each package
save_destination = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..', '..', 'data', 'npm_all.pickled'))


def _download_registry():
    '''
    download data from network and stores it at `save_destination` as a pickle,
    size of data is roughly 180 MBs.
    '''
    print('Downloading...')

    con = http.client.HTTPConnection("registry.npmjs.org")
    con.request("GET", "/-/all")
    r1 = con.getresponse()

    data = json.loads(r1.read().decode('UTF-8'))

    print('Done.')
    return data


def _load_picked():
    '''
    loads the pickled data
    '''
    print('Loading data...')
    file = open(save_destination, 'rb')
    data = pickle.load(file)
    return data


def load_data():
    '''
    loads data, loads data from network and caches it
    '''
    if os.path.isfile(save_destination):
        answer = input('''
            NPM register has been already downloaded at {}.\n
            It has roughly size of 180 mbs
            Do you wish to re-download it again? [y/N]
            '''.format(save_destination))
        if answer is 'y':
            data = _download_registry()
            return _process_data(data)
        else:
            return _load_picked()
    else:
        print('No cached version found, need to download')
        data = _download_registry()
        return _process_data(data)

    return _load_picked()


def _process_data(data):
    '''
    saves the data in pickle format
    '''
    print('Processing data')

    result = []

    for k, v in data.items():
        if not isinstance(v, dict):
            continue

        name = v['name']
        users_count = len(v.get('users', []))
        contributors_count = len(v.get('contributors', []))
        maintainers_count = len(v.get('maintainers', []))
        license = v.get('license')

        if ('url' in v.get('repository', []) and 'github.com' in v.get('repository').get('url')):
            split_url = v.get('repository').get('url').split('/')

            if len(split_url) >= 2:
                owner = split_url[-2]
                github_repo_name = split_url[-1].split('.')[0]

                result.append({
                    'name': name,
                    'users_count': users_count,
                    'contributors_count': contributors_count,
                    'maintainers_count': maintainers_count,
                    'license': license,
                    'owner': owner,
                    'github_repo_name': github_repo_name
                })
                continue

    file = open(save_destination, 'wb')
    pickle.dump(result, file, pickle.HIGHEST_PROTOCOL)

    print('Done.')

    return result

if __name__ == "__main__":
    load_data()
