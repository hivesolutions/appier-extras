{% set theme_r = theme|default(own.admin_part._hybrid('theme')) %}
{% set libs_r = libs|default(own.admin_part._hybrid('libs')) %}

<!-- css inclusion -->
<link rel="stylesheet" type="text/css" href="//libs.bemisc.com/uxf/css/ux-min.css" />
{% if theme_r %}
    {% if theme_r == 'default' %}
        <link rel="stylesheet" type="text/css" href="//libs.bemisc.com/layout/css/layout.css" />
    {% elif theme_r == 'modern' %}
        <link rel="stylesheet" type="text/css" href="//libs.bemisc.com/layout/css/layout.modern.css" />
    {% elif theme_r == 'webook' %}
        <link rel="stylesheet" type="text/css" href="//libs.bemisc.com/layout/css/layout.webook.css" />
    {% endif %}
{% else %}
    <link rel="stylesheet" type="text/css" href="//libs.bemisc.com/layout/css/layout.modern.css" />
{% endif %}
<link rel="stylesheet" type="text/css" href="//libs.bemisc.com/layout/css/layout.extras.css" />
<link rel="stylesheet" type="text/css" href="//libs.bemisc.com/layout/css/layout.data.css" />
<link rel="stylesheet" type="text/css" href="{{ url_for('admin', filename = 'css/layout.css') }}" />

<!-- favicon inclusion -->
<link rel="shortcut icon" href="{{ url_for('admin', filename = 'images/favicon.ico') }}" />

<!-- javascript inclusion -->
{% if libs_r == "legacy" %}
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
{% elif libs_r == "next" %}
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
{% elif libs_r == "edge" %}
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
{% else %}
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
{% endif %}
<script type="text/javascript" src="//libs.bemisc.com/uxf/js/ux-min.js"></script>
<script type="text/javascript" src="//libs.bemisc.com/layout/js/layout.js"></script>
<script type="text/javascript" src="{{ url_for('admin', filename = 'js/main.js') }}"></script>
