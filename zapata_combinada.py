import math

#definir: qa, fc, fy, pd, pl, t, df, Ab, db
#proponer h y considerar rec
# Solicitar al usuario que introduzca los valores de γc y γs
qa = float(input("Introduce el valor de qa (ksf): "))
fc = float(input("Introduce el valor de fc (ksi): "))
fy = float(input("Introduce el valor de fy (ksi): "))
pdi = float(input("Introduce el valor de la carga muerta en la primera columna (k)(i): "))
pli = float(input("Introduce el valor de la carga viva en la primera columna (k)(i): "))
pde = float(input("Introduce el valor de la carga muerta en la segunda columna (k)(e): "))
ple = float(input("Introduce el valor de la carga viva en la segunda columna (k)(e): "))
df = float(input("Introduce el valor de la profundidad en la zapata (ft): "))
C1i = float(input("Introduce el primer valor de la primera columna (i)(in): "))
C2i = float(input("Introduce el segundo valor de la primera columna (i)(in): "))
C1e = float(input("Introduce el primer valor de la segunda columna (e)(in): "))
C2e = float(input("Introduce el segundo valor de la segunda columna (e)(in): "))
Abt = float(input("Introduce el valor de el area de la barra  transversal de acero (in): "))
dbt = float(input("Introduce el valor de el diametro de la barra transversal de acero (in): "))
Abl = float(input("Introduce el valor de el area de la barra lateral de acero (in): "))
dbl = float(input("Introduce el valor de el diametro de la barra lateral de acero (in): "))
gamma_c = float(input("Introduce el valor de γc (KCF): "))
gamma_s = float(input("Introduce el valor de γs (KCF): "))
rec = float(input("Introduce el valor de el recubrimiento (in): "))
h = float(input("Introduce el valor de el alto de la zapata (in): "))
l = float(input("Introduce el valor de la separacion de la zapata (ft): "))

hmin = 6 + rec + (1 / 2) * (dbt + dbl)
d_sup = h - rec - (1 / 2) * dbt
d_inf = h - rec - (1 / 2) * dbl

d = (1/2) * (d_sup + d_inf)
m = (1/2)*C1e
Pse = 1.0*pde + 1.0*ple
Psi = 1.0*pdi + 1.0*pli

qsA = Pse + Psi
Lreq = 2*(m+(Psi/(Pse+Psi))*(l*12))+1

Base_requerida = ((Pse + Psi)/((qa-(gamma_s*(df-(h/12)))-(gamma_c*(h/12)))*(Lreq/12)))    # Base en valor de ft
B = math.ceil(Base_requerida*12)     #Base redondeada en valor de pulgadas

Pue = 1.2*pde + 1.6*ple
Pui = 1.2*pdi + 1.6*pli

qu = ((Pue+Pui)/((B/12)*(Lreq/12)))     #valor en ksf
wu = qu*(B/12)

Rui = (1/2)*wu*((Lreq/12)-(2*(m/12)))*((Lreq/12)/l)
Rue = (wu*(Lreq/12))-Rui

#cortante de diseño (insertar codigo para calculos y diagrama)
#momento de diseño (insertar codigo para calculos y diagrama)

#Falla por cortante en 2 direcciones (falla por punzonamiento)

#columna interior
b1i = C1i + d
b2i = C2i + d
Vui = Rui - qu*(b1i/12)*(b2i/12)
b0i = 2*b1i + 2*b2i
alpha_si = 40 #columna interior
bi = ((max(C1i, C2i))/(min(C1i, C2i)))
phi_Vci = 0.75 * (min(4, (2+(4/bi)), 2+((alpha_si*d)/b0i))) * 1.0 * ((math.sqrt(fc*1000))/1000) * b0i * d 

#columna exterior 
b1e = C1e + ((1/2)*d)
b2e = C2e + d
b0e = 2*b1e + b2e
u = (b1e ** 2)/(b0e)
Vue = Rue - qu*(b1e/12)*(b2e/12)
Mue = (Rue*((b1e/12)-(m/12)-(u/12)))-((qu*(b1e/12)*(b2e/12))*(((1/2)*(b1e/12))-(u/12)))
alpha_f = (1/(1+(2/3)*(math.sqrt(b1e/b2e))))
alpha_v = 1-alpha_f
Jce = 2*(((1/12)*b1e*(d**3))+((1/12)*d*(b1e**3))+(b1e*d*(((1/2)*(b1e-u))**2))) + (1/12)*b2e*(d**3)+b2e*d*(u**2)
Vue2 = (Vue/(b0e*d))+((alpha_v*Mue)/(Jce))*(b1e-u)
alpha_se = 30    #columna exterior
be = ((max(C1e, C2e))/(min(C1e, C2e)))
phi_Vce = 0.75 * (min(4, (2+(4/be)), 2+((alpha_se*d)/b0e))) * 1.0 * ((math.sqrt(fc*1000))/1000) * b0e * d 

