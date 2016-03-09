from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime
# from dynamic_scraper.models import Scraper, SchedulerRuntime
# from scrapy.contrib.djangoitem import DjangoItem

# class NewsWebsite(models.Model):
#     name = models.CharField(max_length=200)
#     url = models.URLField()
#     scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
#     scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

#     def __unicode__(self):
#         return self.name

# class Article(models.Model):
#     title = models.CharField(max_length=200)
#     news_website = models.ForeignKey(NewsWebsite)
#     description = models.TextField(blank=True)
#     url = models.URLField()
#     checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

#     def __unicode__(self):
#         return self.title

# class ArticleItem(DjangoItem):
#     django_model = Article

# cl categories
class ClCategory(models.Model):
    abbr = models.CharField(max_length=3)
    desc = models.CharField(max_length=255)
    cl_type = models.CharField(max_length=50)

# cl areas
class ClArea(models.Model):
    abbr = models.CharField(max_length=3)
    desc = models.CharField(max_length=255)
    parent_abbr = models.CharField(max_length=3, default='')
    is_subarea = models.BooleanField(default=False)
    is_active_market = models.BooleanField(default=False)
    is_paid_market = models.BooleanField(default=False)
    paid_market_price = models.IntegerField(default=0)

# template data for pre-filling job ads
class PostingTemplate(models.Model):
    # see: http://www.craigslist.org/about/bulk_posting_interface
    title = models.TextField()
    description = models.TextField()
    cl_category = models.ForeignKey(ClCategory)
    cl_area = models.ForeignKey(ClArea)
    # cl:reply_email
    cl_reply_email_value = models.TextField()
    cl_reply_email_privacy = models.TextField()
    cl_reply_email_outside_contact_ok = models.BooleanField()
    cl_reply_email_other_contact_info = models.TextField()
    # cl:image
    cl_image_value = models.TextField() # Base 64 Encoded
    cl_image_position = models.IntegerField() # 0-23 (0 is displayed in search results)
    cl_subarea = models.TextField()
    cl_neighborhood = models.TextField()
    cl_price = models.IntegerField()
    # cl:map_location
    cl_map_location_city = models.TextField()
    cl_map_location_state = models.TextField()
    cl_map_location_postal = models.TextField()
    cl_map_location_cross_street_1 = models.TextField()
    cl_map_location_cross_street_2 = models.TextField()
    cl_map_location_latitude = models.FloatField()
    cl_map_location_longitude = models.FloatField()
    cl_map_po_number = models.TextField()
    # cl:job_info
    cl_job_info_compensation = models.TextField()
    cl_job_info_telecommuting = models.BooleanField()
    cl_job_info_part_time = models.BooleanField()
    cl_job_info_contract = models.BooleanField()
    cl_job_info_nonprofit = models.BooleanField()
    cl_job_info_internship = models.BooleanField()
    cl_job_info_disability = models.BooleanField()
    cl_job_info_recruiters_ok = models.BooleanField()
    cl_job_info_phone_calls_ok = models.BooleanField()
    cl_job_info_ok_to_contact = models.BooleanField()
    cl_job_info_ok_to_repost = models.BooleanField()
    # cl:generic
    cl_generic_contact_name = models.TextField()
    cl_generic_contact_ok = models.BooleanField()
    cl_generic_contact_phone = models.TextField()
    cl_generic_contact_phone_extension = models.TextField()
    cl_generic_contact_phone_ok = models.BooleanField()
    cl_generic_contact_text_ok = models.BooleanField()
    cl_generic_fee_disclosure = models.TextField()
    cl_generic_has_license = models.BooleanField()
    cl_generic_license_info = models.TextField()
    cl_generic_repost_of = models.IntegerField()
    cl_generic_repost_ok = models.BooleanField()
    cl_generic_see_my_other = models.BooleanField()
    # cl:job_basics
    cl_job_basics_company_name = models.TextField()
    cl_job_basics_disability_ok = models.BooleanField()
    cl_job_basics_employment_type = models.TextField()
    cl_job_basics_is_contract = models.BooleanField()
    cl_job_basics_is_forpay = models.BooleanField()
    cl_job_basics_is_internship = models.BooleanField()
    cl_job_basics_is_nonprofit = models.BooleanField()
    cl_job_basics_is_parttime = models.BooleanField()
    cl_job_basics_is_telecommuting = models.BooleanField()
    cl_job_basics_recruiters_ok = models.BooleanField()
    cl_job_basics_remuneration = models.TextField()

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

