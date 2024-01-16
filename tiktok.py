from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PyQt5.QtCore import Qt, QRunnable, QObject, pyqtSlot, pyqtSignal, QThreadPool
import requests
from PyQt5.QtCore import QObject, pyqtSignal
import time
from proxy_chrome_driver import get_chromedriver
from auto_action import auto_like, auto_haha, auto_play_video, auto_comment_on_livetream, auto_follow_on_livestream
import traceback
import shutil
from http.cookies import SimpleCookie
from selenium.common.exceptions import NoSuchElementException

from traodoisub import Traodoisub

# facebook_login_credential = {
#         "uid": "61552752544714",
#         "password": "truonghan72h",
#         "fa_secret": "BJCQIMAKXDTWGTAHENDV4IL4UO2LQECT"
#     }

class WorkerSignals(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

    # new
    profile_status = pyqtSignal(int)
    # cookie
    cookie = pyqtSignal(str)

class SeleniumWorker(QRunnable):
    
    def __init__(self, facebook_login_credential: dict, tiktok_login_credential: dict, cookie_str: str, proxy: dict, profile_id: str, tasks: list):
        super(SeleniumWorker, self).__init__()

        # new
        self.facebook_login_credential = facebook_login_credential

        self.cookie_str = cookie_str

        # new
        self.proxy = proxy

        self.signals = WorkerSignals()

        self.traodoisub = Traodoisub(proxy=proxy)

        self.profile_id = profile_id

        # self.driver = get_chromedriver(proxy=proxy, profile_id=profile_id)

        self.driver = None

        self.tasks = tasks

        # NEW
        self.tiktok_login_credential = tiktok_login_credential

    @pyqtSlot()
    def run(self):
        # self.driver = webdriver.Chrome()
        self.driver = get_chromedriver(profile_id=self.profile_id)

    

        # self.login_by_credentials(tiktok_login_credential=self.tiktok_login_credential)

        time.sleep(2000)

        # if 'generate_profile' in self.tasks:

        #     # Perform some simple action (e.g., login facebook, get tds_cookie, etc...
        #     self.generate_profile()

        #     time.sleep(20)


        # if 'test_profile' in self.tasks:
        #     self.test_profile()

        #     time.sleep(20)

    
    def generate_profile(self):
        self.driver = get_chromedriver(proxy=self.proxy, profile_id=self.profile_id)

        self.signals.started.emit()
        try:
            cookie_login_check = self.login_by_cookie(cookie_str = self.cookie_str)

            if cookie_login_check:
                self.signals.result.emit('Lưu profile thành công!')
                self.signals.profile_status.emit(1)
                self.driver.quit()
                return
            
            time.sleep(1)
            # remove chrome profile
            # quit driver before remove a folder
            self.driver.quit()
            self.remove_chrome_profile(user_data_directory=f'./user-profiles/{self.facebook_login_credential["uid"]}')


            # start a new driver for login_by_credentials
            self.driver = get_chromedriver(proxy=self.proxy, profile_id=self.profile_id)

            credentials_login_check = self.login_by_credentials(facebook_login_credential=self.facebook_login_credential)

            if credentials_login_check:
                self.signals.result.emit('Lưu profile thành công!')
                self.signals.profile_status.emit(1)

                # save a new cookie to caller's account
                self.save_cookie()
                self.driver.quit()
            else:
                self.signals.result.emit(f'Lưu profile thất bại!')
                self.signals.profile_status.emit(0)
                self.driver.quit()
                # self.remove_chrome_profile(user_data_directory=f'./user-profiles/{self.facebook_login_credential["uid"]}')
        except Exception as e:
            time.sleep(5)
            # Emit the error signal if an exception occurs
            tb_info = traceback.format_exc()
            self.signals.error.emit((type(e), e.args, tb_info))
        finally:
                # Close the WebDriver
                self.driver.quit()

                # Emit the finished signal
                self.signals.finished.emit()


    def login_by_cookie(self, cookie_str) -> bool:
        self.signals.result.emit(f'Đang đăng nhập bằng cookie...')

        cookie = SimpleCookie()

        cookie.load(cookie_str)


        cookies = {k: v.value for k, v in cookie.items()}

        self.driver.get("https://www.facebook.com")


        for key, value in cookies.items():
            cookie = {'name': key, 'value': value}
            self.driver.add_cookie(cookie)

        time.sleep(2)

        self.driver.refresh()

        time.sleep(2)

        if self.check_success_login():
            self.signals.result.emit('Đăng nhập bằng cookie thành công!')
            return True
        else:
            self.signals.result.emit('Đăng nhập bằng cookie thất bại!')
            return False
    
    def login_by_credentials(self, tiktok_login_credential: dict):

        # tiktok_login_credential = self.tiktok_login_credential

        # self.driver = get_chromedriver(proxy=self.proxy, profile_id=self.profile_id)

        # self.driver = webdriver.Chrome()

        try:
            self.signals.result.emit('Đang đăng nhập...')
            # Navigate to the Facebook login page
            self.driver.get("https://www.tiktok.com/")

            time.sleep(50)

            # WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "header-login-button"))).click()

            # # Find the username and password input fields and the login button using their respective attributes
            # username_input = self.driver.find_element(By.ID, "email")
            # password_input = self.driver.find_element(By.ID, "pass")
            # login_button = self.driver.find_element(By.NAME, "login")

            # # Enter your Facebook credentials
            # username_input.send_keys(tiktok_login_credential["uid"])
            # password_input.send_keys(tiktok_login_credential["password"])


            # # Click the login button
            # login_button.click()

            # time.sleep(5)

            # # Find the appovals_code field and checkPointSubmitbutton after click
            # appovals_code_input = self.driver.find_element(By.ID, "approvals_code")
            # checkPointSubmitbutton = self.driver.find_element(By.ID, "checkpointSubmitButton")

            # # GET 2FA Code
            # two_fa_code = self.get_2FA_Code(tiktok_login_credential["fa_secret"])

            # # Enter 2FA Code
            # appovals_code_input.send_keys(two_fa_code)

            # # Click the CPS_button
            # checkPointSubmitbutton.click()

            # time.sleep(2)

            # # Find checkbox
            # # checkBox = self.driver.find_element(By.XPATH, "//div[@class='uiInputLabel clearfix uiInputLabelLegacy']/label")
            # # click check box
            # # checkBox.click()

        
            # # find and click another CPS_Button
            # checkPointSubmitbutton = self.driver.find_element(By.ID, "checkpointSubmitButton")
            # checkPointSubmitbutton.click()

        except Exception as error:
            time.sleep(36)
            self.signals.result.emit(error)

        finally:
            pass
            # if self.check_success_login():
            #     return True
            # else:
            #     return False

    def check_success_login(self):
        if "https://www.facebook.com/" == self.driver.current_url:

            try:
                ele = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Facebook']")))

                if ele:
                    return True

                return False
            except:
                return False

        return False

    def test_profile(self):

        try:
            self.driver = get_chromedriver(proxy=self.proxy, profile_id=self.profile_id)

            self.driver.get('https://www.facebook.com')

            if self.check_success_login():
                self.signals.result.emit(f'Test: profile này vẫn sống khỏe!')
            else:
                self.signals.result.emit(f'Test: profile này lỗi rồi!!')
                self.signals.profile_status.emit(0)
                # self.driver.quit()
                # self.remove_chrome_profile(user_data_directory=f'./user-profiles/{self.facebook_login_credential["uid"]}')

            time.sleep(100)

        except Exception as e:
            # Emit the error signal if an exception occurs
            tb_info = traceback.format_exc()
            self.signals.error.emit((type(e), e.args, tb_info))


    def open_new_tab(self, url="/"):
        self.driver.execute_script(f"window.open('{url}');")

    def quit_driver(self):
        self.driver.quit()

    def clear_browser(self):
        # Clear cookies
        self.driver.delete_all_cookies()

        # Clear localStorage
        self.driver.execute_script("localStorage.clear();")

        # Clear sessionStorage
        self.driver.execute_script("sessionStorage.clear();")

        # Switch to the parent tab
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Close all remaining tabs
        for handle in self.driver.window_handles[1:]:
            self.driver.switch_to.window(handle)
            self.driver.close()

        # Switch to the parent tab
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.refresh()

    def like_some_post(self, post_count: int):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Thích']")))
            like_buttons = self.driver.find_elements(By.XPATH, "//div[@aria-label='Thích']")
            print("count:", len(like_buttons))

            count = 0

            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Thích']"))).click()

            for like_button in like_buttons:
                if count <= post_count:
                    like_button.click()

                    # increase count
                    count += 1

                    # sleep in 2 seconds
                    time.sleep(2)
                else:
                    break
        except Exception as error:
            print(error)

    def comment_some_post(self, post_count: int):
        try:
            show_comment_box_buttons = self.driver.find_elements(By.XPATH, "//div[@aria-label='Viết bình luận']")

            print("show_comment_box_buttons' count:", len(show_comment_box_buttons))

            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Viết bình luận']"))).click()

            
            for s_c_b_button in show_comment_box_buttons:
                # check
                # //div[@aria-label='Đóng']

                # click
                s_c_b_button.click()

                

                # check length of close buttons (2 if is dialog show and other hand)
            
                if len(self.driver.find_elements(By.XPATH, "//div[@aria-label='Đóng']")) == 2:
                    print('TRUE')
                    WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Đóng']"))).click()


                    self.driver.find_elements(By.XPATH, "//div[@aria-label='Đóng']")[1].click()

                

                # sleep in 2 seconds
                time.sleep(2)
            
        except Exception as error:
            print(error)

    def scroll_down_continuous(self, driver, scroll_delay=2, num_scrolls=None):
        # Define the scroll script
        scroll_script = "window.scrollTo(0, document.body.scrollHeight);"

        try:
            scroll_count = 0
            while num_scrolls is None or scroll_count < num_scrolls:
                # Execute the scroll script
                driver.execute_script(scroll_script)

                # Interacting

                
                # Wait for a short time to allow the content to load
                time.sleep(scroll_delay)

                scroll_count += 1
        except KeyboardInterrupt:
            # Handle interruption with KeyboardInterrupt (Ctrl+C)
            pass

    def open_new_tab_and_interact(self, url='', like=False, comment=False, tab_order = 0, delay=2):

        try:
            self.driver.execute_script(f"window.open('{url}', '_blank');")
            
            
            # Switch to second tab ~ correspond index is 1 (parent tab is 0)
            # In this case, index 1 corresponds to the second tab (since indexing starts from 0)
            self.driver.switch_to.window(self.driver.window_handles[tab_order])


            if like:
                try:
                    WebDriverWait(self.driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Thích']"))).click()
                    time.sleep(2)
                except Exception as error:
                    print(error)

            if comment:
                try:
                    time.sleep(2)
                    WebDriverWait(self.driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Viết bình luận']"))).click()

                    # Locate comment box
                    comment_box = self.driver.find_element(By.XPATH, "//div[@aria-label='Viết bình luận...']/p")

                    # Enter into comment box
                    comment_box.send_keys('Xin chào')

                    # Hit ENTER
                    comment_box.send_keys(Keys.RETURN)
                except Exception as error:
                    print(error)

            # Sleep time between jobs
            time.sleep(delay)

        except Exception as e:
            # Emit the error signal if an exception occurs
            tb_info = traceback.format_exc()
            self.signals.error.emit((type(e), e.args, tb_info))

    def watch_livestream_and_interact(self, url='', like=False, comment=False, delay=2):
        time.sleep(delay)

        try:
            # open new tab
            self.driver.execute_script(f"window.open('{url}');")
            # Switch to second tab ~ correspond index is 1 (parent tab is 0)
            # In this case, index 1 corresponds to the second tab (since indexing starts from 0)
            self.driver.switch_to.window(self.driver.window_handles[1])

            # auto_like(driver, delay_action=5)


            # auto_play_video(driver=driver, delay_action=5)

            # auto_haha(driver, delay_action=5)
            # auto_comment_on_livetream(driver=driver, delay_action=5)

            auto_follow_on_livestream(self.driver, delay_action=5)

            # //div[@aria-label='Phát video']

            # Play video (live stream)
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Phát video']"))).click()
            

        except Exception as error:
            print(error)

    def save_cookie(self):
        cookies = self.driver.get_cookies()

        fb_cookie_str = ""

        for cookie in cookies:
            fb_cookie_str += cookie['name'] + '=' + cookie['value'] + ';'

        self.signals.cookie.emit(fb_cookie_str)

        self.signals.result.emit('Wrote facebook cookie successfully!')

    def remove_chrome_profile(self, user_data_directory):
        time.sleep(2)
        try:
            # Use shutil.rmtree to recursively remove the entire directory
            shutil.rmtree(user_data_directory)
            print(f"Profile at '{user_data_directory}' successfully removed.")
        except Exception as e:
            print(f"An error occurred while removing the profile: {str(e)}")