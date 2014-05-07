{% macro out(entity, name) -%}
    {% set cls = entity.__class__ %}
    {% set value = entity[name + '_meta']|default('N/A', True) %}
    {{ tag_out(cls, name, value) }}
{%- endmacro %}

{% macro tag_out(cls, name, value) -%}
    {% set def = cls[name] %}
    {% set meta = def.get("meta", "text") %}
    {% if meta == "enum" %}
        <span class="tag {{ value }}">{{ value }}</span>
    {% else %}
        {{ value }}
    {% endif %}
{%- endmacro %}

{% block html %}{% endblock %}
