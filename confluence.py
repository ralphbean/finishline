#!/usr/bin/env python
# coding: utf-8
""" confluence - a CLI tool to replace content in Confluence

Author:  Róman Joost <rjoost@redhat.com>

Example:

python2.7 confluence.py --server https://your.confluence.instance.test --pageid 38176033 --auth-path=/additionalloginpath confluence.something
"""
import argparse
import requests
import requests_kerberos
import json


def post_content(session, args, data_to_post):
    url = '{base}/rest/api/content/{pageid}'.format(base=args.server, pageid=args.pageid)
    r = session.put(url, data=data_to_post, headers={'Content-Type': 'application/json'})
    r.raise_for_status()

def prepare_content(session, args, info, content):
    new_version = int(info['version']['number']) + 1
    new_ancestors = info['ancestors'][-1]
    del new_ancestors['_links']
    del new_ancestors['_expandable']
    del new_ancestors['extensions']

    data = {
        'id': args.pageid,
        'type': 'page',
        'title': info['title'],
        'version': {'number': new_version},
        'ancestors': [new_ancestors],
        'body': {
            'storage': {
                'representation': 'storage',
                'value': content,
            }
        }
    }

    return json.dumps(data)

def convert_wiki_markup_to_storage(session, args, markup):
    url = '{base}/rest/api/contentbody/convert/storage'.format(base=args.server)
    data = json.dumps(dict(value=markup, representation='wiki'))
    r = session.post(url, data=data, headers={'Content-Type': 'application/json'})
    r.raise_for_status()
    return r.json()['value']

def get_page_information(session, args):
    url = '{base}/rest/api/content/{pageid}'.format(base=args.server, pageid=args.pageid)
    r = session.get(url, params={'expand': 'history,space,version,ancestors'})
    r.raise_for_status()
    return r.json()

def login(args):
    kerb = requests_kerberos.HTTPKerberosAuth(mutual_authentication=requests_kerberos.DISABLED)
    s = requests.session()
    s.get('{base}{authpath}'.format(base=args.server, authpath=args.auth_path),
          auth=kerb,
          verify=args.cacert)
    return s

def parse_arguments():
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument("-s", "--server", help="Base URL")
    config_parser.add_argument("-p", "--pageid", help="Page ID to update")
    config_parser.add_argument('--auth-path',
                        help='additional (server) path to authenticate first',
                        default=None)
    config_parser.add_argument("markup", help="Confluence markup to post")
    config_parser.add_argument('--cacert', help='CA cert for https validation.',
                               default='/etc/pki/tls/certs/ca-bundle.crt')
    return config_parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    with open(args.markup, 'r') as f:
        wiki_markup = f.read()

    session = login(args)
    storage_content = convert_wiki_markup_to_storage(session, args, wiki_markup)
    info = get_page_information(session, args)
    data_to_post = prepare_content(session, args, info, storage_content)
    post_content(session, args, data_to_post)

    print("{base}/pages/viewpage.action?pageId={pageid}".format(base=args.server, pageid=args.pageid))
