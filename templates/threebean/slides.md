# {{title}}

{% if subtitle %}
## {{subtitle.decode('utf-8')}}
{% endif %}

---
{% for key, epic in epics.items() if epic %}
# [{{ epic.raw['fields']['customfield_10007'] }}]({{ server }}/browse/{{ key }})

{{ epic.raw['fields']['summary'].split('\n')[0] }}

* **Percent**:  %{{epic.percent_complete}}{% if epic.mvp_status %}
* **Status**: {{ epic.mvp_status['value']}}{% endif %}{% if epic.status_update %}
* **Update**: (*{{epic.status_update.updated.split('T')[0]}}*) {{epic.status_update.cleaned}} — *{{epic.status_update.author}}*

{.column} {% endif %}
{% for issue in by_epic[key] %}
* {{ issue.raw['fields']['summary'].replace('[', '').replace(']', ':') }}
  [{{ issue.key }}]({{ server }}/browse/{{ issue.key }})
{% endfor %}
{% if epic.image_url %}![]({{epic.image_url}}){.background}
{% endif %}
---
{% endfor %}
# Thank you
