from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

class MySeleniumTests(StaticLiveServerTestCase):
        # no crearem una BD de test en aquesta ocasió (comentem la linea)
        # fixtures = ['testdb.json',]

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            opts = Options()
            cls.selenium = WebDriver(options=opts)
            cls.selenium.implicitly_wait(5)
            # creem superusuari
            user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
            user.is_superuser = True
            user.is_staff = True
            user.save()


        def test_permisos_staff(self):
            self.selenium.get(self.live_server_url + "/admin/")
            self.selenium.find_element(By.NAME, "username").send_keys("isard")
            self.selenium.find_element(By.NAME, "password").send_keys("pirineus")
            self.selenium.find_element(By.XPATH, "//input[@type='submit']").click()
            self.assertIn("Site administration", self.selenium.page_source)
            self.selenium.get(self.live_server_url + "/admin/auth/user/add/")
            self.selenium.find_element(By.NAME, "username").send_keys("tecnico")
            self.selenium.find_element(By.NAME, "password1").send_keys("Tecnico2026!Seguro")
            self.selenium.find_element(By.NAME, "password2").send_keys("Tecnico2026!Seguro")
            self.selenium.find_element(By.NAME, "_save").click()
            self.selenium.find_element(By.ID, "id_is_staff").click()
            self.selenium.find_element(By.XPATH, "//select[@id='id_user_permissions_from']/option[contains(text(),'Can view user')]").click()
            self.selenium.find_element(By.ID, "id_user_permissions_add").click()
            self.selenium.find_element(By.NAME, "_save").click()
            self.selenium.find_element(By.CSS_SELECTOR, "#logout-form button").click()
            self.selenium.get(self.live_server_url + "/admin/")

            self.selenium.find_element(By.NAME, "username").send_keys("tecnico")
            self.selenium.find_element(By.NAME, "password").send_keys("Tecnico2026!Seguro")
            self.selenium.find_element(By.XPATH, "//input[@type='submit']").click()

            self.assertIn("TECNICO", self.selenium.find_element(By.ID, "user-tools").text.upper())
            self.selenium.get(self.live_server_url + "/admin/auth/user/")
            self.selenium.find_elements(By.LINK_TEXT, "isard")
    
            self.selenium.get(self.live_server_url + "/admin/auth/user/add/")
            self.assertIn("403", self.selenium.page_source)

            self.selenium.get(self.live_server_url + "/admin/auth/user/1/delete/")
            self.assertIn("403", self.selenium.page_source)
