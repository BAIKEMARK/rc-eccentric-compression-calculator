
def pianxin_rc(b,h,lc,N,M1,M2,_as,fc,ft,fy,α1,β1,ξb):
    # 计算相关参数

    fyp = fy  # 一般As，Asp钢筋取同种
    h0 = h - _as
    ea=max(round(h/30,3),20)
    A=b*h
    N=N*1000#单位转换：KN->N
    M1,M2=M1*1000000,M2*1000000#单位转换：KN*m->N*mm
    _asp=_as

    print( '[解]:' + '\n' + '压弯计算' + '\n' + '1)截面几何信息:')
    print( 'b={}mm,h={}mm;'.format(b, h))
    print( '计算长度lc = {}mm; as ={}mm,'.format(lc,_as))
    print( ('h0 = h - as ={} - {} = {} mm;'.format(h,_as,h0)))
    print(('ea = max(h / 30, 20) =max({}, 20)= {}mm;'.format(round(h/30,3),ea)))
    print( '')

    print('2)材料强度信息:')
    print( 'fc={}MPa,ft={}MPa,fy={}MPa;'.format(fc, ft, fy))
    print( '')

    print('3)内力信息:')
    print( ('M1 = {} N·mm, '"\n"
                 'M2 = {} N·mm, '"\n"
                                  'N = {}N;'.format(M1,M2,N)))
    print( '')

    print( '4)二阶效应计算信息:')
    print( ('①  M1 / M2 - 0.9  = {};'.format(round(M1 / M2 - 0.9,3))))
    print( ('②  轴压比:  ''\n'
                 'N / (fc*A) - 0.9 ''\n'
                 '= {} / ({} * {}) - 0.9 = {};'.format(N,fc,A,round(N / (fc*A) - 0.9,3))))
    print( ('③  lc / i - 34 + 12(M1 / M2) ''\n'
                 '= {} / (0.289 * {}) - 34 + 12 * {} = {};'
                 .format(lc,h,round(M1/M2,3),round((lc /(0.289*h))-34+12*(M1/M2),3))))
    if M1 / M2 - 0.9> 0 or N / (fc*A) - 0.9>0 or lc / (0.289*h) - 34 + 12*(M1 / M2)>0:
        print( '由于①②③中有一条件满足 > 0, 所以必须考虑二阶效应.')
        print( '')
        Cm = round(0.7 + 0.3 * (M1 / M2),3)
        print( ('Cm = 0.7 + 0.3*(M1 / M2) = 0.7 + 0.3 * {} = {};'.format(round(M1 / M2,3), round(0.7 + 0.3 * (M1 / M2),3))))
        if Cm <0.7:
            Cm=0.7
            print( '由于Cm < 0.7, 所以取Cm = 0.7;')

        ζc = min(0.5 / (N / (fc * A)),1)
        print( ('ζc = 0.5 / (N / (fc * A)) = 0.5 / {} = {};'.format(round(N / (fc * A),3),round(0.5 / (N / (fc * A)),3))))
        if ζc ==1 :
            print( '由于0.5 / (N / (fc * A)) >= 1, 所以取ζc = 1;')

        ηns = round(1 + (lc / h) * (lc / h) * ζc / (1300 * (M2 / N + ea) / h0),3)
        print( ('ηns =1+(lc/h)*(lc/h)*ζc/(1300*(M2/N+ea)/h0)={}'.format(ηns)))
        Cm_ηns = round(Cm * ηns, 3)
        print( ('Cm * ηns = {} * {} = {};'.format(Cm ,ηns,Cm * ηns)))
        if Cm * ηns < 1.0:
            Cm_ηns=1
            print( '由于Cm * ηns < 1.0, 所以取Cm * ηns = 1.0;')

        M = round(Cm_ηns * M2,3)
        e0=round(M/N,3)
        print( ('M = Cm * ηns * M2 ''\n'
                     '= {} * {} = {}N·mm;'.format(Cm_ηns,M2,M)))
        print( ('e0=M/N={};'.format(e0)))
        print( '')

    else:
        print( '由于①②③均满足< 0, 所以不需要考虑二阶效应;')
        M = M2
        e0 = round(M2 / N,3)
        print( ('M = M2 = {}N·mm;'.format(M2)))
        print( ('e0=M2/N={};'.format(e0)))
        print( '')


    print( '5)采用对称配筋的方法计算配筋:')
    ei=round(e0+ea,3)
    e=round(ei+h/2-_as,3)
    print( ('ei = e0 + ea = {} + {} = {}mm;'.format(e0,ea,ei)))
    print( ('e = ei + h / 2 - as ''\n'
                 '={} +{} / 2 - {} = {}mm;'.format(ei,h,_as,e)))
    ep=h/2-ei-_as
    print( "e'=h/2-ei-as'={}/2-{}-{}={}mm;".format(h,ei,_as,ep))
    x = round(N / (α1 * fc * b))
    print("x =N/(α1*fc*b)={}/({}*{}*{})={}mm;".format(N,α1,fc,b,x))
    xb = round(ξb*h0)
    print("xb=ξb*h0={}*{}={}mm".format(ξb,h0,xb))
    ρmin = round(max(45 * (ft / fy) * 0.01, 0.2 * 0.01), 3)
    print("ρmin =",ρmin)
    As_min=round(ρmin*b*h)
    print("As_min=ρmin*b*h={}mm2".format(As_min))
    if x<=xb:
        print( ('由于x>xb, 属于大偏压情况;'))
        if x>=2*_as:
            print("因为x>=2*_as'={}mm".format(2*_as))
            As=Asp=round((N*e-α1*fc*b*x*(h0-x/2))/(fy*(h0-_as)))
            print("As=As'=(N*e-α1*fc*b*x*(h0-x/2))/(fy'*(h0-as'))="
                       "({}-{}*({}))/({}*({}))={}mm2".format(N*e,α1*fc*b*x,(h0-x/2),fy,(h0-_as),As))
            if As >= As_min:
                print( ('由于As >= As_min={},满足最小配筋率要求，所以As={};'.format(As_min, As)))
            else:
                As = As_min
                print( ('由于As < As_min={},不满足最小配筋率要求，所以取As={};'.format(As_min, As)))
            print( '')
        else:
            print( ("由于x<2*as'={},按式（5-32）计算As：;".format(2 * _asp)))
            As1 = round(N * (ei - 0.5 * h + _asp) / (fy * (h0 - _asp)))
            print( ("As=N*(ei-0.5*h+as') / (fy*(h0-as'))"'\n'
                         '={}*({}-0.5*{}+{}) / ({}*({}-{}))={}'.format(N, ei, h, _asp, fy, h0, _asp, As1)))
            if As1 >= As_min:
                print( ('由于As >= As_min={},满足最小配筋率要求，所以As={};'.format(As_min, As1)))
            else:
                As1 = As_min
                print( ('由于As < As_min={},不满足最小配筋率要求，所以取As={};'.format(As_min, As1)))
            print( '')
            print( "如果按不考虑受压钢筋As’的情况(即As'=0)进行计算：")
            Mu2 = N * e
            print( 'Mu2=N*e={}*{}={}'.format(N, e, Mu2))
            αs = round(Mu2 / (α1 * fc * b * (h0 ** 2)), 3)
            print( ('αs=Mu2/(α1*fc*b*(h0**2))={}'.format(αs)))

            ξ = round(1 - (1 - 2 * αs) ** 0.5, 3)
            print( ('ξ=1-(1-2*αs)**0.5={}'.format(ξ)))
            x = ξ * h0
            print( ('x=ξ*h0={}mm'.format(x)))
            As2 = round((α1 * fc * b * x - N) / fy)
            print( ('As=(α1 * fc * b * x - N) / fy={}'.format(As2)))
            if As2 >= As_min:
                print( ('由于As >= As_min={},满足最小配筋率要求，所以As={};'.format(As_min, As2)))
            else:
                As2 = As_min
                print( ('由于As < As_min={},不满足最小配筋率要求，所以取As={};'.format(As_min, As2)))
            if As1 >= As2:
                As = As2
                print( ('由于As1={} >= As2={},说明本题如不考虑受压钢筋，受拉钢筋As会得到较大数值。因此本题取As={}mm2来配筋;'.format(As1, As2, As)))
            else:
                As = As1
                print( ('由于As1={} < As2={},说明本题如不考虑受压钢筋，受拉钢筋As可以得到较小数值。因此本题取As={}mm2来配筋;'.format(As1, As2, As)))
    else:
        print( ('由于x>xb, 属于小偏压情况;'))
        print("按简化计算方法（近似公式法）计算。")
        print("由β1={}和式（5-44），求ξ")
        Np= round(ξb*α1*fc*b*h0)
        _k=round((N*e-0.431*α1*fc*b*h0*h0)/((β1-ξb)*(h0-_as)))
        ξ= round(((N-Np)/(_k+α1*fc*b*h0))+ξb,3)
        print("Np=ξb*α1*fc*b*h0={}*{}*{}*{}*{}={}".format(ξb,α1,fc,b,h0,Np))
        print( "_k=(N*e-0.431*α1*fc*b*h0*h0)/((β1-ξb)*(h0-_as))=({}-{})/({}*{})={}"
              .format(N*e,round(0.431*α1*fc*b*h0*h0),round(β1-ξb,3),(h0-_as),_k))
        print( "ξ=((N-Np)/(_k+α1*fc*b*h0))+ξb=(({}-{})/({}+{}))+{}={}".format(N,Np,_k,round(α1*fc*b*h0),ξb,ξ))
        x=ξ*h0
        print("x=ξ*h0={}*{}={}mm".format(ξ,h0,x))
        As = Asp = round((N * e - α1 * fc * b * x * (h0 - x / 2)) / (fy * (h0 - _as)))
        print( "As=As'=(N*e-α1*fc*b*x*(h0-x/2))/(fy'*(h0-as'))="
                    "({}-{}*({}))/({}*({}))={}mm2"
              .format(N * e, round(α1 * fc * b * x), (h0 - x / 2), fy, (h0 - _as), As))
        if As >= As_min:
            print(('由于As >= As_min={},满足最小配筋率要求，所以As={};'.format(As_min, As)))
        else:
            As = As_min
            print(('由于As < As_min={},不满足最小配筋率要求，所以取As={};'.format(As_min, As)))
        print('')
    Asp=As
    check(N, _as, h, h0, fc, As, Asp, b, ρmin, lc, fy)
    return As

