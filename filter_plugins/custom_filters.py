def get_remote(users, remote=True):
    """Returns list users which have/have not remote option set"""

    ret = []

    for u in users:
        if remote and 'remote' in u and u['remote'] is True:
            ret.append(u)
        elif not remote and ('remote' not in u or u['remote'] is False):
            ret.append(u)

    return ret


def get_info(users):
    """Returns list of users and their attributes"""

    ret = {}

    if 'results' in users and users['results']:
        for u in users['results']:
            if 'failed' in u and not u['failed']:
                ret[u['name']] = {
                    'comment': u['comment'],
                    'group': u['group'],
                    'home': u['home'],
                    'shell': u['shell'],
                    'uid': u['uid'],
                }

    return ret


class FilterModule(object):
    """Custom Jinja2 filters"""

    def filters(self):
        return {
            'get_remote': get_remote,
            'get_info': get_info,
        }
