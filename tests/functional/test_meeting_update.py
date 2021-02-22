from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import ActionChains
from meetings.models import Meeting
from  datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options



class TestUpdateMeetingPage(LiveServerTestCase):
    def setUp(self):
        opts = Options()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=opts,executable_path=GeckoDriverManager().install())

    def tearDown(self):
        self.driver.close()

    def test_form_loads(self):
        url = f"{self.live_server_url}/update"
        self.driver.get(url)

        # The user opens the home page
        form = self.driver.find_elements_by_id('new-meeting-form')
        assert form
        #assert "MonthWeekDayAgenda" in calendar.text

    # def test_event_has_client_dropdown(self):
    #     url = f"{self.live_server_url}/booking"
    #     self.browser.get(url)
    #     event=self.browser.find_element_by_xpath("//*[@title = 'test_event']")
    #     actions = ActionChains(self.browser);
    #     actions.double_click(event).perform()
    #     dropdown_title = self.browser.find_element_by_class_name("client-dropdown")
    #     assert dropdown_title

    # def test_client_dropdown_displays_name(self):
    #     url = f"{self.live_server_url}/booking"
    #     self.browser.get(url)
    #     event=self.browser.find_element_by_xpath("//*[@title = 'test_event']")
    #     actions = ActionChains(self.browser);
    #     actions.double_click(event).perform()
    #     dropdown = self.browser.find_element_by_class_name("client-dropdown")
    #     actions = ActionChains(self.browser);
        
    #     actions.reset_actions()
    #     actions.move_to_element(dropdown)
    #     actions.click()
    #     actions.perform()
    #     menu = self.browser.find_element_by_xpath("//*[@class='visible menu transition']")
    #     assert 'John Smith' in menu.text
        

    # def test_save_button_enabled_disabled_before_and_after_save(self):
    #     url = f"{self.live_server_url}/booking"
    #     self.browser.get(url)
    #     event=self.browser.find_element_by_xpath("//*[@title = 'test_event']")
    #     actions = ActionChains(self.browser)
    #     actions.double_click(event).perform()
    #     title = self.browser.find_element_by_xpath("//*[@placeholder = 'Title']")
    #     button = self.browser.find_elements_by_class_name('ui.button.disabled')
    #     assert button
    #     title.send_keys("some text")
    #     button = self.browser.find_elements_by_class_name('ui.button.disabled')
    #     assert not button
    #     title.submit()
    #     self.browser.implicitly_wait(5)
    #     button = self.browser.find_elements_by_class_name("ui.button.disabled")#;find_element_by_xpath("//*[@class = 'ui button disabled']")
    #     assert button


    # def test_delete_button_confirms_and_deletes(self):
    #     url = f"{self.live_server_url}/booking"
    #     self.browser.get(url)
    #     event=self.browser.find_element_by_xpath("//*[@title = 'test_event']")
    #     actions = ActionChains(self.browser)
    #     actions.double_click(event).perform()

    #     button = self.browser.find_elements_by_class_name('ui.red.button')
    #     actions2 = ActionChains(self.browser)
        
    #     actions2.click(button[0]).perform()
    #     self.browser.implicitly_wait(5)
        
    #     delete_icon = self.browser.find_elements_by_class_name('delete.icon')
    #     assert delete_icon

     
      
    
        




   
