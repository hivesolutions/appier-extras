{% extends "partials/macros.html.tpl" %}
{% set layout_r = session.layout or layout or own.layout %}
{% set sub_layout_r = session.sub_layout or sub_layout or own.sub_layout %}
{% set theme_r = session.theme or theme or own.theme %}
{% set style_r = session.style or style or own.style %}
{% set libs_r = session.libs or libs or own.libs %}
