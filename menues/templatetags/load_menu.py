import logging

from django import template

from ..models import Menu

register = template.Library()
logger = logging.getLogger('django')


@register.inclusion_tag("menu.html", takes_context=True)
def load_menu(context, slug=None):
    if not slug:
        slug = context.get('slug')
    items_list = []
    try:
        parents = get_all_parents(slug)
        for parent in parents:
            items_list.append(parent)
    except Exception:
        logger.warning('cant get a list')
    return {
        "items": items_list,
    }


def get_all_parents(slug):
    table_name = Menu.objects.model._meta.db_table
    query = f'''
        WITH RECURSIVE parents AS (
            SELECT {table_name}.*, 0 AS relative_depth
            FROM {table_name}
            WHERE slug = %s

            UNION ALL

            SELECT {table_name}.*, parents.relative_depth - 1
            FROM {table_name},parents
            WHERE {table_name}.slug = parents.parent_id
        )
        SELECT slug, name, parent_id, relative_depth
        FROM parents
        UNION ALL
        SELECT {table_name}.*, 1 AS relative_depth
        FROM {table_name}
        WHERE parent_id = %s
        ORDER BY relative_depth;
    '''
    return Menu.objects.raw(query, (slug, slug))
