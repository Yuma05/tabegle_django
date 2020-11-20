import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from api.models import Place


class Command(BaseCommand):
    def add_arguments(self, parser):
        help = 'Updates the place from CSV.'
        parser.add_argument('path', help='CSV file path.')

    def handle(self, *args, **options):
        try:
            new_places = pd.read_csv(options['path']).to_dict(orient='records')
        except FileNotFoundError:
            raise CommandError('File not found.')
        except Exception as e:
            raise CommandError(e)

        Place.objects.all().delete()
        with tqdm(new_places) as pbar:
            for new_place in pbar:
                pbar.postfix = new_place['name']
                Place.objects.create(name=new_place['name'], kana=new_place['kana'],
                                     place_code=new_place['place_code'])
