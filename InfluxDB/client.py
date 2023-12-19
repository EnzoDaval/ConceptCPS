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

def envoyer_donnees_dispositif(dispositif):
    point = Point("dispositif")\
        .tag("ID_Dispositif", dispositif.id)\
        .tag("Nom_Dispositif", dispositif.nom)\
        .tag("Salle", dispositif.salle)\
        .field("Horaires", dispositif.horaire)\
        .field("Noms_Eleves", dispositif.eleves)
    write_api.write(bucket=bucket, org=org, record=point)

def envoyer_donnes_data(data):
    donnees_concatenees = ",".join(data.data)
    point = Point("donnees") \
        .tag("ID_Dispositif", data.id) \
        .field("Donnes", donnees_concatenees)
    write_api.write(bucket=bucket, org=org, record=point)

def get_horaires(id_dispositif):
    # Créer le client InfluxDB
    client = InfluxDBClient(url=url, token=token, org=org)

    # 1. Récupérer les horaires du dispositif depuis la première table
    query_horaires = f'''
        from(bucket: "{bucket}")
            |> range(start: -1d)  # Ajustez la durée si nécessaire
            |> filter(fn: (r) => r["_measurement"] == "dispositif" and r["ID_Dispositif"] == "{id_dispositif}")
            |> yield(name: "horaires")
    '''

    resultats_horaires = client.query_api().query(query_horaires, org=org)
    horaires = [row.values["_value"] for table in resultats_horaires for row in table.records]

    client.close()
    return horaires


def get_data_in_horaire(horaires, id_dispositif):
    client = InfluxDBClient(url=url, token=token, org=org)
    query_second_table = f'''
        from(bucket: "{bucket}")
            |> range(start: -30d)  # Ajustez la durée si nécessaire
            |> filter(fn: (r) => r["_measurement"] == "donnees" and r["ID_Dispositif"] == "{id_dispositif}")
            |> filter(fn: (r) => r["Timestamp"] >= {min(horaires)} and r["Timestamp"] <= {max(horaires)})
    '''

    resultats_second_table = client.query_api().query(query_second_table, org=org)

    # Afficher les résultats de la deuxième table
    for table in resultats_second_table:
        for row in table.records:
            print(row.values)

    client.close()
    return resultats_second_table


#COMMENT UTILISER :
# dispositif = Dispositif(150, "Camera", "E303", "13h30-15h30", "Enzo, Morgane, Emilien")
# envoyer_donnees_dispositif(dispositif)
#
# data = Data(15, ["test", "dispositif", "comment", "548"])
# envoyer_donnes_data(data)

client.close()