#Diseño de cortante a una direccion (se debe tener en cuenta de que es el caso de una zapata cuadrada)
Vui1 = (1/2)*qu*((B/12)-(C1i/12)-(2*(d/12)))*Lreq      #valor en k
g_req_vui1 = (Vui1/(0.75*8*1.0*((math.sqrt(fc*1000))/1000)*(Lreq*12)*d)) ** 3     #gamma requerida por cortante, teniendo en cuenta a phi como 0.75 y lambda como 1.0
As_req_vui1 = g_req_vui1 * (Lreq*12) * d     #acero requerido por cortante en pulgadas

Vue1 = (1/2)*qu*((B/12)-(C1e/12)-(2*(d/12)))*Lreq      #valor en k
g_req_vue1 = (Vue1/(0.75*8*1.0*((math.sqrt(fc*1000))/1000)*(Lreq*12)*d)) ** 3     #gamma requerida por cortante, teniendo en cuenta a phi como 0.75 y lambda como 1.0
As_req_vue1 = g_req_vue1 * (Lreq*12) * d     #acero requerido por cortante en pulgadas

#Diseño a flexion en la direccion principal (para la primera columna)
Mui1 = (1/8) * qu * (((B/12)-(C1i/12)) ** 2) * Lreq    #Momento ultimo en kft
As_req_Mui1 = (Mui1*12) / (0.9*fy*0.95*d)      #acero requerido por momentos en pulgadas
As_min_ui1 = 0.0018*((Lreq*12)*h)       #valor minimo de acero

As1i = max(As_req_vui1, As_req_Mui1, As_min_ui1)
N_reqi1 = As1i/Abt
S_reqi1 = math.floor((Lreq*12)/N_reqi1)
S_maxi1 = min((3*h), 18)
S_mini1 = max(1, (6*dbt), ((4/3)*(3/4)))    #teniendo en cuenta que el diametro del agregado es 3/4 pulgadas

As_ini1 = Abt * ((Lreq*12)/S_reqi1)     #acero requerido en pulgadas
ai1 = (As_ini1 * fy) / (0.85 * fc * (Lreq * 12))
B1i1 = 0.85 - 0.05 * (((fc*1000)-4000)/1000)
c_div_dti1 = 0.003 / ((fy / 29000) + 0.006)
a_div_b1di1 = ai1 / (B1i1*d)

phiMni1 = (0.9*As_ini1*fy*(d-(ai1/2)))/12     #phiMn en valor de kft

#Diseño a flexion en la direccion principal (para la segunda columna)
Mue1 = (1/8) * qu * (((B/12)-(C1e/12)) ** 2) * Lreq    #Momento ultimo en kft
As_req_Mue1 = (Mue1*12) / (0.9*fy*0.95*d)      #acero requerido por momentos en pulgadas
As_min_ue1 = 0.0018*((Lreq*12)*h)       #valor minimo de acero

As1e = max(As_req_vue1, As_req_Mue1, As_min_ue1)
N_reqe1 = As1e/Abt
S_reqe1 = math.floor((Lreq*12)/N_reqe1)
S_maxe1 = min((3*h), 18)
S_mine1 = max(1, (6*dbt), ((4/3)*(3/4)))    #teniendo en cuenta que el diametro del agregado es 3/4 pulgadas

As_ine1 = Abt * ((Lreq*12)/S_reqe1)     #acero requerido en pulgadas
ae1 = (As_ine1 * fy) / (0.85 * fc * (Lreq * 12))
B1e1 = 0.85 - 0.05 * (((fc*1000)-4000)/1000)
c_div_dte1 = 0.003 / ((fy / 29000) + 0.006)
a_div_b1de1 = ae1 / (B1e1*d)

phiMne1 = (0.9*As_ine1*fy*(d-(ae1/2)))/12     #phiMn en valor de kft

#Diseño a flexion en la direccion secundaria (para la primera columna) (crear codigo para calculo de esta)

#Diseño a flexion en la direccion secundaria (para la segunda columna) (crear codigo para calculo de esta)

#Diseño de dovelas
Bui = 1.2*pdi + 1.6*pli
A1i = C1i*C2i
A2i = min(((4*h)+C1i), B) ** 2
phi_Bni = 0.65 * 0.85 * min(fc, min(math.sqrt(A2i/A1i), 2), fc) * A1i

