{% macro drop_relation(relation) -%}
    {{ return(adapter.dispatch('drop_relation', 'dbt')(relation)) }}
{% endmacro %}

{% macro default__drop_relation(relation) -%}
    {% call statement('drop_relation', auto_begin=False) -%}
        {%- if relation.is_table -%}
            {{- drop_table(relation) -}}
        {%- elif relation.is_view -%}
            {{- drop_view(relation) -}}
        {%- elif relation.is_materialized_view -%}
            {{- drop_materialized_view(relation) -}}
        {%- else -%}
            drop {{ relation.type }} if exists {{ relation }} cascade
        {%- endif -%}
    {%- endcall %}
{% endmacro %}


{% macro drop_table(relation) -%}
  {{ return(adapter.dispatch('drop_table', 'dbt')(relation)) }}
{%- endmacro %}

{% macro default__drop_table(relation) -%}
    drop table if exists {{ relation }} cascade
{%- endmacro %}


{% macro drop_view(relation) -%}
  {{ return(adapter.dispatch('drop_view', 'dbt')(relation)) }}
{%- endmacro %}

{% macro default__drop_view(relation) -%}
    drop view if exists {{ relation }} cascade
{%- endmacro %}


{% macro drop_relation_sql(relation_config) -%}
    {{ return(adapter.dispatch('drop_relation_sql', 'dbt')(relation_config)) }}
{%- endmacro %}

{%- macro default__drop_relation_sql(relation_config) -%}
    {%- if relation_config.relation_type == adapter.Relation.MaterializedView -%}
        {{- drop_materialized_view_sql(relation_config) -}}
    {%- else -%}
        drop {{ relation_config.relation_type }} if exists {{ relation_config.fully_qualified_path }} cascade
    {%- endif -%}
{%- endmacro -%}
