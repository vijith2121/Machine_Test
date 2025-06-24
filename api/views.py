

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pickle
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class LinkedInLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Step 1: Open Chrome
        # driver = webdriver.Chrome()
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Firefox()
        # driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections")
        driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
        # driver.get("https://www.linkedin.com/flagship-web/mynetwork/invite-connect/connections")
        time.sleep(2)

        # Step 2: Fill login form
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(5)

        # Step 3: Save cookies
        cookies = driver.get_cookies()
        driver.quit()

        # Step 4: Use cookies with requests to fetch Voyager API data
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # Add headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0',
            'csrf-token': session.cookies.get('JSESSIONID').strip('"'),
            'x-restli-protocol-version': '2.0.0'
        })

        # Voyager API endpoint for connections
        url = "https://www.linkedin.com/voyager/api/relationships/connections?count=50"
        # url = "https://www.linkedin.com/mynetwork/invite-connect/connections/"

        # Fetch connection data
        response = session.get(url)
        if response.status_code == 200:
            data = response.text
            # data = response.json()
            return Response({"connections": data}, status=200)
        else:
            return Response({"error": "Failed to fetch network data", "details": response.text}, status=500)
