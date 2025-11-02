
def pianxin_rc(b,h,lc,N,M1,M2,_as,fc,ft,fy,α1,β1,ξb,Asp):
    # print('测试点：访问槽函数成功')
    # 计算相关参数
    fyp = fy  # 一般As，Asp钢筋取同种
    h0 = h - _as
    ea=max(round(h/30,3),20)
    A=b*h
    N=N*1000#单位转换：KN->N
    M1,M2=M1*1000000,M2*1000000#单位转换：KN*m->N*mm
    # print('测试点：相关参数计算成功')
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
                 .format(lc,h,round(M1/M2,3),round(lc / (0.289*h) - 34 + 12*(M1 / M2),3))))
    # print('测试点：二阶效应判断成功')
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

        print( ('Cm * ηns = {} * {} = {};'.format(Cm ,ηns,Cm * ηns)))
        Cm_ηns = Cm * ηns
        if Cm * ηns < 1.0:
            Cm_ηns=1
            print( '由于Cm * ηns < 1.0, 所以取Cm * ηns = 1.0;')

        M = round(Cm_ηns * M2,3)
        e0=round(M/N,3)
        print( ('M = Cm * ηns * M2 ''\n'
                     '= {} * {} = {}N·mm;'.format(Cm_ηns,M2,M)))
        print( ('e0=M/N={};'.format(e0)))
        print( '')
        # print('测试点：应考虑二阶效应情况时计算成功')
    else:
        print( '由于①②③均满足< 0, 所以不需要考虑二阶效应;')
        M = M2
        e0 = round(M2 / N,3)
        print( ('M = M2 = {}N·mm;'.format(M2)))
        print( ('e0=M2/N={};'.format(e0)))
        print( '')
    # print('测试点：二阶效应计算成功')

    print( '5)采用非对称配筋的方法计算配筋:')
    ei=round(e0+ea,3)
    e=round(ei+h/2-_as,3)
    print( ('ei = e0 + ea = {} + {} = {}mm;'.format(e0,ea,ei)))
    print( ('e = ei + h / 2 - as ''\n'
                 '={} +{} / 2 - {} = {}mm;'.format(ei,h,_as,e)))
    ρmin = round(max(45 * (ft / fy) * 0.01, 0.2 * 0.01), 3)
    As_min=round(ρmin*b*h)
    print("As_min=ρmin*b*h={}mm".format(As_min))
    # print('测试点6')
    if ei > 0.3 * h0:
        print( ('由于ei ={}mm > 0.3 * h0={}mm, 所以取先按大偏压情况计算;'.format(ei,0.3*h0)))
        if Asp is None:
            As,Asp=dapianya_Asp_unknown(N,M,_as,h0,fc,ft,fy,α1,β1,ξb,b,h,e,e0,ea,ei,fyp,As_min)
        else:
            As = dapianya_Asp_known(N,M,_as,h0,fc,ft,fy,α1,β1,ξb,b,h,Asp,e,e0,ea,ei,fyp,As_min)
    else:
        print( ('由于ei ={}mm <= 0.3 * h0={}mm, 所以取先按小偏压情况计算;'.format(ei,0.3*h0)))
        As,Asp=xiaopianxin(N,M,_as,h0,fc,ft,fy,α1,β1,ξb,e,e0,ea,ei,b,h,As_min)
    check(N,_as,h,h0,fc,As,Asp,b,ρmin,lc,fy)
    return As,Asp

