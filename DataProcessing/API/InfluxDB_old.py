from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from Classes.Eleve import *

url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "CHPF60Fmc4WWf1tNKXqjRUVm2we9FU3YTqAJE23oNmURgJcMwnacqN5UIRd_PdM01fq-sqM-lIJH6jOz2meqeg=="
org = "Tricot"
bucket = "CyberPhysique"


def envoyer_donnees(eleves, nom_cours):
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for eleve in eleves:
        point = Point("cours") \
            .tag("nomCours", nom_cours) \
            .tag("nom", eleve.nom) \
            .tag("prenom", eleve.prenom) \
            .field("presence", eleve.presence) \
            .field("certitude", eleve.certitude)
        write_api.write(bucket=bucket, org=org, record=point)

    client.close()


def get_horaires(id_dispositif):
    # Créer le client InfluxDB
    client = InfluxDBClient(url=url, token=token, org=org)

    # 1. Récupérer les horaires du dispositif depuis la première table
    query_horaires = f'''
        from(bucket: "{bucket}")
            |> range(start: -1d)  # Ajustez la durée si nécessaire
            |> filter(fn: (r) => r["_measurement"] == "mesures" and r["ID_Dispositif"] == "{id_dispositif}")
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
            |> filter(fn: (r) => r["_measurement"] == "deuxieme_table" and r["ID_Dispositif"] == "{id_dispositif}")
            |> filter(fn: (r) => r["Timestamp"] >= {min(horaires)} and r["Timestamp"] <= {max(horaires)})
    '''

    resultats_second_table = client.query_api().query(query_second_table, org=org)

    # Afficher les résultats de la deuxième table
    for table in resultats_second_table:
        for row in table.records:
            print(row.values)

    client.close()
    return resultats_second_table

# eleves = [Eleve("Dupont", "Alice", True, 90), Eleve("Tricot", "Bob", False, 70)]
# envoyer_donnees(eleves, "Cours A")
# client.close()
