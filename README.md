# Cluster Apache Spark

Este repositorio contiene los archivos necesarios para la implementacion de un cluster de procesamiento de datos distribuido en Apache Spark Standalone. El cluster esta formado por un archivo .py y un csv ambos en carpetas distintas listos para su implementacion en 2 maquinas virtuales, una siendo el nodo maestro y la otra siendo un nodo worker

# Como usar el repositorio

1. Descargar e instalar VirtualBox desde https://www.virtualbox.org/wiki/Downloads
2. Descargar e instalar Vagrant desde https://developer.hashicorp.com/vagrant/downloads
3. Ejecutar vagrant up para crear las 2 maquinas virtuales
4. Ejecutar
```
vagrant ssh servidorUbuntu
vagrant ssh clienteUbuntu
```
Para ingresar a las maquinas virtuales

# Instalar Apache Spark en servidorUbbuntu
Instalar Java en Ubuntu
```
vagrant@servidorUbuntu:~$ sudo apt update
vagrant@servidorUbuntu:~$ sudo apt install -y openjdk-18-jdk
vagrant@servidorUbuntu:~$ java -version
```
Podras confirmar si Java se instalo junto con su version
## Descargar y descomprimir Spark
Verifique en https://dlcdn.apache.org/spark/ 
la ultima version de Spark y proceda a descargarla usando wget
En mi caso estoy usando la version 3.5.5, la cual es la version mas reciente, si en tu caso ya hay una version nueva existente debes cambiar los numero de la version en el comando de dercarga
```
vagrant@servidorUbuntu:~$ mkdir labSpark 
vagrant@servidorUbuntu:~$ cd labSpark/ 
vagrant@servidorUbuntu:~/labSpark$ wget https://dlcdn.apache.org/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz 
vagrant@servidorUbuntu:~/labSpark$ tar -xvzf spark-3.5.5-bin-hadoop3.tgz 
```
## Clonar este repositorio
Dentro del directorio labSpark realiza lo siguiente 
```
vagrant@servidorUbuntu:~/labSpark$ git clone https://github.com/BrayanTigreros/app_analisis
vagrant@servidorUbuntu:~/labSpark$ cd app_analisis
vagrant@servidorUbuntu:~/labSpark/app_analisis$ ls
app dataset
```
Puedes navegar entre estos 2 directorios, app tiene el codigo para el analisis de datos y dataset contiene el csv que la app va a analizar
# Configurar maquina clienteUbuntu
Realiza los mismos pasos para la maquina clienteUbuntu
Instala java, descarga y descomprime Spark y clona este repositorio
(Asegurate que las versiones de Spark para ambas maquinas sean las mismas y que los directorios que crees tenga los mismos nombre para evitar confusiones)

# Configurar el Cluster Spark
Configuraremos el cluster de Spark en multiples nodos, con el master y el worker corriendo en maquinas diferentes
Dirijete al directorio de configuracion de Spark
```
vagrant@servidorUbuntu:~/labSpark$ cd spark-3.5.0-bin-hadoop3/conf
```
Haz una copia del archivo de configuracion de variables de entorno de Spark
```
cp spark-env.sh.template spark-env.sh 
```
Edita y agregue al final las configuraciones de SPARK_LOCAL_IP y SPARK_MASTER_HOST así
```
SPARK_LOCAL_IP=192.168.100.2
SPARK_MASTER_HOST=192.168.100.2
```
Dirijete a sbin e inicia el master
```
vagrant@servidorUbuntu:~/labSpark/spark-3.5.0-bin-hadoop3/sbin$ ./start-master.sh
starting org.apache.spark.deploy.master.Master, logging to /home/vagrant/labSpark/spark-3.5.5-bin-hadoop3/logs/spark-vagrant-org.apache.spark.deploy.master.Master-1-servidorUbuntu.out 
```
Verifica en tu navegador usando la ip http://192.168.100.2:8080 para ver la interfaz del master

## Configurar e iniciar el worker en la maquina clienteUbuntu
Dirijete al directorio de configuracion de Spark
```
vagrant@servidorUbuntu:~/labSpark$ cd spark-3.5.0-bin-hadoop3/conf
```
Haz una copia del archivo de configuracion de variables de entorno de Spark
```
cp spark-env.sh.template spark-env.sh 
```
Edita y agregue al final las configuraciones de SPARK_LOCAL_IP y SPARK_MASTER_HOST así
```
SPARK_LOCAL_IP=192.168.100.3
SPARK_MASTER_HOST=192.168.100.2
```
Dirijete a sbin e inicia un worker en clienteUbuntu(Debes usar la URL que aparece en la interfaz de administrador del master)
```
vagrant@clienteUbuntu:~/labSpark/spark-3.5.0-bin-hadoop3/sbin$ ./start-worker.sh spark://192.168.100.2:7077
starting org.apache.spark.deploy.worker.Worker, logging to /home/vagrant/labSpark/spark-3.5.5-bin-hadoop3/logs/spark-vagrant-org.apache.spark.deploy.worker.Worker-1-clienteUbuntu.out
```
Revisa la deccion de worker en http://192.168.100.2:8080

# Lanzar la aplicacion
Para probar el cluster lanzaremos la aplicacion de este repositorio la cual usara el dataset de este mismo

IMPORTANTE: Antes de lanzar la aplicacion asegurate de crear el directorio "resultado" en la maquina clienteUbuntu

Una vez creado dirijete a bin y lanza la aplicacion

