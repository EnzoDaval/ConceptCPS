# Membres
- DAVAL Enzo
- PERRAUDEAU Emilien
- TRICOT Thomas
- LORCERY Morgane

# Idee
Fiche d'appel qui se rempli automatiquement via différents catpeurs qui vont assurer avec une certaine certitude la présence, ou non, de l'élève.

# Titre temporaire du service
Fiche d'appel autonome

# Type d'environment
Salle de cours

# Domaine
Confort

# Motivations
TODO

# Analyse de l'existant
TODO

# Innovation et/ou progrès scientifique
TODO

# Schéma architectural de principe

1. Caméras, Micros, et Capteurs d'Ondes
  Placés stratégiquement dans la salle de classe ou la zone de l'université.

2. Dispositifs Edge (Edge Computing)
  Effectuent le premier niveau de traitement des données des capteurs.

3. Bus de Services Logiciels
  Coordonne les données provenant de divers dispositifs edge et les transmet au serveur central.
  Technologies possibles: Kafka, RabbitMQ.

5. Serveur Central
  Traite les données et effectue des analyses plus complexes (comme la reconnaissance faciale).
  Technologies possibles: Serveurs cloud AWS, Azure, ou des serveurs locaux.
  
5. Plateforme de Composition
  Utilisée pour programmer et orchestrer l'interaction entre différents services et clients logiciels.
  Technologies possibles: Kubernetes pour l'orchestration, API REST pour l'interaction.
  
6. Base de Données
  Stocke les fiches d'appel, les informations sur les étudiants, et les données historiques.
  Technologies possibles: MySQL, PostgreSQL.

8. Interface Utilisateur
  Dashboard pour les enseignants/administrateurs pour voir les fiches d'appel en temps réel.
  Technologies possibles: WebApp en React ou Angular.

Comment fonctionne le Flux de Données :
  Les capteurs capturent les données et les transmettent aux dispositifs edge.
  Les dispositifs edge envoient les données au bus de services logiciels.
  Le bus de services logiciels route les données vers le serveur central pour analyse.
  Les résultats sont stockés dans la base de données.
  L'interface utilisateur interroge la base de données pour afficher les informations en temps réel.

# Quelques élement techniques
- Models publics existants de reconnaissance faciale et vocale :
  - https://colab.research.google.com/github/louis030195/colabs/blob/master/face_recognition.ipynb [Face Recognition]
  - https://colab.research.google.com/github/NVIDIA/NeMo/blob/v1.0.0b2/tutorials/speaker_recognition/Speaker_Recognition_Verification.ipynb [Speaker Recognition]
