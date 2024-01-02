{% extends "admin/email/macros.html.tpl" %}
{% block language %}en{% endblock %}
{% block background_color %}#edece4{% endblock %}
{% block font_color %}#4d4d4d{% endblock %}
{% block font_size %}14px{% endblock %}
{% block font_size_mobile %}{{ self.font_size() }}{% endblock %}
{% block font_family %}-apple-system,'BlinkMacSystemFont','Segoe UI','Open Sans',Helvetica,Arial,sans-serif{% endblock %}
{% block border %}1px solid #d9d9d9{% endblock %}
{% block line_height %}22px{% endblock %}
{% block content_width %}520px{% endblock %}
{% block body_css %}{% endblock %}
{% block extra_css %}{% endblock %}
{% block html %}
    <!DOCTYPE html>
    <html lang="{{ self.language() }}">
    <head>
        {% block head %}
            <title>{% block title %}{% endblock %}</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1, minimum-scale=1, maximum-scale=1" />
            <style type="text/css">
                {% block style %}
                    p {
                        color: {{ self.font_color() }};
                        font-family: {{ self.font_family() }};
                        font-size: {{ self.font_size() }};
                        line-height: {{ self.line_height() }};
                        margin: 14px 0px 14px 0px;
                    }

                    @media (max-width: 480px) {
                        body {
                            font-size: {{ self.font_size_mobile() }} !important;
                            background: #ffffff !important;
                            width: 100% !important;
                        }

                        p {
                            font-size: {{ self.font_size_mobile() }} !important;
                        }

                        .container {
                            padding: 0px 0px 0px 0px !important;
                        }

                        .block {
                            box-shadow: none !important;
                            box-sizing: border-box !important;
                            padding: 24px 12px 24px 12px !important;
                            width: 100% !important;
                        }
                    }
                {% endblock %}
            </style>
        {% endblock %}
    </head>
    <body style="font-family:{{ self.font_family() }};font-size:{{ self.font_size() }};line-height:{{ self.line_height() }};color:{{ self.font_color() }};text-align:left;padding:0px 0px 0px 0px;margin:0px 0px 0px 0px;{{ self.body_css() }}" bgcolor="{{ self.background_color() }}">
        {% block metadata %}{% endblock %}
        {% block container %}
            <div class="container" style="background-color:{{ self.background_color() }};margin:0px auto 0px auto;padding:48px 0px 48px 0px;" bgcolor="{{ self.background_color() }}">
                <div class="block" style="background-color:#ffffff;width:{{ self.content_width() }};margin:0px auto 0px auto;padding:42px 72px 42px 72px;border:{{ self.border() }};{{ self.extra_css() }}">
                    {% block logo %}
                        {% set logo_url = owner.logo_raster_url or owner.logo_url %}
                        {% if logo_url %}
                            <div class="logo" style="text-align:center;">
                                <img src="{{ logo_url|absolute_url }}" alt="logo" style="max-width:144px;" />
                            </div>
                        {% endif %}
                    {% endblock %}
                    {% block content_base %}
                        <div class="content">
                            {% set logo_url = owner.logo_raster_url or owner.logo_url %}
                            {% set margin_top = "18px" if logo_url else "38px" %}
                            {{ h1(self.title(), margin_top = margin_top) }}
                            {% block content %}{% endblock %}
                        </div>
                    {% endblock %}
                    {% block footer %}
                        <div class="footer" style="font-size:10px;line-height:16px;text-align:right;margin-top: 48px;">
                            {% set copyright = owner.copyright|default(copyright, True)|default("Hive Solutions", True) %}
                            {% set copyright_year = owner.copyright_year|default(copyright_year, True)|default("2008-2024", True) %}
                            &copy; {{ copyright_year }} {{ copyright }} &middot; {{ "All rights reserved"|locale }}<br/>
                        </div>
                    {% endblock %}
                </div>
            </div>
        {% endblock %}
    </body>
    </html>
{% endblock %}
