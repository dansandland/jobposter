from django.core.management.base import BaseCommand
import craigslist
from craigslist.models import ClCategory, ClArea
import yaml
import os
from django.conf import settings
import pprint
pp = pprint.PrettyPrinter(indent=4)

class Command(BaseCommand):
    args = ''
    help = 'Populates initial data for Craigslist Categories and Areas'

    def _create_categories(self):
        file_path = os.path.join(settings.BASE_DIR, 'craigslist/yaml/categories.yml')
        f = open(file_path)
        dataMap = yaml.safe_load(f)
        f.close()
        pp.pprint(dataMap)
        for key, value in dataMap.iteritems():
            if (key == 'Jobs'): # only Jobs
                for k, v in value.iteritems():
                    c = ClCategory.objects.filter(abbr__icontains=k)
                    if (c):
                        c.update(
                            abbr=k,
                            desc=v,
                            cl_type=key,
                        )
                    else:
                        ClCategory.objects.create(
                            abbr=k,
                            desc=v,
                            cl_type=key,
                        )
        print 'Populated CL Categories'

    def _create_areas(self):
        file_path = os.path.join(settings.BASE_DIR, 'craigslist/yaml/areas.yml')
        f = open(file_path)
        dataMap = yaml.safe_load(f)
        f.close()
        pp.pprint(dataMap)
        for key, value in dataMap.iteritems():
            for k, v in value.iteritems():
                if (k == 'desc'):
                    a = ClArea.objects.filter(abbr__icontains=key, desc__icontains=v, is_subarea=False)
                    if (a):
                        a.update(
                            abbr=key,
                            desc=v,
                            is_subarea=False,
                        )
                    else:
                        ClArea.objects.create(
                            abbr=key,
                            desc=v,
                            is_subarea=False,
                        )
                else: # subareas
                    a = ClArea.objects.filter(abbr__icontains=k, desc__icontains=v['desc'], is_subarea=True)
                    if (a):
                        a.update(
                            abbr=k,
                            desc=v['desc'],
                            parent_abbr=key,
                            is_subarea=True,
                        )
                    else:
                        a = ClArea.objects.create(
                            abbr=k,
                            desc=v['desc'],
                            parent_abbr=key,
                            is_subarea=True,
                        )

        print 'Populated CL Areas'

    def handle(self, *args, **options):
        self._create_categories()
        self._create_areas()