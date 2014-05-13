{% macro out(entity, name, boolean = True) -%}
    {% set cls = entity.__class__ %}
    {% set value = entity[name + '_meta']|default('N/A', boolean) %}
    {{ tag_out(cls, name, value) }}
{%- endmacro %}

{% macro tag_out(cls, name, value) -%}
    {% set meta = cls._solve(name) %}
    {% if meta == "enum" %}
        <span class="tag {{ value }}">{{ value }}</span>
    {% elif meta == "url" %}
        <a href="{{ value }}">{{ value }}</a>
    {% elif meta == "email" %}
        <a href="mailto:{{ value }}">{{ value }}</a>
    {% elif meta == "bool" %}
    	<span class="tag {{ value.lower() }}">{{ value }}</span>		
    {% else %}
        {{ value }}
    {% endif %}
{%- endmacro %}

{% block html %}{% endblock %}
