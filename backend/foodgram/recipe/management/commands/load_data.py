import csv

from django.core.management.base import BaseCommand

from recipe.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в БД'

    def handle(self, *args, **options):
        with open('../../data/ingredients.csv') as file:
            file_data = csv.reader(file)
            for item in file_data:
                name, unit = item
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=unit
                )