def check( N, _as, h, h0, fc, As, Asp, b, ρmin, lc, fy):
        from getConstant import search_fai
        l0 = lc
        φ = search_fai(l0, b)
        print( '')
        print( '6)验算适用条件:')
        ρ = round(As / (b * h0), 3)
        print( ('ρ=As/(b*h0)={}/({}*{})={}>=ρmin*h/h0={},''\n'
                     '已经满足最小配筋率要求.'.format(As, b, h0, ρ, round(ρmin * h / h0, 3))))
        print( '')
        print( '7)验算垂直于弯矩作用平面的轴心受压承载力:')
        print( ('l0/b={}/{}={}'.format(l0, b, l0 / b)))
        print( ('查表可得:φ={}'.format(φ)))
        Nu = round(0.9 * φ * (fc * b * h + fy * (As + Asp)))
        print( ("Nu=0.9φ[fc*b*h+fy'*(As+As')]"'\n'
                     "=0.9*{}[{}*{}*{}+{}*({}+{})]"'\n'
                     "={}N".format(φ, fc, b, h, fy, As, Asp, Nu)))
        if Nu >= N:
            print( ('Nu={}>=N={}, ''\n'
                         '垂直于弯矩作用平面的轴心受压承载力满足'.format(Nu, N)))
        else:
            print( ('Nu={}<N={}, ''\n'
                         '垂直于弯矩作用平面的轴心受压承载力不满足'.format(Nu, N)))

_as, h, b, lc, M1, M2, N = 45, 700, 400, 3300, 0.88*350, 350, 3500
c_level, s_level = 'C40', 'HRB400'
from getConstant import getConstant

fc, ft, ftk, Ec, fy, fyk, Es, ξb, α1, β1 = getConstant(c_level, s_level)
pianxin_rc(b,h,lc,N,M1,M2,_as,fc,ft,fy,α1,β1,ξb)