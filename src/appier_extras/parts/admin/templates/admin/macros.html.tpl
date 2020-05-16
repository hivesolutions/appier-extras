{% macro out(entity, name, boolean = True, default = "-") -%}
    {% set entity, name = entity._res_entity(name, rules = False, meta = True) %}
    {% set cls = entity.__class__ %}
    {% set meta_name = name + "_meta" %}
    {% set meta_name = meta_name if meta_name in entity else name %}
    {% set value = entity[meta_name]|default(default) %}
    {% set is_default = not meta_name in entity and not meta_name in entity.__dict__ and not meta_name in entity.__class__.__dict__ %}
    {% set is_default = is_default or (boolean and value in (None, "")) %}
    {% if is_default %}{% set value = default %}{% endif %}
    {{ tag_out(cls, name, value, entity, default, is_default = is_default) }}
{%- endmacro %}

{% macro input(entity, name, placeholder = None, boolean = True, create = False) -%}
    {% set entity, name = entity._res_entity(name, rules = False, meta = True) %}
    {% set cls = entity.__class__ %}
    {% set info = cls.definition_n(name) %}
    {% set default = info.get("initial", "") if create else "" %}
    {% set disabled = info.get("immutable", False) and not create %}
    {% set value = entity[name]|default(default) %}
    {% set error = errors[name] %}
    {% if value in (None, "") and boolean %}{% set value = "" %}{% endif %}
    {{ tag_input(cls, name, value, entity, error, disabled = disabled) }}
{%- endmacro %}

{% macro tag_out(cls, name, value, entity, default, is_default = False, acl_prefix = "admin.models" ) -%}
    {% set meta = cls._solve(name) %}
    {% if meta == "reference" %}
        {% set info = cls.definition_n(name) %}
        {% set type = info.type %}
        {% set target = type._target() %}
        {% set _value = entity[name] %}
        {% if _value and _value._id and acl(acl_prefix + "." + target._under()) %}
            <a href="{{ url_for('admin.show_entity', model = target._under(), _id = _value._id) }}">{{ value }}</a>
        {% else %}
            <span>{{ value }}</span>
        {% endif %}
    {% elif meta == "references" %}
        {% set _value = entity[name] %}
        {% if _value %}
            {% set counter = [] %}
            {% for item in _value %}
                {% set model = item.resolve() %}
                {% if not model == None %}
                    {% if counter|length > 0 %},{% endif %}
                    {% if acl(acl_prefix + "." + model._under()) %}
                        <a href="{{ url_for('admin.show_entity', model = model.__class__._under(), _id = item._id) }}">{{ item }}</a>
                    {% else %}
                        <span>{{ item }}</span>
                    {% endif %}
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
        {% set info = cls.definition_n(name) %}
        {% set colors = info.get("colors", {}) %}
        {% set color = colors.get(value, "") %}
        {% set value_r = appier.underscore_to_readable(value, capitalize = True) %}
        <span class="tag {{ value }} {{ color }}">{{ value_r }}</span>
    {% elif meta == "url" %}
        {% set info = cls.definition_n(name) %}
        {% set label = info.get("label", value) %}
        {% if is_default %}
            <span>{{ value }}</span>
        {% else %}
            <a href="{{ value }}" target="_blank">{{ label }}</a>
        {% endif %}
    {% elif meta == "email" %}
        {% if is_default %}
            <span>{{ value }}</span>
        {% else %}
            <a href="mailto:{{ value }}">{{ value }}</a>
        {% endif %}
    {% elif meta == "secret" %}
        <span class="secret">{{ value|length * "*" }}</span>
    {% elif meta == "longtext" %}
        {{ value[:60] + " ..." if value|length > 64 else value }}
    {% elif meta == "distance_km" %}
        <span>{{ "%.02f" % (value|float / 1000.0) }} Km</span>
    {% elif meta == "distance_m" %}
        <span>{{ "%.02f" % value|float }} M</span>
    {% elif meta == "time_h" %}
        <span>{{ "%.02f" % (value|float / 3600.0) }} H</span>
    {% elif meta == "time_m" %}
        <span>{{ "%.02f" % (value|float / 60.0) }} M</span>
    {% elif meta == "bool" %}
        <span class="tag {{ value.lower() }}">{{ value }}</span>
    {% elif meta == "image_url" %}
        {% if value and not is_default %}
            <img class="image lightbox-animated" src="{{ value }}" data-lightbox_path="{{ value }}" />
        {% else %}
            <span>{{ value }}</span>
        {% endif %}
    {% else %}
        <span>{{ value }}</span>
    {% endif %}
{%- endmacro %}

