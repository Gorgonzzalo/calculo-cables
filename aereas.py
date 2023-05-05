from math import *

from pandas import *
from tabula import *
from numpy import *
import pickle


def lineasAereas(dicLineas):
    df_dmg = DataFrame(columns = ['TENSIÓN', 'DMG'])
    df_dmg['TENSIÓN'] = [30, 66, 132, 220, 400]
    df_dmg['DMG'] = [2430.140927, 3306.275737, 4793.2242, 6822.543388 ,11295.97718]
    df_dmg['DMG'].apply(lambda x: round(x,2))

    
    datasheet = read_csv("datasheet aereas.csv")

    fdp = 0.9
    tanPhi = 0.48
    altitud = float(dicLineas['elevacion']) #sale del query
    nCondFase = 1 #simplex, duplex 
    nCirc = 1 # uno o dos circuitos como mucho, y sólo dependiendo
    iCirc = round(float(dicLineas['potPOI'])*10**6/(sqrt(3)*fdp*float(dicLineas['tensionAereaLinea'])*10**3),3)

    # Parámetros para calcular el DMG
    rEq = 1 #mm solo para inicializarlo
    distFases = 400 #tomamos 400 mm para duplex y 450 para triplex

    flagCorriente = 0
    flagTension = 0
    flagPotencia = 0
    flagCorona = 0
    flagTorre = 0

    i = 0
    while True:
        cable = datasheet.iloc[i][1]
        r = (datasheet.iloc[i][10]/2)*10**(-3) #m
        iMax = datasheet.iloc[i][17]*nCirc*nCondFase #A
        # potTernaMax = iMax*sqrt(3)*fdp*(dicLineas['tensionAereaLinea']*10**3)*10**(-6)
        resistCable = datasheet.iloc[i][13] #ohm/km

        #Calculamos la resistencia de la línea
        resistKm = resistCable/(nCirc*nCondFase) 
        resistencia = resistKm*float(dicLineas['longAereaLinea'])

        #Calculamos la reactancia de la línea
        # DMG en función del tipo de torre (single circuit or multicircuit(400 kV))
        if(float(dicLineas['tensionAereaLinea']) <= 30) and (flagTorre != 1):
            drs = 2.3323
            dst = 2.55
            drt = 2.4129
            DMGff = cbrt(drs*dst*drt)*1000 #mm
        elif((float(dicLineas['tensionAereaLinea']) > 30 and float(dicLineas['tensionAereaLinea']) <= 66) and (flagTorre != 1)):
            drs = 3.3541
            dst = 3.5794
            drt = 3.0103
            DMGff = cbrt(drs*dst*drt)*1000 #mm
        elif((float(dicLineas['tensionAereaLinea']) > 66 and float(dicLineas['tensionAereaLinea']) <= 132) and (flagTorre != 1)):
            drs = 5.2
            dst = 5.2924
            drt = 4.0012
            DMGff = cbrt(drs*dst*drt)*1000 #mm
        elif((float(dicLineas['tensionAereaLinea'])> 132 and float(dicLineas['tensionAereaLinea']) <= 220) and (flagTorre != 1)):
            drs = 6.8476
            dst = 7.0235
            drt = 6.6030
            DMGff = cbrt(drs*dst*drt)*1000 #mm
        elif(float(dicLineas['tensionAereaLinea']) > 220 and float(dicLineas['tensionAereaLinea']) <= 400) or (flagTorre == 1):
            #multicircuito
            a, b , c = 4.7, 5.6, 5.6
            drs = sqrt(b**2 + (c-a)**2)
            drsp = sqrt(b**2 + (a+c)**2)
            dst = drs
            dstp = drsp
            drt = 2*b
            drtp = 2*a
            drrp = sqrt((2*b)**2 + (2*a)**2)
            dssp = 2*c
            dttp = drrp
            dr = sqrt(drs*drt*drsp*drtp)/drrp
            ds = sqrt(drs*dst*drsp*dstp)/dssp
            dt = sqrt(drt*dst*drtp*dstp)/dttp
            DMGff = cbrt(dr*ds*dt)*1000 #mm

        match nCondFase: #En función de si es simplex o duplex
            case 1: # Simplex
                rEq = r*1000 #mm 
                inductKm = (1/(2*nCondFase) + 4.6*log10(DMGff/rEq))*(10**(-4))
                capacitanciaKm = 24.2*(10**(-9))/(log10(DMGff/rEq))
            case 2: # Duplex
                distFases = 400
                rEq = sqrt(r*1000*distFases) #mm
                inductKm = (1/(2*nCondFase) + 4.6*log10(DMGff/rEq))*(10**(-4))
                capacitanciaKm = 24.2*(10**(-9))/(log10(DMGff/rEq))
            case 3: # triplex
                distFases = 500
                rEq = cbrt(r*1000*distFases**2) #mm
                inductKm = (1/(2*nCondFase) + 4.6*log10(DMGff/rEq))*(10**(-4))
                capacitanciaKm = 24.2*(10**(-9))/(log10(DMGff/rEq))            
            case default:
                pass
        
        match nCirc: #En función del número de circuitos
            case 1:
                inductKm = inductKm/nCirc
                capacitanciaKm = capacitanciaKm*nCirc
            case 2:
                inductKm = inductKm/nCirc
                capacitanciaKm = capacitanciaKm*nCirc
            case default:
                pass
        
        reactancia = inductKm*float(dicLineas['longAereaLinea'])*2*pi*50
        susceptancia = capacitanciaKm*float(dicLineas['longAereaLinea'])*2*pi*50

        #Calculamos la tensión disruptiva

        Uc = 84*1*0.8*r*(10**2)*((3.921*float(dicLineas['presion']))/(273+25))*log((DMGff/10)/(rEq/10))


        # Calculamos los diferentes criterios
        def criterioCorriente():
            if iMax < iCirc: #El cable no puede soportar la máxima potencia.
                flagCorriente = 0
            else: #la iMax que puede circular es mayor que la i para la potencia calculada
                flagCorriente = 1
            return flagCorriente

        def criterioCorona():
            if Uc < float(dicLineas['tensionMaxAereaLinea']): #Hay efecto corona
                flagCorona = 0
            else: #La disruptiva mayor que la máxima, no hay efecto corona
                flagCorona = 1
            return flagCorona
        
        def criterioTension():
            caidaTension = (((float(dicLineas['potPOI']))*(resistencia + reactancia*tanPhi))/((float(dicLineas['tensionAereaLinea'])**2)))*(100)
            if caidaTension > float(dicLineas['caidaTension']): #la caida de tensión es mayor que la permitida, no vale
                flagTension = 0
            else :
                flagTension = 1
            return flagTension

        def criterioPotencia():
            perdidaPotencia = (100*resistencia*float(dicLineas['potPOI']))/((fdp**2)*(float(dicLineas['tensionAereaLinea'])**2))
            if perdidaPotencia > float(dicLineas['perdidaPotencia']): #si la pérdida de potencia en % es mayor que el límite, no cumple
                flagPotencia = 0
            else :
                flagPotencia = 1
            return flagPotencia
        
        flagCorriente = criterioCorriente()
        flagTension = criterioTension()
        flagPotencia = criterioPotencia()
        flagCorona = criterioCorona()

        if (flagCorriente != 0 and flagTension !=0 and flagPotencia !=0 and flagCorona !=0):
            dicLineas['faseNAereaCable'] = str(nCirc) + " x " + str(nCondFase)
            dicLineas['faseAereaCable'] = cable
            dicLineas['faseNAereaTierra'] = "48"
            dicLineas['faseAereaTierra'] = "OPGW Tipo 1 17kA – 15,3 mm"
            break

        elif (nCondFase == 1) and (i<len(datasheet)-1): 
            i +=1 # Hay que pasar de cable
            continue         
        elif (i == len(datasheet)-1) and (nCondFase==1): 
            i = 0 # Hay volver al cable 1
            nCondFase = 2 # Probamos todos los cables en duplex por cuestión de precio
            continue 
        elif (nCondFase == 2) : # Hay que hacer triplex
            i = 0
            nCondFase = 3
            continue
        elif (nCondFase == 3) and (i<len(datasheet)-1): 
            #Hay que hacer multicircuito
            flagTorre = 1
            nCondFase = 1
            nCirc = 2
            i = 0
            continue 
        else:
            print("cable not found for the requirements, verify calculations")
            exit()

    return dicLineas


