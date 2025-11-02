import os.path,sys
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtCore
from PyQt5.QtGui import QIcon
from io import StringIO

# 创建一个字符串缓冲区来替代默认的标准输出
buffer = StringIO()
sys.stdout = buffer
def processPath(path):
    '''
    :param path: 相对于根目录的路径
    :return: 拼接好的路径
    '''
    if getattr(sys, 'frozen', False):  # 判断是否存在属性frozen，以此判断是打包的程序还是源代码。false为默认值，即没有frozen属性时返回false
        base_path = sys._MEIPASS #该属性也是打包程序才会有，源代码尝试获取该属性会报错
    else:
        base_path = os.path.abspath(".") # 当源代码运行时使用该路径
    return os.path.join(base_path, path)

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    #读取ui界面信息
    def init_ui(self):
        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle("偏心受压构件计算器")
        # self.ui = uic.loadUi('compression_design.ui')
        self.ui = uic.loadUi(processPath('compression_design.ui'))
        # print(self.ui.__dict__)  # 查看ui文件中有哪些控件

        # 非对称截面设计
        # 参数
        self._as = self.ui._as
        self.h = self.ui.h
        self.b = self.ui.b
        self.c_level = self.ui.c_level
        self.s_level = self.ui.s_level
        self.Asp = self.ui.Asp
        self.Asp.setVisible(False)
        self.lc = self.ui.lc
        self.M1 = self.ui.M1
        self.M2 = self.ui.M2
        self.N = self.ui.N
        # 控件
        self.Asp_lable = self.ui.Asp_lable
        self.Asp_lable.setVisible(False)
        self.show_As_an = self.ui.show_As_an #As计算结果展示
        self.show_Asp_an = self.ui.show_Asp_an #Asp计算结果展示
        self.show_process_ansymmetric = self.ui.show_process_ansymmetric  # 计算过程展示
        self.calculate_an = self.ui.calculate_an #开始运算
        self.of = self.ui.checkBox
        # 绑定信号与槽函数
        self.calculate_an.clicked.connect(self.f_calculate_ansymmetric)
        self.of.stateChanged.connect(self.h_w)

        # 对称截面设计
        # 参数
        self._as_2 = self.ui._as_2
        self.h_2 = self.ui.h_2
        self.b_2 = self.ui.b_2
        self.c_level_2 = self.ui.c_level_2
        self.s_level_2 = self.ui.s_level_2
        self.lc_2 = self.ui.lc_2
        self.M1_2 = self.ui.M1_2
        self.M2_2 = self.ui.M2_2
        self.N_2 = self.ui.N_2
        # 控件
        self.show_As = self.ui.show_As  # As计算结果展示
        self.show_process_symmetric = self.ui.show_process_symmetric  # 计算过程展示
        self.calculate_As = self.ui.calculate_As  # 开始运算
        # 绑定信号与槽函数
        self.calculate_As.clicked.connect(self.f_calculate_symmetric)

        # 截面核验
        self._as_4 = self.ui._as_4
        self.h_4 = self.ui.h_4
        self.b_4 = self.ui.b_4
        self.c_level_4 = self.ui.c_level_4
        self.s_level_4 = self.ui.s_level_4
        self.As_4 = self.ui.As_4
        self.Asp_4 = self.ui.Asp_4
        self.lc_4 = self.ui.lc_4
        self.M1_M2 = self.ui.M1_M2
        self.change = self.ui.change
        self.label_m1m2=self.ui.label_m1m2
        self.label_change=self.ui.label_change
        self.label_43=self.ui.label_43
        # 控件
        self.show_M2 = self.ui.show_M2  # As计算结果展示
        self.show_process_check = self.ui.show_process_check  # 计算过程展示
        self.calculate_M2 = self.ui.calculate_M2  # 开始运算
        self.checkBox_n=self.ui.checkBox_n
        # 绑定信号与槽函数
        self.checkBox_n.stateChanged.connect(self.h_w_n)
        self.calculate_M2.clicked.connect(self.f_calculate_check)

    #槽函数
    def h_w(self,state) :
        if state == 2:
            self.Asp.setVisible(True)
            self.Asp_lable.setVisible(True)
        else:
            self.Asp.hide()
            self.Asp_lable.hide()

    def h_w_n(self, state):
        if state == 2:
            self.label_change.setText('轴力N（KN）')
            self.label_m1m2.setVisible(True)
            self.M1_M2.setVisible(True)
            self.label_43.setText('能承载M(KNm)')
        else:
            self.label_change.setText('偏心距e0(mm)')
            self.label_m1m2.hide()
            self.M1_M2.hide()
            self.label_43.setText('能承载N(KN)')

    def f_calculate_ansymmetric(self):
        self.show_process_ansymmetric.clear()
        _as = self._as.text()
        h= self.h.text()
        b= self.b.text()
        c_level= self.c_level.currentText()
        s_level= self.s_level.currentText()
        Asp = self.Asp.text()
        lc = self.lc.text()
        M1 = self.M1.text()
        M2 = self.M2.text()
        N = self.N.text()
        # print('测试点:参数获取成功')
        # test:
        # _as, h, b, lc, M1, M2, N, Asp = 40, 500, 300, 6000, 250.9, 250.9, 160, 1520
        # c_level, s_level = 'C30', 'HRB400'
        try:
            if _as and h and b and lc and M1 and M2 and N != '':
                _as, h, b, lc, M1, M2, N= float(_as), float(h), float(b), float(lc), float(M1),float(M2), float(N)
                if Asp == '':
                    Asp = None
                else:
                    Asp = float(Asp)

                from getConstant import getConstant
                fc, ft, ftk, Ec, fy, fyk, Es, ξb,  α1, β1 = getConstant(c_level, s_level)

                # print('测试点：查询参数成功')
                h0 = h - _as  # 截面有效高度

                from asymmetrical_rc_eccentric_compression import pianxin_rc
                try:
                    As,Asp = pianxin_rc(b,h,lc,N,M1,M2,_as,fc,ft,fy,α1,β1,ξb,Asp)
                except TypeError:
                    buffer.truncate(0)
                    buffer.seek(0)
                    print("数据类型错误")
                    As=Asp= "False"
                except ArithmeticError:
                    buffer.truncate(0)
                    buffer.seek(0)
                    print("过程中出现计算错误，数据不合理！")
                    As=Asp= "False"
                except:
                    buffer.truncate(0)
                    buffer.seek(0)
                    print("出现未知错误！")
                    As=Asp= "False"

                # print('测试点：获取As，Asp成功')

                #输出结果
                output = buffer.getvalue()
                self.show_process_ansymmetric.setText(output)
                self.show_process_ansymmetric.repaint()
                self.show_As_an.setText(str(As))
                self.show_As_an.repaint()
                self.show_Asp_an.setText(str(Asp))
                self.show_Asp_an.repaint()
            else:
                self.show_process_ansymmetric.setText('参数不能为空')
                self.show_process_ansymmetric.repaint()
        except:
            buffer.truncate(0)
            buffer.seek(0)
            print("数据类型错误")
            As = Asp = "False"
            output = buffer.getvalue()
            self.show_process_ansymmetric.setText(output)
            self.show_process_ansymmetric.repaint()
            self.show_As_an.setText(str(As))
            self.show_As_an.repaint()
            self.show_Asp_an.setText(str(Asp))
            self.show_Asp_an.repaint()
        buffer.truncate(0)
        buffer.seek(0)

    def f_calculate_symmetric(self):
        self.show_process_symmetric.clear()
        _as = self._as_2.text()
        h = self.h_2.text()
        b = self.b_2.text()
        c_level = self.c_level_2.currentText()
        s_level = self.s_level_2.currentText()
        lc = self.lc_2.text()
        M1 = self.M1_2.text()
        M2 = self.M2_2.text()
        N = self.N_2.text()
        # print('测试点:参数获取成功')
        # test:
        _as, h, b, lc, M1, M2, N = 45, 700, 400, 3300, 0.88*350, 350, 3500
        c_level, s_level = 'C40', 'HRB400'
        try:
            if _as and h and b and lc and M1 and M2 and N != '':
                _as, h, b, lc, M1, M2, N = float(_as), float(h), float(b), float(lc), float(M1), float(M2), float(N)

                from getConstant import getConstant
                fc, ft, ftk, Ec, fy, fyk, Es, ξb, α1, β1 = getConstant(c_level, s_level)

                # print('测试点：查询参数成功')
                h0 = h - _as  # 截面有效高度

                from symmetrical_rc_compression import pianxin_rc
                try:
                    As= pianxin_rc(b, h, lc, N, M1, M2, _as, fc, ft, fy, α1, β1, ξb)
                except TypeError:
                    buffer.truncate(0)
                    buffer.seek(0)
                    print("数据类型错误1")
                    As = "False"
                except ArithmeticError:
                    buffer.truncate(0)
                    buffer.seek(0)
                    print("过程中出现计算错误，数据不合理！")
                    As = "False"
                except:
                    buffer.truncate(0)
                    buffer.seek(0)
                    print("出现未知错误！")
                    As = "False"
                # print('测试点：获取As成功')

                # 输出结果
                output = buffer.getvalue()
                self.show_process_symmetric.setText(output)
                self.show_process_symmetric.repaint()
                self.show_As.setText(str(As))
                self.show_As.repaint()

            else:
                self.show_process_symmetric.setText('参数不能为空')
                self.show_process_symmetric.repaint()
        except:
            buffer.truncate(0)
            buffer.seek(0)
            print("数据类型错误2")
            As = "False"
            output = buffer.getvalue()
            self.show_process_symmetric.setText(output)
            self.show_process_symmetric.repaint()
            self.show_As.setText(str(As))
            self.show_As.repaint()
        buffer.truncate(0)
        buffer.seek(0)

    def f_calculate_check(self):
        self.show_process_check.clear()
        _as_4 = self._as_4.text()
        h_4 = self.h_4.text()
        b_4 = self.b_4.text()
        c_level_4 = self.c_level_4.currentText()
        s_level_4 = self.s_level_4.currentText()
        As_4 = self.As_4.text()
        Asp_4 = self.Asp_4.text()
        lc_4 = self.lc_4.text()
        M1_M2 = self.M1_M2.text()
        e0=self.change.text()
        N=self.change.text()
        # sys.stdout = sys.__stdout__
        # print('测试点:参数获取成功')
        # test:
        # _as_4, h_4, b_4, lc_4,As_4,Asp_4,e0,N=40,600,400,4000,1256,1520,1200,1200
        # c_level_4, s_level_4 = 'C40', 'HRB400'
        # M1_M2=0.85
        from getConstant import getConstant
        fc, ft, ftk, Ec, fy, fyk, Es, ξb, α1, β1 = getConstant(c_level_4, s_level_4)
        try:
            if _as_4 and h_4 and b_4 and lc_4 and As_4 and Asp_4 and e0 and N!= '':
                _as, h, b, lc,As,Asp,e0,N = float(_as_4), float(h_4), float(b_4), float(lc_4),float(As_4),float(Asp_4),float(e0),float(N)
                # print('测试点：查询参数成功')
                h0 = h - _as  # 截面有效高度
                if self.checkBox_n.isChecked():
                    # print("测试")
                    if M1_M2 == '':
                        output="参数不能为空"
                        OUT="false"
                    else:
                        M1_M2 = float(M1_M2)
                        from rc_check import known_n
                        try:
                            OUT=known_n( b, h, lc, N, _as, fc, ft, fy, α1, β1, ξb, As, Asp, M1_M2)
                        except TypeError:
                            buffer.truncate(0)
                            buffer.seek(0)
                            print("数据类型错误")
                            OUT = "False"
                        except ArithmeticError:
                            buffer.truncate(0)
                            buffer.seek(0)
                            print("过程中出现计算错误，数据不合理！")
                            OUT = "False"
                        except:
                            buffer.truncate(0)
                            buffer.seek(0)
                            print("出现未知错误！")
                            OUT = "False"
                else:
                    from rc_check import known_e0
                    try:
                        OUT=known_e0(b, h, lc, e0, _as, fc, ft, fy, α1, β1, ξb, As, Asp)
                    except TypeError:
                        buffer.truncate(0)
                        buffer.seek(0)
                        print("数据类型错误")
                        OUT="False"
                    except ArithmeticError:
                        buffer.truncate(0)
                        buffer.seek(0)
                        print("过程中出现计算错误，数据不合理！")
                        OUT = "False"
                    except:
                        buffer.truncate(0)
                        buffer.seek(0)
                        print("出现未知错误！")
                        OUT = "False"

                # print('测试点：获取As，Asp成功')

                # 输出结果
                output = buffer.getvalue()
                self.show_process_check.setText(output)
                self.show_process_check.repaint()
                self.show_M2.setText(str(OUT))
                self.show_M2.repaint()
            else:
                self.show_process_check.setText('参数不能为空')
                self.show_process_check.repaint()
        except:
            buffer.truncate(0)
            buffer.seek(0)
            print("数据类型错误")
            OUT = "False"
            output = buffer.getvalue()
            self.show_process_check.setText(output)
            self.show_process_check.repaint()
            self.show_M2.setText(str(OUT))
            self.show_M2.repaint()
        buffer.truncate(0)
        buffer.seek(0)

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app=QApplication(sys.argv)
    w=MyWindow()
    w.ui.show()
    sys.exit(app.exec())