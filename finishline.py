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
    parser.add_argument('--epic-field', help='Epic field key.',
                        default='customfield_10006')
    parser.add_argument('--mvp-status-field', help='MVP status field key.',
                        default='customfield_11908')
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


def extract_status_update(args, epic):
    sentinnels = [
        'h1. Status Update:',
        'Status Update:',
        'h1. Status Update',
        'Status Update',
    ]
    for comment in epic.fields.comment.comments:
        for sentinnel in sentinnels:
            body = comment.body
            if body.startswith(sentinnel):
                # Attach a cleaned version for the template.
                body = body[len(sentinnel):].lstrip()
                body = body.split('\n\n')[0].strip()
                comment.cleaned = body
                return comment


def extract_mvp_status(args, epic):
    return epic.raw['fields'][args.mvp_status_field]


def get_epic_details(client, args, key):
    if not key:
        return None
    epic = client.issue(key)

    #epic.image_url = 'https://placekitten.com/1600/900'
    epic.status_update = extract_status_update(args, epic)
    epic.mvp_status = extract_mvp_status(args, epic)
    return epic


def collate_issues(client, args, issues):
    epics = {}
    by_epic = collections.defaultdict(set)
    for issue in issues:
        epic = issue.raw['fields'][args.epic_field]

        # Enrich with details
        if not epic in epics:
            epics[epic] = get_epic_details(client, args, epic)

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
