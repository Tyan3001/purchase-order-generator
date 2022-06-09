import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from datetime import datetime

from po_data_gen import gen_po_data


URL = 'http://pnwtraining.cswg.com/trn_pnw/ua/r/trn_pnw/SMMNU'

class Po_generator(webdriver.Chrome):
    def __init__(self, driver_path = '', teardown = False, log = 'log.txt', suppress_window = False, config = None):
        if config:
            self.driver_path = config['driver_path']
            self.teardown = config['teardown']
            self.log = config['log']
        else:
            self.driver_path = driver_path
            self.teardown = teardown
            self.log = log
        self.logged_in = False
        self.po_num = -1
        options = webdriver.ChromeOptions()
        if suppress_window or config['suppress_window']:
            options.add_argument('headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Po_generator, self).__init__(options=options)
        self.implicitly_wait(1000)
    
    def __exit__(self, *args):
        if self.teardown:
            time.sleep(5)
            self.quit()
    
    def login(self, user = 'trsupr04', password = 'trsupr04'):
        self.get(URL)
        login_elm = self.find_element(By.XPATH, '/html/body/form/table/tbody/tr[3]/td[2]/table/tbody/tr/td[1]/input')
        login_elm.send_keys(f'{user}{Keys.TAB}{password}')
        submit_elm = self.find_element(By.XPATH, '/html/body/form/table/tbody/tr[5]/td[2]/table/tbody/tr/td[1]/input')
        submit_elm.click()
        self.logged_in = True
    
    def create_po(self, po_data):
        if not self.logged_in:
            print(f'You are not logged in...')
            return

        #STEP 1: Go to IMPOA
        nav_elm = self.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/form/div/div[5]/div/div[2]/div/div[1]')
        nav_elm.click() #navigator
        form_elm = self.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[2]/form/div/div[4]/div[2]/div/div[1]/div/div[1]/div/div/div[1]/div/div/div/div[2]/div/div/div[5]/div/div[1]/input')
        form_elm.send_keys('IMPOA' + Keys.ENTER) #IMPOA

        #STEP 2: hit "Cancel"
        cancel_elm = self.find_element(By.XPATH, '//*[@id="w_4293"]/div')
        cancel_elm.click()

        #STEP 3: hit "Add-Hdr"
        add_hdr_elm = self.find_element(By.XPATH,'//*[@id="w_4330"]/div')
        add_hdr_elm.click()

        #STEP 4: Vendor Info and Accept
        actions = ActionChains(self)
        actions.send_keys(Keys.TAB + Keys.TAB + po_data['vendor'])
        actions.send_keys(Keys.ENTER)
        actions.perform() #fill out vendor info

        actions = ActionChains(self)
        actions.send_keys(Keys.ARROW_RIGHT + Keys.ARROW_RIGHT + Keys.ENTER)
        actions.perform()

        po_num_elm = self.find_element(By.CSS_SELECTOR, '#w_4170')

        #STEP 5: Adding Products
        for p_id in po_data['products']:
            actions = ActionChains(self)
            actions.send_keys(str(p_id) + Keys.TAB + po_data['products'][p_id] + Keys.ENTER + Keys.ENTER)
            actions.perform()
        
        #STEP 6: Hit cancel
        actions = ActionChains(self)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        time.sleep(2)
        po_num_elm = self.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[2]/form/div/div[4]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div[2]/div/div/div[8]/div/input')
        self.po_num = po_num_elm.get_attribute('value').strip()
        #po_num_elm = self.find_element(By.XPATH, '//*[@id="w_4170"]/input')
    def logging(self, duration):
        with open(self.log, 'a') as f:
            if self.po_num != -1:
                f.write(f'PO {self.po_num} created in {duration.total_seconds():.2f}s\n')
            else:
                f.write(f'PO failed to create\n')



# if __name__ == '__main__':
#     with Po_generator(teardown=True) as pg:
#         start = datetime.now()
#         pg.login()
#         pg.create_po(gen_po_data(num_items=10))
#         end = datetime.now()
#         duration = end - start
#         pg.logging(duration)


