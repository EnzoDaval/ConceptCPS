# Configuration Mosquitto

Ce référentiel contient la configuration personnalisée pour le broker Mosquitto, avec des modifications spécifiques.

## Changements effectués

### 1. Authentification avec `allow_anonymous false`

La configuration Mosquitto a été modifiée pour désactiver l'accès anonyme. Cela signifie que toutes les connexions nécessitent désormais une authentification.

```allow_anonymous false```

### 2. Utilisation de password_file pour l'authentification

Un fichier password.txt a été ajouté pour stocker les informations d'authentification des utilisateurs. Assurez-vous que ce fichier est correctement configuré avec les noms d'utilisateur et les mots de passe.

```password_file password.txt```

### 3. Désactivation de la session propre avec cleansession false

La session propre a été désactivée pour permettre aux clients de reprendre une session existante en cas de perte de connexion.

```connection bridge_name``` 
```address localhost:1883``` 
```topic topic_name both 2```
```cleansession false```


# Lancement de mosquitto

### 1. Installation de Mosquitto sur son ordinateur

https://mosquitto.org/download/
Rajouter le path dans les variables d'environnement

### 2. Config file

Remplacer le config file (mosquitto.conf) original par celui présent dans le github

### 3. Création du compte

Lancer la commande ```mosquitto_passwd -c password.txt <nom d'utilisateur>``` dans un windows PowerShell exécuté en administrateur dans le dossier mosquitto et indiquer le mot de passe voulu. Ces informations seront enregistrés dans un fichier nommé password.txt.

### 4. Lancer le MQTT

Lancer la commande ```.\mosquitto.exe -c mosquitto.conf -v``` dans un windows PowerShell dans le dossier mosquitto.
