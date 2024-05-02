import math

#definir: qa, fc, fy, pd, pl, t, df, Ab, db
#proponer h y considerar rec
# Solicitar al usuario que introduzca los valores de γc y γs
qa = float(input("Introduce el valor de qa (ksf): "))
fc = float(input("Introduce el valor de fc (ksi): "))
fy = float(input("Introduce el valor de fy (ksi): "))
pd = float(input("Introduce el valor de la carga muerta (k): "))
pl = float(input("Introduce el valor de la carga viva (k): "))
df = float(input("Introduce el valor de la profundidad en la zapata (ft): "))
t = float(input("Introduce el valor de el ancho de la columna (in): "))
Ab = float(input("Introduce el valor de el area de la barra de acero (in): "))
db = float(input("Introduce el valor de el diametro de la barra de acero (in): "))
gamma_c = float(input("Introduce el valor de γc (KCF): "))
gamma_s = float(input("Introduce el valor de γs (KCF): "))
rec = float(input("Introduce el valor de el recubrimiento (in): "))
h = float(input("Introduce el valor de el alto de la zapata (in): "))

hmin = 6 + rec + ((1/2)*db)
d = h - rec - ((1/2)*db)

#base que evita la falla por aplastamiento del suelo

Base_requerida = math.sqrt(((1.0*pd)+(1.0*pl))/((qa-(gamma_s*(df-(h/12)))-(gamma_c*(h/12)))))    # Base en valor de ft
B = math.ceil(Base_requerida*12)     #Base redondeada en valor de pulgadas

qu = ((1.2*pd)+(1.6*pl))/((B/12) ** 2)     #valor en ksf

#Falla por cortante en 2 direcciones, fallas por funcionamiento

Vu = qu * (((B/12) ** 2) - (((t/12)+(d/12)) ** 2))
b0 = 4 * (t + d)
alpha_s = 40    #columna interior
B0 = t/t
phi_Vn = 0.75 * min(4 ,(2+(4/B0)), (2+((alpha_s*d)/b0))) * 1.0 * ((math.sqrt(fc*1000))/1000) * b0 * d   #phi = 0.75, lambda = 1.0
# print(phi_Vn, ">=", Vu)
#Falla por cortante en una direccion
Vu1 = (1/2) * qu * ((B/12) - (t/12) - (2*(d/12))) * B/12
g_req_v = ((Vu1/(0.75*8*1.0*((math.sqrt(fc*1000))/1000)*B*d)) ** 3)    #gamma requerida por cortante, teniendo en cuenta a phi como 0.75 y lambda como 1.0
As_req_v = g_req_v * B * d     #acero requerido por cortante en pulgadas
#Falla por flexion
Mu = (1/8) * qu * (((B/12)-(t/12)) ** 2) * B    #Momento ultimo en kft
As_req_M = (Mu*12) / (0.9*fy*0.95*d)      #acero requerido por momentos en pulgadas
As_min = 0.0018*(B*h)       #valor minimo de acero
As = max(As_req_v, As_req_M, As_min)
N_req = math.ceil(As/Ab)
S_req = math.floor((B-(2*rec)-2*(1/2)*db)/(N_req)-1)
S_max = min((2*h), 18)
S_min = max(1, (6*db), ((4/3)*(3/4)))    #teniendo en cuenta que el diametro del agregado es 3/4 pulgadas
As_in = N_req*Ab
a = (As_in*fy)/(0.85*fc*B)
B1 = 0.85 - 0.05 * (((fc*1000)-4000)/1000)
c_div_dt = 0.003 / ((fy / 29000) + 0.006)
a_div_b1d = a / (B1*d)
phiMn = (0.9*As_in*fy*(d-(a/2)))    #phiMn en valor de kft
#Falla por aplastamiento del concreto
Bu = 1.2*pd + 1.6*pl
A1 = t ** 2
A2 = min(((4*h)+t), B) ** 2
phi_Bn = 0.65 * 0.85 * min(fc, min(math.sqrt(A2/A1), 2), fc) * A1

As_min = 0.005*A1 

dovelas = 0
while dovelas*Ab < As_min:
    dovelas += 1

#Falla por anclaje inadecuado
la = (B-t-(2*rec))/2    #la en pulgadas
#Encontrar el valor de alpha
if db < 0.76:
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

ld = ((fy * psi * 1.00 * 1.00) / (alpha * 1.00 * ((math.sqrt(fc * 1000)) / 1000))) * db

print (hmin, "<", h, "si esto no cumple considera una diferente altura de zapata ")
print (S_min, " < ", S_req, " < ", S_max, " Si el valor no concuerda hay problemas con la separacion de las barras")
print (0.65, "<", B1, "<", 0.85, "Si B1 es mayor a 0.85 se usa 0.85")
print (phiMn >= Mu, "si cumple esta bien en momentos")
print (ld > 12, " Si esto se cumple no se requieren ganchos estandar de 90° en los extremos de las barras. ")

print("Profundidad efectiva, d: ", d)
print("Base, B: ", B)
print("Capacidad última del suelo, qu: ", qu)
print("Capacidad cortante última, Vu: ", Vu)
print("el valor de b0 es: ", b0)
print("el valor de alpha_s es: ", alpha_s)
print("el valor de B0 es: ", B0)
print("el valor de phi_Vn es: ", phi_Vn)
print("el valor de Vu1 es: ", Vu1)
print("Cuantía por cortante, g_req_v: ", g_req_v)
print("Acero requerido por cortante, As_req_v: ", As_req_v)
print("Momento último, Mu: ", Mu)
print("Acero requerido por momento, As_req_M: ", As_req_M)
print("Acero mínimo, As_min: ", As_min)
print("Acero utilizado, As: ", As)
print("Número de barras requeridas, N_req: ", N_req)
print("Separación requerida, S_req: ", S_req)
print("Separación máxima, S_max: ", S_max)
print("Separación mínima, S_min: ", S_min)
print("Cantidad de acero en pulgadas, As_in: ", As_in)
print("Valor de a: ", a)
print("Valor de beta 1, B1: ", B1)
print("c/dt: ", c_div_dt)
print("a_div_b1d", a_div_b1d)
print("phi de Mn: ", phiMn)
print("este es el valor de Bu: ", Bu)
print("este es el valor de A1: ", A1)
print("este es el valor de A2: ", A2)
print("este es el valor de phi_bn: ", phi_Bn)
print("este es el valor As_min: ", As_min)
print("este es el numero de dovelas: ", dovelas)
print("Valor de la, la: ", la)
print("Valor de ld: ", ld)