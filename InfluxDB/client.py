from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from dispositif import *
from data import *

url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "CHPF60Fmc4WWf1tNKXqjRUVm2we9FU3YTqAJE23oNmURgJcMwnacqN5UIRd_PdM01fq-sqM-lIJH6jOz2meqeg=="
org = "Tricot"
bucket = "CyberPhysique"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def envoyer_donnees_dispositif(disositif):
    point = Point("dispositif")\
        .tag("ID_Dispositif", disositif.id)\
        .tag("Nom_Dispositif", disositif.nom)\
        .tag("Salle", disositif.salle)\
        .field("Horaires", disositif.horaire)\
        .field("Noms_Eleves", disositif.eleves)
    write_api.write(bucket=bucket, org=org, record=point)

def envoyer_donnes_data(data):
    donnees_concatenees = ",".join(data.data)
    point = Point("donnees") \
        .tag("ID_Dispositif", data.id) \
        .field("Donnes", donnees_concatenees)
    write_api.write(bucket=bucket, org=org, record=point)


#COMMENT UTILISER :
# dispositif = Dispositif(150, "Camera", "E303", "13h30-15h30", "Enzo, Morgane, Emilien")
# envoyer_donnees_dispositif(dispositif)
#
# data = Data(15, ["test", "dispositif", "comment", "548"])
# envoyer_donnes_data(data)

client.close()