{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ model._name() }}{% endblock %}
{% block name %}{{ model._name() }}{% endblock %}
{% block content %}
    <form action="{{ url_for('admin.create_entity', model = model._name()) }}"
          enctype="multipart/form-data" method="post" class="form inline">
        <div class="section">
            {% for name in model.create_names() %}
                <div class="item">
                    <div class="label">
                        <label>{{ name }}</label>
                    </div>
                    <div class="input">
                        {{ input(entity, name, create = True) }}
                    </div>
                </div>
            {% endfor %}
        </div>
        <div class="separator strong"></div>
        <div class="buttons">
            <span class="button button-color button-green" data-submit="true">Create</span>
            <span class="or">or</span>
            <span class="button button-color button-grey"
                  data-link="{{ url_for('admin.show_model', model = model._name()) }}">Cancel</span>
        </div>
    </form>
{% endblock %}
