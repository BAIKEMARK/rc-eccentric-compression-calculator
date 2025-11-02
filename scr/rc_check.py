
def known_n(b,h,lc,N,_as,fc,ft,fy,α1,β1,ξb,As,Asp,k):
    _asp=_as
    fyp = fy  # 一般As，Asp钢筋取同种
    h0 = h - _as
    ea=max(round(h/30,3),20)
    A=b*h
    N=N*1000#单位转换：KN->N
    ρ = round(As / (b * h0),4)
    ρp = round(Asp / (b * h0),4)
    ρmin = round(max(45 * (ft / fy) * 0.01, 0.2 * 0.01), 3)
    print( '[解]:' + '\n' + '压弯计算' + '\n' + '1)截面几何信息:')
    print( 'b={}mm,h={}mm;'.format(b, h))
    print( '计算长度lc = {}mm; as ={}mm,'.format(lc,_as))
    print( ('h0 = h - as ={} - {} = {} mm;'.format(h,_as,h0)))
    print(('ea = max(h / 30, 20) =max({}, 20)= {}mm;'.format(round(h/30,3),ea)))
    print( '受拉配筋率ρ = As / (bh0) = {} / ({} * {}) = {};'.format(As,b,h,ρ))
    print( ('受压配筋率ρp = Asp / (bh0) = {} / ({} * {}) = {};'.format(Asp,b,h,ρp)))
    print("ρmin = max(45 * (ft / fy) * 0.01, 0.2 * 0.01)={}".format(ρmin))
    print( '')



    ξcy = 2 * β1 - ξb
    xb = ξb * h0
    xcy = round(ξcy * h0)
    print( '2)材料强度信息:')
    print( 'fc={}MPa,ft={}MPa,fy={}MPa;'.format(fc, ft, fy))
    print( "α1 = {}, β1 = {};".format(α1, β1))
    print( "εcu = 0.0033;".format())
    print( "ξcy = 2 * β1 - ξb ={}".format(ξcy))
    print( "xb = ξb * h0 = {}mm;".format(xb))
    print( "xcy = ξcy * h0 ={}mm;".format(xcy))
    print('')

    x = round((N - fyp*Asp +fy * As) / (α1*fc*b))
    print( '3)复核计算:')
    print( '先假设为大偏心受压，计算出x')
    print( "x = (N - fy'*As'+fy * As)/(α1*fc*b) "'\n'
                "= (({})-{}*{}+{}*{})/{}= {}mm;".format(N,fyp,Asp,fy,As,round(α1*fc*b),x))

    if x < xb:
        e = round((α1 * fc * b * x * (h0 - 0.5 * x) + fyp * Asp * (h0 - _asp)) / N)
        ei = round(e - h / 2 + _asp)
        e0 = round(ei - ea)
        M2=N*e0
        M1=k*M2
        print( "x = {}mm < xb = {}mm, 所假设大偏心受压成立;".format(x,xb))
        print( "e=(α1*fc*b*x*(h0-0.5*x)+fy'*As'*(h0-as'))/N""\n"
                    "=({}*{}*{}*{}*({}-0.5*{})+{}*{}*({}-{}))/{}={}mm;".format(α1,fc,b,x,h0,x,fyp,Asp,h0,_asp,N,e))
        print( "ei=e-h/2+as'={}mm;".format(ei))
        print( "e0=ei-ea={}mm;".format(e0))
        M2=p_delta_check( M1, M2, N, fc, A, lc, h, ea, h0)
        check( N, _as, h, h0, fc, As, Asp, b, ρmin, lc, fy)
        return round(M2/1000000)
    else:

        x = round((-N * ξb + N * β1 + fyp * Asp * ξb - fyp * Asp * β1 + fy * As * β1) * h0 / (
                    -α1 * fc * b * h0 * ξb + α1 * fc * b * h0 * β1 + fy * As))
        e = round((α1 * fc * b * x * (h0 - 0.5 * x) + fyp * Asp * (h0 - _asp)) / N,3)
        e0 = round(e - 0.5 * h + _asp-ea,3)
        M2=round(N*e0)
        M1=round(k*M2)
        print( "x = {}mm > xb = {}mm, 属于小偏压破坏情况;".format(x, xb))
        print( "重新求x")
        print( "根据以下三条公式:"'\n'
                    "Nu=α1fcbx+fy'As'-σsAs; （a）"'\n'
                    "σs=（ξ-β1）*fy/(ξb-β1) （b）"'\n'
                    "Nu*e=α1fcbx(h0-0.5x)+fy'As'(h0-as') (c)")
        print('可以计算出x')
        print("x = (-N * ξb + N * β1 + fy'*As' * ξb-fy'*As' * β1+fy * As * β1) * h0 "'\n'
              "/ (-α1 * fc * b * h0 * ξb + α1 * fc * b * h0 * β1 + fy * As) "'\n'
                   "= {} * {} / {} = {}mm;".format((-N * ξb + N * β1 + fyp*Asp * ξb-fyp*Asp * β1+fy * As * β1),h0,(-α1 * fc * b * h0 * ξb + α1 * fc * b * h0 * β1 + fy * As),x))
        if x<ξcy*h0:
            print("e = (α1 * fc * b * x * (h0 - 0.5 * x) + fy'*As' * (h0- as '))/N=({}*{}*{}*{}*{}+{}*{}*{})/{}={}mm".format(α1, fc, b , x , (h0 - 0.5 * x), fyp ,Asp ,(h0- _asp),N,e))
            print("e0=e-0.5*h+as'-ea={}mm".format(e0))
            print("M2 = N * e0={}*{}={}KNm")
            M2=p_delta_check(M1, M2, N, fc, A, lc, h, ea, h0)
            check(N, _as, h, h0, fc, As, Asp, b, ρmin, lc, fy)
            return round(M2/1000000)
        else:
            print("x>=ξcy*h0,假定错误，应按照式（5-36）重新计算x")
            ep=h/2-(e0+ea)-_asp
            ξ = round(_asp / h0 + ((_asp / h0) ** 2 + 2 * (
                        N * ep / (α1 * fc * b * h0 ** 2) - (As * fyp / (b * h0 * α1 * fc)) * (1 - _asp / h0))) ** 0.5,3)
            print("ξ=as'/h0+((as'/h0)**2+2*(N*e'/(α1*fc*b*h0**2)-(As*fy'/(b*h0*α1*fc))*(1-as'/h0)))**0.5=" + '\n' +
                  "={}".format( ξ))
            x=round(ξ*h0)
            print("x=ξ*h0={}".format(x))
            e = round((α1 * fc * b * x * (h0 - 0.5 * x) + fyp * Asp * (h0 - _asp)) / N, 3)
            print("e = (α1 * fc * b * x * (h0 - 0.5 * x) + fyp * Asp * (h0 - _asp)) / N")
            e0 = round(e - 0.5 * h + _asp - ea, 3)
            M2 = round(N * e0)
            M1 = round(k * M2)
            print("M2 = N * e0={}*{}={}KNm")
            M2=p_delta_check(M1, M2, N, fc, A, lc, h, ea, h0)
            check(N, _as, h, h0, fc, As, Asp, b, ρmin, lc, fy)
            return round(M2/1000000)


        # ep = h / 2 - ei - _asp
        # print( "求ξ，并按ξ的情况求As':")
        # u = round(_asp / h0 + (fy * As / ((ξb - β1) * α1 * fc * b * h0)) * (1 - _asp / h0), 4)
        # print( ("u=(as'/h0)+(fy*As/((ξb-β1)*α1*fc*b*h0))*(1-as'/h0)={}".format(u)))
        # v = round(2 * N * ep / (α1 * fc * b * h0 ** 2) - (2 * β1 * fy * As / ((ξb - β1) * α1 * fc * b * h0)) * (
        #             1 - _asp / h0), 4)
        # print( ("v=2*N*e'/(α1*fc*b*h0**2)-(2*β1*fy*As/((ξb-β1)*α1*fc*b*h0))*(1-as'/h0)={}".format(v)))
        # ξ = round(u + (u ** 2 + v) ** 0.5, 4)
        # print( ("ξ=u+(u**2+v)**0.5={}+({}**2+{})={}".format(u, u, v, ξ)))
        # if ξ >= ξb:
        #     print( ('由于ξ>=ξb={},故前面假定为小偏心受压是对的;'.format(ξb)))
        #     ξcy = 2 * β1 - ξb
        #     print( ('ξcy = 2 * β1 - ξb = 2 * {} - {} = {};'.format(β1, ξb, ξcy)))
        #     # 判断三种情况：
        #     if ξcy > ξ:
        #         print( '由于ξcy>ξ>ξb,故属于小偏心受压的第一种情况，由力的平衡方程得：')
        #         Asp = round((N - α1 * fc * ξ * b * h0 + ((ξ - β1) / (ξb - β1)) * fy * As) / fyp)
        #         print( "As'=(N-α1*fc*ξ*b*h0+(ξ-β1)/(ξb-β1)*fy*As)/fy'" +
        #               "=({}-{}*{}*{}*{}*{}+({:.3f})*{}*{})/{}={}".format(N, α1, fc, ξ, b, h0, (ξ - β1) / (ξb - β1), fy,
        #                                                                  As, fyp, Asp))
        #     elif ξcy <= ξ and ξ < h / h0:
        #         print( "由于h/h0>ξ>ξcy,故属于小偏心受压的第二种情况，取σs=-fy',按下式重新求ξ：")
        #         ξ = _asp / h0 + ((_asp / h0) ** 2 + 2 * (
        #                     N * ep / (α1 * fc * b * h0 ** 2) - (As * fyp / (b * h0 * α1 * fc)) * (
        #                         1 - _asp / h0))) ** 0.5
        #         print(
        #               "ξ=as'/h0+((as'/h0)**2+2*(N*e'/(α1*fc*b*h0**2)-(As*fy'/(b*h0*α1*fc))*(1-as'/h0)))**0.5=" + '\n' +
        #               "{}/{}+(({}/{})**2+2*({}*{}/({}*{}*{}*{}**2)-({}*{}/({}*{}*{}*{}))*(1-{}/{})))**0.5={}"
        #               .format(_asp, h0, _asp, h0, N, ep, α1, fc, b, h0, As, fyp, b, h0, α1, fc, _asp, h0, ξ))
        #         print( "再按（5-20）求出As':")
        #         Asp = (N - α1 * fc * ξ * b * h0 - As * fyp) / fyp
        #         print( ("As'=(N-α1*fc*ξ*b*h0-fy'*As)/fy'" + '\n' +
        #                      "=({}-{}*{}*{}*{}*{}-{}*{})/{}".format(N, α1, fc, ξ, b, h0, fyp, As, fyp)))
        #     elif ξcy <= ξ and ξ >= h / h0:
        #         print( ("由于ξcy<=ξ 且 ξ>=h/h0={},故属于小偏心受压的第三种情况,取x=h,σs=-fy',α1=1,由式（5-21）得：;".format(ξ)))
        #         Asp = (N * e - fc * b * h * (h0 - 0.5 * h)) / (fyp * (h0 - _asp))
        #         print( "As'=(N*e-fc*b*h*(h0-0.5*h))/(fy'*(h0-as'))=" + '\n' +
        #               "({}*{}-{}*{}*{}*({}-0.5*{}))/({}*({}-{}))={}".format(N, e, fc, b, h, h0, h, fyp, h0, _asp, Asp))
        # σs =(ξ - β1)*fy / (ξb - β1)

