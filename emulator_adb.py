import io
import json
import os,time

import requests
try:
 import threading,subprocess,base64,cv2,random
 import numpy as np
except:
  os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
  os.system("pip install numpy")
import threading,subprocess,base64,cv2,random
import numpy as np
from datetime import datetime
import traceback
import datetime
import base64
from PIL import Image
from PyQt5.QtCore import Qt, QRunnable, QObject, pyqtSlot, pyqtSignal, QThreadPool

# com.zhiliaoapp.musically




class Auto():
    def __init__(self, handle):
        self.handle = handle
    def set_proxy(self, proxy):
        os.system(f"adb -s {self.handle} shell settings put global http_proxy {proxy}")
    def remove_proxy(self):
        os.system(f"adb -s {self.handle} shell settings put global http_proxy :0")
    def screen_capture(self,name):
        os.system(f"adb -s {self.handle} exec-out screencap -p > {name}.png ")
    def capture_captcha(self, save_path, name) -> str:
        file_path = f"{save_path}/{name}.png"
        os.system(f"adb -s {self.handle} exec-out screencap -p > {file_path}")
        return file_path
    def click(self,x,y):
        os.system(f"adb -s {self.handle} shell input tap {x} {y}")
    def heart(self,x,y):
        tap_command = f'input tap {x} {y}'
        tap_count = random.randint(3, 6)  # You can adjust this count based on your needs
        delay_between_taps = 0.2  # You can adjust the delay in seconds

        tap_commands = f' & sleep {delay_between_taps} & '.join([f'{tap_command}' for _ in range(tap_count)])

        os.system(f'adb -s {self.handle} shell "{tap_commands}"')

        print("hearting...")
        time.sleep(1)

    def heart2(self,x,y):
        tap_command = f'input tap {x} {y}'
        tap_count = random.randint(6, 10)  # You can adjust this count based on your needs
        delay_between_taps = 0.4  # You can adjust the delay in seconds

        tap_commands = ' & '.join([f'{tap_command} & sleep {delay_between_taps}' for _ in range(tap_count)])

        os.system(f'adb -s {self.handle} shell "{tap_commands}"')

    def heart_text(self, x, y):
        os.system(f"adb -s {self.handle} shell input tap {x} {y}")
        print('đang thả tim')
            
        
    def find(self,img='',template_pic_name=False,threshold=0.99):
        if template_pic_name == False:
            self.screen_capture(self.handle)
            template_pic_name = self.handle+'.png'
        else:
            self.screen_capture(template_pic_name)
        img = cv2.imread(img)
        img2 = cv2.imread(template_pic_name)
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        test_data = list(zip(*loc[::-1]))
        return test_data
    def find2(self, img='', template_pic_name=False, threshold=0.99):
        if template_pic_name == False:
            self.screen_capture(self.handle)
            template_pic_name = self.handle + '.png'
        else:
            self.screen_capture(template_pic_name)

        # Read the images in color
        img = cv2.imread(img)
        img2 = cv2.imread(template_pic_name)

        # Perform template matching for each channel (B, G, R)
        result = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED)

        # Find locations where the result is greater than or equal to the threshold
        loc = np.where(result >= threshold)

        # Zip the coordinates to get the test_data
        test_data = list(zip(*loc[::-1]))

        # Return the result
        return test_data
    def sendText(self, text: str) -> None:
        os.system(f"adb -s {self.handle} shell input text '{text}'")
    def sendUnicodeText(self, text: str) -> None:
        os.system(f"adb -s {self.handle} shell am broadcast -a ADB_INPUT_TEXT --es msg '{text}'")
    def deleteText(self) -> None:
        os.system(f"adb -s {self.handle} shell input keyevent KEYCODE_DEL")
    def enter(self) -> None:
        os.system(f"adb -s {self.handle} shell input keyevent 66")
    # def clearApp(self, package_name: str) -> None:
    #     os.system(f"adb -s {self.handle} shell pm clear {package_name}")
    def clearApp(self) -> None:
        os.system(f"adb -s {self.handle} shell pm clear com.zhiliaoapp.musically")
    def offApp(self, package_name: str) -> None:
        os.system(f"adb -s {self.handle} shell am force-stop {package_name}")
    def swipe(self, x1, y1, x2, y2):
        subprocess.call(f"adb -s {self.handle} shell input touchscreen swipe {x1} {y1} {x2} {y2} 1000", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def backHome(self):
        os.system(f"adb -s {self.handle} shell input keyevent KEYCODE_HOME")

def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if len(p) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 0
        
class WorkerSignals(QObject):
    result = pyqtSignal(object)
    error = pyqtSignal(tuple)
    device_status = pyqtSignal(tuple)
    account_device_connect_status = pyqtSignal(tuple)
    account_configure = pyqtSignal(object)
    debug = pyqtSignal(tuple)

class EmulatorWorker(QRunnable):
    def __init__(self, device_name: str, account: str|None, proxy:str|None, configure: dict|None) -> None:
        super(EmulatorWorker, self).__init__()
        self.device = device_name
        self.account = account
        self.proxy = proxy
        self.configure = configure

        self.signals = WorkerSignals()

    def get_date_time(self):
        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Format the date and time as a string
        formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

        return formatted_datetime
    

    def convert_png_to_base64(self, png_file_path, compression_quality=85):
        # Open the PNG image using Pillow
        with Image.open(png_file_path) as img:
            # Convert the PNG image to RGB mode (JPEG doesn't support transparency)
            img = img.convert("RGB")

            # Create an in-memory binary stream
            img_stream = io.BytesIO()

            # Save the image as a JPEG with the specified compression quality to the stream
            # img.save(img_stream, "JPEG", quality=compression_quality)
            img.save(img_stream, "JPEG")

            # Get the binary data from the stream
            img_binary = img_stream.getvalue()

            # Encode the binary data as base64
            base64_encoded = base64.b64encode(img_binary)

            # Convert the bytes to a string (decode)
            base64_string = base64_encoded.decode("utf-8")

        return base64_string

    
    def write_base64_to_file(self, base64_string, output_file_path):
        with open(output_file_path, "w") as output_file:
            output_file.write(base64_string)
    
    def convert_png_to_jpg(png_file_path, jpg_file_path, compression_quality=85):
    # Open the PNG image using Pillow
        with Image.open(png_file_path) as img:
            # Convert the PNG image to RGB mode (if it's not already in that mode)
            img = img.convert("RGB")

            # Save the image as a JPEG with the specified compression quality
            img.save(jpg_file_path, "JPEG", quality=compression_quality)
    
    def solve_captcha(self, base64_string: str, type: str):
        api_token = "zRNjqIDpjur5aRONjGZts7wqewMzDmdZ3FUB5lPrTGIu6KNxJXSi6GrpgdIAMAyVIKn1HG81daaiEQUS"
        try:

            url = "https://omocaptcha.com/api/createJob"

            data = {
                "api_token": "zRNjqIDpjur5aRONjGZts7wqewMzDmdZ3FUB5lPrTGIu6KNxJXSi6GrpgdIAMAyVIKn1HG81daaiEQUS",
                "data": {
                    "type_job_id": type,
                    "image_base64": base64_string
                }
            }

            json_data = json.dumps(data)

            # Set the headers to indicate that you are sending JSON data
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, data=json_data, headers=headers)
            status_code = response.status_code
            try:
                response = response.json()
                self.signals.debug.emit((f"{self.device} - response", response))
                self.signals.debug.emit((f"{self.device} - success status code", status_code))
            except:
                self.signals.debug.emit((f"{self.device} - response text", status_code))
                self.signals.debug.emit((f"{self.device} - error status code", status_code))

        
            job_id = None
            if response['error'] is False:
                job_id = response['job_id']

            self.signals.debug.emit(("job_id", job_id))




            if job_id is not None:
                url_2 = "https://omocaptcha.com/api/getJobResult"

                data_2 = {
                    "api_token": "zRNjqIDpjur5aRONjGZts7wqewMzDmdZ3FUB5lPrTGIu6KNxJXSi6GrpgdIAMAyVIKn1HG81daaiEQUS",
                    "job_id": int(job_id)
                }

                json_data_2 = json.dumps(data_2)

                # Set the headers to indicate that you are sending JSON data
                headers = {'Content-Type': 'application/json'}

                

                start = 0
                end = 60
                while start < end:
                    try:
                        response_2 = requests.post(url_2, data=json_data_2, headers=headers)
                        response_2 = response_2.json()
                        # self.signals.debug.emit((f"{self.device} - response 2", response_2))
                        if response_2["status"] == "success":
                            return response_2["result"]
                        elif response_2["status"] == "running":
                            pass
                        elif response_2["status"] == "waiting":
                            pass
                        elif response_2["status"] == "fail":
                            return response_2["result"]
                    except:
                        pass

                    
                    start += 1
                    time.sleep(2)

            return None

        except Exception as e:
            tb_info = traceback.format_exc()
            self.signals.error.emit((type(e), e.args, tb_info))

    def config_proxy(self, adb_auto: Auto) -> bool:
        locating_img_path = "./images/proxy-college-phone-1.png"
        proxy = self.account["proxy"].split(":")
        print("Đang tiến hành config proxy:", proxy)

        while True:
            try:
                point = adb_auto.find(locating_img_path)
                if point > [(0,0)]:
                    adb_auto.click(point[0][0], point[0][1])

                    # SET UP PROXY
                    start_check_time = time.time()
                    while time.time() - start_check_time < 10:
                        point_2 = adb_auto.find("./images/proxy-host-label-1.png")
                        if point_2 > [(0, 0)]:
                            break
                        else:
                            time.sleep(0.5)
                    point_3 = adb_auto.find("./images/proxy-port-label-1.png")
                    point_4 = adb_auto.find("./images/proxy-username-label-1.png")
                    point_5 = adb_auto.find("./images/proxy-password-label-1.png")
                    point_6 = adb_auto.find("./images/start-proxy-button-1.png")
                    if point_2 > [(0,0)]:
                        adb_auto.click(point_2[0][0]+1000, point_2[0][1])
                        adb_auto.sendText(proxy[0])
                    if point_3 > [(0,0)]:
                        adb_auto.click(point_3[0][0]+1000, point_3[0][1])
                        adb_auto.sendText(proxy[1])
                    if point_4 > [(0,0)]:
                        adb_auto.click(point_4[0][0]+1000, point_4[0][1])
                        adb_auto.sendText(proxy[2])
                    if point_5 > [(0,0)]:
                        adb_auto.click(point_5[0][0]+1000, point_5[0][1])
                        adb_auto.sendText(proxy[3])

                    if point_6 > [(0,0)]:
                        adb_auto.click(point_6[0][0], point_6[0][1])
                        
                    start_check_time = time.time()
                    while time.time() - start_check_time < 30:
                        try:
                            point_7 = adb_auto.find("./images/connection-request-ok-button-1.png")
                            if point_7 > [(0,0)]:
                                adb_auto.click(point_7[0][0], point_7[0][1])
                                time.sleep(1)
                            
                            point_9 = adb_auto.find("./images/stop-proxy-button-1.png")
                            if point_9 > [(0, 0)]:
                                return True #Set up proxy successfully!

                        except:
                            print("Element not found!")
                        time.sleep(2)

                return False #Set up proxy Failed!
            except Exception as err:
                print("Lỗi khi config proxy:", err)
                traceback.print_exc()
                return False #Set up proxy Failed!
    
    def saveTiktokAccountIntoDevice(self, adb_auto: Auto, app_img_path: str):

        self.signals.device_status.emit((self.device, "busy"))

        self.signals.result.emit('Đang tiến hành thiết lập...')
        adb_auto.backHome()
        time.sleep(2)


        point_1 = adb_auto.find("./images/tiktok-phone-1.png")
        point_1_tmp = adb_auto.find("./images/tiktok-phone-2.png")

        if point_1 > [(0, 0)]:
            adb_auto.click(point_1[0][0], point_1[0][1])
        elif point_1_tmp > [(0, 0)]:
            adb_auto.click(point_1_tmp[0][0], point_1_tmp[0][1])


        time.sleep(4)
        adb_auto.clearApp()
        time.sleep(1)


        # start app
        # start_check_time = time.time()
        # while time.time() - start_check_time < 20:
        try:
            point_1 = adb_auto.find("./images/tiktok-phone-1.png")
            point_1_tmp = adb_auto.find("./images/tiktok-phone-2.png")
            if point_1 > [(0, 0)]:
                adb_auto.click(point_1[0][0], point_1[0][1])
                # break
            elif point_1_tmp > [(0, 0)]:
                adb_auto.click(point_1_tmp[0][0], point_1_tmp[0][1])
                # break
        except Exception as e:
            tb_info = traceback.format_exc()
            self.signals.error.emit((type(e), e.args, tb_info))

      
        start_check_time = time.time()
        self.signals.result.emit('Đang tìm và xử lý point_2')
        start_check_time = time.time()
        while time.time() - start_check_time < 20:
            # print('Processing point_3 ...')
            point_2 = adb_auto.find("./images/tiktok-agree-and-continue.png")
            if point_2 > [(0, 0)]:
                adb_auto.click(point_2[0][0], point_2[0][1])
                break


        
        self.signals.result.emit('Đang tìm và xử lý point_3')
        start_check_time = time.time()
        while time.time() - start_check_time < 20:
            point_3 = adb_auto.find("./images/tiktok-skip-interest-2.png")
            if point_3 > [(0, 0)]:
                adb_auto.click(point_3[0][0], point_3[0][1])
                break
        
        self.signals.result.emit('Đang tìm và xử lý point_4')
        while time.time() - start_check_time < 20:
            point_4 = adb_auto.find("./images/tiktok-start-watching-3.png")
            if point_4 > [(0, 0)]:
                adb_auto.click(point_4[0][0], point_4[0][1])
                break

        

        # Đang trượt lên
        time.sleep(2)
        adb_auto.swipe(768.6,1810.5, 768.6,600.8)
        time.sleep(0.2)
        adb_auto.swipe(768.6,1810.5, 768.6,600.8)
        
        # self.signals.result.emit('Đang tìm và xử lý point_5')
        # start_check_time = time.time()
        # while time.time() - start_check_time < 20:
        #     # print('Processing point_5 (swipe) ...')
        #     point_5 = adb_auto.find("./images/swipe-up-for-more-2.png")
        #     if point_5 > [(0, 0)]:
        #         print('Swipped up')
        #         adb_auto.swipe(768.6,1810.5, 768.6,400.8)
        #         time.sleep(0.2)
        #         adb_auto.swipe(768.6,1810.5, 768.6,600.8)
        #         break

        # Click profile button
        time.sleep(1)
        # click profile tab
        adb_auto.click(1305.2,2456.4)


        self.signals.result.emit('Đang tìm và xử lý point_6')
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            # print('Processing point_6 ...')
            point_6 = adb_auto.find("./images/tiktok-phone-or-email-login-3.png")
            if point_6 > [(0, 0)]:
                adb_auto.click(point_6[0][0], point_6[0][1])
                break
        

        self.signals.result.emit('Đang tìm và xử lý point_7')
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            # print('Processing point_7 ...')
            point_7 = adb_auto.find("./images/tiktok-username-login-tab-2.png")
            if point_7 > [(0, 0)]:
                adb_auto.click(point_7[0][0], point_7[0][1])
                time.sleep(0.5)
                adb_auto.sendText(self.account["username"]) # send username input
                break

        self.signals.result.emit('Đang tìm và xử lý button continue')
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            button_continue = adb_auto.find("./images/tiktok-login-form-continue-button.png")
            if button_continue > [(0, 0)]:
                adb_auto.click(button_continue[0][0], button_continue[0][1])
                break

        
        
        self.signals.result.emit('Đang tìm và xử lý point_8')
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            # print('Processing point_8 ...')
            point_8 = adb_auto.find("./images/tiktok-password-input.png")
            if point_8 > [(0, 0)]:
                adb_auto.sendText(self.account["password"]) # send password input
                break

        self.signals.result.emit('Đang tìm và xử lý point_9')
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            # print('Processing point_9 ...')
            point_9 = adb_auto.find("./images/tiktok-login-button-2.png")
            if point_9 > [(0, 0)]:
                adb_auto.click(point_9[0][0], point_9[0][1])
                break

        # Click Deny-access-contacts button
        self.signals.result.emit(f"Đang tìm và xử lý button DENY_ACCESS_CONTACTS")
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_15 = adb_auto.find("./images/deny-access-contacts-2.png")
            if point_15 > [(0, 0)]:
                time.sleep(0.5)
                adb_auto.click(point_15[0][0], point_15[0][1])
                break
        
        # RESOLVE CAPTCHA...
        self.signals.result.emit('Đang tìm và xử lý point_10 (captcha)')
        start_check_time = time.time()
        while time.time() - start_check_time < 30:
            # print('Processing point_10 (captcha) ...')
            point_10 = adb_auto.find("./images/tiktok-verify-captcha-label.png")
            point_11 = adb_auto.find("./images/tiktok-verify-captcha-type-2-label.png")
            if point_10 > [(0, 0)]:
                attempt = 1
                while attempt <= 4:
                    formatted_datetime = self.get_date_time()
                    file_name = f"capt_{formatted_datetime}"
                    captcha_path = adb_auto.capture_captcha(save_path="./captchas", name=file_name)
                    try:
                        base64_representation = self.convert_png_to_base64(captcha_path)
                        formatted_datetime = self.get_date_time()
                        # output_file_path = f"./outputs/base64_{self.device}_{formatted_datetime}"
                        # self.write_base64_to_file(base64_representation, output_file_path)
                        capt_result = self.solve_captcha(base64_representation, type="24")
                        self.signals.debug.emit(("capt_result", capt_result))
                        if capt_result is not None:
                            cordinates = capt_result
                            self.signals.debug.emit(('cordinates', cordinates))
                            x1,y1,x2,y2 = cordinates.split('|')
                            x1 = int(x1)
                            y1 = int(y1)
                            x2 = int(x2)
                            y2 = int(y2)
                            time.sleep(0.5)
                            adb_auto.swipe(x1,y1,x2,y2)
                        else:
                            print('Resolve captcha not successfully!')
                        
                    except Exception as e:
                        tb_info = traceback.format_exc()
                        self.signals.error.emit((type(e), e.args, tb_info))

                    time.sleep(5)
                    point_10 = adb_auto.find("./images/tiktok-verify-captcha-label.png")
                    if point_10 > [(0, 0)]:
                        attempt+=1
                    else:
                        break
                break
        

            if point_11 > [(0, 0)]:
                attempt = 1
                while attempt <= 4:
                    formatted_datetime = self.get_date_time()
                    file_name = f"capt2_{formatted_datetime}"
                    captcha_path = adb_auto.capture_captcha(save_path="./captchas", name=file_name)
                    try:
                        base64_representation = self.convert_png_to_base64(captcha_path)
                        formatted_datetime = self.get_date_time()
                        capt_result = self.solve_captcha(base64_representation, type="25")
                        self.signals.debug.emit(("capt2_result", capt_result))
                        if capt_result is not None:
                            point_12 = adb_auto.find("./images/tiktok-confirm-captcha-type-2-button.png")
                            cordinates = capt_result
                            x1,y1,x2,y2 = cordinates.split('|')
                            x1 = int(x1)
                            y1 = int(y1)
                            x2 = int(x2)
                            y2 = int(y2)
                            adb_auto.click(x1, y1)
                            time.sleep(0.2)
                            adb_auto.click(x2, y2)
                            time.sleep(1)
                            adb_auto.click(point_12[0][0], point_12[0][1])

                            # Check whether solve
                            time.sleep(5)
                            point_11 = adb_auto.find("./images/tiktok-verify-captcha-type-2-label.png")
                            if point_11 > [(0, 0)]:
                                attempt+=1
                            else:
                                break
                        else:
                            print('Resolve captcha not successfully!')
                        
                    except Exception as e:
                        tb_info = traceback.format_exc()
                        self.signals.error.emit((type(e), e.args, tb_info))
                break

        # Click Deny-access-contacts button
        self.signals.result.emit(f"Đang tìm và xử lý button DENY_ACCESS_CONTACTS")
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_15 = adb_auto.find("./images/deny-access-contacts-2.png")
            if point_15 > [(0, 0)]:
                time.sleep(0.5)
                adb_auto.click(point_15[0][0], point_15[0][1])
                break
        
        
        # Click login tab
        self.signals.result.emit(f"Đang tìm tab profile")
        adb_auto.click(1305.2,2456.4)


        # Click Deny-access-contacts button
        self.signals.result.emit(f"Đang kiểm tra trạng thái đang nhập")
        start_check_time = time.time()
        while time.time() - start_check_time < 20:
            point_16 = adb_auto.find("./images/tiktok-login-success-sign-3.png")
            if point_16 > [(0, 0)]:
                
                # self.signals.account_configure.emit(self.device)
                # self.signals.device_status.emit((self.device, "free"))

                # Important - Save status connect from device to account to file
                self.account["device_id"] = self.device
                self.signals.result.emit('Thiết lập thành công!')
                self.signals.account_device_connect_status.emit((self.account, self.device, True))
                time.sleep(10)
                return

        self.signals.result.emit('Thiết lập thất bại!')
        self.signals.account_device_connect_status.emit((self.account, self.device, False))
        return

    def interact_tiktok(self, adb_auto: Auto):
        try:
            while True:
                #########################(STEP 0 - SET PROXY)##############################
                # self.signals.result.emit(f'Đang tiến hành set proxy {self.proxy}')
                # adb_auto.remove_proxy()
                # time.sleep(1)
                # adb_auto.set_proxy(self.proxy)
                

                #########################(STEP 1 - BACK TO THE HOME SCREEN)##############################
                time.sleep(2)
                self.signals.result.emit('Đang tiến hành tương tác...')
                adb_auto.backHome()
                time.sleep(2)

                adb_auto.offApp("com.zhiliaoapp.musically")
                time.sleep(1)

                #########################(STEP 2 - START THE TIKTOK APP)##############################

                self.signals.result.emit('Đang mở app tiktok')
                start_check_time = time.time()
                while time.time() - start_check_time < 20:
                    point_1 = adb_auto.find("./images/tiktok-phone-1.png")
                    point_1_tmp = adb_auto.find("./images/tiktok-phone-2.png")
                    if point_1 > [(0, 0)]:
                        adb_auto.click(point_1[0][0], point_1[0][1])
                        break
                    elif point_1_tmp > [(0, 0)]:
                        adb_auto.click(point_1_tmp[0][0], point_1_tmp[0][1])
                        break
                
                #########################(STEP 3 - LOCATE TO THE TIKTOK HOME SCREEN)##############################
                # self.signals.result.emit('Chuyển qua màn hình chính của tiktok')
                # start_check_time = time.time()
                # while time.time() - start_check_time < 20:
                #     point_2 = adb_auto.find("./images/tiktok-home-tab.png")
                #     if point_2 > [(0, 0)]:
                #         time.sleep(0.5)
                #         adb_auto.click(point_2[0][0], point_2[0][1])

                #########################(STEP 4 - SWIPE UP WITH A FEW TIMES)##############################
                self.signals.result.emit('Lướt random vài lần...')
                random_num = random.randint(2, 10)
                time.sleep(1)
                for i in range(random_num):
                    ran_sleep = random.uniform(0.4, 1.4)
                    adb_auto.swipe(766.8,1810.5, 768.6,600.8)
                    time.sleep(ran_sleep)

                
                #########################(STEP 5 - SEARCH LIVESTREAM)##############################
                self.signals.result.emit('Đang tìm livestream nguồn...')
                start_check_time = time.time()
                while time.time() - start_check_time < 20:
                    point_3 = adb_auto.find("./images/tiktok-create-new-button.png")
                    if point_3 > [(0, 0)]:
                        time.sleep(0.5)
                        adb_auto.click(1326.9,185.0)
                        time.sleep(4)
                        adb_auto.sendText(self.configure["live_source"])
                        time.sleep(0.5)
                        adb_auto.enter()

                #########################(STEP 6 - CLICK LIVE TAB)##############################
                self.signals.result.emit('Chuyển qua tab LIVE')
                start_check_time = time.time()
                while time.time() - start_check_time < 20:
                    point_4 = adb_auto.find("./images/tiktok-live-tab.png")
                    if point_4 > [(0, 0)]:
                        time.sleep(0.5)
                        adb_auto.click(point_4[0][0], point_4[0][1])
                        break

                time.sleep(2)

                #########################(STEP 7 - CLICK FIRST LIVESTREAM)##############################
                self.signals.result.emit('Vào livestream đầu tiên')
                adb_auto.click(373.2,1329.4)

                #########################(STEP 8 - CHECK WHETHER BLOCKING FEATURES)##############################
                # self.signals.result.emit('Kiểm tra xem liệu có bị chặn tính năng?')
                # start_check_time = time.time()
                # while time.time() - start_check_time < 30:
                #     point_5 = adb_auto.find("./images/blocking_feat_sign-3.png")
                #     if point_5 > [(0, 0)]:
                #         break
                
                # Throw some heart first
                # adb_auto.heart2(728.7,1004.3)
                

                #########################(STEP 9 - HEARTING)##############################
                time.sleep(4)
                self.signals.result.emit('Tiến hành thả tim')
                # start_interaction_time = time.time()
                # while True:
                    # 1192.5,1234.0
                count = 0
                while True:
                    if count >= 6:
                        point_6 = adb_auto.find("./images/blocking_feat_sign-3.png")
                        if point_6 > [(0, 0)]:
                            break
                        count = 0

                    if count == 3: #commenting
                        with open("./tik_configs/comments.txt", 'r', encoding='utf-8') as file:
                            lines = file.readlines()
                            lines = [line.replace("\n", "") for line in lines]

                        random_num = random.randint(0, len(lines) - 1)
                        ran_cmt = lines[random_num]
                        print(ran_cmt)

                        adb_auto.click(342.9,2460.8)
                        time.sleep(2)
                        adb_auto.sendUnicodeText(ran_cmt)
                        # os.system(f"adb -s ce011711e365a00304 shell am broadcast -a ADB_INPUT_TEXT --es msg '{str(ran_cmt)}'")
                        time.sleep(10)
                        adb_auto.enter()
                    # adb_auto.heart(728.7, 1004.3)
                        
                    adb_auto.heart(715.7,713.8)
                    # 342.9,2460.

                    count += 1
                        
                    

        except Exception as e:
            print(e)
        finally:
            pass
            #########################(STEP FINAL - BACK TO PROFILE TAB)##############################
            # time.sleep(1)
            # self.signals.result.emit('Trở về tab profile')
            # adb_auto.click(1305.2,2456.4)
            # time.sleep(0.3)
            # adb_auto.click(1305.2,2456.4)
            # time.sleep(0.3)
            # adb_auto.click(1305.2,2456.4)


        
    @pyqtSlot()                
    def run(self):
        try:
            adb_auto = Auto(self.device)
            # Configure accounts with phones
            if self.account is not None:
                self.saveTiktokAccountIntoDevice(adb_auto, [(169.5, 250.0)])
            else: #Interactions
                print("account:", self.account)
                print(f"{self.device} - Interacting...")
                self.interact_tiktok(adb_auto)
 
        except Exception as e:
            print(e)


    
def start_worker(device_name, this_worker):
    time.sleep(0.5)
    # device_name = GetDevices()[worker_index]
    worker = EmulatorWorker(device_name, this_worker)
    worker.run()

def main():
    thread_count = len(GetDevices())
    print('thread_count', thread_count)

    proxies = []
    p_count = 0
    with open('./resources/proxy-101-200.txt') as f:
        proxies = f.read().split('\n')

    for i in range(thread_count):
        worker_index = i
        threading.Thread(target=start_worker, args=(worker_index, proxies[p_count])).start()
        p_count += 1

if __name__=="__main__": 
    main()