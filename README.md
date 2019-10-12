**MCOC-Proyecto-2**

_**Objetivo principal:**_ del proyecto consiste en implementar y validar un programa de simulación de transporte de sedimentos de fondo. 
Este se logra considerando un modelo lagrangiano, mediante el cual se sigue cada particula de manera individual, para luego ir 
extendiendolo para que funcione en cantidades de sedimentos mas grandes y cercanas a la realidad. Junto a esto, se busca comprender 
en que consiste el termino "complejidad computacional", en el cual se analiza como influyen las desiciones de algoritmo de implementacion,
ademas de estudiar los metodos INPUT-OUTPUT (IO) en el rendimiento del programa.

Para lograr el objetivo es importante tener la informacion y los conocimientos necesarios acerca del transporte de sedimentos y com-
prender porque es necesario su estudio. Si se junta mucha cantidad de sedimentos, estos disminuyen el volumen de diseño de un embalse o una represa, perjudicando la obra. 

Las particulas se pueden representar en un perfil de velocidades de manera logaritmica, siendo las de la pared aquellas que no se  mueven
(sedidmentos de fondo). Las particulas que estan cerca de la pared, las cuales son llamadas las del transporte de fondo, son arenas o 
gravas y se mueven rodando, arrastrandose sin rodar o saltando (mayoria). Esta utima es la que se estudia en el proyecto.

El analisis se hace considerando el movimiento del flujo de manera euleriana en un espacio, y luego considerando el movimiento de la 
particula de forma langrangiana. Se va a discretizar la particula, para luego en cada celda resolver navier stoke, y asi obtener el corte
y la presion. Si la presion y los cortes sen las celdas de la parte de arriba son mas grandes que los de abajo, entonces la particula
tiene una fuerza neta que va hacia arriba y se mueve. La particula pasa por un espacio con caracteristicas definidas (velocidades), y 
tiene cuatro formas tipicas de acoplarse. 

Como se va a considerar un perfil logaritmico para la velocidad del flujo, este cambia en la vertical y no en la horizontal (considerando 2 dimensiones), y asi, depende de a que altura "z" se encuentra. Luego se debe proceder a calcular las fuerzas aerodinámicas, para poder establecer una relacion entre las fuerzas aerodinamicas y el peso sumergido. Para ello se considera el cambio de momentum igual a la sumatoria de fuerzas (masa de la particula x la derivada de la velocidad es igual a  una aceleracion igual a la sumatoria de fuerzas). Es importante considerar y asegurar que la discretizacion en el tiempo que se hace es independiente de la
solucion. 

Las fuerzas importantes a considerar son el peso sumergido (empuje menos peso de la particula), fuerza de arrastre, fuerza de sustentacion, y fuerza de magnus. Se consideran los saltos de la particula para luego sacar un promedio en la altura h y el largo L
del salto, ademas de un promedio de la velocidad, la mediana y la deviacion estandar. Finalmente se podra comparar estos resultados con los existentes de una simulacion.

**Supuestos para la simulaciòn:**

- Diàmetro partìcula: 0.15 (mm)
- Densidad partìcula (obtenida por Nino and Garcia 1994): 2650 (kg/m3)
- Densidad agua: 1000 (kg/m3)
- Constante Drag (Cd): 0.47
- Constante de lifting (Cl): 0.2
- Constante de peso (Cm): 0.5



