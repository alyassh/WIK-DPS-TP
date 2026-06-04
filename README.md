# WIK-DPS-TP01
Projet concernant le TP du 03/06/2026 réalisé au sein d'Ynov Campus.

### Utilisation

Le fichier **tp.py** représente le travail effectué en classe. Afin de le lancer, il suffit d'avoir *python3* d'installé sur sa machine, et d'executer `python3 tp.py` dans un terminal de commandes. Ensuite, ouvrir le lien https://127.0.0.1:8081/ping sur sa machine locale dans la suite des consignes.

### Présentation

Codé en Python, ce script nécessite un total de **5** dépendances amplement nécessaires à son fonctionnement :
- *http.server* : Lanceur de serveur web par la source.
- *socketserver* : Complément au serveur http, pour intéragir avec lui.
- *threading* : Framework utile au multi-tâches (serveur web / API).
- *fastapi* : Gestionnaire d'API sur les serveurs Python.
- *uvicorn* : Implémentation de serveur web ASGI, suppléant à http.

### Explications


    def serveur ():
    class ThreadedHTTPServer(threading.Thread):
        def run(self):
            port = 8081
            handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("",port),handler) as tcp_server:
                tcp_server.serve_forever()

Mise en place de la structure du base du serveur avec *threading* et *http.server* sur le port **8080**. Celui ci ne sera pas utilisé pour le TP, il sert juste de structure (le TP ne fonctionne pas autrement).

    server_thread = ThreadedHTTPServer()
    server_thread.daemon = True
    server_thread.start()

Définition du multi-threading pour supporter à la fois le serveur web, mais aussi l'API et son utilisation lors de l'accès à la page **/ping**.

    app = FastAPI()
    @app.get("/ping")
    async def root(request: Request):
        my_header = request.headers
        return {"message": my_header}

Inclusion de l'API dans la structure du site web.
    
    uvicorn.run(app, host="127.0.0.1", port=8081)

Déploiement du serveur web qui sera, cette fois ci, utilisée pour accéder à la page **/ping** par l'URL https://127.0.0.1/8081 afin de compléter le TP.
    
    serveur()

Lancement du serveur au complet.


# WIK-DPS-TP02
Projet concernant le TP du 04/06/2026 réalisé au sein d'Ynov Campus.

### Utilisation

Les deux fichiers **Dockerfile** et **Dockerfile-multistage** sont des fichiers de création docker qui permettent, à la suite du TP01, mettre sous Docker l'API du script `tp.py`.

### Présentation
Les deux Dockerfiles reposent sur l'image de base **python:3.12-slim**, une version allégée de Python 3.12 adaptée à la production. Ils exposent tous deux les ports *8080* et *8081*, et exécutent le script **tp.py** via la commande `python3 tp.py`.

La différence principale réside dans leur approche :
- *Dockerfile* : construction en une seule étape, simple et directe.
- *Dockerfile-multistage* : construction en deux étapes distinctes (*builder* et *runtime*), permettant de produire une image finale plus propre, sans les outils de build.

Dans les deux cas, un utilisateur système dédié (**appuser**) est créé pour exécuter l'application sans privilèges root, ce qui constitue une bonne pratique de sécurité.

### Explications

**Dockerfile**

    FROM python:3.12-slim
Image de base légère Python 3.12, suffisante pour faire tourner le script sans surcharge inutile.

    RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
Création d'un groupe système *appgroup* et d'un utilisateur système *appuser* appartenant à ce groupe, afin d'éviter d'exécuter le conteneur en tant que *root*.

    RUN pip install --no-cache-dir fastapi uvicorn
Installation des deux dépendances nécessaires au fonctionnement de l'API : *fastapi* et *uvicorn*. L'option `--no-cache-dir` évite de conserver le cache pip dans l'image, réduisant ainsi sa taille.

    WORKDIR /app
    COPY tp.py .
Définition du répertoire de travail à `/app`, puis copie du script `tp.py` dans ce répertoire au sein du conteneur.

    RUN chown -R appuser:appgroup /app
    USER appuser
Attribution des droits sur le dossier `/app` à *appuser*, puis bascule vers cet utilisateur pour la suite de l'exécution.

    EXPOSE 8080 8081
Déclaration des ports **8080** et **8081** comme ports exposés par le conteneur (respectivement le serveur HTTP de base et le serveur uvicorn).

    CMD ["python", "tp.py"]
Commande de démarrage du conteneur : lancement du script Python principal.

---

**Dockerfile-multistage**

    FROM python:3.12-slim AS builder
    WORKDIR /build
    RUN python -m venv /build/venv
    RUN /build/venv/bin/pip install --no-cache-dir fastapi uvicorn
Première étape (*builder*) : création d'un environnement virtuel Python dans `/build/venv` et installation des dépendances dans cet environnement isolé. Cette étape sert uniquement à préparer les paquets, elle ne sera pas conservée dans l'image finale.

    FROM python:3.12-slim AS runtime
Deuxième étape (*runtime*) : nouvelle image de base propre, sans aucun résidu de la phase de build.

    RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
    WORKDIR /app
    COPY --from=builder /build/venv /app/venv
    COPY tp.py .
Création de l'utilisateur système, définition du répertoire de travail, puis récupération du virtualenv construit à l'étape précédente via `--from=builder`. Seuls les fichiers strictement nécessaires sont copiés dans l'image finale.

    RUN chown -R appuser:appgroup /app
    USER appuser
Attribution des droits sur `/app` à *appuser*, puis bascule vers cet utilisateur non-privilégié.

    ENV PATH="/app/venv/bin:$PATH"
Ajout du virtualenv au `PATH` du conteneur, afin que `python` et les commandes installées (*uvicorn*, etc.) soient directement accessibles sans activer manuellement l'environnement virtuel.

    EXPOSE 8080 8081
    CMD ["python", "tp.py"]
Exposition des ports et lancement du script, identiques au Dockerfile simple.