{% macro tag_input(cls, name, value, entity, error, disabled = False) -%}
    {% set meta = cls._solve(name) %}
    {% set disabled_s = "\" data-disabled=\"1" if disabled else "" %}
    {% if meta == "reference" %}
        {% set info = cls.definition_n(name) %}
        {% set type = info.type %}
        {% set target = type._target() %}
        {% set _name = type._name %}
        {% set _default = target.default()|default("name") %}
        {% set logic = value[_name]|default("") %}
        {% set display = value[_default]|default("") %}
        <div class="drop-field {{ disabled_s|safe }}" value="{{ display }}" data-error="{{ error }}"
             data-value_attribute="{{ _name }}" data-display_attribute="{{ _default }}" data-number_options="-1">
            <input type="hidden" class="hidden-field" name="{{ name }}" value="{{ logic|default('', True) }}" />
            <div class="data-source" data-type="json"
                 data-url="{{ url_for('admin.show_model_json', model = target._under() ) }}"></div>
        </div>
    {% elif meta == "references" %}
        {% set info = cls.definition_n(name) %}
        {% set type = info.type %}
        {% set target = type._target() %}
        {% set _name = type._name %}
        {% set _default = target.default()|default("name") %}
        <div name="{{ name }}" class="tag-field {{ disabled_s|safe }}" data-error="{{ error }}"
             data-value_attribute="{{ _name }}" data-display_attribute="{{ _default }}" data-number_options="-1"
             data-auto_width="1">
            <ul class="tags">
                {% for item in value %}
                    {% set model = item.resolve() %}
                    {% set logic = item[_name]|default("") %}
                    {% set display = item[_default]|default("") %}
                    {% if not model == None %}
                        <li data-value="{{ logic }}">{{ display }}</li>
                    {% endif %}
                {% endfor %}
            </ul>
            <div class="data-source" data-type="json"
                 data-url="{{ url_for('admin.show_model_json', model = target._under() ) }}"></div>
        </div>
    {% elif meta == "enum" %}
        {% set info = cls.definition_n(name) %}
        {% set enum = info.enum %}
        <div class="drop-field drop-field-select {{ disabled_s|safe }}"
             data-error="{{ error }}" data-display_attribute="name"
             data-value_attribute="internal" data-number_options="-1">
            <input name="{{ name }}" type="hidden" class="hidden-field"
                   value="{{ value|string if value in (True, False) else value|default('', True) }}" />
            <ul class="data-source" data-type="local">
                {% for key, value in enum.items() %}
                    {% set value_r = appier.underscore_to_readable(value, capitalize = True) %}
                    <li>
                        <span name="name">{{ value_r }}</span>
                        <span name="internal">{{ key }}</span>
                    </li>
                {% endfor %}
            </ul>
        </div>
    {% elif meta == "country" %}
         <div class="drop-field drop-field-select {{ disabled_s|safe }}" data-error="{{ error }}"
              data-number_options="-1">
            <input name="{{ name }}" type="hidden" class="hidden-field" value="{{ value|default('', True) }}" />
            <div class="data-source" data-type="isocountries" data-iso="iso2"></div>
        </div>
    {% elif meta == "file" %}
        <a data-name="{{ name }}" class="uploader {{ disabled_s|safe }}"
           data-error="{{ error }}">Select file</a>
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
    {% elif meta == "list" %}
        <input type="text" class="text-field {{ disabled_s|safe }}" name="{{ name }}"
               value="{{ value|dumps if value else '[]' }}" data-error="{{ error }}" />
    {% elif meta == "map" %}
        <input type="text" class="text-field {{ disabled_s|safe }}" name="{{ name }}"
               value="{{ value|dumps if value else '{}' }}" data-error="{{ error }}" />
    {% elif meta == "longmap" %}
        <textarea class="text-area {{ disabled_s|safe }}" name="{{ name }}"
                  data-error="{{ error }}">{{ value|dumps if value else "{}" }}</textarea>
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