As_mini = 0.005*A1i 

dovelas_i = 0
while dovelas_i*Abt < As_mini:
    dovelas_i += 1


Bue = 1.2*pde + 1.6*ple
A1e = C1e*C2e
A2e = min(((4*h)+C1e), B) ** 2
phi_Bne = 0.65 * 0.85 * min(fc, min(math.sqrt(A2e/A1e), 2), fc) * A1e

As_min_e = 0.005*A1e

dovelas_e = 0
while dovelas_e*Abt < As_min_e:
    dovelas_e += 1

#Falla por anclaje inadecuado
la_i = (B-C1i-(2*rec))/2    #la en pulgadas
la_e = (B-C1e-(2*rec))/2 

#Encontrar el valor de alpha
if dbt < 0.76:
        alpha = 25
else:
        alpha = 20
#Encontrar el valor de psi
if fy <= 60:
        psi = 1.00
elif fy == 80:
        psi = 1.15
elif fy == 100:
        psi = 1.30
else:
        print("cambia el valor")

ld = ((fy * psi * 1.00 * 1.00) / (alpha * 1.00 * ((math.sqrt(fc * 1000)) / 1000))) * dbt

print("hmin: ", hmin)
print("d_sup: ", d_sup)
print("d_inf: ", d_inf)
print("d: ", d)
print("m: ", m)
print("Pse: ", Pse)
print("Psi: ", Psi)
print("qsA: ", qsA)
print("Lreq: ", Lreq)
print("Base_requerida: ", Base_requerida)
print("B: ", B)
print("Pue: ", Pue)
print("Pui: ", Pui)
print("qu: ", qu)
print("wu: ", wu)
print("Rui: ", Rui)
print("Rue: ", Rue)
print("b1i: ", b1i)
print("b2i: ", b2i)
print("Vui: ", Vui)
print("b0i: ", b0i)
print("alpha_si: ", alpha_si)
print("bi: ", bi)
print("phi_Vci: ", phi_Vci)
print("b1e: ", b1e)
print("b2e: ", b2e)
print("b0e: ", b0e)
print("u: ", u)
print("Vue: ", Vue)
print("Mue: ", Mue)
print("alpha_f: ", alpha_f)
print("alpha_v: ", alpha_v)
print("Jce: ", Jce)
print("Vue2: ", Vue2)
print("alpha_se: ", alpha_se)
print("be: ", be)
print("phi_Vce: ", phi_Vce)
print("Vui1: ", Vui1)
print("g_req_vui1: ", g_req_vui1)
print("As_req_vui1: ", As_req_vui1)
print("Vue1: ", Vue1)
print("g_req_vue1: ", g_req_vue1)
print("As_req_vue1: ", As_req_vue1)
print("Mui1: ", Mui1)
print("As_req_Mui1: ", As_req_Mui1)
print("As_min_ui1: ", As_min_ui1)
print("As1i: ", As1i)
print("N_reqi1: ", N_reqi1)
print("S_reqi1: ", S_reqi1)
print("S_maxi1: ", S_maxi1)
print("S_mini1: ", S_mini1)
print("As_ini1: ", As_ini1)
print("ai1: ", ai1)
print("B1i1: ", B1i1)
print("c_div_dti1: ", c_div_dti1)
print("a_div_b1di1: ", a_div_b1di1)
print("phiMni1: ", phiMni1)
print("Mue1: ", Mue1)
print("As_req_Mue1: ", As_req_Mue1)
print("As_min_ue1: ", As_min_ue1)
print("As1e: ", As1e)
print("N_reqe1: ", N_reqe1)
print("S_reqe1: ", S_reqe1)
print("S_maxe1: ", S_maxe1)
print("S_mine1: ", S_mine1)
print("As_ine1: ", As_ine1)
print("ae1: ", ae1)
print("B1e1: ", B1e1)
print("c_div_dte1: ", c_div_dte1)
print("a_div_b1de1: ", a_div_b1de1)
print("phiMne1: ", phiMne1)
print("Bui: ", Bui)
print("A1i: ", A1i)
print("A2i: ", A2i)
print("phi_Bni: ", phi_Bni)
print("As_mini: ", As_mini)
print("dovelas_i: ", dovelas_i)
print("Bue: ", Bue)
print("A1e: ", A1e)
print("A2e: ", A2e)
print("phi_Bne: ", phi_Bne)
print("As_min_e: ", As_min_e)
print("dovelas_e: ", dovelas_e)
print("la_i: ", la_i)
print("la_e: ", la_e)
print("alpha: ", alpha)
print("psi: ", psi)
print("ld: ", ld)


