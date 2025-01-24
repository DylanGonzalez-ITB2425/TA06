# TA06

1. Obtención de los datos

*Solicitamos la API KEY generada en la OPENDATA AEMET*

![API](https://github.com/user-attachments/assets/d2564348-3eaa-478a-aa10-0e2a797d64ab)

![API2](https://github.com/user-attachments/assets/eac65133-a99a-47d3-9113-691cfbce5fce)

*Correo de alta en el servicio AEMET OPENDATA*

![API3](https://github.com/user-attachments/assets/0a2ebc0e-c0aa-4a77-9d9c-faf9918af72e)

![API4](https://github.com/user-attachments/assets/0b22bcb6-8abc-4bcf-a048-4157dd7ea2a2)

*En el centro de descarga de la pagina oficial de la AEMET se descarga el siguiente fichero y se extrae en formato ZIP*

![API5](https://github.com/user-attachments/assets/8ea8c162-87a1-41c6-944c-183996509954)


![API6](https://github.com/user-attachments/assets/1564e373-2930-4106-be5e-ebc3a7c641f2)


2  Organitzar i processar les dades

- Primero debemos filtrar todos los archivos y detectar todos aquellos que contengan algún tipo de error.
  
- Para poder organizarlo le hemos pasado unos parámetros a cumplicar, cualquier tipo de anomalia se contará como un error y nos notificará el tipo y el lugar
  
- A la hora de establecer los parametros nos hemos basado el primer archivo, el numero de columnas, filas y su formato, de los demás archivos, han de ser el mismo que el archivo principal.
  
- Tambien antes de procesar los archivos, se comprueba que la carpeta especificada exista. Si no es así, se muestra un mensaje informativo al usuario y el proceso se detiene de manera segura.
  
- Se valida que la lista de valores para cada año no esté vacía antes de realizar la división, evitando errores por división entre cero y asegurando cálculos confiables.

Al momento de procesar los datos los hemos agrupado en 17 bloques de 1.000 para hacer más rápida su lectura. A su vez también hemos agrupado los errores con el objetivo de mejorar el rendimiento del proceso. Se encapsulan las operaciones críticas dentro de bloques try-except, permitiendo manejar errores inesperados sin interrumpir el procesamiento de otros archivos o datos.



Para aquellos valores nulos (-999) se han transformado, en el programa, a NONE para poder procesarlos y despúes han vuelto a su formato original.

*CALCULO DE PORCENTAJES*

