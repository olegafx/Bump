import os
import json
from functools import cmp_to_key
from string import Template
from urllib import request
from urllib.parse import urljoin

from . import settings as conf
from . import defaults
from .lib import semver

def get_request(pathname):
    webURL = request.urlopen(pathname)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    return json.loads(data.decode(encoding))

def fetch_package_version(package, version, callback = None):
    registry = conf.settings.get('registry', defaults.get_registry())
    pathname = urljoin(registry, package.replace('/', '%2F'))
    pathname = Template('$pathname?version=$version').substitute(pathname=pathname, version=version)
    response = get_request(pathname)

    if (callback and ('versions' in response)):
        orderedVersions = sorted(response['versions'].keys(), key=cmp_to_key(lambda v1, v2: semver.rcompare(v1, v2, loose=True)))
        latestVersion = next(iter(orderedVersions))

        callback(latestVersion)
