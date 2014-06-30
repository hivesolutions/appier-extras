{% macro out(entity, name, boolean = True) -%}
    {% set cls = entity.__class__ %}
    {% set value = entity[name + '_meta']|default('N/A') %}
    {% if value in (None, '') and boolean %}{% set value = 'N/A' %}{% endif %}
    {{ tag_out(cls, name, value, entity) }}
{%- endmacro %}

{% macro input(entity, name, placeholder = None, boolean = True, create = False) -%}
    {% set cls = entity.__class__ %}
    {% set info = cls[name]|default({}, True) %}
    {% set disabled = info.get('immutable', False) and not create %}
    {% set value = entity[name]|default('') %}
    {% set error = errors[name] %}
    {% if value in (None, '') and boolean %}{% set value = '' %}{% endif %}
    {{ tag_input(cls, name, value, entity, error, disabled = disabled) }}
{%- endmacro %}

{% macro tag_out(cls, name, value, entity) -%}
    {% set meta = cls._solve(name) %}
    {% if meta == "reference" %}
        {% set info = cls[name] %}
        {% set type = info["type"] %}
        {% set target = type._target() %}
        {% set _value = entity[name] %}
        {% if _value %}
            <a href="{{ url_for('admin.show_entity', model = target._name(), _id = _value._id) }}">{{ value }}</a>
        {% else %}
            {{ value }}
        {% endif %}
    {% elif meta == "references" %}
        {% set _value = entity[name] %}
        {% for item in _value %}
            <a href="{{ url_for('admin.show_entity', model = item.resolve().__class__._name(), _id = item._id) }}">{{ item }}</a>
        {% endfor %}
    {% elif meta == "enum" %}
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

{% macro tag_input(cls, name, value, entity, error, disabled = False) -%}
    {% set meta = cls._solve(name) %}
    {% set disabled_s = "\" data-disabled=\"1" if disabled else "" %}
    {% if meta == "reference" %}
        {% set info = cls[name] %}
        {% set type = info["type"] %}
        {% set target = type._target() %}
        {% set _name = type._name %}
        <div class="drop-field {{ disabled_s|safe }}"  value="{{ value }}" data-error="{{ error }}"
             data-value_attribute="{{ _name }}"  data-number_options="-1">
            <input type="hidden" class="hidden-field" name="{{ name }}" value="{{ value }}" />
            <div class="data-source" data-type="json"
                 data-url="{{ url_for('admin.show_model_json', model = target._name() ) }}"></div>
        </div>
    {% elif meta == "references" %}
        {% set info = cls[name] %}
        {% set type = info["type"] %}
        {% set target = type._target() %}
        {% set _name = type._name %}
        <div class="tag-field {{ disabled_s|safe }}" value="{{ value }}" data-error="{{ error }}"
             data-value_attribute="{{ _name }}"  data-number_options="-1">
            <input type="hidden" class="hidden-field" name="{{ name }}" value="{{ value }}" />
            <div class="data-source" data-type="json"
                 data-url="{{ url_for('admin.show_model_json', model = target._name() ) }}"></div>
        </div>
    {% elif meta == "date" %}
        <input type="text" class="text-field {{ disabled_s|safe }}" name="{{ name }}" value="{{ value }}"
               data-type="date" data-error="{{ error }}" />
    {% elif meta == "datetime" %}
        <input type="text" class="text-field {{ disabled_s|safe }}" name="{{ name }}" value="{{ value }}"
               data-type="date" data-error="{{ error }}" />
    {% elif meta == "secret" %}
        <input type="password" class="text-field {{ disabled_s|safe }}" name="{{ name }}"
               value="{{ value }}" data-error="{{ error }}" />
    {% else %}
        <input type="text" class="text-field {{ disabled_s|safe }}" name="{{ name }}"
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

{% macro paging(current, count, caller = None, size = 5) -%}
    <div class="pages">
        {% if caller %}
            {% set previous = caller(page = current - 1) %}
            {% set next = caller(page = current + 1) %}
            {% set first = caller(page = 1) %}
            {% set last = caller(page = count) %}
        {% else %}
            {% set previous = "#" %}
            {% set next = "#" %}
        {% endif %}
        {% if current == 1 %}
            <span class="page disabled">&#8592;</span>
        {% else %}
            <a href="{{ previous }}" class="page">&#8592;</a>
        {% endif %}
        {% if current != 1 %}
            <a href="{{ first }}" class="page">first</a>
        {% endif %}

        {% set offset_start = (current - size - 1) %}
        {% if offset_start > 0 %}{% set offset_start = size %}
        {% else %}{% set offset_start = size + offset_start %}
        {% endif %}

        {% set extra = size - offset_start %}
        {% set size_end = size + extra %}

        {% set offset_end = count - (current + size_end) %}
        {% if offset_end > 0 %}{% set offset_end = size_end %}
        {% else %}{% set offset_end = size_end + offset_end %}
        {% endif %}

        {% set extra = size - offset_end %}
        {% set size_start = size + extra %}

        {% set offset_start = (current - size_start - 1) %}
        {% if offset_start > 0 %}{% set offset_start = size_start %}
        {% else %}{% set offset_start = size_start + offset_start %}
        {% endif %}

        {% for index in range(current - offset_start - 1, current + offset_end) %}
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
        {% if current != count %}
            <a href="{{ last }}" class="page">last</a>
        {% endif %}
        {% if current == count %}
            <span class="page disabled">&#8594;</span>
        {% else %}
            <a href="{{ next }}" class="page">&#8594;</a>
        {% endif %}
    </div>
{%- endmacro %}

{% block html %}{% endblock %}