def dapianya_Asp_unknown(N,M,_as,h0,fc,ft,fy,α1,β1,ξb,b,h,e,e0,ea,ei,fyp,As_min):
    _asp=_as
    print( '由式（5-30）得：')
    # Asp = (N * e - α1 * fc * b * ξb * (h0**2) * (1-0.5*ξb)) / (fy * (h0 - _as))
    Asp = round((N * e - α1 * fc * b * ξb * (h0 ** 2) * (1 - 0.5 * ξb)) / (fyp * (h0 - _asp)))#若用两种钢筋
    print( ("As' = (N * e - α1 * fc * b * ξb * (h0**2) * (1-0.5*ξb)) / (fy * (h0 - _as))"'\n'
                 '=({}*{}-{}*{}*{}*{}*({}**2)*(1-0.5{})) /（{}*({}-{})）={}mm2;'
                 .format(N,e,α1,fc,b,ξb,h0,ξb,fy,h0,_asp,Asp)))
    if Asp>=As_min:
        print( ('由于Asp >= As_min={},满足最小配筋率要求，所以Asp={};'.format(As_min,Asp)))
    else:
        Asp = As_min
        print( ('由于Asp < As_min={},不满足最小配筋率要求，所以取Asp={};'.format(As_min,Asp)))

    print( '由式（5-31）得：')

    # As = (( α1 * fc * b * ξb * h0 -N) / fy )+Asp
    # print( ('As = (( α1 * fc * b * ξb * h0 -N) / fy )+(fyp/fy)*Asp'
    #              '=As = (( {} * {} * {} * {} * {} -{}) / {} )+{}={}mm2;'.format(α1,fc,b,ξb,h0,N,fy,Asp,As)))
    As = round(((α1 * fc * b * ξb * h0 - N) / fy) + (fyp/fy)*Asp)
    print( ('As = (( α1 * fc * b * ξb * h0 -N) / fy )+(fyp/fy)*Asp''\n'
                 '=As = (( {} * {} * {} * {} * {} -{}) / {} )+{}={}mm2;'.format(α1, fc, b, ξb, h0, N, fy, (fyp/fy)*Asp, As)))
    if As >= As_min:
        print( ('由于As >= As_min={},满足最小配筋率要求，所以As={};'.format(As_min, As)))
    else:
        As = As_min
        print( ('由于As < As_min={},不满足最小配筋率要求，所以取As={};'.format(As_min, As)))

    print( '由式（5-13）得：')
    x = N / (α1 * fc * b)
    print("x=N/(α1*fc*b)={}/({}*{}*{})={}mm;".format(N, α1, fc, b,x))
    ξ=x/h0
    print( ('ξ=x/h0={};'.format(x/h0)))
    if ξ<ξb:
        print( ('由于ξ<ξb={},故前面假定为大偏心受压是正确的;'.format(ξb)))
    else:
        As=xiaopianxin(N,M,_as,h0,fc,ft,fy,α1,β1,ξb,e,e0,ea,ei,b,h,As_min)
    return As,Asp

def dapianya_Asp_known(N,M,_as,h0,fc,ft,fy,α1,β1,ξb,b,h,Asp,e,e0,ea,ei,fyp,As_min):
    _asp=_as
    print( '由式（5-14）得：')
    Mu2=N*e-fyp*Asp*(h0-_asp)
    print( 'Mu2=N*e-fyp*Asp*(h0-_asp)''\n'
                '={}*{}-{}*{}*({}-{})={}'.format(N,e,fyp,Asp,h0,_asp,Mu2))
    αs=round(Mu2/(α1*fc*b*(h0**2)),3)
    print( ('αs=Mu2/(α1*fc*b*(h0**2))''\n'
                 '={}/({}*{}*{}*({}**2))={}'.format(Mu2, α1, fc, b, h0, αs)))
    ξ=round(1-(1-2*αs)**0.5,3)
    print( ('ξ=1-(1-2*αs)**0.5={}'.format(ξ)))

    if ξ<ξb:
        print( ('由于ξ<ξb={},故前面假定为大偏心受压是正确的;'.format(ξb)))
        x = ξ * h0
        print( ('x=ξ*h0={}'.format(x)))
        if x>=(2*_asp):
            print( ("由于x>=2*as'={},由式（5-13）得：;".format(2*_asp)))
            As=round((α1 * fc * b * ξb * h0 - N) / fy)
            print( ('As=(α1*fc*b*ξb*h0-N)/fy''\n'
                         '=({} * {} * {} * {} * {} -{}) / {}={}'.format(α1,fc,b,ξb,h0,N,fy,As)))
            if As >= As_min:
                print( ('由于As >= As_min={},满足最小配筋率要求，所以As={};'.format(As_min, As)))
            else:
                As = As_min
                print( ('由于As < As_min={},不满足最小配筋率要求，所以取As={};'.format(As_min, As)))
            print( '')
        else:
            print( ("由于x<2*as'={},按式（5-32）计算As：;".format(2 * _asp)))
            As1 = round(N*(ei-0.5*h+_asp) / (fy*(h0-_asp)))
            print( ("As=N*(ei-0.5*h+as') / (fy*(h0-as'))"'\n'
                         '={}*({}-0.5*{}+{}) / ({}*({}-{}))={}'.format(N,ei,h,_asp,fy,h0,_asp,As1)))
            if As1 >= As_min:
                print( ('由于As >= As_min={},满足最小配筋率要求，所以As={};'.format(As_min, As1)))
            else:
                As1 = As_min
                print( ('由于As < As_min={},不满足最小配筋率要求，所以取As={};'.format(As_min, As1)))
            print( '')
            print( "如果按不考虑受压钢筋As’的情况(即As'=0)进行计算：")
            Mu2=N*e
            print( 'Mu2=N*e={}*{}={}'.format(N,e,Mu2))
            αs=round(Mu2/(α1*fc*b*(h0**2)),3)
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
            if As1>=As2:
                As = As2
                print( ('由于As1={} >= As2={},说明本题如不考虑受压钢筋，受拉钢筋As会得到较大数值。因此本题取As={}mm2来配筋;'.format(As1,As2, As)))
            else:
                As = As1
                print( ('由于As1={} < As2={},说明本题如不考虑受压钢筋，受拉钢筋As可以得到较小数值。因此本题取As={}mm2来配筋;'.format(As1,As2, As)))
    else:
        print( ('由于ξ>=ξb={},故前面假定为大偏心受压是错的;'.format(ξb)))
        As, Asp=xiaopianxin(N,M,_as,h0,fc,ft,fy,α1,β1,ξb,e,e0,ea,ei,b,h,As_min)
    return As

