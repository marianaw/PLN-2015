# Ejercicio 1.

Resultados de estadísticas sobre el corpus áncora:
Estadísticas básicas:
----------------------

Cantidad de oraciones:  517269
Cantidad de palabras:  46482
Cantidad de tags:  81
Cantidad de ocurrencias de palabras:  517269

Etiquetas más frecuentes:


|Tag    |Frecuencia     |Porcentaje|
|-----:------------:----------|
| sps |  70141  | 13.559869236316114 |
| da0 |  51828  | 10.019544956299335 |
| ncm |  46641  | 9.016778504027885 |
| ncf |  40880  | 7.903044644082673 |
| aq0 |  33904  | 6.554423327127664 |
| vmi |  30682  | 5.931536589279466 |
| fc |  30148   | 5.828302102001087 |
| np0 |  29113  | 5.62821278677052 |
| fp |  17513   | 3.3856658721090964 |
| rg |  15333   | 2.964221710560656 |

Palabras más frecuentes:


|Tag    |(Palabra, cantidad)|
|-----:-------------------|
| sps |  [('de', 28474), ('en', 12114), ('a', 8192), ('con', 4150), ('por', 4087)] |
| da0 |  [('la', 17897), ('el', 14524), ('los', 7758), ('las', 4882), ('El', 2817)] |
| ncm |  [('años', 849), ('presidente', 682), ('millones', 616), ('equipo', 457), ('partido', 438)] |
| ncf |  [('personas', 273), ('parte', 267), ('vida', 257), ('situación', 232), ('vez', 223)] |
| aq0 |  [('pasado', 393), ('gran', 275), ('mayor', 248), ('nuevo', 234), ('próximo', 213)] |
| vmi |  [('está', 564), ('tiene', 511), ('dijo', 499), ('puede', 381), ('hace', 350)] |
| fc |  [(',', 30148)] |
| np0 |  [('Gobierno', 554), ('España', 380), ('PP', 234), ('Barcelona', 232), ('Madrid', 196)] |
| fp |  [('.', 17513)] |
| rg |  [('más', 1707), ('hoy', 772), ('también', 683), ('ayer', 593), ('ya', 544)] |

Ambigüedad:


-------------------
|Palabra        | Nivel de ambigüedad   | Frecuencia|
|---------:----------------------:-----------|
| que   | 6             | 15391 |
| de    | 5             | 28478 |
| a     | 4             | 8200 |
| .     | 3             | 17520 |
| la    | 2             | 18100 |
| ,     | 1             | 30148 |



|Nivel de ambigüedad    |Cantidad de palabras   |Porcentaje del corpus|
|---------------------:----------------------:---------------------|
| 1             | 43889                 | 94.4214964932662 |
| 2             | 2344          | 5.042812271416892 |
| 3             | 213           | 0.4582419000903576 |
| 4             | 26            | 0.05593563099694505 |
| 5             | 6             | 0.01290822253775655 |
| 6             | 4             | 0.0086054816918377 |
| 7             | 0             | 0.0 |
| 8             | 0             | 0.0 |
| 9             | 0             | 0.0 |


### Ejercicio 3.
Resultados del modelo baseline:

1100.0% (0.30%)
Accuracy: 85.29%
Accuracy unknown words: 0.30%
Accuracy known words: 94.56%
Confusion matrix:
     ao0  aq0  cc  cs  dat  dd0  de0  di0  dn0  dp1  dt0  fs  fz  nc0  ncc
ao0    0    0   0   0    0    0    0    0    0    0    0   0   0    0    0
aq0    0    0   0   0    0    3    0   25    0    0    0   0   0    5   70
cc     0    0   0  22    0    0    0    0    0    0    0   0   0    0    0
cs     0    0   1   0    0    0    0    0    0    0    0   0   0    0    0
da0    0    0   0   0    0    0    0    0    0    0    0   0   0    0    0
dat    0    0   0   0    0    0    0    0    0    0    0   0   0    0    0
dd0    0    0   0   0    0    0    0    0    0    0    0   0   0    0    0
di0    0   27   0   0    0    0    0    0   28    0    0   0   0    0    0
dn0    0    9   0   0    1    0    0    0    0    0    0   0   0    0    0
dp1    0    0   0   0    0    0    0    0    0    0    0   0   0    0    0
dp3    0    0   0   0    0    0    0    0    0    0    0   0   0    0    0
dt0    0    0   0   0    0    0    0    0    0    0    0   0   0    0    0
fe     0    0   0   0    0    0    0    0    0    0    0   0   0    0    0
fg     0    0   0   0    0    0    0    0    0    0    0   0   0    0    0
fp     0    0   0   0    0    0    0    0    0    0    0   0   0    0    0



