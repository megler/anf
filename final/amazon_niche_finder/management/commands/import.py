import csv
from django.core.management import BaseCommand
from amazon_niche_finder.models import Category


class Command(BaseCommand):
    help = "Load an Amazon categories csv file into the database"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["path"]

        with open(path, "rt") as f:
            reader = csv.reader(f, dialect="excel")
            next(reader)
            for row in reader:
                if int(row[2]) == 0:
                    obj = Category(
                        cat_id=int(row[0]),
                        cat_name=row[1],
                        cat_parent_id=int(row[2]),
                        cat_level=int(row[3]),
                        cat_link=row[4],
                    )
                    obj.save()
                else:
                    parent_id = Category.objects.get(cat_id=int(row[2]))
                    obj = Category(
                        cat_id=int(row[0]),
                        cat_name=row[1],
                        cat_parent_id=int(row[2]),
                        cat_level=int(row[3]),
                        cat_link=row[4],
                        parent=parent_id,
                    )
                    obj.save()
