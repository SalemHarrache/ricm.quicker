Application web pour l'emploi du temps à Polytech'Grenoble (RICM). J'utilise
l'application à titre personnel.

Lien : http://ricm.quicker.fr/


Fonctionnalités :
=================

 - Emploi du temps IMAG et Polytech sur une même page
 - Accessible depuis les smartphones et autres appareils ne supportant pas les iframes de l'ADE
 - Mise en cache : vitesse de chargement des pages très rapide
 - Miroir : Délivrance de l'emploi du temps même en cas de crash de l'ADE
 - ICalendar : Calendrier au format iCal (Google Agenda, Thunderbird Lightning, Android...).
 - Open source !


Installation :
=============

Tout d'abord il faut installer les dépendances, si ce n'est déjà fait,
commencer par installer python et virtualenv.

::

    sudo apt-get install python2.7 python-virtualenv


Virtualenv permet d'installer les packages python dans un environnement virtuel
propre à chaque projet. Ainsi l'un des avantages c'est de ne pas polluer son
environnement système de libs de toutes sortes. L'autre avantage, c'est qu'il
n'y a pas besoin d'être root pour installer les packages (ce qui est le cas
sur la plupart des hébergeurs).


J'ai simplifié la phase d'installation des dépendances dans un nouveau
virtualenv avec make. Ainsi vous n'avez qu'à lancer la commande suivante :

::

    make setup


Activer le virtualenv avant de continuer:


::

    source ./env/bin/activate


Utilisation :
=============

Un petit script est disponible pour faciliter la mise en place du site.
Le manager !

::

    ./manager.py

    Please provide a command:
      initdb       Creates database tables and insert data
      runserver    Runs the Flask server
      shell        Runs a Python shell inside Flask application context.
      updatecache  Update cache


Dans un premier temps on initialise la base de données selon la configuration
définie dans le fichier website/config.py.
(J'utilise PostgreSQL en production et SQLite en développement.)

Pour ce faire on lance la commande : `initdb`


::

    ./manager.py initdb -c dev


 - -c : configuration ("prod", "dev")

Une fois les données initialisées, on peut lancer le serveur avec la
commande : `runserver`


::

    ./manager.py runserver -c dev
     * Running on http://127.0.1.1:9090/
     * Restarting with reloader

Le site est désormais accessible à l'adresse : http://127.0.1.1:9090/


Pour déployer le site, un exemple de configuration se trouve dans le dossier
examples.