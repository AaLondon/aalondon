from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import ActionChains
from meetings.models import Meeting
from  datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

'''
In order for these tests to run successfully you need to run 
python manage.py collectstatic first
'''

class TestUpdateMeetingPage(LiveServerTestCase):
    pass
    """ def setUp(self):
        opts = Options()
        #opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=opts,executable_path=GeckoDriverManager().install())

    def tearDown(self):
        self.driver.close()

    def test_form_loads(self):
        url = f"{self.live_server_url}/update"
        self.driver.get(url)

        # The user opens the home page
        form = self.driver.find_elements_by_id('new-meeting-form')
        assert form
        dropdown=self.driver.find_element_by_xpath("//*[@role = 'listbox']")
        actions = ActionChains(self.driver);
        actions.click(dropdown).perform()
        
        dropdown.send_keys(Keys.DOWN)#.send_keys(Keys.DOWN).send_keys(Keys.RETURN)
        dropdown.send_keys(Keys.DOWN)
        dropdown.send_keys(Keys.RETURN)
        dropdown.send_keys(Keys.TAB)
        
        assert 1==1
 """
        

        
        

    
     
      
    
        




   
