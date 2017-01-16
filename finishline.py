""" Finish Line!  A CLI tool for wrapping up your sprints.

See the README for more information.

Author:  Ralph Bean <rbean@redhat.com>

"""

import argparse
import datetime
import collections

import bs4
import docutils.examples
import requests
import jinja2


custom_filters = {
    'slugify': lambda x: x.lower().replace(' ', '-'),
    'rst2html': lambda rst: docutils.examples.html_parts(rst, input_encoding='utf-8')['body'],
    'replace': lambda string, char: char * len(string),
}


def scrape_links(session, args):
    response = session.get(args.url)
    soup = bs4.BeautifulSoup(response.text, 'html5lib')
    return [l.text for l in soup.find(id='content').findAll('a')[5:]]


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='HTTP-accessible directory where sprint videos and descriptions are stored.')
    parser.add_argument('--title', help='Title of the report.')
    parser.add_argument('--template', help='Path to a template for output.')
    args = parser.parse_args()
    if not args.url:
        raise ValueError('--url is required')
    if not args.title:
        raise ValueError('--title is required')
    if not args.template:
        raise ValueError('--template is required')
    return args


def prepare(session, args, links):
    get = lambda filename: session.get(args.url + '/' + filename).text

    try:
        links.remove('readme.rst')
        summary = get('readme.rst')
    except ValueError:
        summary = ''

    collated = collections.defaultdict(dict)
    for link in links:
        key, extension = link.rsplit('.')
        collated[key][extension] = link

    entries = []
    for key, items in collated.items():

        username, rest = key.split('-', 1)
        heading = "%s, by %s" % (rest, username)

        extensions = items.keys()
        try:
            extensions.remove('rst')
            body = get(items['rst'])
        except ValueError:
            body = None

        assert(len(extensions) == 1)
        link = items[extensions[0]]

        entries.append((heading, body, args.url + '/' + link,))

    entries.sort()

    return dict(summary=summary, entries=entries)


def render(args, data):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
    )
    env.filters.update(custom_filters)
    template = env.get_template(args.template)

    data = data.copy()

    fmt = "%Y/%m/%d %H:%M:%S"
    data['current_date'] = datetime.datetime.now().strftime(fmt)

    data.update(args._get_kwargs())

    return template.render(**data)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    args = parse_arguments()

    session = requests.session()

    links = scrape_links(session, args)

    data = prepare(session, args, links)

    output = render(args, data)
    print output
