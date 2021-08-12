from PySide2.QtCore import *  # 导入QT运行核心
from PySide2.QtGui import *  # 导入QT Gui
from PySide2.QtMultimedia import QSound  # 导入QT音频驱动
from PySide2.QtWebEngineWidgets import QWebEngineView  # 导入QT(Pyside2) Web 视图引擎
from PySide2.QtWidgets import *  # 导入QT窗体控件列表
from qt_for_python.uic.wews import Ui_wews
import Gdata
import sys
import time
import threading

__version__ = '1.5.5'

class main(QMainWindow,Ui_wews):
    def __init__(self):
        super().__init__()
        self.setupUi(self)        
        self.show()
        self.set_up()

        self.page = 1   #1 = 城市界面  2 = 生活指数



    def set_up(self):
        self.lb_start.move(60,320)
        self.setWindowIcon(QPixmap('builds\cloud.png'))
        # self.lb_bg.setPixmap(QPixmap('builds\bg.png'))
        # self.lb_bg.setScaledContents(True)
        self.setWindowTitle(f'WEWS丨{__version__}')
        self.tray = Tray()   
        self.pbtn_search.setIcon(QIcon('builds\search.png'))
        self.pbtn_search.setIconSize(QSize(25, 25))
        self.pbtn_refresh.setIcon(QIcon('builds\刷新.png'))
        self.pbtn_refresh.setIconSize(QSize(30, 30))
        self.pbtn_next.setIcon(QIcon('builds\下一个.png'))
        self.pbtn_next.setIconSize(QSize(30, 30))
        self.pbtn_last.setIcon(QIcon('builds\上一个.png'))
        self.pbtn_last.setIconSize(QSize(30, 30))

        self.pbtn_next.clicked.connect(self.switch)
        self.pbtn_last.clicked.connect(self.switch)
        self.pbtn_refresh.clicked.connect(self.get_data)
        self.pbtn_search.clicked.connect(self.s_show)
        self.s_window = search_window()
        self.s_window.hide()
        self.s_window.button.clicked.connect(self.search)

        self.get_data()

    def get_data(self):
        self.page = 1
        self.pbtn_refresh.setEnabled(False)
        self.pbtn_next.setEnabled(False)
        self.pbtn_search.setEnabled(False)
        self.pbtn_last.setEnabled(False)

        self.wgs = [[self.g1,self.g2,self.g3,self.g4,self.g5,self.g6,self.g7],[self.lb_g1_left,self.lb_g2_left,self.lb_g3_left,self.lb_g4_left,self.lb_g5_left,self.lb_g6_left,self.lb_g7_left],[self.lb_g1_middle,self.lb_g2_middle,self.lb_g3_middle,self.lb_g4_middle,self.lb_g5_middle,self.lb_g6_middle,self.lb_g7_middle],[self.lb_g1_right,self.lb_g2_right,self.lb_g3_right,self.lb_g4_right,self.lb_g5_right,self.lb_g6_right,self.lb_g7_right],[self.lb_g1_bg,self.lb_g2_bg,self.lb_g3_bg,self.lb_g4_bg,self.lb_g5_bg,self.lb_g6_bg,self.lb_g7_bg]]
        #clear 
        for i in self.wgs[1]:
            i.setPixmap(QPixmap('builds\刷新.png'))
        for k in self.wgs[3]:
            k.setPixmap(QPixmap('builds\刷新.png'))        
        for j in self.wgs[2]:
            j.setText('Refresh....')


        self.data,self.locate  = Gdata.Glocal()
        if self.data['code'] == 0:
            self.local_weather = [str(self.data['data']['observe']['weather']),str(self.data['data']['observe']['weather_code']),str(self.data['data']['observe']['degree']),str(self.data['data']['observe']['wind_direction']),str(self.data['data']['observe']['wind_power'])]
        else:
            self.lb_g1_middle.setText('您所在的地区无数据')
            e = self.data['code']
            self.lb_g2_middle.setText(f'Error: {e}')
            return

        # print(self.local_weather)
        self.lb_start.hide()
        for i in self.wgs[4]:
            i.setPixmap(QPixmap('builds\group_bg.png'))
        # self.lb_g1_top.setPixmap(QPixmap('builds\mark.png'))
        self.lb_g1_left.setPixmap(QPixmap(str(self.get_pic(self.local_weather[1]))))
        self.lb_g1_middle.setText(f'{self.locate[1]}，{self.local_weather[0]}\n{self.local_weather[2]}°C，{self.get_wind(str(self.local_weather[3]))}， {self.local_weather[4]}级')
        self.lb_g1_right.setPixmap(QPixmap(str(self.get_pic(self.local_weather[3]))))

        self.lb_g2_left.setPixmap(QPixmap('builds\空气质量.png'))
        self.lb_g2_right.setPixmap(QPixmap('builds\等级.png'))
        _l2 = [self.data['data']['air']['aqi'],self.data['data']['air']['aqi_level'],self.data['data']['air']['pm2.5']]
        self.lb_g2_middle.setText(f'空气质量：{_l2[0]}，{_l2[1]}级\nPm2.5含量{_l2[2]}')

        if  self.data['data']['alarm']:
            _la = [self.data['data']['alarm'][0]['level_name'],self.data['data']['alarm'][0]['type_name']]
            if _la[0] == '蓝色':
                self.lb_g3_left.setPixmap(QPixmap('builds\蓝色预警.png'))
                self.lb_g3_middle.setText(f'{_la[1]}蓝色预警\n-注意气象')
            if _la[0] == '黄色':
                self.lb_g3_left.setPixmap(QPixmap('builds\黄色预警.png'))
                self.lb_g3_middle.setText(f'{_la[1]}黄色预警\n-注意气象')
            if _la[0] == '橙色':
                self.lb_g3_left.setPixmap(QPixmap('builds\橙色预警.png'))
                self.lb_g3_middle.setText(f'{_la[1]}橙色预警\n-注意防护')
            if _la[0] == '红色':
                self.lb_g3_left.setPixmap(QPixmap('builds\红色预警.png'))
                self.lb_g3_middle.setText(f'{_la[1]}红色预警\n-准备防灾')
        else:
            self.lb_g3_left.setPixmap(QPixmap('builds\安全.png'))
            self.lb_g3_middle.setText(f'目前本地无预警')
        self.lb_g3_right.setPixmap(QPixmap('builds\雷达.png'))

        self.lb_g4_left.setPixmap(QPixmap('builds\雨伞.png'))
        self.lb_g4_right.setPixmap(QPixmap('builds\降水.png'))
        _ly = [self.data['data']['observe']['precipitation'],self.data['data']['observe']['humidity']]
        if int(_ly[0]) == 0:
            self.lb_g4_middle.setText(f'不带伞，湿度{_ly[1]}%')
        else:
            self.lb_g4_middle.setText(f'降水量{_ly[0]}mm 带伞\n湿度{_ly[1]}%')           

        self.lb_g5_left.setPixmap(QPixmap('builds\气压.png'))
        self.lb_g5_right.setPixmap(QPixmap('builds\压力.png'))
        _l5 = self.data['data']['observe']['pressure']
        self.lb_g5_middle.setText(f'当前大气压{_l5}Pa')       

        self.lb_g6_left.setPixmap(QPixmap('builds\紫外线强.png'))
        self.lb_g6_right.setPixmap(QPixmap('builds\防晒.png'))
        _l6 = self.data['data']['life_index']['ultraviolet']['info']
        self.lb_g6_middle.setText(f'紫外线强度: {_l6}')            


        self.lb_g7_left.setPixmap(QPixmap('builds\刷新.png'))
        self.lb_g7_right.setPixmap(QPixmap('builds\怀表.png'))
        _l7 = self.data['data']['air']['update_time']
        self.lb_g7_middle.setText(f'数据更新时间:\n{_l7}')     

        self.pbtn_refresh.setEnabled(True)
        self.pbtn_search.setEnabled(True)
        self.pbtn_next.setEnabled(True)
        self.pbtn_last.setEnabled(True)

    def get_pic(self,code):
        if code == '00' or code== '01':
            t = time.gmtime()
            # print(time.strftime('%H',t))
            if int(time.strftime('%H',t))+8 <18 and int(time.strftime('%H',t))+8 >=6:
                r = f'builds\{code}-0.png'
            else:
                r = f'builds\{code}-1.png'
            # print(r)
            return r
        elif int(code) >= 21 and int(code)<=28:
            if len(code - 14) == 1:
                r = f'builds\0{code - 14}.png'
                # print(r)
                return r    
            elif code - 14 >= 12:
                r = f'builds\{code-13}.png'
                # print(r)
                return r    

        elif len(code) <=2:
            r = f'builds\{code}.png'
            # print(r)
            return r         


    def get_wind(self,code):
        wind_level = {'1':'西北风','2':'西风','3':'西南风','4':'南风','5':'东南风','6':'东风','7':'东北风','8':'北风'}
        return wind_level[str(code)]

    def s_show(self):
        self.s_window.show()

    def search(self):
        self.page = 1   #1 = 城市界面  2 = 生活指数
        self.s_locate = str(self.s_window.edit.text()).split('，')
   

        self.wgs = [[self.g1,self.g2,self.g3,self.g4,self.g5,self.g6,self.g7],[self.lb_g1_left,self.lb_g2_left,self.lb_g3_left,self.lb_g4_left,self.lb_g5_left,self.lb_g6_left,self.lb_g7_left],[self.lb_g1_middle,self.lb_g2_middle,self.lb_g3_middle,self.lb_g4_middle,self.lb_g5_middle,self.lb_g6_middle,self.lb_g7_middle],[self.lb_g1_right,self.lb_g2_right,self.lb_g3_right,self.lb_g4_right,self.lb_g5_right,self.lb_g6_right,self.lb_g7_right],[self.lb_g1_bg,self.lb_g2_bg,self.lb_g3_bg,self.lb_g4_bg,self.lb_g5_bg,self.lb_g6_bg,self.lb_g7_bg]]
        #clear 
        for i in self.wgs[1]:
            i.setPixmap(QPixmap('builds\刷新.png'))
        for k in self.wgs[3]:
            k.setPixmap(QPixmap('builds\刷新.png'))        
        for j in self.wgs[2]:
            j.setText('Refresh....')


        self.data  = Gdata.Gweather(self.s_locate[0],self.s_locate[1])
        if self.data['code'] == 0:
            self.local_weather = [str(self.data['data']['observe']['weather']),str(self.data['data']['observe']['weather_code']),str(self.data['data']['observe']['degree']),str(self.data['data']['observe']['wind_direction']),str(self.data['data']['observe']['wind_power'])]
        else:
            self.lb_g1_middle.setText('您查找的地区无数据')
            e = self.data['code']
            self.lb_g2_middle.setText(f'Error: {e}')
            return

        # print(self.local_weather)
        self.lb_start.hide()

        # self.lb_g1_top.setPixmap(QPixmap('builds\mark.png'))
        self.lb_g1_left.setPixmap(QPixmap(str(self.get_pic(self.local_weather[1]))))
        self.lb_g1_middle.setText(f'{self.s_locate[1]}，{self.local_weather[0]}\n{self.local_weather[2]}°C，{self.get_wind(str(self.local_weather[3]))}， {self.local_weather[4]}级')
        self.lb_g1_right.setPixmap(QPixmap(str(self.get_pic(self.local_weather[3]))))

        self.lb_g2_left.setPixmap(QPixmap('builds\空气质量.png'))
        self.lb_g2_right.setPixmap(QPixmap('builds\等级.png'))
        _l2 = [self.data['data']['air']['aqi'],self.data['data']['air']['aqi_level'],self.data['data']['air']['pm2.5']]
        self.lb_g2_middle.setText(f'空气质量：{_l2[0]}，{_l2[1]}级\nPm2.5含量{_l2[2]}')

        if  self.data['data']['alarm']:
            _la = [self.data['data']['alarm'][0]['level_name'],self.data['data']['alarm'][0]['type_name']]
            if _la[0] == '蓝色':
                self.lb_g3_left.setPixmap(QPixmap('builds\蓝色预警.png'))
                self.lb_g3_middle.setText(f'{_la[1]}蓝色预警\n-注意气象')
            if _la[0] == '黄色':
                self.lb_g3_left.setPixmap(QPixmap('builds\黄色预警.png'))
                self.lb_g3_middle.setText(f'{_la[1]}黄色预警\n-注意气象')
            if _la[0] == '橙色':
                self.lb_g3_left.setPixmap(QPixmap('builds\橙色预警.png'))
                self.lb_g3_middle.setText(f'{_la[1]}橙色预警\n-注意防护')
            if _la[0] == '红色':
                self.lb_g3_left.setPixmap(QPixmap('builds\红色预警.png'))
                self.lb_g3_middle.setText(f'{_la[1]}红色预警\n-准备防灾')
        else:
            self.lb_g3_left.setPixmap(QPixmap('builds\安全.png'))
            self.lb_g3_middle.setText(f'目前{self.s_locate[1]}无预警')
        self.lb_g3_right.setPixmap(QPixmap('builds\雷达.png'))

        self.lb_g4_left.setPixmap(QPixmap('builds\雨伞.png'))
        self.lb_g4_right.setPixmap(QPixmap('builds\降水.png'))
        _ly = [self.data['data']['observe']['precipitation'],self.data['data']['observe']['humidity']]
        if int(_ly[0]) == 0:
            self.lb_g4_middle.setText(f'不带伞，湿度{_ly[1]}%')
        else:
            self.lb_g4_middle.setText(f'降水量{_ly[0]}mm 带伞\n湿度{_ly[1]}%')           

        self.lb_g5_left.setPixmap(QPixmap('builds\气压.png'))
        self.lb_g5_right.setPixmap(QPixmap('builds\压力.png'))
        _l5 = self.data['data']['observe']['pressure']
        self.lb_g5_middle.setText(f'当前大气压{_l5}Pa')       

        self.lb_g6_left.setPixmap(QPixmap('builds\紫外线强.png'))
        self.lb_g6_right.setPixmap(QPixmap('builds\防晒.png'))
        _l6 = self.data['data']['life_index']['ultraviolet']['info']
        self.lb_g6_middle.setText(f'紫外线强度: {_l6}')            


        self.lb_g7_left.setPixmap(QPixmap('builds\刷新.png'))
        self.lb_g7_right.setPixmap(QPixmap('builds\怀表.png'))
        _l7 = self.data['data']['air']['update_time']
        self.lb_g7_middle.setText(f'数据更新时间:\n{_l7}')     
        self.s_window.hide()

    def switch(self):
        if self.page == 1:
            self.page = 2       
            for i in self.wgs[1]:
                i.setPixmap(QPixmap('builds\刷新.png'))
            for k in self.wgs[3]:
                k.setPixmap(QPixmap('builds\刷新.png'))        
            for j in self.wgs[2]:
                j.setText('Refresh....')


            self.lb_g1_left.setPixmap(QPixmap('builds\空调.png'))
            if self.data['data']['life_index']['airconditioner']['detail']:
                _o1 = self.data['data']['life_index']['airconditioner']['detail']
                self.lb_g1_middle.setText(f'<font size=2>{_o1}</font>')
            else:
                _o1 = [self.data['data']['life_index']['airconditioner']['name'],self.data['data']['life_index']['airconditioner']['info']]
                self.lb_g1_middle.setText(f'<font size=2>{_o1[0]}：{_o1[1]}</font>')
            self.lb_g1_right.setPixmap(QPixmap('builds\雪花.png'))

            self.lb_g2_left.setPixmap(QPixmap('builds\衣服.png'))
            if self.data['data']['life_index']['clothes']['detail']:
                _o1 = self.data['data']['life_index']['clothes']['detail']
                self.lb_g2_middle.setText(f'<font size=2>{_o1}</font>')
            else:
                _o1 = [self.data['data']['life_index']['clothes']['name'],self.data['data']['life_index']['clothes']['info']]
                self.lb_g2_middle.setText(f'<font size=2>{_o1[0]}：{_o1[1]}</font>')
            self.lb_g2_right.setPixmap(QPixmap('builds\领带.png'))

            self.lb_g3_left.setPixmap(QPixmap('builds\钓鱼.png'))
            if self.data['data']['life_index']['fish']['detail']:
                _o1 = self.data['data']['life_index']['fish']['detail']
                self.lb_g3_middle.setText(f'<font size=2>{_o1}</font>')
            else:
                _o1 = [self.data['data']['life_index']['fish']['name'],self.data['data']['life_index']['fish']['info']]
                self.lb_g3_middle.setText(f'<font size=2>{_o1[0]}：{_o1[1]}</font>')
            self.lb_g3_right.setPixmap(QPixmap('builds\鱼.png'))

            self.lb_g4_left.setPixmap(QPixmap('builds\运动.png'))
            if self.data['data']['life_index']['carwash']['detail']:
                _o1 = self.data['data']['life_index']['carwash']['detail']
                self.lb_g4_middle.setText(f'<font size=2>{_o1}</font>')
            else:
                _o1 = [self.data['data']['life_index']['carwash']['name'],self.data['data']['life_index']['carwash']['info']]
                self.lb_g4_middle.setText(f'<font size=2>{_o1[0]}：{_o1[1]}</font>')
            self.lb_g4_right.setPixmap(QPixmap('builds\哑铃.png'))

            self.lb_g5_left.setPixmap(QPixmap('builds\洗车.png'))
            if self.data['data']['life_index']['sports']['detail']:
                _o1 = self.data['data']['life_index']['sports']['detail']
                self.lb_g5_middle.setText(f'<font size=2>{_o1}</font>')
            else:
                _o1 = [self.data['data']['life_index']['sports']['name'],self.data['data']['life_index']['sports']['info']]
                self.lb_g5_middle.setText(f'<font size=2>{_o1[0]}：{_o1[1]}</font>')
            self.lb_g5_right.setPixmap(QPixmap('builds\气泡.png'))

            self.lb_g6_left.setPixmap(QPixmap('builds\防晒喷雾.png'))
            if self.data['data']['life_index']['sunscreen']['detail']:
                _o1 = self.data['data']['life_index']['sunscreen']['detail']
                self.lb_g6_middle.setText(f'<font size=2>{_o1}</font>')
            else:
                _o1 = [self.data['data']['life_index']['sunscreen']['name'],self.data['data']['life_index']['sunscreen']['info']]
                self.lb_g6_middle.setText(f'<font size=2>{_o1[0]}：{_o1[1]}</font>')
            self.lb_g6_right.setPixmap(QPixmap('builds\太阳镜.png'))

            self.lb_g7_left.setPixmap(QPixmap('builds\旅游.png'))
            if self.data['data']['life_index']['tourism']['detail']:
                _o1 = self.data['data']['life_index']['tourism']['detail']
                self.lb_g7_middle.setText(f'<font size=2>{_o1}</font>')
            else:
                _o1 = [self.data['data']['life_index']['tourism']['name'],self.data['data']['life_index']['tourism']['info']]
                self.lb_g7_middle.setText(f'<font size=2>{_o1[0]}：{_o1[1]}</font>')
            self.lb_g7_right.setPixmap(QPixmap('builds\美食.png'))


        elif self.page == 2:
            self.page = 1
            self.lb_g1_left.setPixmap(QPixmap(str(self.get_pic(self.local_weather[1]))))
            try:
                self.lb_g1_middle.setText(f'{self.s_locate[1]}，{self.local_weather[0]}\n{self.local_weather[2]}°C，{self.get_wind(str(self.local_weather[3]))}， {self.local_weather[4]}级')
            except:
                self.lb_g1_middle.setText(f'{self.locate[1]}，{self.local_weather[0]}\n{self.local_weather[2]}°C，{self.get_wind(str(self.local_weather[3]))}， {self.local_weather[4]}级')
            self.lb_g1_right.setPixmap(QPixmap(str(self.get_pic(self.local_weather[3]))))

            self.lb_g2_left.setPixmap(QPixmap('builds\空气质量.png'))
            self.lb_g2_right.setPixmap(QPixmap('builds\等级.png'))
            _l2 = [self.data['data']['air']['aqi'],self.data['data']['air']['aqi_level'],self.data['data']['air']['pm2.5']]
            self.lb_g2_middle.setText(f'空气质量：{_l2[0]}，{_l2[1]}级\nPm2.5含量{_l2[2]}')

            if  self.data['data']['alarm']:
                _la = [self.data['data']['alarm'][0]['level_name'],self.data['data']['alarm'][0]['type_name']]
                if _la[0] == '蓝色':
                    self.lb_g3_left.setPixmap(QPixmap('builds\蓝色预警.png'))
                    self.lb_g3_middle.setText(f'{_la[1]}蓝色预警\n-注意气象')
                if _la[0] == '黄色':
                    self.lb_g3_left.setPixmap(QPixmap('builds\黄色预警.png'))
                    self.lb_g3_middle.setText(f'{_la[1]}黄色预警\n-注意气象')
                if _la[0] == '橙色':
                    self.lb_g3_left.setPixmap(QPixmap('builds\橙色预警.png'))
                    self.lb_g3_middle.setText(f'{_la[1]}橙色预警\n-注意防护')
                if _la[0] == '红色':
                    self.lb_g3_left.setPixmap(QPixmap('builds\红色预警.png'))
                    self.lb_g3_middle.setText(f'{_la[1]}红色预警\n-准备防灾')
            else:
                self.lb_g3_left.setPixmap(QPixmap('builds\安全.png'))
                try:
                    self.lb_g3_middle.setText(f'目前{self.s_locate[1]}无预警')
                except:
                    self.lb_g3_middle.setText(f'目前{self.locate[1]}无预警')

            self.lb_g3_right.setPixmap(QPixmap('builds\雷达.png'))

            self.lb_g4_left.setPixmap(QPixmap('builds\雨伞.png'))
            self.lb_g4_right.setPixmap(QPixmap('builds\降水.png'))
            _ly = [self.data['data']['observe']['precipitation'],self.data['data']['observe']['humidity']]
            if int(_ly[0]) == 0:
                self.lb_g4_middle.setText(f'不带伞，湿度{_ly[1]}%')
            else:
                self.lb_g4_middle.setText(f'降水量{_ly[0]}mm 带伞\n湿度{_ly[1]}%')           

            self.lb_g5_left.setPixmap(QPixmap('builds\气压.png'))
            self.lb_g5_right.setPixmap(QPixmap('builds\压力.png'))
            _l5 = self.data['data']['observe']['pressure']
            self.lb_g5_middle.setText(f'当前大气压{_l5}Pa')       

            self.lb_g6_left.setPixmap(QPixmap('builds\紫外线强.png'))
            self.lb_g6_right.setPixmap(QPixmap('builds\防晒.png'))
            _l6 = self.data['data']['life_index']['ultraviolet']['info']
            self.lb_g6_middle.setText(f'紫外线强度: {_l6}')            


            self.lb_g7_left.setPixmap(QPixmap('builds\刷新.png'))
            self.lb_g7_right.setPixmap(QPixmap('builds\怀表.png'))
            _l7 = self.data['data']['air']['update_time']
            self.lb_g7_middle.setText(f'数据更新时间:\n{_l7}')     



