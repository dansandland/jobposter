import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobposter.settings") #Changed in DDS v.0.3

BOT_NAME = 'craigslist'

SPIDER_MODULES = ['dynamic_scraper.spiders', 'craigslist.scraper',]
USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')

#Scrapy 0.20+
ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'craigslist.scraper.pipelines.DjangoWriterPipeline': 800,
}

# #Scrapy up to 0.18
# ITEM_PIPELINES = [
#     'dynamic_scraper.pipelines.ValidationPipeline',
#     'craigslist.scraper.pipelines.DjangoWriterPipeline',
# ]