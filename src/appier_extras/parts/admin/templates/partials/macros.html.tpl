{% macro out(entity, name) -%}
    {% set value = entity[name + '_meta']|default('N/A', True) %}
    {{ tag_out(entity, name, value) }}
{%- endmacro %}

{% macro tag_out(entity, name, value) -%}
    {% set cls = entity.__class__ %}
    {% set def = cls[name] %}
    {% set meta = def.get("meta", "text") %}
    {% if meta == "enum" %}
        <span class="tag">{{ value }}</span>
    {% else %}
        {{ value }}
    {% endif %}
{%- endmacro %}

{% block html %}{% endblock %}
