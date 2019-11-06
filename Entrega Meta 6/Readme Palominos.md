Validación para múltiples partículas:

Para este punto la validación se hizo con 5, 7 y 10 partículas, con un perfil de velocidad logaritmico que solo depende de la altura donde se ubique la partícula.

Los resultados de la simulación son discutibles, ya que en el comportamiento de cada simulación es parecido al mostrado por el profesor, pero son muy diferentes al real, ya que hay varias excepciones y suposiciones que alejan a la simulacion de lo real.

Los resultados de cada simulación fueron:

Resultados

N° particulas             Tiempo[s]
      2                      206.0
      5                     305.5
      10                    1509.2

Validación para múltiples particulas con un método alternativo:

Para este punto la validación se hizo con 5, 7 y 10 partículas, con un perfil de velocidad logaritmico que solo depende de la altura donde se ubique la partícula, donde se separaron en cada delta de tiempo las partículas que chocaban entre sí y las que no chocan entre sí. 

Se hizo esta separación por que se quiere optimizar el tiempo de demora de la simulación y se determino de manera experimental que la parte que más demora en el método ocupado en las entregas anteriores fue la parte del choque entre partículas, esto hace que demoré el resto del programa, provocando un tiempo prolongado en cada simulación.

Los resultados de la simulación son discutibles, ya que en el comportamiento de cada simulación es parecido al mostrado por el profesor, pero son muy diferentes al real, ya que hay varias excepciones y suposiciones que alejan a la simulacion de lo real.

Los resultados de cada simulación fueron:

Resultados

N° particulas             Tiempo[s]
      2						Tiempo total:  56.4379999638

      5 					Tiempo total:  130.956998825

      10 					Tiempo total:  244.971999168

	  20					Tiempo total:  462.79200983

Como podemos ver los tiempos en cada unas de las simulaciones es mucho menor que en el método anterior. Entonces podemos decir que el enfoque que se dio fue el correcto ya que la implicancia que tenia el choque entre particulas en las demás particulas que solamente eran influenciadas con el entorno hacia que el la función odeint se demorára mucho más de lo deseado. 

Además podemos ver los resultados de mis compañeros:

Resultados 
  Computador Martin                    				Computador Maria Luisa                   
  N° particulas             Tiempo[s]             N° particulas           Tiempo[s]           
        2                      30,1                     2                   71,7                				
        5                      75,9                     5                  165,6                   
        10                    144,8                     10                 334,1                 
        20                    323,7                     20                2220,4                     

Podemos ver algunas similitudes en los tiempos pero sin embargo no son iguales, esto se puede asociar a que cada computador tiene diferentes procesadores y memoria RAM.
