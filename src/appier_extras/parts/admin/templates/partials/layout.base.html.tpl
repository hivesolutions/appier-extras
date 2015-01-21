{% extends "partials/macros.html.tpl" %}
{% set libs_r = session.libs or libs or own.libs %}
{% set theme_r = session.theme or theme or own.theme %}
{% set style_r = session.style or style or own.style %}
{% set sub_type_r = session.sub_type or sub_type or own.sub_type %}
