# Projet : Notre Journal Intime - Microservices & Sécurité Kubernetes

Ce projet consiste en une application de "journal intime" développée en Python, conteneurisée avec Docker et orchestrée via Kubernetes.

## Auteurs 
- **Doralie DORCAL (22208270)**
- **Jeen Juvana JENY JEYARAJ (22519719)**

## Structure du projet 
DORCAL_JENY_JEYARAJ/
├── frontend/     # Application Python (interface)
├── backend/      # Application Python (logique métier)
├── kube/         # Manifests Kubernetes (déploiements, services, base de données MySQL, sécurité)
└── README.md

## Prérequis 
- Docker
- Minikube
- Kubectl

**Configuration DNS locale (Indispensable) :** 
Pour accéder au projet via l'URL `http://journalintime.info`, vous devez éditer votre fichier `hosts` :
- **Windows :** `C:\windows\system32\drivers\etc\hosts`
- **Linux/macOS :** `/etc/hosts`

Ajoutez cette ligne à la fin du fichier :
```text
127.0.0.1  journalintime.info
```

## Guide d'installation

Ouvrez un terminal à la racine du dossier et exécutez les commandes suivantes dans l'ordre :

```bash
# 1. Démarrer Minikube 
minikube start

# 2. Activer les addons requis (Ingress, Istio, DNS) 
minikube addons enable ingress
minikube addons enable istio-provisioner
minikube addons enable istio
minikube addons enable ingress-dns

# 3. Activer l'injection automatique d'Istio dans le namespace par défaut
kubectl label namespace default istio-injection=enabled

# 4. Appliquer tous les manifestes Kubernetes
kubectl apply -f kube/

# 5. Lancer le tunnel pour exposer l'application
minikube tunnel

```

## Accès à l'application 

Une fois le tunnel lancé (laissez le terminal ouvert), accédez à l'application via votre navigateur :
[http://journalintime.info](http://journalintime.info)

## Sécurité implémentée 

Ce projet répond aux standards de sécurité suivants :
* **Vulnerability Scanning :** Scan des images Docker via Docker Hub pour s'assurer qu'elles ne contiennent pas de virus ou de librairies périmées
* **mTLS (Istio) :** Cryptage des échanges entre les services 
* **RBAC :** Mécanisme de contrôle d'accès qui définit les rôles et les autorisations de chaque utilisateur 
* **Network Policies :** Pare-feu interne qui n'autorise que le backend à parler à la base de données
* **Secrets :** Définit le mot de passe qui sera utilisé lors de la connexion au serveur MySQL