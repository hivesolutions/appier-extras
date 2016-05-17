{% macro h1(contents) -%}
    <h1 style="margin-top:38px;margin-bottom:26px;font-size:28px;font-weight:600;color:#2d2d2d;">{{ contents }}</h1>
{%- endmacro %}

{% macro h2(contents) -%}
    <h2 style="margin-top:38px;font-size:22px;font-weight:600;color:#2d2d2d;">{{ contents }}</h2>
{%- endmacro %}

{% macro link(href, contents, base = True, simple = False) -%}
    {% if base %}{% set href = base_url|default('', True) + href %}{% endif %}
    {% if simple %}
        <a href="{{ href }}">{{ contents }}</a>
    {% else %}
        <a href="{{ href }}" style="color:#1b75bb;text-decoration:none;padding-bottom:1px;">{{ contents }}</a>
    {% endif %}
{%- endmacro %}
{% block html %}{% endblock %}
