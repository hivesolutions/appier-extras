{% extends "admin/email/macros.html.tpl" %}
{% block html %}
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        {% block head %}
            <title>{% block title %}{% endblock %}</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        {% endblock %}
    </head>
    <body style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:#4d4d4d;text-align:left;padding:0px 0px 0px 0px;margin:0px 0px 0px 0px;" bgcolor="#edece4">
        <div class="container" style="background-color:#edece4;margin:0px auto 0px auto;padding:48px 0px 48px 0px;" bgcolor="#edece4">
            <div style="background-color:#ffffff;width:520px;margin:0px auto 0px auto;padding:42px 72px 42px 72px;border:1px solid #d9d9d9;">
            	{% block logo %}{% endblock %}
                <div class="content">
                    {{ h1(self.title()) }}
                    {% block content %}{% endblock %}
                </div>
                <div class="footer" style="font-size:10px;line-height:16px;text-align:right;margin-top: 48px;">
                    &copy; {{ owner.copyright|default(copyright, True)|default("2014-2016 Hive Solutions", True) }} &middot; {{ "All rights reserved"|locale }}<br/>
                </div>
            </div>
        </div>
    </body>
    </html>
{% endblock %}
