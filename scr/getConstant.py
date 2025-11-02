import os.path,sys


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

def getConstant(strength_concrete,strength_steelbar):
    # _as = float(input('请输入计算的as值（mm）：'))
    # h = float(input('请输入梁的高度（mm）：'))
    # b = float(input('请输入梁的宽度（mm）：'))
    # strength_concrete = input('请输入混凝土强度等级:(例：C30)')
    # strength_steelbar = input('请输入钢筋强度等级:(例：HPB300)')
    fc, ft, ftk, Ec=search_conctete_strength(strength_concrete)
    fy, fyk, Es=search_steelbar_strength(strength_steelbar)
    epsilon_b=search_epsilon(strength_concrete,strength_steelbar)
    a1,b1=search_a1b1(strength_concrete)
    return fc, ft, ftk, Ec,fy, fyk, Es,epsilon_b,a1,b1

def search_conctete_strength(strength_concrete):
    concrete = open(processPath('csv\\concrete.csv'), 'r')
    ls_c=[]
    for line in concrete:
        line = line.replace("\n", '')
        line = line.split(',')
        if line[0] == strength_concrete:
            ls_c = line
    concrete.close()
    fc = float(ls_c[1])
    ft = float(ls_c[2])
    ftk = float(ls_c[3])
    Ec = float(ls_c[4])
    return fc, ft, ftk, Ec

def search_steelbar_strength(strength_steelbar):
    steelbar = open(processPath('csv\\steelbar.csv'), 'r')
    ls_s = []
    for line in steelbar:
        line = line.replace("\n", '')
        line = line.split(',')
        if line[0] == strength_steelbar:
            ls_s = line
    steelbar.close()
    fy = float(ls_s[1])
    fyk = float(ls_s[2])
    Es = float(ls_s[3])
    return fy,fyk,Es

def search_epsilon(strength_concrete,strength_steelbar):
    epsilon=open(processPath('csv\\epsilon_b.csv'),'r')
    ls_e = []
    for line in epsilon:
        line = line.replace("\n", '')
        line = line.split(',')
        if line[0] == strength_steelbar:
            ls_e = line
    level=strength_concrete[1:]
    if level<='50':
        epsilon_b=ls_e[1]
    elif level=='60':
        epsilon_b=ls_e[2]
    elif level=='70':
        epsilon_b=ls_e[3]
    elif level=='80':
        epsilon_b=ls_e[4]
    epsilon_b=float(epsilon_b)
    return epsilon_b

def search_a1b1(strength_concrete):
    level = strength_concrete[1:]
    if level <= '50':
        a1=1
        b1=0.8
    elif level == '60':
        a1 =0.98
        b1 =0.78
    elif level == '70':
        a1 =0.96
        b1 =0.76
    elif level == '80':
        a1 =0.94
        b1 =0.74
    return a1, b1

def search_fai(l0,b):
    k=l0 / b
    fai, fai_u, fai_d = None, None, None
    if k<=8:
        fai=1
    elif k>=50:
        fai=0.19
    else:
        _fai = open(processPath('csv\\fai.csv'), 'r',encoding='UTF-8-sig')
        for line in _fai:
            line = line.replace("\n", '')
            line = line.split(',')
            if line[0]:
                if eval(line[0]) == k:
                    fai = eval(line[1])
                else:
                    if eval(line[0]) == int(k):
                        fai_d=eval(line[1])
                    if eval(line[0]) == int(k)+1:
                        fai_u=eval(line[1])
                    if fai_d and fai_u:
                        fai = fai_u + (k - int(k)) * (fai_d - fai_u)
        _fai.close()

    fai=round(fai,2)
    return fai


search_fai(3300,400)