```
vagrant@servidorUbuntu:~/labSpark/spark-3.3.1-bin-hadoop3/bin$ ./spark-submit --master spark://192.168.100.2:7077 --conf spark.executor.memory=1g /home/vagrant/labSpark/app_analisis/app/analisis_proyecto.py "/home/vagrant/labSpark/app_analisis/dataset/*csv" "/home/vagrant/labSpark/resultado"
grant/labSpark/app_analisis/dataset/*csv" "/home/vagrant/labSpark/resultado"
25/05/22 06:04:50 INFO SparkContext: Running Spark version 3.5.5
25/05/22 06:04:50 INFO SparkContext: OS info Linux, 5.15.0-116-generic, amd64
25/05/22 06:04:50 INFO SparkContext: Java version 18.0.2-ea
25/05/22 06:04:50 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
25/05/22 06:04:50 INFO ResourceUtils: ==============================================================
25/05/22 06:04:50 INFO ResourceUtils: No custom resources configured for spark.driver.
25/05/22 06:04:50 INFO ResourceUtils: ==============================================================
25/05/22 06:04:50 INFO SparkContext: Submitted application: App_analisis_distribuido
25/05/22 06:04:50 INFO ResourceProfile: Default ResourceProfile created, executor resources: Map(memory -> name: memory, amount: 1024, script: , vendor: , offHeap -> name: offHeap, amount: 0, script: , vendor: ), task resources: Map(cpus -> name: cpus, amount: 1.0)
```
Verifica los resultados del analisis en "resultado" en clienteUbuntu
```
vagrant@clienteUbuntu:~/labSpark/resultado$ ls
contar_marca  gpu_rtx_laptops  laptops_mas_grandes  laptops_Premium  promedio_precio_marca  promedio_tactiles
vagrant@clienteUbuntu:~/labSpark/resultado$ cd contar_marca
vagrant@clienteUbuntu:~/labSpark/resultado/contar_marca$ ls
_temporary
vagrant@clienteUbuntu:~/labSpark/resultado/contar_marca$ cd _temporary
vagrant@clienteUbuntu:~/labSpark/resultado/contar_marca/_temporary$ ls
0
vagrant@clienteUbuntu:~/labSpark/resultado/contar_marca/_temporary$ cd 0
vagrant@clienteUbuntu:~/labSpark/resultado/contar_marca/_temporary/0$ ls
task_20250522060508249477865858796732_0004_m_000000  _temporary
vagrant@clienteUbuntu:~/labSpark/resultado/contar_marca/_temporary/0$ cd task_20250522060508249477865858796732_0004_m_000000
vagrant@clienteUbuntu:~/labSpark/resultado/contar_marca/_temporary/0/task_20250522060508249477865858796732_0004_m_000000$ ls
part-00000-b745a428-4a05-41b7-ba87-2c7446fbe547-c000.csv
vagrant@clienteUbuntu:~/labSpark/resultado/contar_marca/_temporary/0/task_20250522060508249477865858796732_0004_m_000000$ cat part-00000-b745a428-4a05-41b7-ba87-2c7446fbe547-c000.csv
Brand,count
Razer,1049
Millenium,2
Realme,1
Medion,31
HP,1386
Dell,1143
Jetwing,1
Primux,8
Dynabook Toshiba,19
Acer,1125
Asus,1379
Deep Gaming,8
Lenovo,1357
Vant,6
Samsung,1027
Thomson,4
LG,31
Microsoft,72
Prixton,3
Apple,1065
Innjoo,6
MSI,1277
Alurin,29
PcCom,24
Toshiba,997
Denver,1
```
Verifica la aplicacion lanzada en el dashboard en http://192.168.100.2:8080

# Pasar los resultados a la maquina anfitriona
Con los resultados en la maquina clienteUbuntu puedes pasarlos a tu maquina anfitriona haciendo uso del directorio sincronico de vagrant, asi
```
vagrant@clienteUbuntu:~$ cd labSpark
vagrant@clienteUbuntu:~/labSpark$ ls
analisis_distribuido  dataset  population  resultado  resultsCluster  resultsPopulation  spark-3.5.5-bin-hadoop3  spark-3.5.5-bin-hadoop3.tgz
vagrant@clienteUbuntu:~/labSpark$ find resultado -type f -name "*.csv" -exec cp {} /vagrant/ \;
```
Lo puedes confirmar asi
```
vagrant@clienteUbuntu:~/labSpark$ cd /vagrant/
vagrant@clienteUbuntu:/vagrant$ ls
2019-Dec.zip                                              part-00000-a9f20651-926e-4572-a303-c3a626ae2f78-c000.csv
laptops_csv_REI.zip                                       part-00000-b371e97b-bb11-4e41-a376-0ddc9a9dcde4-c000.csv
mynew.box                                                 part-00000-b745a428-4a05-41b7-ba87-2c7446fbe547-c000.csv
part-00000-46c81b23-f533-4217-9616-60a5d271d765-c000.csv  Vagrantfile
part-00000-60698991-288e-4aa1-ae4d-05ec15fd1985-c000.csv  Vagrantfile.txt
part-00000-883072b7-e8ef-4bb5-ab02-d85dc59fdc38-c000.csv  world_population.zip
vagrant@clienteUbuntu:/vagrant$
```
De esta forma se transfieren todos los csv de los directorios dentro del directorio "resultado" y se guardan en directorio compartido de vagrant en la maquina anfitriona