### Ejercicio 5.
Resultados para MLHMM:
n=1:
----

Accuracy: 64.48%
Accuracy unknown words: 0.01%
Accuracy known words: 71.51%
Confusion matrix:
     ao0  aq0  cc    cs  da0  dat  dd0  de0  di0  dn0  dp3  dt0  fp  fpt  fs
ao0    0    0   0     0    0    0    0    0    0    1    0    0   0    0   0
aq0    0    0   0     0    0    0    0    0    2    0    0    0   0    0   0
cc     0    0   0  1603    0    0    0    0    0    0    0    0   0    0   0
cs     0    0   0     0    0    0    0    0    0    0    0    0   0    0   0
da0    0    0   0     0    0    0    0    0    0    0    0    0   0    0   0
dat    0    0   0     0    0    0    0    0    0    0    0    0   0    0   0
dd0    0    8   0     0    0    0    0    0    0    0    0    0   0    0   0
di0    0   54   0     0    0    0    0    0    0    1    0    0   0    0   0
dn0    0    0   0     0    0    0    0    0    0    0    0    0   0    0   0
dp1    0    0   0     0    0    0    0    0    0    0    0    0   0    0   0
dt0    0    0   0     0    0    0    0    8    0    0    0    0   0    0   0
fe     0    0   0     0    0    0    0    0    0    0    0    0   0    0   0
fg     0    0   0     0    0    0    0    0    0    0    0    0   0    0   0
fpa    0    0   0     0    0    0    0    0    0    0    0    0   0    0   0
i      0    0   0     0    0    0    0    0    0    0    0    0   0    0   0


n=2:
----

Accuracy: 88.31%                                                                                                                                                   
Accuracy unknown words: 16.56%                                                                                                                                     
Accuracy known words: 96.14%                                                                                                                                       
Confusion matrix:                                                                                                                                                  
     ao0  aq0  cc  cs  da0  dat  dd0  de0  di0  dn0  dp1  dp3  dt0  fia  fs                                                                                        
ao0    0    0   0   0    0    0    0    0    0    0    0    0    0    0   0                                                                                        
aq0    0    0   0   0    0    0    0    0   67    1    0    0    0    0   0                                                                                        
cc     0    0   0  26    0    0    0    0    0    0    0    0    0    0   0                                                                                        
cs     0    0   0   0    0    0    0    0    0    0    0    0    0    0   0                                                                                        
da0    0  280   1  10    0   45    2    0    5    3    0    0    2    0   0                                                                                        
dat    0    1   0   0    0    0    0    0    0    0    0    0    0    0   0                                                                                        
dd0    0    0   0   0    0    0    0    0    0    0    0    0    0    0   0                                                                     
de0    0    0   0   0    0    0    0    0    0    0    0    0    3    0   0
di0    0   11   0   0    0    0    0    0    0   28    0    0    0    0   0
dn0    0    6   0   0    0    1    0    0    0    0    0    0    0    0   0
dp1    0    0   0   0    0    0    0    0    0    0    0    0    0    0   0
dt0    0    0   0   0    0    0    0    0    0    0    0    0    0    0   0
fc     0   18   0   1    0    0    0    0    0    0    0    0    0    0   0
fe     0    3   0   0    0    0    0    0    0    0    0    0    0    0   0
fg     0   12   0   0    0    7    0    0    0    0    0    0    0    0   0

