from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from eleve import *

url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "CHPF60Fmc4WWf1tNKXqjRUVm2we9FU3YTqAJE23oNmURgJcMwnacqN5UIRd_PdM01fq-sqM-lIJH6jOz2meqeg=="
org = "Tricot"
bucket = "CyberPhysique"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def envoyer_donnees(eleves, nom_cours):
    for eleve in eleves:
        point = Point("cours")\
            .tag("nomCours", nom_cours)\
            .tag("eleve", eleve.nom)\
            .field("presence", eleve.presence)\
            .field("certitude", eleve.certitude)
        write_api.write(bucket=bucket, org=org, record=point)

eleves = [Eleve("Alice", True, 90), Eleve("Bob", False, 70)]
envoyer_donnees(eleves, "Cours A")
client.close()
