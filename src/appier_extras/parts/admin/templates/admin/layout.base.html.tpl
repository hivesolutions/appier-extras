{% extends "admin/macros.html.tpl" %}
{% set layout_r = layout|default(own.admin_part._hybrid('layout', '')) %}
{% set sub_layout_r = sub_layout|default(own.admin_part._hybrid('sub_layout', '')) %}
{% set theme_r = theme|default(own.admin_part._hybrid('theme', '')) %}
{% set style_r = style|default(own.admin_part._hybrid('style', '')) %}
{% set libs_r = libs|default(own.admin_part._hybrid('libs', '')) %}