{% macro tag_input_b(name, value = "", placeholder = "", error = "", type = None, disabled = False) -%}
    {% set disabled_s = "\" data-disabled=\"1" if disabled else "" %}
    {% set type_s = own.admin_part._to_meta(type) %}
    {% if type_s == "reference" %}
        {% set target = type._target() %}
        {% set _name = type._name %}
        {% set _default = target.default()|default("name") %}
        {% set logic = value[_name]|default("") %}
        {% set display = value[_default]|default("") %}
        <div class="drop-field {{ disabled_s|safe }}" value="{{ display }}" data-error="{{ error }}"
             data-value_attribute="{{ _name }}" data-display_attribute="{{ _default }}" data-number_options="-1">
            <input type="hidden" class="hidden-field" name="{{ name }}" value="{{ logic|default('', True) }}" />
            <div class="data-source" data-type="json"
                 data-url="{{ url_for('admin.show_model_json', model = target._under() ) }}"></div>
        </div>
    {% elif type_s == "file" %}
        <a data-name="{{ name }}" class="uploader" data-error="{{ error }}">Select file</a>
    {% elif type_s == "date" %}
        <input type="text" class="text-field" name="{{ name }}" value="{{ value }}"
               placeholder="{{ placeholder }}" data-type="date" data-error="{{ error }}" />
    {% elif type_s == "datetime" %}
        <input type="text" class="text-field" name="{{ name }}" value="{{ value }}"
               placeholder="{{ placeholder }}" data-type="date" data-error="{{ error }}" />
    {% elif type_s == "longtext" %}
        <textarea class="text-area" name="{{ name }}" data-error="{{ error }}">{{ value }}</textarea>
    {% elif type_s == "list" %}
        <input type="text" class="text-field" name="{{ name }}"
               value="{{ value|dumps if value else '[]' }}" placeholder="{{ placeholder }}"
               data-error="{{ error }}" />
    {% elif type_s == "map" %}
        <input type="text" class="text-field" name="{{ name }}"
               value="{{ value|dumps if value else '{}' }}" placeholder="{{ placeholder }}"
               data-error="{{ error }}" />
    {% elif type_s == "longmap" %}
        <textarea class="text-area" name="{{ name }}"
                  data-error="{{ error }}">{{ value|dumps if value else "{}" }}</textarea>
    {% elif type_s == "country" %}
        <div class="drop-field drop-field-select {{ disabled_s|safe }}" data-error="{{ error }}"
             data-number_options="-1">
            <input name="{{ name }}" type="hidden" class="hidden-field" />
            <div class="data-source" data-type="isocountries" data-iso="iso2"></div>
        </div>
    {% elif type_s == "bool" %}
        {% if value %}
            <input type="checkbox" class="check-field" name="{{ name }}"
                   data-checked="on" data-error="{{ error }}" />
        {% else %}
            <input type="checkbox" class="check-field" name="{{ name }}" data-error="{{ error }}" />
        {% endif %}
    {% else %}
        <input type="text" class="text-field" name="{{ name }}" value="{{ value }}"
               placeholder="{{ placeholder }}" data-error="{{ error }}" />
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
                <a href="{{ href }}" class="page other">{{ index }}</a>
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

{% macro paging_listers(items, model, page, view = None, names = None, id_name = "_id", selection = False) -%}
    {% set names = names or model.list_names() %}
    {% set _caller = caller %}
    <div class="listers">
        {% call(item, name) paging_cards(items, model, names = names, id_name = id_name) %}
            {{ _caller(item, name, mode = "card") }}
        {% endcall %}
        <table class="filter lister {% if selection %}bulk{% endif %}" data-no_input="1"
               data-size="{{ page.size }}" data-total="{{ page.total }}" data-pages="{{ page.count }}"
               data-view="{{ view|default('', True) }}">
            {{ paging_header(request, model, page, names = names, selection = selection) }}
            {% call(item, name) paging_body(items, names = names, id_name = id_name, selection = selection) %}
                {{ _caller(item, name, mode = "cell") }}
            {% endcall %}
        </table>
    </div>
    {% if page.count > 1 %}
        {{ paging(page.index, page.count, caller = page.query) }}
    {% endif %}
{%- endmacro %}

{% macro paging_cards(items, model, names = None, id_name = "_id") -%}
    {% set names = names or model.list_names() %}
    <div class="cards lister">
        {% for item in items %}
            <div class="card" data-id="{{ item[id_name]|default('', True) }}">
                <dl>
                    {% for name in names %}
                        {% if caller %}
                            {{ caller(item, name) }}
                        {% else %}
                            {% set description = model.to_description(name) %}
                            <div class="item">
                                <dt>{{ description }}</dt>
                                <dd>{{ item[name] }}</dd>
                            </div>
                        {% endif %}
                    {% endfor %}
                </dl>
            </div>
        {% endfor %}
    </div>
{%- endmacro %}

