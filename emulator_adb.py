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
# from com.dtmilano.android.viewclient import ViewClient


class Auto:
    def __init__(self,handle):
        self.handle = handle
    def screen_capture(self,name):
        os.system(f"adb -s {self.handle} exec-out screencap -p > {name}.png ")
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
    def __init__(self, device_name: str, proxy: str) -> None:
        super().__init__()
        self.device = device_name
        self.proxy = proxy

    def config_proxy(self, adb_auto: Auto) -> bool:
        locating_img_path = "./images/proxy-app-1.png"
        proxy = self.proxy.split(":")
        print("Đang tiến hành config proxy:", proxy)

        while True:
            try:
                point = adb_auto.find(locating_img_path)
                if point > [(0,0)]:
                    adb_auto.click(point[0][0], point[0][1])

                    # CHECKPOINTS
                    start_check_time = time.time()
                    while time.time() - start_check_time < 30:
                        cancel_point_1 = adb_auto.find("./images/cancel_button.png")
                        if cancel_point_1 > [(0, 0)]:
                            adb_auto.click(cancel_point_1[0][0], cancel_point_1[0][1])
                            time.sleep(0.5)
                            cancel_point_2 = adb_auto.find("./images/cancel_button.png")
                            adb_auto.click(cancel_point_2[0][0], cancel_point_2[0][1])
                            time.sleep(0.5)
                            oke_point_1 = adb_auto.find("./images/proxy-app-ok-button.png")
                            adb_auto.click(oke_point_1[0][0], oke_point_1[0][1])
                            break
                        else:
                            time.sleep(0.5)


                    # SET UP PROXY
                    start_check_time = time.time()
                    while time.time() - start_check_time < 30:
                        point_2 = adb_auto.find("./images/proxy-host-label.png")
                        if point_2 > [(0, 0)]:
                            break
                        else:
                            time.sleep(0.5)

                    point_3 = adb_auto.find("./images/proxy-port-label.png")
                    point_4 = adb_auto.find("./images/proxy-username-label.png")
                    point_5 = adb_auto.find("./images/proxy-password-label.png")
                    point_6 = adb_auto.find("./images/start-proxy.png")
                    if point_2 > [(0,0)]:
                        adb_auto.click(point_2[0][0]+350, point_2[0][1])
                        # adb_auto.click(point_2[0][0]+350, point_2[0][1])
                        adb_auto.sendText(proxy[0])
                        time.sleep(0.5)
                    if point_3 > [(0,0)]:
                        adb_auto.click(point_3[0][0]+348, point_3[0][1])
                        # adb_auto.click(point_3[0][0]+348, point_3[0][1])
                        adb_auto.sendText(proxy[1])
                        time.sleep(0.5)
                    if point_4 > [(0,0)]:
                        adb_auto.click(point_4[0][0]+348, point_4[0][1])
                        # adb_auto.click(point_4[0][0]+348, point_4[0][1])
                        adb_auto.sendText(proxy[2])
                        time.sleep(0.5)
                    if point_5 > [(0,0)]:
                        adb_auto.click(point_5[0][0]+348, point_5[0][1])
                        # adb_auto.click(point_5[0][0]+348, point_5[0][1])
                        adb_auto.sendText(proxy[3])
                    
                    start_check_time = time.time()
                    while time.time() - start_check_time < 30:
                        if point_6 > [(0,0)]:
                            adb_auto.click(point_6[0][0], point_6[0][1])
                            point_7 = adb_auto.find("./images/start-proxy-service.png")
                            if point_7 > [(0,0)]:
                                adb_auto.click(point_7[0][0], point_7[0][1])
                                
                                # time.sleep(0.5)
                                # # Oke button
                                # point_8 = adb_auto.find("./images/proxy-confirm-ok-2.png")
                                # if point_8 > [(0, 0)]:
                                #     adb_auto.click(point_8[0][0], point_8[0][1])

                                p9_start_time = time.time()
                                while time.time() - p9_start_time < 20:
                                    point_9 = adb_auto.find("./images/start-proxy-service-2.png")
                                    if point_9 > [(0, 0)]:
                                        adb_auto.click(point_9[0][0], point_9[0][1])
                                        time.sleep(2)
                                    else:
                                        time.sleep(0.5)

                                p10_start_time = time.time()
                                while time.time() - p10_start_time < 30:
                                    point_10 = adb_auto.find("./images/proxy-config-success.png")
                                    print(point_10)
                                    if point_10 > [(0, 0)]:
                                        print(f'Config proxy "{self.proxy}" thành công')
                                        return True
                                    else:
                                        time.sleep(0.5)
                        else:
                            time.sleep(0.5)
                return False
            except Exception as err:
                print("Lỗi khi config proxy:", err)
                traceback.print_exc()
                return False


    def startApp(self, adb_auto: Auto, app_img_path: str) -> None:
        while True:
            try:
                img_point = adb_auto.find(app_img_path)
                if img_point > [(0,0)]:
                    adb_auto.click(img_point[0][0], img_point[0][1])
                break
            except Exception as e:
                print("Err", e)


    def run(self):
        try:
            adb_auto = Auto(self.device)
            tiktok_img_path = "./images/tiktok-phone-1.png"

            print('--------------------')
            print(f"Device {self.device} started")
            # for i in range(1):
            #     # Config proxy for the emulator
            #     proxy_config_check = self.config_proxy(adb_auto)


            #     if proxy_config_check:
            #         self.startApp(adb_auto, )


            #     print('proxy_config_check', proxy_config_check)
            #     adb_auto.offApp("com.android.browser")
            #     adb_auto.clearApp("com.cell47.College_Proxy")
            #     time.sleep(3)

            self.startApp(adb_auto=adb_auto, app_img_path=tiktok_img_path)
                
        except Exception as e:
            print(e)
    
def start_worker(worker_index, proxy):
    time.sleep(0.5)
    device_name = GetDevices()[worker_index]    
    worker = EmulatorWorker(device_name, proxy)
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