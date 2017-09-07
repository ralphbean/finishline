""" Finish Line!  A CLI tool for wrapping up your sprints.

See the README for more information.

Author:  Ralph Bean <rbean@redhat.com>

"""

import argparse
import datetime
import collections

import bs4
import docutils.examples
import jinja2

import jira

date_format = '%Y-%m-%d'

custom_filters = {
    'slugify': lambda x: x.lower().replace(' ', '-'),
    'rst2html': lambda rst: docutils.examples.html_parts(rst, input_encoding='utf-8')['body'],
    'replace': lambda string, char: char * len(string),
}


def scrape_links(session, args):
    response = session.get(args.server)
    soup = bs4.BeautifulSoup(response.text, 'html5lib')
    return [l.text for l in soup.find(id='content').findAll('a')[5:]]


def parse_arguments():
    two_weeks = datetime.timedelta(days=14)
    default_since = (datetime.date.today() - two_weeks).strftime(date_format)
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', help='server to your JIRA instance.')
    parser.add_argument('--insecure', help='Do not verify SSL certs.',
                        default=False, action='store_true')
    parser.add_argument('--project', help='JIRA project to report on.')
    parser.add_argument('--since', help='Past date from which to pull data.',
                        default=default_since)
    parser.add_argument('--title', help='Title of the report.')
    parser.add_argument('--subtitle', help='Subtitle of the report.')
    parser.add_argument('--template', help='Path to a template for output.')
    parser.add_argument('--epicfield', help='Epic customfield key.',
                        default='customfield_10006')
    args = parser.parse_args()
    if not args.server:
        raise ValueError('--server is required')
    if not args.project:
        raise ValueError('--project is required')
    if not args.title:
        raise ValueError('--title is required')
    if not args.template:
        raise ValueError('--template is required')
    return args


def render(args, data):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
    )
    env.filters.update(custom_filters)
    template = env.get_template(args.template)

    data = data.copy()

    data['today'] = datetime.datetime.utcnow().strftime(date_format)

    data.update(args._get_kwargs())

    return template.render(**data)

def pull_issues(client, args):
    tmpl = (
        'project = %s'
        ' AND resolution is not EMPTY'
        ' AND resolutiondate >= %s'
        ' AND status != Dropped'
    )
    query = tmpl % (args.project, args.since)
    issues = client.search_issues(query)
    for issue in issues:
        yield issue


def get_epic_details(client, key):
    if not key:
        return None
    epic = client.issue(key)

    epic.image_url = 'https://placekitten.com/1600/900'

    epic.status_update = 'foo bar'
    epic.status_update_date = '2017-01-01'

    return epic


def collate_issues(client, args, issues):
    epics = {}
    by_epic = collections.defaultdict(set)
    for issue in issues:
        epic = issue.raw['fields'][args.epicfield]

        # Enrich with details
        if not epic in epics:
            epics[epic] = get_epic_details(client, epic)

        # Associate the issue with the enriched epic.
        by_epic[epic].add(issue)

    return dict(epics=epics, by_epic=by_epic)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    args = parse_arguments()

    client = jira.client.JIRA(
        server=args.server,
        options=dict(verify=not args.insecure),
        kerberos=True,
    )

    issues = pull_issues(client, args)
    data = collate_issues(client, args, issues)

    output = render(args, data)
    print output.encode('utf-8')