def known_e0(b,h,lc,e0,_as,fc,ft,fy,α1,β1,ξb,As,Asp):
    _asp=_as
    fyp = fy  # 一般As，Asp钢筋取同种
    h0 = h - _as
    ea=max(round(h/30,3),20)
    A=b*h
    ρ = round(As / (b * h0),3)
    ρp = round(Asp / (b * h0),3)
    ρmin = round(max(45 * (ft / fy) * 0.01, 0.2 * 0.01), 3)
    print( '[解]:' + '\n' + '压弯计算' + '\n' + '1)截面几何信息:')
    print( 'b={}mm,h={}mm;'.format(b, h))
    print( '计算长度lc = {}mm; as ={}mm,'.format(lc,_as))
    print( ('h0 = h - as ={} - {} = {} mm;'.format(h,_as,h0)))
    print(('ea = max(h / 30, 20) =max({}, 20)= {}mm;'.format(round(h/30,3),ea)))
    print( '受拉配筋率ρ =As/(bh0)={}/({}*{})={};'.format(As,b,h,ρ))
    print( ('受压配筋率ρp=Asp/(bh0)={};'.format(ρp)))
    print("ρmin = max(45 * (ft / fy) * 0.01, 0.2 * 0.01)={}".format(ρmin))
    print( '')



    ξcy = 2 * β1 - ξb
    xb = ξb * h0
    xcy = round(ξcy * h0)
    print( '2)材料强度信息:')
    print( 'fc={}MPa,ft={}MPa,fy={}MPa;'.format(fc, ft, fy))
    print( "α1 = {}, β1 = {};".format(α1, β1))
    print( "εcu = 0.0033;".format())
    print( "ξcy = 2 * β1 - ξb ={}".format(ξcy))
    print( "xb = ξb * h0 = {}mm;".format(xb))
    print( "xcy = ξcy * h0 ={}mm;".format(xcy))
    print('')

    print("3)求混凝土轴向力设计值")
    ei=round(e0+ea,3)
    ζ1=1
    ζ2=1.15-0.01*lc/h
    print("先求偏心增大系数η")
    if lc / h <= 5:
        η = 1
        print("由于lc/h<=5，η=1")
    else:
        print("ζ1=0.5*fc*A/Nc,由于Nc未知，设ζ1=1,ζ2=1.15-0.01*lc/h={}".format(ζ2))
        if lc/h<15:
            ζ2 = 1
            print("由于lc/h<15，ζ2 = 1")
        η=min(round(1+ζ1*ζ2*(lc/h)**2/(1400*ei/h0),3),1)
        print("η=min(1+ζ1*ζ2*(lc/h)**2/(1400*ei/h0),1)={}".format(η))
    e=round(η*ei+h/2-_as,3)
    print( ('ei=e0 + ea = {} + {} = {}mm;'.format( e0,ea,ei)))
    print( ('e=η*ei+h/2-as''\n'
                 '={}*{}+{}/2-{}={}mm;'.format(η,ei,h,_as,e)))

    print("由于截面配筋已知，按照大偏压情况，对Nu点取矩得：")
    # k = (fyp*Asp * (e-h0- _asp)-fy*As*e)/α1*fc*b
    # x1=(h0-e+((e-h0)**2-2*k)**0.5)
    # x2=(h0-e-((e-h0)**2-2*k)**0.5)
    # x=x2
    print("α1*fc*b*x*(ei-h/2+x/2)=fy*As*(ei+h/2-as')-fy'*As'*(ei-h/2+as')")
    k=b*fc*α1*(-8.0*As*_as*fy + 8.0*As*ei*fy + 4.0*As*fy*h - 8.0*Asp*_asp*fyp - 8.0*Asp*ei*fyp + 4.0*Asp*fyp*h + 4.0*b*ei**2*fc*α1 - 4.0*b*ei*fc*h*α1 + b*fc*h**2*α1)
    x1 = 0.5*(b*fc*α1*(-2.0*ei + h)-k**0.5)/(b*fc*α1)
    x2 = 0.5*(b*fc*α1*(-2.0*ei + h)+k**0.5)/(b*fc*α1)
    x=round(max(x1,x2))
    print("代入数据，解得：x={}mm".format(x))
    if x<=xb:
        print("x<=xb={}，按大偏压计算".format(xb))
        if x>=2*_asp:
            print("因x>=2as':")
            N = α1*fc*b*x+fyp*Asp-fy*As
            print("N=α1*fc*b*x+fyp*Asp-fy*As={}KNm".format(round(N/1000)))
        else:
            print("因x<2as',令x=as'，则有:")
            N = As*fy*(h0-_asp)/e
            print("N=α1*fc*b*x+fy'*As'-fy*As=As*fy*(h0-as')/e ={}KNm".format(round(N/1000)))
    else:
        print("为小偏压,将已知信息代入以下三式："'\n'
                    "Nu=α1fcbx+fy'As'-σsAs; （a）"'\n'
                    "σs=（ξ-β1）*fy/(ξb-β1) （b）"'\n'
                    "Nu*e=α1fcbx(h0-0.5x)+fy'As'(h0-as') (c)")
        print('可以计算出N:')
        tempt0=-As*e*fy - b*e*fc*h0*α1*β1 + b*e*fc*h0*α1*ξb + b*fc*h0**2*α1*β1 - b*fc*h0**2*α1*ξb
        tempt=(0.25*As**2*e**2*fy**2 + 0.5*As*b*e**2*fc*fy*h0*α1*β1 - 0.5*As*b*e**2*fc*fy*h0*α1*ξb + 0.5*As*b*e*fc*fy*h0**2*α1*β1**2 - 0.5*As*b*e*fc*fy*h0**2*α1*β1*ξb - 0.5*As*b*e*fc*fy*h0**2*α1*β1 + 0.5*As*b*e*fc*fy*h0**2*α1*ξb - 0.5*Asp*_asp*b*fc*fyp*h0**2*α1*β1**2 + Asp*_asp*b*fc*fyp*h0**2*α1*β1*ξb - 0.5*Asp*_asp*b*fc*fyp*h0**2*α1*ξb**2 - 0.5*Asp*b*e*fc*fyp*h0**2*α1*β1**2 + Asp*b*e*fc*fyp*h0**2*α1*β1*ξb - 0.5*Asp*b*e*fc*fyp*h0**2*α1*ξb**2 + 0.5*Asp*b*fc*fyp*h0**3*α1*β1**2 - Asp*b*fc*fyp*h0**3*α1*β1*ξb + 0.5*Asp*b*fc*fyp*h0**3*α1*ξb**2 + 0.25*b**2*e**2*fc**2*h0**2*α1**2*β1**2 - 0.5*b**2*e**2*fc**2*h0**2*α1**2*β1*ξb + 0.25*b**2*e**2*fc**2*h0**2*α1**2*ξb**2 - 0.5*b**2*e*fc**2*h0**3*α1**2*β1**2 + b**2*e*fc**2*h0**3*α1**2*β1*ξb - 0.5*b**2*e*fc**2*h0**3*α1**2*ξb**2 + 0.25*b**2*fc**2*h0**4*α1**2*β1**2 - 0.5*b**2*fc**2*h0**4*α1**2*β1*ξb + 0.25*b**2*fc**2*h0**4*α1**2*ξb**2)
        x=round(max((tempt0- 2.0*tempt**0.5),(tempt0 + 2.0*tempt**0.5)))
        σs =round((x/h0 - β1)*fy / (ξb - β1))
        N = round(α1*fc*b*x+fyp*Asp - σs*As)
        print("σs =(x/h0 - β1)*fy / (ξb - β1)={}"'\n'
              "Nu = α1*fc*b*x+fyp*Asp - σs*As".format(σs,N))
    check(N, _as, h, h0, fc, As, Asp, b, ρmin, lc, fy)
    return round(N/1000)

