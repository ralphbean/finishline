# {{title}}

{% if subtitle %}
## {{subtitle.decode('utf-8')}}
{% endif %}

---
{% for objective in objectives | sort %}# {{ objective }} {.big}
---
{% for key, epic in epics.items() if epic and key in objectives[objective] %}
# [{{ epic.raw['fields']['customfield_10007'] }}]({{ server }}/browse/{{ key }})

{{ epic.raw['fields']['summary'].split('\n')[0] }}

* **Progress**:  {{epic.percent_complete}}%{% if epic.mvp_status %}
* **Status**: {{ epic.mvp_status['value']}}{% endif %}{% if epic.status_update %}
* **Update**: (*{{epic.status_update.updated.split('T')[0]}}*) {{epic.status_update.cleaned}} — *{{epic.status_update.author}}*{% endif %}

{.column}
{% for category in by_epic[key] | sort %}
**{{ category }}**:
{% for issue in by_epic[key][category] %}
* ([{{ issue.key }}]({{ server }}/browse/{{ issue.key }}))
  {{ issue.raw['fields']['summary'].replace('[', '').replace(']', ':') }}{% endfor %}
{% endfor %}
{% if epic.image_url %}![]({{epic.image_url}}){.background}{% endif %}
---
{% endfor %}
{% endfor %}
# Thank you {.big}
Slides auto-generated from JIRA data with [finishline](https://github.com/ralphbean/finishline).