'''     
    def copy_group(self,name=list,x=int,y=int):
  # name = [self.g1,self.lb_g1_left,self.lb_g1_middle,self.lb_g1_right,self.lb_g1_bg]
        objname = [str(i).split('.')[1] for i in name]
        name[0] = QGroupBox(self.centralwidget)
        name[0].setObjectName(objname[0])
        name[0].setGeometry(QRect(x, y, 400, 110))
        name[0].setMinimumSize(QSize(400, 110))
        name[0].setMaximumSize(QSize(400, 110))
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1 Light")
        name[0].setFont(font1)
        name[1] = QLabel(name[0])
        name[1].setObjectName(objname[1])
        name[1].setGeometry(QRect(x+20, y+20, 60, 60))
        name[1].setMinimumSize(QSize(55, 55))
        name[1].setMaximumSize(QSize(70, 70))
        name[1].setScaledContents(True)
        name[2] = QLabel(name[0])
        name[2].setObjectName(objname[2])
        name[2].setGeometry(QRect(x+100, y+20, 170, 70))
        name[2].setMinimumSize(QSize(170, 70))
        name[2].setMaximumSize(QSize(170, 70))
        name[2].setScaledContents(True)
        name[3] = QLabel(name[0])
        name[3].setObjectName(objname[3])
        name[3].setGeometry(QRect(x+300, y+20, 50, 50))
        name[3].setMinimumSize(QSize(50, 50))
        name[3].setMaximumSize(QSize(70, 70))
        name[3].setScaledContents(True)
        name[4] = QLabel(name[0])
        name[4].setObjectName(objname[4])
        name[4].setGeometry(QRect(x-10, y+10, 400, 90))
        name[4].setMinimumSize(QSize(400, 90))
        name[4].setMaximumSize(QSize(400, 110))
        name[4].setScaledContents(True)
        name[1].raise_()
        name[2].raise_()
        name[3].raise_()
        name[4].raise_()
        name[0].raise_()
        name[1].setText("")
        name[2].setText("")
        name[3].setText("")
        name[4].setText("")
'''