def p_delta_check(M1,M2,N, fc, A,lc, h, ea, h0):
    print( ('①  M1 / M2 - 0.9  = {};'.format(round(M1 / M2 - 0.9, 3))))
    print( ('②  轴压比:  ''\n'
                 'N / (fc*A) - 0.9 ''\n'
                 '= {} / ({} * {}) - 0.9 = {};'.format(N, fc, A, round(N / (fc * A) - 0.9, 3))))
    print( ('③  lc / i - 34 + 12(M1 / M2) ''\n'
                 '= {} / (0.289 * {}) - 34 + 12 * {} = {};'
                 .format(lc, h, round(M1 / M2, 3), round(lc / (0.289 * h) - 34 + 12 * (M1 / M2), 3))))
    if M1 / M2 - 0.9 > 0 or N / (fc * A) - 0.9 > 0 or lc / (0.289 * h) - 34 + 12 * (M1 / M2) > 0:
        print( '由于①②③中有一条件满足 > 0, 所以必须考虑二阶效应.')
        print( '')
        Cm = round(0.7 + 0.3 * (M1 / M2), 3)
        print( ('Cm = 0.7 + 0.3*(M1 / M2) = 0.7 + 0.3 * {} = {};'.format(round(M1 / M2, 3),
                                                                              round(0.7 + 0.3 * (M1 / M2), 3))))
        if Cm < 0.7:
            Cm = 0.7
            print( '由于Cm < 0.7, 所以取Cm = 0.7;')

        ζc = min(0.5 / (N / (fc * A)), 1)
        print( ('ζc = 0.5 / (N / (fc * A)) = 0.5 / {} = {};'.format(round(N / (fc * A), 3),
                                                                         round(0.5 / (N / (fc * A)), 3))))
        if ζc == 1:
            print( '由于0.5 / (N / (fc * A)) >= 1, 所以取ζc = 1;')

        ηns = round(1 + (lc / h) * (lc / h) * ζc / (1300 * (M2 / N + ea) / h0), 3)
        print( ('ηns =1+(lc/h)*(lc/h)*ζc/(1300*(M2/N+ea)/h0)={}'.format(ηns)))
        Cm_ηns =round(Cm * ηns)
        print( ('Cm * ηns = {} * {} = {};'.format(Cm, ηns, Cm * ηns)))

        if Cm * ηns < 1.0:
            Cm_ηns = 1
            print( '由于Cm * ηns < 1.0, 所以取Cm * ηns = 1.0;')

        M = round(Cm_ηns * M2, 3)
        print( ('M = Cm * ηns * M2 ''\n'
                     '= {} * {} = {}N·mm;'.format(Cm_ηns, M2, M)))
        print( '')

    else:
        print( '由于①②③均满足< 0, 所以不需要考虑二阶效应;')
        M = M2
        print( ('M = M2 = {}N·mm;'.format(M2)))
        print( '')
    return M

def check(N,_as,h,h0,fc,As,Asp,b,ρmin,lc,fy):
    from getConstant import search_fai
    l0=lc
    φ=search_fai(l0,b)
    print( '')
    print( '4)验算适用条件:')
    ρ = round(As / (b * h0),3)
    print( ('ρ=As/(b*h0)={}/({}*{})={}>=ρmin*h/h0={},''\n'
                 '已经满足最小配筋率要求.'.format(As,b,h0,ρ,round(ρmin*h/h0,3))))
    ρp = round(Asp / (b * h0),3)
    print( ("ρ'=As'/(b*h0)={}/({}*{})={}>=ρmin*h/h0={},"'\n'
                 "已经满足最小配筋率要求.".format(Asp, b, h0, ρp, round(ρmin * h / h0,3))))
    print( '')
    print( '5)验算垂直于弯矩作用平面的轴心受压承载力:')
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

