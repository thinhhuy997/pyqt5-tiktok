import os,time
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


class Auto:
    def __init__(self,handle):
        self.handle = handle
    def screen_capture(self,name):
        os.system(f"adb -s {self.handle} exec-out screencap -p > {name}.png ")
    def capture_captcha(self, save_path, name) -> str:
        file_path = f"{save_path}/{name}.png"
        os.system(f"adb -s {self.handle} exec-out screencap -p > {file_path}")
        return file_path
    def click(self,x,y):
        os.system(f"adb -s {self.handle} shell input tap {x} {y}")
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
    def sendText(self, text: str) -> None:
        os.system(f"adb -s {self.handle} shell input text '{text}'")
    def deleteText(self) -> None:
        os.system(f"adb -s {self.handle} shell input keyevent KEYCODE_DEL")
    def enter(self) -> None:
        os.system(f"adb -s {self.handle} shell input keyevent 66")
    def clearApp(self, package_name: str) -> None:
        os.system(f"adb -s {self.handle} shell pm clear {package_name}")
    def offApp(self, package_name: str) -> None:
        os.system(f"adb -s {self.handle} shell am force-stop {package_name}")
    def swipe(self, x1, y1, x2, y2):
        subprocess.call(f"adb -s {self.handle} shell input touchscreen swipe {x1} {y1} {x2} {y2} 1000", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if len(p) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 0
        
class EmulatorWorker(threading.Thread):
    def __init__(self, device_name: str, account: str) -> None:
        super().__init__()
        self.device = device_name
        self.account = account

    def get_date_time(self):
        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Format the date and time as a string
        formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

        return formatted_datetime
    
    
    def image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            # Read the image file
            image_binary = image_file.read()
            # Encode the image binary data to base64
            base64_encoded = base64.b64encode(image_binary).decode('utf-8')
            return base64_encoded
        


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
            
    
    def saveTiktokAccountIntoDevice(self, adb_auto: Auto, app_coordinates: list):
        point_1 = app_coordinates
        adb_auto.click(point_1[0][0], point_1[0][1])
        print("point_1 is clicked")

        start_check_time = time.time()
        while time.time() - start_check_time < 20:
            point_2 = adb_auto.find("./images/tiktok-agree-and-continue.png")
            if point_2 > [(0, 0)]:
                adb_auto.click(point_2[0][0], point_2[0][1])
                break
        
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_3 = adb_auto.find("./images/tiktok-skip-interest.png")
            if point_3 > [(0, 0)]:
                adb_auto.click(point_3[0][0], point_3[0][1])
                break

        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_4 = adb_auto.find("./images/tiktok-start-watching.png")
            if point_4 > [(0, 0)]:
                adb_auto.click(point_4[0][0], point_4[0][1])
                break

        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_5 = adb_auto.find("./images/tiktok-swipe-up-for-more.png")
            if point_5 > [(0, 0)]:
                print('Swipped up')
                adb_auto.swipe(768.6,1810.5, 768.6,400.8)
                time.sleep(0.2)
                adb_auto.swipe(768.6,1810.5, 768.6,600.8)
                break

        # 1305.2,2456.4
        # Click profile button
        time.sleep(1)
        adb_auto.click(1305.2,2456.4)

        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_6 = adb_auto.find("./images/tiktok-login-button.png")
            if point_6 > [(0, 0)]:
                adb_auto.click(point_6[0][0], point_6[0][1])
                break
        
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_7 = adb_auto.find("./images/tiktok-username-login-tab.png")
            if point_7 > [(0, 0)]:
                adb_auto.click(point_7[0][0], point_7[0][1])
                time.sleep(0.5)
                adb_auto.sendText(self.account["username"]) # send username input
                break
        
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_8 = adb_auto.find("./images/tiktok-login-password-input.png")
            if point_8 > [(0, 0)]:
                adb_auto.click(point_8[0][0], point_8[0][1])
                time.sleep(0.5)
                adb_auto.sendText(self.account["password"]) # send password input
                break

        
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_9 = adb_auto.find("./images/tiktok-login-form-button.png")
            if point_9 > [(0, 0)]:
                adb_auto.click(point_9[0][0], point_9[0][1])
                break
        
        
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_10 = adb_auto.find("./images/tiktok-verify-captcha-label.png")
            if point_10 > [(0, 0)]:
                formatted_datetime = self.get_date_time()
                file_name = f"capt_{formatted_datetime}"
                captcha_path = adb_auto.capture_captcha(save_path="./captchas", name=file_name)
                try:
                    print('captcha_path:', captcha_path)
                    base64_encoded_str = self.image_to_base64(image_path=captcha_path)
                    print(base64_encoded_str)
                except Exception as err:
                    print(err)
                break


    def interactTiktok(self, adb_auto: Auto, app_img_path: str) -> None:
        app_started_check = False
        start_check_time = time.time()
        while time.time() - start_check_time < 10:
            point_1 = adb_auto.find(app_img_path)
            if point_1 > [(0,0)]:
                print('clicked point_1')
                adb_auto.click(point_1[0][0], point_1[0][1])
                app_started_check = True
                break

        if app_started_check:
            start_check_time = time.time()
            while time.time() - start_check_time < 20:
                point_2 = adb_auto.find("./images/tiktok-agree-and-continue.png")
                if point_2 > [(0, 0)]:
                    adb_auto.click(point_2[0][0], point_2[0][1])
                    break
            
            start_check_time = time.time()
            while time.time() - start_check_time < 10:
                point_3 = adb_auto.find("./images/tiktok-skip-interest.png")
                if point_3 > [(0, 0)]:
                    adb_auto.click(point_3[0][0], point_3[0][1])
                    break

            start_check_time = time.time()
            while time.time() - start_check_time < 10:
                point_4 = adb_auto.find("./images/tiktok-start-watching.png")
                if point_4 > [(0, 0)]:
                    adb_auto.click(point_4[0][0], point_4[0][1])
                    break

            start_check_time = time.time()
            while time.time() - start_check_time < 10:
                point_5 = adb_auto.find("./images/tiktok-swipe-up-for-more.png")
                if point_5 > [(0, 0)]:
                    print('Swipped up')
                    adb_auto.swipe(768.6,1810.5, 768.6,400.8)
                    time.sleep(0.2)
                    adb_auto.swipe(768.6,1810.5, 768.6,600.8)
                    break

            # 1305.2,2456.4
            # Click profile button
            time.sleep(1)
            adb_auto.click(1305.2,2456.4)

            # start_check_time = time.time()
            # while time.time() - start_check_time < 10:
            #     print('check point_6')
            #     point_6 = adb_auto.find("./images/tiktok-profile-button.png")
            #     if point_6 > [(0, 0)]:
            #         print('point_6', point_6)
            #         adb_auto.click(point_6[0][0], point_6[0][1])
            #         break

            start_check_time = time.time()
            while time.time() - start_check_time < 10:
                point_6 = adb_auto.find("./images/tiktok-login-button.png")
                if point_6 > [(0, 0)]:
                    adb_auto.click(point_6[0][0], point_6[0][1])
                    break
            
            start_check_time = time.time()
            while time.time() - start_check_time < 10:
                point_7 = adb_auto.find("./images/tiktok-username-login-tab.png")
                if point_7 > [(0, 0)]:
                    adb_auto.click(point_7[0][0], point_7[0][1])
                    time.sleep(0.5)
                    adb_auto.sendText(self.account["username"]) # send username input
                    break
            
            start_check_time = time.time()
            while time.time() - start_check_time < 10:
                point_8 = adb_auto.find("./images/tiktok-login-password-input.png")
                if point_8 > [(0, 0)]:
                    adb_auto.click(point_8[0][0], point_8[0][1])
                    time.sleep(0.5)
                    adb_auto.sendText(self.account["password"]) # send password input
                    break

            
            start_check_time = time.time()
            while time.time() - start_check_time < 10:
                point_9 = adb_auto.find("./images/tiktok-login-form-button.png")
                if point_9 > [(0, 0)]:
                    adb_auto.click(point_9[0][0], point_9[0][1])
                    break
            
            
            start_check_time = time.time()
            while time.time() - start_check_time < 10:
                point_10 = adb_auto.find("./images/tiktok-verify-captcha-label.png")
                if point_10 > [(0, 0)]:
                    formatted_datetime = self.get_date_time()
                    file_name = f"capt_{formatted_datetime}"
                    captcha_path = adb_auto.capture_captcha(save_path="./captchas", name=file_name)
                    try:
                        print('captcha_path:', captcha_path)
                        base64_encoded_str = self.image_to_base64(image_path=captcha_path)
                        print(base64_encoded_str)
                    except Exception as err:
                        print(err)
                    break    



    def run(self):
        try:
            adb_auto = Auto(self.device)
            # tiktok_img_path = "./images/tiktok-phone-1.png"

            # print('--------------------')
            # print(f"Device {self.device} started")
            # for i in range(1):
            #     # Config proxy for the emulator
            #     # proxy_config_check = self.config_proxy(adb_auto)

            #     # adb_auto.clearApp("com.cell47.College_Proxy")
            #     # time.sleep(2)

            #     proxy_config_check = True
            #     if proxy_config_check:
            #         self.interactTiktok(adb_auto, tiktok_img_path)
            #     time.sleep(40)
            #     adb_auto.clearApp("com.ss.android.ugc.trill")

            # -------------------------
            self.saveTiktokAccountIntoDevice(adb_auto, [(169.5, 250.0)])
            # self.saveTiktokAccountIntoDevice(adb_auto, [(169.5+286,250.0)])
 
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