'''----==--==#-*-并不华丽的分割线-*-#==--==----'''

class Tray(QSystemTrayIcon,main):
    def __init__(self):
        super().__init__()
        self.setup()
        self.show()
        self.is_window_show = '显示'
        

    def setup(self):

        icon = QIcon('builds\cloud.png')
        self.setIcon(icon)

        self.menu = QMenu()
        #创建一个功能
        #tiggered参数若不填，则有显示信息作用
        #下面这行代码#得到一个功能选项的对象 参数['功能选项上面显示的文字&符号','图标对象','传入要激活功能选项(要实现的函数)']  
        action = QAction(f'-WEWS- 丨{__version__}',self,icon=QIcon('builds\刷新.png')) 
        self.menu.addAction(action) #加入这个功能到menu菜单中
        #顺序由添加顺序决定 , 自上而下
        action2 = QAction('查询天气', self,icon=QIcon('builds\search.png'),triggered=self.search)
        self.menu.addAction(action2)
        action3 = QAction('显示/隐藏 - show/hide',self,icon=QIcon('builds\show.png'),triggered=self.show_or_hide)
        self.menu.addAction(action3)
        action4 = QAction('退出 - exit',self,icon=QIcon('builds\exit.png'),triggered=self.exit)       #,triggered=
        self.menu.addAction(action4)
        #把menu传入系统托盘当中
        self.setContextMenu(self.menu)


    def show_or_hide(self):
        if self.is_window_show == '隐藏':
            self.is_window_show = '显示'
            main.show(window)
        elif self.is_window_show == '显示':
            self.is_window_show = '隐藏'
            main.hide(window)
        
    def exit(self):
        main.hide(window)
        self.hide()
        sys.exit()

    def search(self):
        main.search(self=main)