n=3:
----
Accuracy: 88.48%
Accuracy unknown words: 20.32%
Accuracy known words: 95.91%
Confusion matrix:
     ao0  aq0  cc  cs  da0  dat  dd0  de0  di0  dn0  dp1  dp3  dt0  fs  fz
ao0    0    1   0   0    0    0    0    0    0    0    0    0    0   0   0
aq0    0    0   0   0    0    0    0    0   70    0    0    0    0   0   0
cc     0    1   0  25    0    0    0    0    0    0    0    0    0   0   2
cs     0    5   1   0    0    0    0    0    0    0    0    0    0   0   0
da0    0  180   5  14    0   42    2    0    5    4    0    0    1   0   1
dat    0    5   0   0    0    0    0    0    0    0    0    0    0   0   0
dd0    0    2   0   0    0    0    0    0    0    0    0    0    0   0   0
de0    0    0   0   0    0    0    0    0    0    0    0    0    3   0   0
di0    0   16   0   0    0    0    0    0    0   28    0    0    0   0   0
dn0    0   11   0   0    0    1    0    0    0    0    0    0    0   0   0
dp1    0    0   0   0    0    0    0    0    0    0    0    0    0   0   0
dp3    0    1   0   0    0    0    0    0    0    0    0    0    0   0   0
dt0    0    0   0   0    0    0    0    4    0    0    0    0    0   0   0
faa    0    2   0   0    0    0    0    0    0    0    0    0    0   0   0
fat    0    1   0   0    0    0    0    0    0    0    0    0    0   0   0

n=4:
-----
Accuracy: 87.65%
Accuracy unknown words: 18.67%
Accuracy known words: 95.17%
Confusion matrix:
     ao0  aq0  cc  cs  da0  dat  dd0  de0  di0  dn0  dp1  dp3  dt0  fs  fz
ao0    0    2   0   0    0    2    0    0    0    0    0    0    0   0   0
aq0    0    0   0   1    0    0    0    0   38    0    0    0    0   0   0
cc     0   15   0  24    0    0    0    0    0    0    0    0    0   0   0
cs     0    5   1   0    0    0    0    0    0    0    0    0    0   0   0
da0    0  140   5  12    0   36    2    0    5    3    0    0    1   0   2
dat    0    2   0   0    0    0    0    0    0    0    0    0    0   0   0
dd0    0    5   0   0    0    0    0    0    0    0    0    0    0   0   0
de0    0    4   0   0    0    0    0    0    0    0    0    0    3   0   0
di0    0   29   0   0    0    0    0    0    0   28    0    0    0   0   0
dn0    0   14   0   0    0    1    0    0    0    0    0    0    0   0   0
dp1    0    0   0   0    0    0    0    0    0    0    0    0    0   0   0
dp2    0    2   0   0    0    1    0    0    0    0    0    0    0   0   0
dp3    0    3   0   0    0    1    0    0    0    0    0    0    0   0   0
dt0    0    4   0   0    0    0    0    4    0    0    0    0    0   0   0
faa    0    0   0   0    0    0    0    0    0    0    0    0    0   0   0


### Ejercicio 7.

Memm with n=1:
--------------

Accuracy: 78.72%                                                                                                                                                   
Accuracy unknown words: 34.91%                                                                                                                                     
Accuracy known words: 83.50%                                                                                                                                       
Confusion matrix of ten tags:                                                                                                                                                  
     ao0  aq0   cc   cs  dat  dd0  de0  di0  dn0  dp1                                                                                                              
aq0    1    0    1    2    2   11    0  105   12    2                                                                                                              
cc     0    0    0   18    0    0    0    0    0    0                                                                                                              
cs     0    1    1    0    0    2    0    0    0    0                                                                                                              
da0   14  222  128  158   50  305    3  133   76   85                                                                                                              
di0    0    4    0    0    0    0    0    0   27    0                                                                                                              
fc     1   67    0    0    0    9    0    5    4    3                                                                                                              
fe     0    0    0    0    0    0    0    0    0    0
fp     0    1    0    0    0    0    0    0    0    0
ncf   80  287    4    0    3    7    0   39   52    3
ncm  147  370    1    1  133   82    0   49   85    2


