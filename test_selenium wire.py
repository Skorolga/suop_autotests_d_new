#!/usr/bin/env python
"""Quick test to verify seleniumwire is intercepting requests"""
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import base64
import time

# Configure browser
options = Options()
options.set_preference('intl.accept_languages', 'ru-RU,ru')

service = Service(GeckoDriverManager().install())

seleniumwire_options = {
    'disable_encoding': True,
    'verify_ssl': False,
}

# Create browser
browser = webdriver.Firefox(
    service=service,
    options=options,
    seleniumwire_options=seleniumwire_options
)

# Setup auth interceptor
auth_string = base64.b64encode(b'tnop:TZjLZ~uOx1~0EG~').decode('utf-8')

def interceptor(request):
    print(f'[INTERCEPT] {request.method} {request.url}')
    if 'tnop12.rt.ru' in request.url:
        request.headers['Authorization'] = f'Basic {auth_string}'
        print(f'[AUTH ADDED]  Authorization: {request.headers.get("Authorization")}')

browser.request_interceptor = interceptor

print('[BROWSER] Navigating to https://www.tnop12.rt.ru')
browser.get('https://www.tnop12.rt.ru')

# Wait and check response
time.sleep(5)

print(f'[PAGE] Current URL: {browser.current_url}')
print(f'[PAGE] Title: {browser.title}')

# Check captured requests
print(f'\n[REQUESTS] Total requests captured: {len(browser.requests)}')
for request in browser.requests[:5]:  # Show first 5 requests
    response = request.response
    status = response.status_code if response else 'No response'
    print(f'  {request.method} {request.url} -> {status}')

browser.quit()
