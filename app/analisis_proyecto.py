import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg

# Crear la sesión Spark
spark = SparkSession.builder.appName("App_analisis_distribuido").getOrCreate()

# Leer el CSV
input_path = sys.argv[1]
output_dir = sys.argv[2]

df = spark.read.option("header", True).option("inferSchema", True).option("delimiter", ";").csv(input_path)

# Limpieza mínima
df = df.withColumnRenamed("Final price", "Final_price").withColumnRenamed("Storage type", "Storage_type")

# ================= Análisis 1 =================
# Marca, número de veces que aparece
brand_count = df.groupBy("Brand").agg(count("*").alias("count"))
brand_count.write.mode("overwrite").csv(f"{output_dir}/contar_marca", header=True)

# ================= Análisis 2 =================
# Marca, promedio de ventas (precio promedio)
brand_avg_price = df.groupBy("Brand").agg(avg("Final_price").alias("avg_price"))
brand_avg_price.write.mode("overwrite").csv(f"{output_dir}/promedio_precio_marca", header=True)

# ================= Análisis 3 =================
# Marca, Modelo, RAM >= 32, Almacenamiento en TB, Tipo de almacenamiento SSD, Precio
high_ram_tb_ssd = df.filter((col("RAM") >= 32) & 
                            (col("Storage").contains("TB")) & 
                            (col("Storage_type") == "SSD")) \
                   .select("Brand", "Model", "RAM", "Storage", "Storage_type", "Final_price")
high_ram_tb_ssd.write.mode("overwrite").csv(f"{output_dir}/laptops_Premium", header=True)

# ================= Análisis 4 =================
# Marca, promedio de precio para laptops táctiles
brand_touch_avg = df.filter(col("Touch") == "Yes").groupBy("Brand").agg(avg("Final_price").alias("avg_touch_price"))
brand_touch_avg.write.mode("overwrite").csv(f"{output_dir}/promedio_tactiles", header=True)

# ================= Análisis 5 =================
# Marca, Modelo, Tamaño de pantalla mayor a 16.0 pulgadas
large_screen_laptops = df.filter(col("Screen") > 16.0).select("Brand", "Model", "Screen")
large_screen_laptops.write.mode("overwrite").csv(f"{output_dir}/laptops_mas_grandes", header=True)

# ================= Análisis 6 =================
# Marca, Modelo, CPU, Si contiene RTX
gpu_rtx_laptops = df.filter(col("GPU").contains("RTX")).select("Brand", "Model", "CPU", "GPU")
gpu_rtx_laptops.write.mode("overwrite").csv(f"{output_dir}/gpu_rtx_laptops", header=True)
