{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Database Import{% endblock %}
{% block name %}Database Import{% endblock %}
{% block content %}
    <div class="flow-content">
        <div class="quote">
            Please provide the file containing the database data to be imported
            to the data source.<br/>
            Remember this is a <strong>dangerous operation</strong>.
        </div>
        <div class="separator-horizontal"></div>
        <div class="quote error">
            {{ error }}
        </div>
        <form enctype="multipart/form-data" action="{{ url_for('admin.database_import_do') }}"
              method="post" class="form small">
            <div class="input">
                 <a data-name="import_file" class="uploader">Select & Upload the import file</a>
            </div>
            <div class="buttons">
                <span class="button button-color button-green" data-submit="true">Upload</span>
                <span class="or">or</span>
                <span class="button button-color button-grey"
                      data-link="{{ url_for('admin.database') }}">Cancel</span>
            </div>
        </form>
    </div>
{% endblock %}
