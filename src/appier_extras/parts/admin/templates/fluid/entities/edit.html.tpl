{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ entity }}{% endblock %}
{% block name %}
    {% if own._is_available(model) %}
        <a href="{{ url_for('admin.show_model', model = model._under()) }}">
            {{ model._readable(plural = True) }}
        </a>
    {% else %}
        <span>{{ model._readable(plural = True) }}</span>
    {% endif %}
    <span>/</span>
    <span>{{ entity }}</span>
{% endblock %}
{% block buttons %}
    {{ super() }}
    <div class="button button-color button-red button-confirm" data-link="{{ url_for('admin.delete_entity', model = model._under(), _id = entity._id) }}"
         data-message="Do you really want to delete [{{ entity }}] ?">Delete</div>
{% endblock %}
{% block content %}
    <div class="shortcuts">
        <div class="key" data-key="67" data-url="{{ url_for('admin.show_entity', model = model._under(), _id = entity._id) }}"></div>
    </div>
    <form action="{{ url_for('admin.update_entity', model = model._under(), _id = entity._id) }}"
          enctype="multipart/form-data" method="post" class="form inline">
        <div class="section">
            {% for name in model.update_names() %}
                {% set description = model.to_description(name) %}
                {% set observations = model.to_observations(name) %}
                <div class="item">
                    <div class="label">
                        {% if observations %}
                            <div class="balloon balloon-observations">
                                <label class="baloon-icon">{{ description }}</label>
                                <div class="balloon-contents">{{ observations|sentence|markdown }}</div>
                            </div>
                        {% else%}
                            <label>{{ description }}</label>
                        {% endif %}
                    </div>
                    <div class="input">
                        {{ input(entity, name) }}
                    </div>
                </div>
            {% endfor %}
        </div>
        <div class="separator strong"></div>
        <div class="buttons">
            <span class="button button-color button-green" data-submit="true">Update</span>
            <span class="or">or</span>
            <span class="button button-color button-grey"
                  data-link="{{ url_for('admin.show_entity', model = model._under(), _id = entity._id) }}">Cancel</span>
        </div>
    </form>
{% endblock %}
