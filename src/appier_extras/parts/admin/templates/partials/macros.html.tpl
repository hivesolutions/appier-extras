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

{% macro menu_link(name, href = "#") -%}
    {% if area == name %}
        <a class="active" href="{{ href }}">{{ name }}</a>
    {% else %}
        <a href="{{ href }}">{{ name }}</a>
    {% endif %}
{%- endmacro %}

{% macro paging(current, count, caller = None) -%}
    <div class="pages">
        {% if caller %}
            {% set previous = caller(page = current - 1) %}
            {% set next = caller(page = current + 1) %}
        {% else %}
            {% set previous = "#" %}
            {% set next = "#" %}
        {% endif %}
        {% if current == 1 %}
            <span class="page disabled">&#8592;</span>
        {% else %}
            <a href="{{ previous }}" class="page">&#8592;</a>
        {% endif %}
        {% for index in range(count) %}
            {% set index = index + 1 %}
            {% if caller %}
                {% set href = caller(page = index) %}
            {% else %}
                {% set href = "#" %}
            {% endif %}
            {% if index == current %}
                <span class="page selected">{{ index }}</span>
            {% else %}
                <a href="{{ href }}" class="page">{{ index }}</a>
            {% endif %}
        {% endfor %}
        {% if current == count %}
            <span class="page disabled">&#8594;</span>
        {% else %}
            <a href="{{ next }}" class="page">&#8594;</a>
        {% endif %}
    </div>
{%- endmacro %}

{% block html %}{% endblock %}
