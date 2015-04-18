{% macro out(entity, name, boolean = True, default = 'N/A') -%}
    {% set cls = entity.__class__ %}
    {% set value = entity[name + '_meta']|default(default) %}
    {% if value in (None, '') and boolean %}{% set value = default %}{% endif %}
    {{ tag_out(cls, name, value, entity, default) }}
{%- endmacro %}

{% macro input(entity, name, placeholder = None, boolean = True, create = False) -%}
    {% set cls = entity.__class__ %}
    {% set info = cls[name]|default({}, True) %}
    {% set default = cls[name].get('initial', '') if create else '' %}
    {% set disabled = info.get('immutable', False) and not create %}
    {% set value = entity[name]|default(default) %}
    {% set error = errors[name] %}
    {% if value in (None, '') and boolean %}{% set value = '' %}{% endif %}
    {{ tag_input(cls, name, value, entity, error, disabled = disabled) }}
{%- endmacro %}

{% macro tag_out(cls, name, value, entity, default) -%}
    {% set meta = cls._solve(name) %}
    {% set is_default = value == default %}
    {% if meta == "reference" %}
        {% set info = cls[name] %}
        {% set type = info["type"] %}
        {% set target = type._target() %}
        {% set _value = entity[name] %}
        {% if _value and _value._id %}
            <a href="{{ url_for('admin.show_entity', model = target._name(), _id = _value._id) }}">{{ value }}</a>
        {% else %}
            <span>{{ default }}</span>
        {% endif %}
    {% elif meta == "references" %}
        {% set _value = entity[name] %}
        {% if _value %}
            {% set counter = [] %}
            {% for item in _value %}
                {% set model = item.resolve() %}
                {% if model != None %}
                    {% if counter|length > 0 %},{% endif %}
                    <a href="{{ url_for('admin.show_entity', model = model.__class__._name(), _id = item._id) }}">{{ item }}</a>
                    {% do counter.append(1) %}
                {% endif %}
            {% endfor %}
            {% if counter|length == 0 %}
                <span>{{ default }}</span>
            {% endif %}
        {% else %}
            <span>{{ default }}</span>
        {% endif %}
    {% elif meta == "enum" %}
        <span class="tag {{ value }}">{{ value }}</span>
    {% elif meta == "url" %}
        {% if is_default %}
            <span>{{ value }}</span>
        {% else %}
            <a href="{{ value }}">{{ value }}</a>
        {% endif %}
    {% elif meta == "email" %}
        <a href="mailto:{{ value }}">{{ value }}</a>
    {% elif meta == "longtext" %}
        {{ value[:60] + " ..." if value|length > 64 else value }}
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
        {% set _default = target.default()|default('name') %}
        {% set logic = value[_name]|default('') %}
        {% set display = value[_default]|default('') %}
        <div class="drop-field {{ disabled_s|safe }}" value="{{ display }}" data-error="{{ error }}"
             data-value_attribute="{{ _name }}" data-display_attribute="{{ _default }}" data-number_options="-1">
            <input type="hidden" class="hidden-field" name="{{ name }}" value="{{ logic }}" />
            <div class="data-source" data-type="json"
                 data-url="{{ url_for('admin.show_model_json', model = target._name() ) }}"></div>
        </div>
    {% elif meta == "references" %}
        {% set info = cls[name] %}
        {% set type = info["type"] %}
        {% set target = type._target() %}
        {% set _name = type._name %}
        {% set _default = target.default()|default('name') %}
        <div name="{{ name }}" class="tag-field {{ disabled_s|safe }}" data-error="{{ error }}"
             data-value_attribute="{{ _name }}" data-display_attribute="{{ _default }}" data-number_options="-1"
             data-auto_width="1">
            <ul class="tags">
                {% for item in value %}
                    {% set model = item.resolve() %}
                    {% set logic = item[_name]|default('') %}
                    {% set display = item[_default]|default('') %}
                    {% if model != None %}
                        <li data-value="{{ logic }}">{{ display }}</li>
                    {% endif %}
                {% endfor %}
            </ul>
            <div class="data-source" data-type="json"
                 data-url="{{ url_for('admin.show_model_json', model = target._name() ) }}"></div>
        </div>
    {% elif meta == "enum" %}
        {% set info = cls[name] %}
        {% set enum = info["enum"] %}
        <div class="drop-field drop-field-select {{ disabled_s|safe }}"
               data-error="{{ error }}" data-display_attribute="name"
               data-value_attribute="internal" data-number_options="-1">
            <input name="{{ name }}" type="hidden" class="hidden-field"
                   value="{{ value }}" />
            <ul class="data-source" data-type="local">
                {% for key, value in enum.items() %}
                    <li>
                        <span name="name">{{ value }}</span>
                        <span name="internal">{{ key }}</span>
                    </li>
                {% endfor %}
            </ul>
        </div>
    {% elif meta == "file" %}
        <input type="file" class="file-field {{ disabled_s|safe }}" name="{{ name }}"
               data-error="{{ error }}" />
    {% elif meta == "date" %}
        <input type="text" class="text-field {{ disabled_s|safe }}" name="{{ name }}" value="{{ value }}"
               data-type="date" data-error="{{ error }}" />
    {% elif meta == "datetime" %}
        <input type="text" class="text-field {{ disabled_s|safe }}" name="{{ name }}" value="{{ value }}"
               data-type="date" data-error="{{ error }}" />
    {% elif meta == "secret" %}
        <input type="password" class="text-field {{ disabled_s|safe }}" name="{{ name }}"
               value="{{ value }}" data-error="{{ error }}" />
    {% elif meta == "longtext" %}
        <textarea class="text-area {{ disabled_s|safe }}" name="{{ name }}"
                  data-error="{{ error }}">{{ value }}</textarea>
    {% elif meta == "bool" %}
        {% if value %}
            <input type="radio" name="{{ name }}" id="{{ name }}-1" value="1" checked="1" />
        {% else %}
            <input type="radio" name="{{ name }}" id="{{ name }}-1" value="1" />
        {% endif %}
        <label class="radio-label" for="{{ name }}-1">True</label>
        {% if value %}
            <input type="radio" name="{{ name }}" id="{{ name }}-0" value="0" />
        {% else %}
            <input type="radio" name="{{ name }}" id="{{ name }}-0" value="0" checked="1" />
        {% endif %}
        <label class="radio-label" for="{{ name }}-0">False</label>
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
