# Proyecto de Inteligencia Artificial: Jugador HEX

Implementación de un jugador virtual utilizando los conocimientos teóricos adquiridos en las clases de la asignatura Inteligencia Artificial. Se empleó un algoritmo MinMax con una heuristica basada en el camino más corto para obtener la meta.

## Fase Inicial del Juego

Durante la Fase inicial de la partida, llamemos fase inicial a cuando aun no se han colocado mas piezas que la mitad del tablero, el jugador virtual no iniciará el algoritmo minmax, ya que aún no hay información suficiente en el tablero.

La primera jugada estará encaminada en apoderarse del centro, si este libre, lo ocupará, sino pues tomará una de sus adyacencias. Esto debido a que en las fases iniciales de una partida, controlar el centro es ideal para el desarrollo del juego, ya que existe una alta probabilidad de que los caminos pasen por esa zona.

Lo siguiente será la formación de puentes. Aquí la función de evaluación dará más peso a la casilla obtenida si:

- Forma un puente con alguna casilla existente
- Acorta el camino de costo minimo a la meta
- Alarga el camino del oponente

De esta forma para las fases iniciales se tendrá una estructura sólida antes de comenzar el MinMax.

## Priorizar celdas une-puentes

Durante todo el juego se le dará prioridad a este aspecto, ya que los puentes se hacen para facilitar el camino a la meta. Si el oponente selecciona una de las casillas existentes entre tu puente, pues la IA selecciona la otra casilla, de esta manera crea una conexion solida para su camino.

## MinMax

El algoritmo MinMax es el clásico algoritmo donde el jugador virtual prioriza maximizar y el oponente minimizar. Para este punto ya en el tablero habrá un número significativo de casillas ocupadas por lo que disminuye la cantidad de opciones a explorar. La función heuristica de evaluación consiste en:

- Si al colocar una ficha en una posición, da la victoria se devuelve con maximo valor
- Si al colocar una ficha en una posición, da la victoria al oponente se devuelve con minimo valor
- Se prioriza disminuir la distancia del camino mínimo propio
- Se da puntuación extra si aumenta la distancia del camino mínimo del oponente

Las dos primeras estrategias, se llaman *Fichas criticas*, y se analizan justo antes de comenzar la busqueda MinMax para no mandar a correr el algoritmo de forma innecesaria. Las otras dos utilizan un algoritmo de búsqueda de camino de costo mínimo.

## Algoritmo de Búsqueda Planteado

Como se notó la heurisitca empleada calcula el camino de costo para determinar si la jugada analizada es la mejor o no. Para lograr esto se usó el algoritmo de BFS 0-1.

El algoritmo BFS nos da el camino de longitud mínima desde un origen a todos los nodos del grafo. Básicamente es lo mismo que obtener el camino de costo mínimo, si todas las aristas del grafo tiene costo 1.

La modelación de cada celda del tablero se hizo de la siguiente forma:
$$
C(i,j) =
\begin{cases}
1 & \text{si } B[i,j] = 0 \\
0 & \text{si } B[i,j] = \alpha \\
\infty & \text{en otro caso}
\end{cases}
$$
donde $B[i,j]$ es la celda $(i,j)$ del tablero y $\alpha$ es el valor de la casilla del jugador

De esta manera, se corre el algoritmo BFS 0-1 ignorando incluso las casillas del adversario, ya que aporta peso infinito. Al usar una cola de inserción al inicio y al final, la constante de agregar la celda adyacente se reduce a $O(1)$ mucho más eficiente que el algoritmo Djkistra que es $O(log n)$. Además al insertar en la cola primero las celdas de costo 0, se prioriza siempre avanzar por las casillas que ya colocaste primero, lo cual es imprescindible para la poda Alpha Beta del algoritmo MinMax, ya que se analizan primero las mejores jugadas.