{% macro paging_header(items, model, page, names = None, selection = False) -%}
    {% set names = names or model.list_names() %}
    <thead>
        <tr class="table-row table-header">
            {% if selection %}
                <th class="text-left selection">
                    <input type="checkbox" class="square small" />
                </th>
            {% endif %}
            {% for name in names %}
                {% set description = model.to_description(name) %}
                {% if name == page.sorter %}
                    <th class="text-left direction {{ page.direction }}">
                        <a href="{{ page.query(sorter = name) }}">{{ description }}</a>
                    </th>
                {% else %}
                    <th class="text-left">
                        <a href="{{ page.query(sorter = name) }}">{{ description }}</a>
                    </th>
                {% endif %}
            {% endfor %}
        </tr>
    </thead>
{%- endmacro %}

{% macro paging_body(items, names = None, id_name = "_id", selection = False) -%}
    {% set names = names or model.list_names() %}
    <tbody class="filter-contents">
        {% for item in items %}
            <tr class="table-row" data-id="{{ item[id_name]|default('', True) }}">
                {% if selection %}
                    <td class="text-left selection">
                        <input type="checkbox" class="square small" />
                    </td>
                {% endif %}
                {% for name in names %}
                    {% if caller %}
                        {{ caller(item, name) }}
                    {% else %}
                        <td class="text-left">{{ item[name] }}</td>
                    {% endif %}
                {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
{%- endmacro %}

{% macro paging_item(name, value = None, alignment = "left", mode = "card") -%}
    {% set _caller = caller %}
    {% if mode == "card" %}
        {% if _caller %}
            {% call paging_card(name, value = value) %}
                {{ _caller() }}
            {% endcall %}
        {% else %}
            {{ paging_card(name, value = value) }}
        {% endif %}
    {% endif %}
    {% if mode == "cell" %}
        {% if _caller %}
            {% call paging_cell(value = value, alignment = alignment) %}
                {{ _caller() }}
            {% endcall %}
        {% else %}
            {{ paging_cell(value = value, alignment = alignment) }}
        {% endif %}
    {% endif %}
{%- endmacro %}

{% macro paging_card(name, value = None) -%}
    <div class="item">
        <dt>{{ name }}</dt>
        <dd>
            {% if caller %}
                {{ caller() }}
            {% else %}
                {{ value }}
            {% endif %}
        </dd>
    </div>
{%- endmacro %}

{% macro paging_cell(value = None, alignment = "left") -%}
    <td class="text-{{ alignment }}">
        {% if caller %}
            {{ caller() }}
        {% else %}
            {{ value }}
        {% endif %}
    </td>
{%- endmacro %}

{% macro build_hashtags(hashtags) -%}{% set hashtags_f = "" %}{% for hashtag in hashtags %}#{{ hashtag }}{% if not loop.last %} {% endif %}{% endfor %}{%- endmacro %}

{% macro facebook_share(url, app_id = None, display = "page", prefix = "https://www.facebook.com/dialog/share") -%}{{ prefix }}?app_id={{ quote(app_id|default("", True)) }}&href={{ quote(url) }}&display={{ quote(display) }}{%- endmacro %}

{% macro twitter_share(url, description = None, hashtags = None, prefix = "https://www.twitter.com/share") -%}{{ prefix }}?url={{ quote(url) }}&text={{ quote(description|default("", True)) }}&hashtags={{ quote(",".join(hashtags) if hashtags else "") }}{%- endmacro %}

{% macro pinterest_share(url, image_url = None, description = None, hashtags = None, prefix = "https://pinterest.com/pin/create/button") -%}{% set description = (description or "") + " " + build_hashtags(hashtags) if hashtags else description %}{{ prefix }}?url={{ quote(url) }}&media={{ quote(image_url) }}&description={{ quote(description|default("", True)) }}{%- endmacro %}

{% macro whatsapp_share(url, description = None, prefix = "whatsapp://send") -%}{% set text = (description + " " if description else "") + url %}{{ prefix }}?text={{ quote(text) }}{%- endmacro %}

{% block html %}{% endblock %}
