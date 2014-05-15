{% macro out(entity, name, boolean = True) -%}
    {% set cls = entity.__class__ %}
    {% set value = entity[name + '_meta']|default('N/A', boolean) %}
    {{ tag_out(cls, name, value) }}
{%- endmacro %}

{% macro input(entity, name, placeholder = None, boolean = True) -%}
    {% set cls = entity.__class__ %}
    {% set value = entity[name]|default('', boolean) %}
    {% set error = errors[name] %}
    {{ tag_input(cls, name, value, error) }}
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

{% macro tag_input(cls, name, value, error) -%}
    {% set meta = cls._solve(name) %}
    {% if meta == "secret" %}
        <input type="password" class="text-field" name="{{ name }}"
               value="{{ value }}" data-error="{{ error }}" />
    {% else %}
        <input type="text" class="text-field" name="{{ name }}"
               value="{{ value }}" data-error="{{ error }}" />
    {% endif %}
{%- endmacro %}

{% block html %}{% endblock %}
