# SR4-Flat-Shading

Instrucciones (se realiza en el archivo **main.py**): 
1. Se define un *width* y un *height* con valores enteros
2. Se inicializa la funcion **glInit(width, height)**
3. Se inicializa la funcion **load('./models/pumpkin.obj', (t1, t2, t3), (s1, s2, s3))**. t1, t2 y t3 son valores para que se transforme en *x*, *y* y *z* respectivamente el resultado y s1, s2 y s3 son valores para cambiar el tamaño del modelo tanto en el eje x, eje y y eje z respectivamente.
4. Se inicializa la funcion **glFinish("nombreDelArchivo.bmp", width, height)**.

Un buen resultado se puede encontrar en el archivo main.py con valores prederminados pero igual pueden ser cambiados. El zbuffer ya es renderizado dentro de la funcion **glInit**
por lo tanto no se debe hacer mayor trabajo.