def xiaopianxin(N,M,_as,h0,fc,ft,fy,α1,β1,ξb,e,e0,ea,ei,b,h,As_min):
    fyp=fy
    _asp=_as
    h0p=h0
    print( '（1）确定As:')
    if N>fc*b*h:
        print( 'N={}KN>fc*b*h={}*{}*{}={}KN，故令N=Nu，按反向破坏的式（5-28）（5-29）求As'.format(N/1000,fc,b,h,fc*b*h/1000))
        ep=h/2-_asp-(e0-ea)
        print( ("e'=h/2-_asp-(e0-ea)={}mm".format(ep)))
        As=round((N*ep-α1*fc*b*h*(h0p-h/2))/(fy*(h0-_as)))
        print( ("As=(N*e'-α1*fc*b*h*(h0p-h/2))/(fy*(h0-_as))="+'\n'+
                     '({}*{}-{}*{}*{}*{}*({}-{}/2))/({}*({}-{}))={}'
                     .format(N,ep,α1,fc,b,h,h0p,h,fy,h0,_as,As)))
        if As >= 0.002*b*h:
            print( ('由于As >= 0.002*b*h={},满足最小配筋率要求，所以As={};'.format(0.002*b*h, As)))
        else:
            As = round(0.002*b*h)
            print( ('由于As < 0.002*b*h={},不满足最小配筋率要求，所以取As={};'.format(0.002*b*h, As)))
    else:
        print('N={}KN<=fc*b*h={}*{}*{}={}KN，求As'.format(N / 1000, fc, b, h, fc * b * h / 1000))
        ep=h/2-ei-_asp
        print( ("e'=h/2-ei-as'={}mm".format(ep)))
        As = round(0.002 * b * h)
        print( 'As =0.002*b*h={};'.format(0.002 * b * h))
    print( "求ξ，并按ξ的情况求As':")
    u=round(_asp/h0+(fy*As/((ξb-β1)*α1*fc*b*h0))*(1-_asp/h0),4)
    print( ("u=(as'/h0)+(fy*As/((ξb-β1)*α1*fc*b*h0))*(1-as'/h0)={}".format(u)))
    v= round(2*N*ep/(α1*fc*b*h0**2)-(2*β1*fy*As/((ξb-β1)*α1*fc*b*h0))*(1-_asp/h0), 4)
    print( ("v=2*N*e'/(α1*fc*b*h0**2)-(2*β1*fy*As/((ξb-β1)*α1*fc*b*h0))*(1-as'/h0)={}".format(v)))
    ξ = round(u+(u**2+v)**0.5, 4)
    print( ("ξ=u+(u**2+v)**0.5={}+({}**2+{})={}".format(u,u,v,ξ)))
    if ξ >= ξb:
        print( ('由于ξ>=ξb={},故前面假定为小偏心受压是对的;'.format(ξb)))
        ξcy = 2 * β1 - ξb
        print( ('ξcy = 2 * β1 - ξb = 2 * {} - {} = {};'.format(β1, ξb, ξcy)))
        # 判断三种情况：
        if ξcy > ξ:
            print( '由于ξcy>ξ>ξb,故属于小偏心受压的第一种情况，由力的平衡方程得：')
            Asp=round((N-α1*fc*ξ*b*h0+((ξ-β1)/(ξb-β1))*fy*As)/fyp)
            print( "As'=(N-α1*fc*ξ*b*h0+(ξ-β1)/(ξb-β1)*fy*As)/fy'"+
                        "=({}-{}*{}*{}*{}*{}+({:.3f})*{}*{})/{}={}".format(N,α1,fc,ξ,b,h0,(ξ-β1)/(ξb-β1),fy,As,fyp,Asp))
        elif ξcy<=ξ and ξ<h/h0:
            print( "由于h/h0>ξ>ξcy,故属于小偏心受压的第二种情况，取σs=-fy',按下式重新求ξ：")
            ξ=_asp/h0+((_asp/h0)**2+2*(N*ep/(α1*fc*b*h0**2)-(As*fyp/(b*h0*α1*fc))*(1-_asp/h0)))**0.5
            print( "ξ=as'/h0+((as'/h0)**2+2*(N*e'/(α1*fc*b*h0**2)-(As*fy'/(b*h0*α1*fc))*(1-as'/h0)))**0.5="+'\n'+
                        "{}/{}+(({}/{})**2+2*({}*{}/({}*{}*{}*{}**2)-({}*{}/({}*{}*{}*{}))*(1-{}/{})))**0.5={}"
                  .format(_asp,h0,_asp,h0,N,ep,α1,fc,b,h0,As,fyp,b,h0,α1,fc,_asp,h0,ξ))
            print( "再按（5-20）求出As':")
            Asp = (N - α1 * fc * ξ * b * h0 - As*fyp) / fyp
            print( ("As'=(N-α1*fc*ξ*b*h0-fy'*As)/fy'" + '\n'+
                            "=({}-{}*{}*{}*{}*{}-{}*{})/{}".format(N, α1, fc,ξ, b, h0,fyp,As, fyp)))
        elif ξcy<=ξ and ξ>=h/h0:
            print( ("由于ξcy<=ξ 且 ξ>=h/h0={},故属于小偏心受压的第三种情况,取x=h,σs=-fy',α1=1,由式（5-21）得：;".format(ξ)))
            Asp=(N*e-fc*b*h*(h0-0.5*h))/(fyp*(h0-_asp))
            print( "As'=(N*e-fc*b*h*(h0-0.5*h))/(fy'*(h0-as'))="+'\n'+
                        "({}*{}-{}*{}*{}*({}-0.5*{}))/({}*({}-{}))={}".format(N,e,fc,b,h,h0,h,fyp,h0,_asp, Asp))
        else:
            print( '!!!!!!!!!!!!!!!运算过程出错,结果不可信!!!!!!!!!!!!!!!')
            print( '!!!!!!!!!!!!!!!运算过程出错,结果不可信!!!!!!!!!!!!!!!')
            print( '!!!!!!!!!!!!!!!运算过程出错,结果不可信!!!!!!!!!!!!!!!')
            Asp=None
        if Asp >= 0.002 * b * h:
            print( ('由于Asp >= 0.002*b*h={},满足最小配筋率要求，所以Asp={};'.format(0.002 * b * h, Asp)))
        else:
            Asp = 0.002 * b * h
            print( ('由于Asp < 0.002*b*h={},不满足最小配筋率要求，所以取Asp={};'.format(0.002 * b * h, Asp)))
    else:
        print( ('由于ξ<ξb={},故前面假定为小偏心受压是错的;'.format(ξb)))
        As,Asp=dapianya_Asp_unknown(N,M,_as,h0,fc,ft,fy,α1,β1,ξb,b,h,e,e0,ea,ei,fyp,As_min)

    return As,Asp

