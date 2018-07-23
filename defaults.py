import datetime
import logging
import os


DATE_FORMAT = '%Y-%m-%d'
two_weeks = datetime.timedelta(days=14)

REQUIRED_OPTIONS = [
    'server',
    'project',
    'title',
    'template'
]


DEFAULTS = dict(
    cacert='/etc/pki/tls/certs/ca-bundle.crt',
    query_template='query.j2',
    okr_query_template='okrquery.j2',
    since=(datetime.date.today() - two_weeks).strftime(DATE_FORMAT),
    epic_field='customfield_10006',
    mvp_status_field='customfield_11908',
    story_point_field='customfield_10002',
    default_story_points=float(3),
    hide_epics=[],
    include_epics=[],
    placeholder_objective='Miscellaneous',
    attribution=False,
    query_context=[],
)


LIST_FIELDS = [
    'hide_epics',
    'include_epics',
    'query_context',
]

NUMERIC_FIELDS = [
    'default_story_points'
]

BOOL_FIELDS = [
    'attribution'
]


def _massage_fields(config):
    options = config['options']
    for field in LIST_FIELDS:
        if field in options:
            raw = options[field].split(',')
            options[field] = [f.strip() for f in raw]

    for field in NUMERIC_FIELDS:
        if field in options:
            options[field] = float(options[field])

    for field in BOOL_FIELDS:
        if field in options:
            options[field] = bool(options[field])

    return config


def _replace_date(field_value):
    today = datetime.date.today()
    return field_value.format(DATE=today.strftime('%B %d, %Y'))


def set_defaults(config):
    config = _massage_fields(config)
    user_options = config['options']
    for option, value in DEFAULTS.items():
        if option not in user_options:
            user_options[option] = value

    # Allow for service account password from environment variable
    env_passwd = os.getenv('FINISHLINE_SERVICE_ACCOUNT_PASSWORD')
    if ('service_account_password' not in user_options and
            env_passwd is not None):
        user_options['service_account_password'] = env_passwd
    if 'service_account_password' in user_options:
        logging.warn('WARNING: service account password in use')

    config['options'] = user_options

    if 'subtitle' in user_options and '{DATE}' in user_options['subtitle']:
        config['options']['subtitle'] = _replace_date(user_options['subtitle'])

    return config


def validate_config(options):
    for option in REQUIRED_OPTIONS.copy():
        if option in options:
            REQUIRED_OPTIONS.remove(option)

    if len(REQUIRED_OPTIONS) > 0:
        msg = ('The following required options were not specified in the '
               'config file: {missing}').format(missing=REQUIRED_OPTIONS)
        raise Exception(msg)

    for epic in options['include_epics']:
        if epic in options['hide_epics']:
            raise Exception("%r may not be both hidden and included." % epic)


def override_scenario(config, scenario):
    assert scenario in config
    config['options'].update(config[scenario])
    return config