class search_window(QDialog,main):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("查询")
        self.setWindowIcon(QIcon('builds\search.png'))

        #创建窗口
        self.edit = QLineEdit("例：上海，上海")
        self.button = QPushButton("确定")

        #创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        #设置布局
        self.setLayout(layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main()
    sys.exit(app.exec_())

'''{'00':'晴'
    ,'01':'多云'
    ,'02':'阴'
    ,'03':'阵雨'
    ,'04':'雷阵雨'
    ,'05':'雷阵雨伴有冰雹'
    ,'06':'雨夹雪'
    ,'07':'小雨'
    ,'08':'中雨'
    ,'09':'大雨'
    ,'10':'暴雨'
    ,'11':'大暴雨'
    ,'12':'特大暴雨'
    ,'13':'阵雪'
    ,'14':'小雪'
    ,'15':'中雪'
    ,'16':'大雪'
    ,'17':'暴雪'
    ,'18':'雾'
    ,'19':'冻雨'
    ,'20':'沙尘暴'
    ,'21':'小雨-中雨'
    ,'22':'中雨-大雨'
    ,'23':'大雨-暴雨'
    ,'24':'暴雨-大暴雨'
    ,'25':'大暴雨-特大暴雨'
    ,'26':'小雪-中雪'
    ,'27':'中雪-大雪'
    ,'28':'大雪-暴雪'
    ,'29':'浮尘'
    ,'30':'扬沙'
    ,'31':'强沙尘暴'
    ,'32':'霾'}
'''