def check(N,_as,h,h0,fc,As,Asp,b,ρmin,lc,fy):
    from getConstant import search_fai
    l0=lc
    φ=search_fai(l0,b)
    print( '')
    print( '6)验算适用条件:')
    ρ = round(As / (b * h0),3)
    print( ('ρ=As/(b*h0)={}/({}*{})={}>=ρmin*h/h0={},''\n'
                 '已经满足最小配筋率要求.'.format(As,b,h0,ρ,round(ρmin*h/h0,3))))
    ρp = round(Asp / (b * h0),3)
    print( ("ρ'=As'/(b*h0)={}/({}*{})={}>=ρmin*h/h0={},"'\n'
                 "已经满足最小配筋率要求.".format(Asp, b, h0, ρp, round(ρmin * h / h0,3))))
    print( '')
    print( '7)验算垂直于弯矩作用平面的轴心受压承载力:')
    print( ('l0/b={}/{}={}'.format(l0,b,l0/b)))
    print( ('查表可得:φ={}'.format(φ)))
    Nu = round(0.9*φ*(fc * b * h + fy*(As+Asp)))
    print( ("Nu=0.9φ[fc*b*h+fy'*(As+As')]"'\n'
                 "=0.9*{}[{}*{}*{}+{}*({}+{})]"'\n'
                 "={}N".format(φ,fc,b,h,fy,As,Asp,Nu)))
    if Nu>=N:
        print( ('Nu={}>=N={}, ''\n'
                     '垂直于弯矩作用平面的轴心受压承载力满足'.format(Nu,N)))
    else:
        print( ('Nu={}<N={}, ''\n'
                     '垂直于弯矩作用平面的轴心受压承载力不满足'.format(Nu,N)))










