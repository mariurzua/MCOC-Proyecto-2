Validación para múltiples partículas:

Para este punto la validación se hizo con 5, 7 y 10 partículas, con un perfil de velocidad logaritmico que solo depende de la altura donde se ubique la partícula.

Los resultados de la simulación son discutibles, ya que en el comportamiento de cada simulación es parecido al mostrado por el profesor, pero son muy diferentes al real, ya que hay varias excepciones y suposiciones que alejan a la simulacion de lo real.

Los resultados de cada simulación fueron:

Resultados

N° particulas             Tiempo[s]
      2                      206.0
      5                     305.5
      10                    1509.2

Las limitantes de los resultados son varias, primero el choque de particulas no corresponde a un intercambio de momentum entre dos particulas, sino a una constante fijada anteriormente que satisfaga un resultado acorde a los resultados reales. Segundo es el choque de las partículas con el suelo que deberia ser que el choque provocaría una perdida de momentum en la partícula, el que se muestra en el programa es un caso parecido al del choque entre partículas en que se simulo que el choque provocaría una fuerza igual a una constante multiplicada por la posicion de la partícula.

Los cuellos de botella de nuestro programa se provocan por las interacciones de las particulas entre sí y la interacción de las partículas con el suelo. 

La complicación empírica de este problema, es que para cada delta t se tiene que "integrar", por lo tanto si se tiene 100 partículas y se quiere ver la trayectoria en un tiempo T, entonces en cada delta t se tiene que integrar 100 por cada delta t. Esto se ve reflejado en el tiempo que demora la simulación, que aumenta por cada partícula que se agrega a la simulación.

Solución para acortar el tiempo entre cada simulación,  es ocupar el sistema operativo de linux para cada simulación, ya que el sistema operativo Windows es conocido por demorarse mucho más. En la simulación para 2 particulas en Windows demoró el tiempo de 206 segundos y en linux 69 segundos, cabe destacar que se ocupo el mismo equipo para cada simulación, lo único que cambio fue el sistema operativo ocupado. Como se puede observar hay una disminción de tiempo considerable, en conclusión es favorable ocupar linux a la hora de querer simular algun programa de python.




