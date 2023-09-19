# Membres
- DAVAL Enzo
- PERRAUDEAU Emilien
- TRICOT Thomas
- LORCERY Morgane

# Idee
Fiche d'appel qui se rempli automatiquement via différents catpeurs qui vont assurer avec une certaine certitude la présence, ou non, des élèves.

# Titre temporaire du service
Fiche d'appel autonome

# Type d'environment
Salle de cours

# Domaine
Confort

# Motivations
Pression du Législateur : 
1) Réglementations sur la présence en cours: En France, la présence en cours est généralement obligatoire, surtout pour les étudiants apprentis qui ont un contrat de travail associé à leurs études. Cela est en conformité avec le Code de l'éducation.
2) Loi sur la protection des données: Le système doit être conforme au RGPD (Règlement général sur la protection des données), notamment en ce qui concerne le stockage et le traitement des données personnelles des étudiants. 
Attentes Sociétales :
1) Efficiences Administrative et Pédagogique: Automatiser la fiche d'appel permet de libérer du temps pour l'enseignant, qui peut ainsi se concentrer davantage sur des tâches pédagogiques. Cela peut également réduire les erreurs humaines dans la tenue des registres.
2) Transparence et Responsabilité: Un système automatisé permet une meilleure transparence et peut fournir des preuves en cas de contestation de la part des étudiants ou des parents.

Attentes des Parties Prenantes :
1) Écoles et Universités: Pour ces institutions, un tel système peut représenter des économies de temps et de ressources humaines, ainsi qu'un moyen de se conformer plus facilement aux réglementations.
2) Entreprises partenaires: Pour les entreprises qui emploient des étudiants apprentis, assurer une bonne assiduité en cours peut être crucial pour le développement des compétences nécessaires en milieu professionnel.

Références :
1) Code de l'éducation, articles relatifs à l'obligation de présence en cours.
2) RGPD, Articles 5, 6 et 9 concernant la licéité du traitement des données personnelles.

# Analyse de l'existant, innovation et/ou progrès scientifique
- http://thesis.essa-tlemcen.dz/bitstream/handle/STDB_UNAM/237/memoire%20master%20final.pdf?sequence=1&isAllowed=y (thèse sur les caméras)
- https://www.hikvision.com/fr/solutions/solutions-by-function/student-attendance/ et https://www.aimaira.fr/controle-de-presence-casse-tete-lenseignement-superieur/ (système déjà mis en place avec les cartes)
- https://spotteredu.com/stories/opportunity-cost/ depuis https://etudiant.lefigaro.fr/article/une-universite-americaine-controle-la-presence-en-cours-avec-une-application_9e9c8846-4736-11ea-8181-5c043fd26a1a/ (appli qui detecte les etudiants avec le bluetooth)

# Schéma architectural de principe
1. Caméras, Micros, et Capteurs d'Ondes: Placés stratégiquement dans la salle de classe ou la zone de l'université.
2. Dispositifs Edge (Edge Computing): Effectuent le premier niveau de traitement des données des capteurs.
3. Bus de Services Logiciels: Coordonne les données provenant de divers dispositifs edge et les transmet au serveur central. \
   Technologies possibles: Kafka, RabbitMQ.
4. Serveur Central : Traite les données et effectue des analyses plus complexes (comme la reconnaissance faciale). \
  Technologies possibles: Serveurs cloud AWS, Azure, ou des serveurs locaux.
5. Plateforme de Composition: Utilisée pour programmer et orchestrer l'interaction entre différents services et clients logiciels. \
  Technologies possibles: Kubernetes pour l'orchestration, API REST pour l'interaction.
6. Base de Données: Stocke les fiches d'appel, les informations sur les étudiants, et les données historiques. \
  Technologies possibles: MySQL, PostgreSQL.
7. Interface Utilisateur: Dashboard pour les enseignants/administrateurs pour voir les fiches d'appel en temps réel. \
  Technologies possibles: WebApp en React ou Angular.

Comment fonctionne le Flux de Données : \
  Les capteurs capturent les données et les transmettent aux dispositifs edge. \
  Les dispositifs edge envoient les données au bus de services logiciels. \
  Le bus de services logiciels route les données vers le serveur central pour analyse. \
  Les résultats sont stockés dans la base de données. \
  L'interface utilisateur interroge la base de données pour afficher les informations en temps réel. \

# Quelques élement techniques
- Models publics existants de reconnaissance faciale et vocale :
  - https://colab.research.google.com/github/louis030195/colabs/blob/master/face_recognition.ipynb [Face Recognition]
  - https://colab.research.google.com/github/NVIDIA/NeMo/blob/v1.0.0b2/tutorials/speaker_recognition/Speaker_Recognition_Verification.ipynb [Speaker Recognition]
