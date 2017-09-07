# {{title}}
{% if subtitle %}
## {{subtitle}}
## {{today}}
### PnT DevOps
{% endif %}
---
{% for key, epic in epics.items() if epic %}
# [{{ epic.raw['fields']['customfield_10007'] }}]({{ server }}/browse/{{ key }})

{{ epic.raw['fields']['summary'] }}

{% if epic.status_update %}**Status**: (*{{epic.status_update_date}}*) {{epic.status_update}} {% endif %}
{% for issue in by_epic[key] %}
* {{ issue.raw['fields']['summary'].replace('[', '').replace(']', ':') }}
  [{{ issue.key }}]({{ server }}/browse/{{ issue.key }})
{% endfor %}
{% if epic.image_url %}![]({{epic.image_url}}){.background}
{% endif %}
---
{% endfor %}
# Thank you
