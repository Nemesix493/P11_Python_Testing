import pytest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from .run_server import start_server, stop_server, clubs, competitions


class TestUserExperience:
    def setup_class(cls):
        options = Options()
        options.add_argument('-headless')
        cls.data = {'clubs': clubs, 'competitions': competitions}
        start_server()
        cls.browser = webdriver.Firefox(options=options)
        cls.browser.implicitly_wait(2)

    def teardown_class(cls):
        stop_server()

    def is_loaded(self, select_type, select: str):
        time.sleep(1)
        try:
            WebDriverWait(self.browser, 5).until(
                expected_conditions.presence_of_element_located((select_type, select))
            )
            return True
        except Exception:
            return False

    def check_clubs_points_view(self) -> bool:
        if not self.is_loaded(By.TAG_NAME, 'table'):
            return False
        table = self.browser.find_element(By.TAG_NAME, 'table')
        table_rows = table.find_elements(By.TAG_NAME, 'tr')
        if table_rows is None:
            return False
        table_tds = self.browser.find_elements(By.CSS_SELECTOR, 'table td')
        table_tds_text = [td.text for td in table_tds]
        return False not in [
            club['name'] in table_tds_text
            for club in self.data['clubs']
        ]

    def check_index_view(self):
        if not self.is_loaded(By.TAG_NAME, 'h1'):
            return False
        title = self.browser.find_element(By.TAG_NAME, 'h1')
        return title.text == 'Welcome to the GUDLFT Registration Portal!'

    def check_show_summary_view(self, club: dict):
        if not self.is_loaded(By.TAG_NAME, 'h2'):
            return False
        title = self.browser.find_element(By.TAG_NAME, 'h2')
        return title.text == f'Welcome, {club["email"]}'

    def check_book_view(self, club):
        if not self.is_loaded(By.TAG_NAME, 'form'):
            return False
        competitions_names = [competition['name'] for competition in self.data['competitions']]
        url_segment = self.browser.current_url.replace('%20', ' ').split('/')
        return url_segment[-3] == 'book' and url_segment[-2] in competitions_names and url_segment[-1] == club['name']

    def check_purchase_place_view(self, place_purchased: int):
        if not self.is_loaded(By.CSS_SELECTOR, 'ul li'):
            return False
        flash_messages = self.browser.find_elements(By.CSS_SELECTOR, 'ul li')
        expected_message = f'Great-booking complete ({place_purchased} booked) !'
        return expected_message in [flash_message.text for flash_message in flash_messages]

    def test_user_experience(self):
        self.browser.get('http://localhost:5000/')
        assert self.check_index_view()
        link = self.browser.find_element(By.CSS_SELECTOR, 'p a')
        # Go to Clubs Points
        link.click()
        assert self.check_clubs_points_view(), 'Error on clubs points view !'
        link = self.browser.find_element(By.CSS_SELECTOR, 'p a')
        # Go to Index page
        link.click()
        assert self.check_index_view(), 'Error on index view !'
        form_input = self.browser.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        form_input.send_keys(self.data['clubs'][0]['email'])
        # Go to Show Summary
        form_input.submit()
        assert self.check_show_summary_view(club=self.data['clubs'][0]), 'Error on show summary view !'
        link = self.browser.find_elements(By.CSS_SELECTOR, 'li a')[0]
        # Go to book view
        link.click()
        assert self.check_book_view(club=self.data['clubs'][0]), 'Error on book view !'
        input_number = self.browser.find_element(By.CSS_SELECTOR, 'form input[type="number"]')
        place_purchased = 3
        input_number.send_keys(str(place_purchased))
        input_number.submit()
        assert self.check_purchase_place_view(place_purchased=place_purchased), 'Error on purchase place view'
