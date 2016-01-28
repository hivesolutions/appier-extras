{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ entity }}{% endblock %}
{% block name %}{{ entity }}{% endblock %}
{% block buttons %}
    {{ super() }}
    <div class="button button-color button-red button-confirm" data-link="{{ url_for('admin.delete_entity', model = model._name(), _id = entity._id) }}"
         data-message="Do you really want to delete [{{ entity }}] ?">Delete</div>
{% endblock %}
{% block content %}
    <form action="{{ url_for('admin.update_entity', model = model._name(), _id = entity._id) }}"
          enctype="multipart/form-data" method="post" class="form inline">
        <div class="section">
            {% for name in model.update_names() %}
                <div class="item">
                    <div class="label">
                        <label>{{ name }}</label>
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
                  data-link="{{ url_for('admin.show_entity', model = model._name(), _id = entity._id) }}">Cancel</span>
        </div>
    </form>
{% endblock %}
