**MCOC-PROYECTO-2**

*CARACTERISTICAS DEL COMPUTADOR*

Modelo: ASUS X456U

Memoria RAM: 8 GB

Procesador: Intel Core i5-6200U (de hasta 2.8GHz)

S.O.: Windows 10 64 bits

*RESULTADOS*

        Saltation many particles faster                     Computador Maria Luisa                       Computador Joaquin
      N° particulas             Tiempo[s]             N° particulas           Tiempo[s]           N° particulas           Tiempo[s]
            2                      30,1                     2                                            2
            5                      75,9                     5                                            5
            10                    144,8                     10                                           10
            20                    323,7                     20                                           20

         Saltation many particles (entrega anterior)
       N° particulas             Tiempo[s]
            2                       60,7
            5                      390,5
            10                     1491,4
            20                     5768,3
 
 
*Anotaciones*

Se puede apreciar que a medida que aumenta el numero de particulas el tiempo que demora en simular la situacion se eleva 
exponencialmente, demorando un tiempo similar al obtenido por el profesor en su simulacion propia.

Por otro lado, una posible mejora para el codigo puede ser el que estamos creando condiciones iniciales nuevas cada vez que se reinicia el conteo, lo que claramente hace que vaya mas lento ya que de vez en cuando la consola nos muestra un mensaje que da cuenta de que se esta realizando un exceso de trabajo por lo que el codigo debe volver a pasar "por el mismo punto". Como esto puede suceder mas de una vez en el mismo punto claramente no es lo optimo. 

Sin embargo, se logro una notable mejora en cuanto a los tiempos que demora en correr el codigo, esto ya que se utilizan funciones mas efectivas, como por ejemplo slice, las que nos permiten hacer que el codigo sea mas corto y no tenga que pasar por otras funciones condicionales para ejecutarse. Ademas, es importante destacar en este aspecto que se utilizo una mayor cantidad de arreglos que en el codigo anterior, lo que permite que el programa se demore menos en ejecutar el codigo.

Finalmente, se puede apreciar una ligera diferencia con respecto a los tiempos de ejecucion de cada uno de nuestros computadores, lo que se nota en la diferencia en los procesadores de cada computador y en la memoria RAM.
