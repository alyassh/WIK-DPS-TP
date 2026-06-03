# TP-WIK-DPS-TP01
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