{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Status{% endblock %}
{% block name %}Status{% endblock %}
{% block style %}no-header{% endblock %}
{% block content %}
    {% set models_c = own._administrable(own.models_r)|length %}
    {% set routes_c = own.info_dict().routes %}
    {% set configs_c = own.info_dict().configs %}
    {% set parts_c = own.info_dict().parts|length %}
    {% set libaries_c = own.info_dict().libraries|length %}
    {% set sessions_c = request.session_c.count() %}
    {% set peers_c = own._peers|length %}
    {% set counters_c = own._counters().count() %}
    {% set cron_jobs_c = own._cron_jobs_count() %}
    <div class="show-panel">
        <div class="panel-header">
            <img class="image square no-border" src="{{ own.logo_square_url or url_for('admin', filename = 'images/logo_96.png') }}" />
            <div class="buttons">
                {{ self.buttons() }}
            </div>
            <div class="details">
                <h2>{{ owner.description }}{% if owner.version %} {{ owner.version }}{% endif %}</h2>
                {% if owner.observations %}
                    <h3>{{ owner.observations }}</h3>
                {% endif %}
            </div>
        </div>
        <div class="panel-contents">
            <dl class="inline">
                <div class="item">
                    <dt>Name</dt>
                    <dd>{{ own.info_dict().name }}</dd>
                </div>
                <div class="item">
                    <dt>Instance</dt>
                    <dd>{{ own.info_dict().instance|default("global", True) }}</dd>
                </div>
                <div class="item">
                    <dt>Uptime</dt>
                    <dd>{{ own.info_dict().uptime }}</dd>
                </div>
                <div class="item">
                    <dt>Platform</dt>
                    <dd>{{ own.info_dict().platform |default("-", True) }}</dd>
                </div>
                <div class="item">
                    <dt>Server</dt>
                    <dd>{{ own.info_dict().server|default("-", True) }} {{ own.info_dict().server_version|default("", True) }}</dd>
                </div>
                <div class="item">
                    <dt>Appier</dt>
                    <dd>{{ own.info_dict().appier }}</dd>
                </div>
                <div class="item">
                    <dt>Models</dt>
                    <dd>{{ models_c }} {% if models_c == 1 %}model{% else %}models{% endif %}</dd>
                </div>
                <div class="item">
                    <dt>Routes</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_routes') }}">{{ routes_c }} {% if routes_c == 1 %}route{% else %}routes{% endif %}</a>
                    </dd>
                </div>
                <div class="item">
                    <dt>Configuration</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_configs') }}">{{ configs_c }} {% if configs_c == 1 %}item{% else %}items{% endif %}</a>
                    </dd>
                </div>
                <div class="item">

                    <dt>Parts</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_parts') }}">{{ parts_c }} {% if parts_c == 1 %}part{% else %}parts{% endif %}</a>
                    </dd>
                </div>
                <div class="item">
                    <dt>Libraries</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_libraries') }}">{{ libaries_c }} {% if libaries_c == 1 %}library{% else %}libraries{% endif %}</a>
                    </dd>
                </div>
                <div class="separator"></div>
                <div class="item">
                    <dt>Session class</dt>
                    <dd>{{ request.session_c.__name__ }}</dd>
                </div>
                <div class="item">
                    <dt>Session count</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_sessions') }}">{{ sessions_c }} {% if sessions_c == 1 %}session{% else %}sessions{% endif %}</a>
                    </dd>
                </div>
                <div class="item">
                    <dt>Peers</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_peers') }}">{{ peers_c }} {% if peers_c == 1 %}peer{% else %}peers{% endif %}</a>
                    </dd>
                </div>
                <div class="item">
                    <dt>Counters</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_counters') }}">{{ counters_c }} {% if counters_c == 1 %}counter{% else %}counters{% endif %}</a>
                    </dd>
                </div>
                <div class="item">
                    <dt>Cron Jobs</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_cron_jobs') }}">{{ cron_jobs_c }} {% if cron_jobs_c == 1 %}job{% else %}jobs{% endif %}</a>
                    </dd>
                </div>
                <div class="item">
                    <dt>Cache class</dt>
                    <dd>{{ own.cache_c.__name__ }}</dd>
                </div>
                <div class="item">
                    <dt>Preferences class</dt>
                    <dd>{{ own.preferences_c.__name__ }}</dd>
                </div>
                <div class="item">
                    <dt>Bus class</dt>
                    <dd>{{ own.bus_c.__name__ }}</dd>
                </div>
                <div class="item">
                    <dt>Adapter class</dt>
                    <dd>{{ own.adapter.__class__.__name__ }}</dd>
                </div>
                <div class="item">
                    <dt>Manager class</dt>
                    <dd>{{ own.manager.__class__.__name__ }}</dd>
                </div>
                {% if appier.Git.is_git() %}
                    <div class="separator"></div>
                    <div class="item">
                        <dt>Branch</dt>
                        <dd>{{ appier.Git.get_branch() }}</dd>
                    </div>
                    <div class="item">
                        <dt>Commit</dt>
                        <dd>{{ appier.Git.get_commit() }}</dd>
                    </div>
                    <div class="item">
                        <dt>Origin</dt>
                        <dd>{{ appier.Git.get_origin() }}</dd>
                    </div>
                {% endif %}
            </dl>
        </div>
    </div>
{% endblock %}
