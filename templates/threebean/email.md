{{title}}
{% if subtitle %}{{subtitle.decode('utf-8')}}
{% endif %}
---
# OKR Summary
{% for objective in objectives | sort %}
{{objective}}{% for key, epic in epics.items() if epic and key in objectives[objective] %}
  {{ epic.raw['fields']['summary'].split('\n')[0] }} - {{ server }}/browse/{{ key }} - {{epic.percent_complete}}%{% endfor %}
{% endfor %}
---
{% for objective in objectives | sort %}# {{ objective }}
{% for key, epic in epics.items() if epic and key in objectives[objective] %}
{{ epic.raw['fields']['summary'].split('\n')[0].strip() }} - {{ server }}/browse/{{ key }}

- Progress:  {{epic.percent_complete}}%{% if epic.target_date %}
- Target: {{ epic.target_date}}{% endif %}{% if epic.mvp_status %}
- Status: {{ epic.mvp_status['value']}}{% endif %}{% if epic.status_update %}
- Update: (*{{epic.status_update.updated.split('T')[0]}}*) {{epic.status_update.cleaned}}{% if attribution %} — {{epic.status_update.author}}{% endif %}{% endif %}
{% for category in by_epic[key] | sort %}
**{{ category }}**:
{% for issue in by_epic[key][category] %}
- {{ issue.key }} - {{ issue.raw['fields']['summary'].replace('[', '').replace(']', ':') }}{% endfor %}
{% endfor %}
---{% endfor %}
{% endfor %}
# Thank you

For any questions, feel free to reach out to mikeb@redhat.com (Product Owner)
and rbean@redhat.com (Team Lead), respond on list, or join to chat in #pnt-devops-dev.
