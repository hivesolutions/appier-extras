{% extends "admin/macros.html.tpl" %}
{% set layout_r = layout|default(own._hybrid('layout', '')) %}
{% set sub_layout_r = sub_layout|default(own._hybrid('sub_layout', '')) %}
{% set theme_r = theme|default(own._hybrid('theme', '')) %}
{% set style_r = style|default(own._hybrid('style', '')) %}
{% set libs_r = libs|default(own._hybrid('libs', '')) %}
