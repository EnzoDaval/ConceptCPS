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

```connection bridge_name
address localhost:1883
topic topic_name both 2
cleansession false```
