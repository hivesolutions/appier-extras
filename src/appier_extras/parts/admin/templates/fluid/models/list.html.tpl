{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Admin{% endblock %}
{% block name %}Site Administration{% endblock %}
{% block content %}
    <div>
        {% for section, models in own.admin_part.models_d.items() %}
            {% set available = own._available(models) %}
            {% if available|length > 0 %}
                <div class="panel-model">
                    <h3>{{ appier.underscore_to_readable(section, capitalize = True) }}</h3>
                    <ul>
                        {% for model in available %}
                            {% if acl("admin.models." + model._under()) %}
                                <li>
                                    <div class="left">
                                        <a class="name" href="{{ url_for('admin.show_model', model = model._under()) }}">{{ model._readable(plural = True) }}</a>
                                    </div>
                                    <div class="right">
                                        <span class="button create" data-link="{{ url_for('admin.new_entity', model = model._under()) }}">create</span>
                                        <span class="button update" data-link="{{ url_for('admin.show_model', model = model._under()) }}">update</span>
                                    </div>
                                    <div class="clear"></div>
                                </li>
                            {% endif %}
                        {% endfor %}
                    </ul>
                 </div>
             {% endif %}
        {% endfor %}
    </div>
{% endblock %}
