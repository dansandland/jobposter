from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from django_tools.middlewares import ThreadLocal


def index(request):
    cl_email = request.session.get('cl_email')
    cl_password = request.session.get('cl_password')
    cl_id = request.session.get('cl_id')
    show_job_post_form = True
    if len(cl_id) == 0 :
        cl_id = '?'
        show_job_post_form = False

    context = {
        'cl_email': cl_email,
        'cl_password': cl_password,
        'cl_id': cl_id,
        'show_job_post_form': show_job_post_form
    }
    return render(request, 'craigslist/index.html', context)


# verify email/password and retrieve account id
def verify_auth(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')

    # log into cl

    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    base_url = "https://accounts.craigslist.org/"
    verificationErrors = []
    accept_next_alert = True
    driver.get(base_url + "/login?rt=L&amp;rp=%2Flogin%2Fhome")
    driver.find_element_by_id("inputEmailHandle").clear()
    driver.find_element_by_id("inputEmailHandle").send_keys(email) # danzhizhi
    driver.find_element_by_id("inputPassword").clear()
    driver.find_element_by_id("inputPassword").send_keys(password)
    driver.find_element_by_css_selector("button[type=\"submit\"]").click()

    # check for "Please try again" (authentication failed)
    try:
        driver.implicitly_wait(0)
        error = driver.find_element_by_css_selector(".error")
        # error = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.error')))
        error_text = error.text
        if (error.is_displayed()):
            driver.implicitly_wait(0)
            driver.quit()
            return JsonResponse({ 'success':False, 'error': error_text })
    except TimeoutException:
        pass
    except NoSuchElementException:
        pass
    finally:
        pass

    driver.implicitly_wait(10)
    driver.find_element_by_link_text("billing").click()

    try:
        driver.implicitly_wait(1)
        no_account = driver.find_elements_by_xpath("//*[contains(text(), 'No paid posting accounts exist.')]")
        if (no_account):
            driver.implicitly_wait(0)
            driver.quit()
            return JsonResponse({ 'success':False, 'error': 'No paid posting accounts exist.' })
    except TimeoutException:
        pass

    account_id = driver.find_element_by_xpath("//*[@id='pagecontainer']/section/fieldset/table/tbody/tr[3]/td[1]/small").text
    account_id = re.sub("\D", "", account_id)
    driver.implicitly_wait(0)
    driver.quit()

    request.session['cl_email'] = email
    request.session['cl_password'] = password

    # validate account id
    if (account_id.isdigit() and len(account_id) > 0):
        
        # save in session
        request.session['cl_id'] = account_id
        return JsonResponse({ 'success':True, 'account_id': account_id })

    else:

        return JsonResponse({ 'success':False, 'account_id': account_id, 'message': 'Account ID Not Found' })


