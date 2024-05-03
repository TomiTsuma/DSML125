from pyspark.sql import SparkSession
import findspark
findspark.init()

spark = SparkSession.builder \
    .appName("New Spectral DB connection") \
    .config("spark.jars", "file:///home/tom/DSML125/lib/postgresql-42.7.3.jar") \
    .getOrCreate()

url = "jdbc:postgresql://db-postgresql-cl1-do-user-2276924-0.db.ondigitalocean.com:25060/MandatoryMetadata"
properties = {
    "user": "doadmin",
    "password": "yzmodwh2oh16iks6",
    "driver": "org.postgresql.Driver",
}

spectraldata = spark.read \
    .format("jdbc") \
    .option("url", url) \
    .option("dbtable", f"historical.spectraldata") \
    .option("user", "doadmin") \
    .option("password", "yzmodwh2oh16iks6") \
    .option("driver", "org.postgresql.Driver") \
    .option("port","25060") \
    .load() 

mandatorymetadata = spark.read \
    .format("jdbc") \
    .option("url", url) \
    .option("dbtable", f"historical.mandatorymetadata") \
    .option("user", "doadmin") \
    .option("password", "yzmodwh2oh16iks6") \
    .option("driver", "org.postgresql.Driver") \
    .option("port","25060") \
    .load() 


spc = spectraldata.join(mandatorymetadata, spectraldata.metadata_id == mandatorymetadata.metadata_id, 'inner').select(spectraldata.metadata_id, spectraldata.averaged_spectra, mandatorymetadata.sample_code).collect() 

spc.show(2)


# spark.current_schema("historical")
# joined_df = spark.sql("""
#     SELECT 
#         spectraldata.metadata_id, spectraldata.averaged_spectra, mandatorymetadata.sample_code  
#     FROM 
#         spectraldata
#     INNER JOIN 
#         mandatorymetadata 
#     ON 
#         mandatorymetadata.metadata_id = spectraldata.metadata_id 
#     WHERE 
#         is_finalized=True AND passed=True AND is_active=True AND averaged=True
# """)

# joined_df.show()

# spectraldata = spark.read.jdbc(url=url,properties=properties, table="historical.spectraldata")
# spectraldata = spark.filter(
#     (spectraldata['is_finalized'] == True) &
#     (spectraldata['passed'] == True) &
#     (spectraldata['is_active'] == True) &
#     (spectraldata['averaged'] == True)
# )
# mandatorymetadata = spark.read.jdbc(url=url,properties=properties, table="historical.mandatorymetadata")
# mandatorymetadata = spark.filter(
#     mandatorymetadata['is_finalized']
# )
# spc_df = spectraldata.join(mandatorymetadata, spectraldata.metadata_id == mandatorymetadata.metadata_id)