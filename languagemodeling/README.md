# Ejercicio 1.

El módulo corpus_reader.py consta de dos funciones:
  - sents: a partir de texto plano devuelve de manera lazy las sentencias tokenizadas asumiendo como tokens los signos de puntuación.
  - corpus: lo mismo que lo anterior pero devuelve todas las oraciones tokenizadas.

Para separar las oraciones usamos split('.') y para tokenizar usamos una expresión regular que busca palabras o signos de puntuación.

### Ejercicio 2.

La interfaz de n-gramas cuenta con los siguientes atributos:

* el orden del modelo,
* el símbolo que marca el inicio de una oración, 
* un diccionario que guarda los recuentos de n-gramas y (n-1)-gramas.

Para inicializar los conteos concatemanos (n-1) veces el símbolo de inicio al comienzo de cada sentencia y el símbolo de STOP al final. Usamos este diccionario para implementar la probabilidad condicional, y con ella las funciones que computan la probabilidad de la sentencia y las log probabilidades.

### Ejercicio 3.

Para inicializar probs y sorted_probs usamos map para calcular las probabilidades condicionales y generar diccionarios y reduce para mezclarlos.

Oraciones con un modelo de unigramas entranado con letras de Divididos (generador
de rock natural):

>luz No importante mar ? luz de ? si un vuelto la

>angustia No la de

>alba alba ser

>El ser papá

Con bigramas:

>la hilacha lavando el alba

>Luz , hay un hombre que si asi como asi como vianda de un gran favor

>Y mostraste la cancion en la tinta

>Si El papel y religi ? ita voladora que redact regula el ciclope del alma soy un hombre que olvido su dolor

Con trigramas:

>Que hay de esa imagen en mi infierno si ya fui roto a tomar aire caminastes por mis >brazas me soñé en la oscuridad me estrellé contra mi

>Mezcla rara de angustia y canita voladora que si asi como asi somos ? api de mama No >pensar

>Encarnada en un pie que olvido su dolor

>Hubo un tiempo que fui hermoso y fui preso de verdad

Con cuatrigramas:

>El papel

>Y mostraste la hilacha lavando el traje de papá

>Pero algo nos junt ? fue la ? api de mam ?

>Buenos Aires se ve como vianda de ayer

### Ejercicio 4.

La clase AddOneNGram hereda de NGram e implementa una nueva funcion V que usa los
counts para calcular el tamaño del vocabulario. 

### Ejercicio 5.

Perplexity y entropy para los modelos del ejercicio anterior:

- Unigrama. Perplexity: 267.5753862186347, entropy: 8.063801600920309
- Bigrama. Perplexity: 183.18369983121548, entropy: 7.517147324110752
- Trigrama. Perplexity: 183.7899831500141, entropy: 7.521914329341818
- Cuatrigrama. Perplexity: 183.76080539223014, entropy: 7.521685274703058

Debería mejorar más. Se usó un corpus de entrenamiento muy pequeño por ser el proceso de entrenamiento muy lento. 

### Ejercicio 6.

Entropía y perplejidad para InterpolatedNGram:

- Unigramas. Perplejidad: 318.5236584777838, entropía: 8.315256723012844
- Bigramas. Perplejidad: 457.251611698827, entropía: 8.836844444900837
- Trigramas. Entropía: 8.340428566116772, perplejidad: 324.1299596063715
- Cuatrigramas. Perplejidad: 411.307167158278, entropía: 8.68407240125225

### Ejercicio 7.

Unigramas:
Entropy:
7.487777508980411
Perplexity:
179.49222083272036

Bigramas:
Entropy:
7.966029648775438
Perplexity:
250.04252197667188

Trigramas:
Entropy:
8.483783829526677
Perplexity:
357.99207236242336

Cuatrigramas:
Entropy:
8.463972549826778
Perplexity:
353.1096773023866


