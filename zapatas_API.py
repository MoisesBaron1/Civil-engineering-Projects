import math

#definir: qa, fc, fy, pd, pl, t, df, Ab, db
#proponer h y considerar rec
# Solicitar al usuario que introduzca los valores de γc y γs
qa = float(input("Introduce el valor de qa (ksf): "))
fc = float(input("Introduce el valor de fc (ksi): "))
fy = float(input("Introduce el valor de fy (ksi): "))
pd = float(input("Introduce el valor de la carga muerta (k/ft): "))
pl = float(input("Introduce el valor de la carga viva (k/ft): "))
df = float(input("Introduce el valor de la profundidad en la zapata (ft): "))
t = float(input("Introduce el valor de el ancho de la columna (in): "))
Ab = float(input("Introduce el valor de el area de la barra de acero (in): "))
db = float(input("Introduce el valor de el diametro de la barra de acero (in): "))
gamma_c = float(input("Introduce el valor de γc (KCF): "))
gamma_s = float(input("Introduce el valor de γs (KCF): "))
rec = float(input("Introduce el valor de el recubrimiento (in): "))
h = float(input("Introduce el valor de el alto de la zapata (in): "))
L = float(input("ingresa el valor de la longitud (ft) (si la zapata es corrida se recomienda usar 1): "))

hmin = 6 + rec + ((1/2)*db)
d = h - rec - ((1/2)*db)

#base que evita la falla por aplastamiento del suelo

Base_requerida = (((1.0*pd)+(1.0*pl))/((qa-(gamma_s*(df-(h/12)))-(gamma_c*(h/12)))*L))    # Base en valor de ft
B = math.ceil(Base_requerida*12)     #Base redondeada en valor de pulgadas

qu = ((1.2*pd)+(1.6*pl))/((B/12)*L)     #valor en ksf

#falla por cortante en una direccion

Vu = (1/2)*qu*((B/12)-(t/12)-(2*(d/12)))*L      #valor en k
g_req_v = (Vu/(0.75*8*1.0*((math.sqrt(fc*1000))/1000)*(L*12)*d)) ** 3     #gamma requerida por cortante, teniendo en cuenta a phi como 0.75 y lambda como 1.0
As_req_v = g_req_v * (L*12) * d     #acero requerido por cortante en pulgadas

#Falla por flexion en la direccion principal

Mu = (1/8) * qu * (((B/12)-(t/12)) ** 2) * L    #Momento ultimo en kft
As_req_M = (Mu*12) / (0.9*fy*0.95*d)      #acero requerido por momentos en pulgadas
As_min = 0.0018*((L*12)*h)       #valor minimo de acero

As = max(As_req_v, As_req_M, As_min)
N_req = As/Ab
S_req = math.floor((L*12)/N_req)
S_max = min((3*h), 18)
S_min = max(1, (6*db), ((4/3)*(3/4)))    #teniendo en cuenta que el diametro del agregado es 3/4 pulgadas

As_in = Ab * ((L*12)/S_req)     #acero requerido en pulgadas
a = (As_in * fy) / (0.85 * fc * (L * 12))
B1 = 0.85 - 0.05 * (((fc*1000)-4000)/1000)
c_div_dt = 0.003 / ((fy / 29000) + 0.006)
a_div_b1d = a / (B1*d)

phiMn = (0.9*As_in*fy*(d-(a/2)))/12     #phiMn en valor de kft

#Falla por temperatura y retraccion del concreto en la direccion secundaria 
As2 = 0.0018*B*h    #acero minimo usando el ancho de la zapata y el alto de la zapata
N2 = math.ceil(As2 / Ab)
S2 = math.ceil((B - (2 * rec) - (2 * (1 / 2) * db)) / (N2 - 1))

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
print(S_min, "<", S2, "<", S_max, " Si esto se cumple todo va perfecto")
print (ld > 12, " Si esto se cumple no se requieren ganchos estandar de 90° en los extremos de las barras. ")

print("Profundidad efectiva, d: ", d)
print("Base, B: ", B)
print("Capacidad última del suelo, qu: ", qu)
print("Capacidad cortante última, Vu: ", Vu)
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
print("phi de Mn: ", phiMn)
print("Acero en dirección secundaria, As2: ", As2)
print("Número de barras en la dirección secundaria, N2: ", N2)
print("Separación en la dirección secundaria, S2: ", S2)
print("Valor de la, la: ", la)
print("Valor de ld: ", ld)
