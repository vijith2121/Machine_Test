from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
from selenium.webdriver.common.keys import Keys

class LinkedInLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        print("Logging in with:", username)

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        # Initialize Chrome
        driver = webdriver.Chrome()

        # Open LinkedIn Connections page
        driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections")

        # Wait for login page to load
        time.sleep(2)

        # Type username
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys(username)

        from selenium.webdriver.common.keys import Keys
        # Type password
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(password)

        # Submit form (press Enter or click button)
        password_input.send_keys(Keys.RETURN)

        # Optional: wait for the connections page to load after login
        time.sleep(5)

