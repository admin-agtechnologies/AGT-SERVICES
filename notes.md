# Notes générales et intérogations sur notre architecchture mico-services

## Service auth
Après avoir suivi avec succès les instructions d'installation et de lancement de ce premier micro-service, je me suis posé les questiosn suivantes :
- En effet, cahque micro service a sa propre basez de donée, cependant, va t'on cérer un conteneur docker de base de donnée pour chacun ? si oui est-ce optimal en terme de ressources ?
- comment configurer et comment à utiliser ce premeir service d'authentification ?
- doit-on mettre sur pied un guide de configuration et d'utilisation du service d'authentification pour nos developpeurs internes ?

celà m'a poussé à me poser les questions suivantes pour les services à venir :

- comment configurer chaque microservice ?
- comment déployer nos micro-services ensembles ?
- comprendre comment fonctionne chacun de nos micro-services ?
- comment utiliser notre éco-système microservice ?
- faut-il mettre sur pied un backend métier template qui intègre tous nos micro-services ?
- faut-il mettre sur pied un frontend métier template qui intègre notre backend métier ?
- faut-il mettre en place le monitoring de notre architechture micro-services ?
- ne doit-on pas faire un petite plateforme rapide de faq pour répondre à toutes ces questions pour nos dévéloppeurs? danslaquelle on répond à chaque question en markdown et on versionne les réponse, une sorte de forum internet à Ag-technologies afin que chaque nouveau développeru puisse s'épanouir ?
- est-il nécessaire de faire un service MESH pour Ag-technologies ? j'ai vu ça sur youtube 

## Service users

Je me pose les mêmes questions que pour le service auth

# Services notifications
Après avoir lancé ce service, je me suis posé les mêmes questions que pour le service auth, mais j'ai trouvé que ici le swagger semble complet. Par ailleurs; j'ai aussi vu le lien vers rabitmq, mais on me demande un mot de passe et un username pour y accéder, ça relance la question de guiude d'utilisation  persiste donc à ce niveau                     