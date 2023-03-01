from django.db import models
from django.core.exceptions import ValidationError


class Menu(models.Model):
    slug = models.SlugField(
        verbose_name='URL',
        max_length=50,
        unique=True,
        primary_key=True
    )
    name = models.CharField(
        verbose_name='название',
        max_length=50
    )
    parent = models.ForeignKey(
        'Menu',
        verbose_name='родитель',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.name

    def clean(self):
        if self.slug == self.parent.slug:
            raise ValidationError('сам объект не может быть родителем')
        granpas = self.get_all_parents(self.parent.slug)
        for granpa in granpas:
            if granpa.slug == self.slug:
                raise ValidationError('объект в родителях у родителя')

    def get_all_parents(self, slug):
        table_name = Menu.objects.model._meta.db_table
        query = f'''
            WITH RECURSIVE parents AS (
                SELECT {table_name}.*
                FROM {table_name}
                WHERE slug = %s

                UNION ALL

                SELECT {table_name}.*
                FROM {table_name},parents
                WHERE {table_name}.slug = parents.parent_id
            )
            SELECT slug, name, parent_id
            FROM parents;
        '''
        return Menu.objects.raw(query, (slug,))
