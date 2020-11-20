import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from api.models import Category


class Command(BaseCommand):
    def add_arguments(self, parser):
        help = 'Updates the category from CSV.'
        parser.add_argument('path', help='CSV file path.')

    def handle(self, *args, **options):
        try:
            new_categories = pd.read_csv(options['path']).to_dict(orient='records')
        except FileNotFoundError:
            raise CommandError('File not found.')
        except Exception as e:
            raise CommandError(e)

        Category.objects.all().delete()
        with tqdm(new_categories) as pbar:
            for new_category in pbar:
                pbar.postfix = new_category['name']
                Category.objects.create(name=new_category['name'], kana=new_category['kana'],
                                        category_code=new_category['category_code'])
