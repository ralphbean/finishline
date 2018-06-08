# {{title}}
{% if subtitle %}
## {{subtitle}}
{% endif %}
---
# OKR Summary
{% for objective in objectives | sort %}
* {{objective}}{% for key, epic in epics.items() if epic and key in objectives[objective] %}
  * [{{ epic.raw['fields']['summary'].split('\n')[0] }}]({{ server }}/browse/{{ key }})  **{{epic.percent_complete}}%**{% endfor %}
{% endfor %}
---
{% for objective in objectives | sort %}# {{ objective }} {.big}
---
{% for key, epic in epics.items() if epic and key in objectives[objective] %}
# [{{ epic.raw['fields']['summary'].split('\n')[0].split('KR:')[-1].strip() }}]({{ server }}/browse/{{ key }})

* **Progress**:  {{epic.percent_complete}}%{% if epic.target_date %}
* **Target**: {{ epic.target_date}}{% endif %}{% if epic.mvp_status %}
* **Status**: **{{ epic.mvp_status['value']}}**{% endif %}{% if epic.status_update %}
* **Update**: (*{{epic.status_update.updated.split('T')[0]}}*) {{epic.status_update.cleaned}}{% if attribution %} — *{{epic.status_update.author}}*{% endif %}{% endif %}

{.column}
{% for category in by_epic[key] | sort %}
**{{ category }}**:
{% for issue in by_epic[key][category] %}
* ([{{ issue.key }}]({{ server }}/browse/{{ issue.key }}))
  {{ issue['summary'].replace('[', '').replace(']', ':') }}{% endfor %}
{% endfor %}
{% if epic.image_url %}![]({{epic.image_url}}){.background}{% endif %}
---{% endfor %}
{% endfor %}
# Thank you {.big}

Auto-generated from JIRA data with [finishline](https://github.com/ralphbean/finishline).
{% if references %}
---
{{references}}
{% endif %}