# actual post
class Posting(models.Model):

    # foreign keys
    defaults = models.ForeignKey(PostingTemplate)
    cl_category = models.ForeignKey(ClCategory)
    cl_area = models.ForeignKey(ClArea)

    # non cl values
    is_active = models.BooleanField(default=True)
    tracking_url = models.TextField() # https://get.rideshare.com/cl/?utm_source=craigslist&utm_campaign=Craigslist_1_1_US-San-Francisco-peninsula_D_DSK_ACQ_fix_en_paidmarket_130_HOD-11_nokey&utm_medium=Fall-3_wheel-girl_E201511_SULCL
    paid_posting = models.BooleanField(default=True)
    posting_price = models.IntegerField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # cl values see: http://www.craigslist.org/about/bulk_posting_interface
    title = models.TextField() # TODO add title template relation
    description = models.TextField() # TODO add description template relation
    # cl:reply_email
    cl_reply_email_value = models.TextField()
    cl_reply_email_privacy = models.TextField()
    cl_reply_email_outside_contact_ok = models.BooleanField()
    cl_reply_email_other_contact_info = models.TextField()
    # cl:image
    cl_image_value = models.TextField() # Base 64 Encoded
    cl_image_position = models.IntegerField() # 0-23 (0 is displayed in search results)
    cl_subarea = models.TextField()
    cl_neighborhood = models.TextField()
    cl_price = models.IntegerField()
    # cl:map_location
    cl_map_location_city = models.TextField()
    cl_map_location_state = models.TextField()
    cl_map_location_postal = models.TextField()
    cl_map_location_cross_street_1 = models.TextField()
    cl_map_location_cross_street_2 = models.TextField()
    cl_map_location_latitude = models.FloatField()
    cl_map_location_longitude = models.FloatField()
    cl_map_po_number = models.TextField()
    # cl:job_info
    cl_job_info_compensation = models.TextField()
    cl_job_info_telecommuting = models.BooleanField()
    cl_job_info_part_time = models.BooleanField()
    cl_job_info_contract = models.BooleanField()
    cl_job_info_nonprofit = models.BooleanField()
    cl_job_info_internship = models.BooleanField()
    cl_job_info_disability = models.BooleanField()
    cl_job_info_recruiters_ok = models.BooleanField()
    cl_job_info_phone_calls_ok = models.BooleanField()
    cl_job_info_ok_to_contact = models.BooleanField()
    cl_job_info_ok_to_repost = models.BooleanField()
    # cl:generic
    cl_generic_contact_name = models.TextField()
    cl_generic_contact_ok = models.BooleanField()
    cl_generic_contact_phone = models.TextField()
    cl_generic_contact_phone_extension = models.TextField()
    cl_generic_contact_phone_ok = models.BooleanField()
    cl_generic_contact_text_ok = models.BooleanField()
    cl_generic_fee_disclosure = models.TextField()
    cl_generic_has_license = models.BooleanField()
    cl_generic_license_info = models.TextField()
    cl_generic_repost_of = models.IntegerField()
    cl_generic_repost_ok = models.BooleanField()
    cl_generic_see_my_other = models.BooleanField()
    # cl:job_basics
    cl_job_basics_company_name = models.TextField()
    cl_job_basics_disability_ok = models.BooleanField()
    cl_job_basics_employment_type = models.TextField()
    cl_job_basics_is_contract = models.BooleanField()
    cl_job_basics_is_forpay = models.BooleanField()
    cl_job_basics_is_internship = models.BooleanField()
    cl_job_basics_is_nonprofit = models.BooleanField()
    cl_job_basics_is_parttime = models.BooleanField()
    cl_job_basics_is_telecommuting = models.BooleanField()
    cl_job_basics_recruiters_ok = models.BooleanField()
    cl_job_basics_remuneration = models.TextField()


# Posting strategy algorithm
# Determine most efficient posting strategy
# Posting factors:
#  - Unique frequency (ad/location/category every 48 hours is CL's "requirement")
#  - Distribution over time


