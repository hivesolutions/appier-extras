{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ model._readable() }}{% endblock %}
{% block name %}{{ model._readable() }}{% endblock %}
{% block content %}
    <div class="shortcuts">
        <div class="key" data-key="67" data-url="{{ url_for('admin.show_model', model = model._under()) }}"></div>
    </div>
    <form action="{{ url_for('admin.create_entity', model = model._under()) }}"
          enctype="multipart/form-data" method="post" class="form inline">
        <div class="section">
            {% for name in model.create_names() %}
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
                        {{ input(entity, name, create = True) }}
                    </div>
                </div>
            {% endfor %}
        </div>
        <div class="separator strong"></div>
        <div class="buttons">
            <span class="button button-color button-green" data-submit="true">
                <span class="base">Create</span>
                <span class="locked">Creating</span>
            </span>
            <span class="or">or</span>
            <span class="button button-color button-grey"
                  data-link="{{ url_for('admin.show_model', model = model._under()) }}">Cancel</span>
        </div>
    </form>
{% endblock %}
