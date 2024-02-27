First project objectif (choose 1):

- Farm mobs
	- Gestion de combat (sorts, deplacements, passer tour, ...) [1,2,3,... & shift+1, shift+2, ...]
	- Gestion des deplacements (map to map, ne pas sortir de la zone, in map) 
	- Detection des groupes (specific mob, nbr, ...) [z]
	- Gestion de random Moderateur (message pv -->chatgpt?)

- Forgemagie
	- Kamas pour testing
	- objectif exos?, fm presque parf?

- Farming ressouces (paysan, pecheur, ...)
	- Gestion de combat (aggresion defenseur de ressources)
	- Gestion des deplacements
	- Detection des ressources [y]
	- Gestion de random Moderateur

- Chasse aux tresors
	- PNJ communication
	- Gestion interface avec dofusDB pour indices pos
	- Gestion de combat (mobs de la fin)
	- Gestion des deplacements

- Almanax
	- PNJ communication
	- Gestion HDV/magasin_joueur
	- Gestion de deplacements (popo, map2map)

- Quetes (quotidiennes ou pas)
	- PNJ communication
	- Gestion des deplacements
	? - Gestion de l'inventaire
	? - Gestion de combat

- Multicompte Helper
	- Communication with client (laptop level)

- Deplacement Helper
	- Same as DD autopilote

---------------------------------- QUESTIONS D'ORGANISATION ---------------------------------- 

IMAGE FEED

- Every second capture current screen and process it
OR
- Continuous image capture (few ms)
OR
- Occasionnal image capture (only when needed)

--------------------------------

INFORMATION ACQUISITION (map_coord, player around, ...)

- From image : template matching, SIFT, CNN, ...
- From api : data between client & serveur

--------------------------------

REPO ORGANISATION

- Low level scripts (action control : move, fight, change map,...)
- High level scripts (decision making : farm this zone, change zone, put ressources in bank)
OR/AND
- Folder for each project
OR
Folders:
- Detection (detect & localize stuff: mobs, ressources, players, + how many)
- Actions (shortcuts for spells, click change map, click fight, ...)
- Specific strategies? (for this mobs, fight like that)
- Gestion multicomptes
- Gestion Log files
- General decisions (Scripts : capture archi, farm paysan, ...)
...

--------------------------------

SECURITE ANTIBAN

- VPN
- New accounts with new email
- Jamais utilisé son IP pour se connecter sur les bot accounts

--------------------------------

STARTING POINT

- Fixé l'objectif
- Paper review (Qu'est qui existe, comment c'est fait, retour de la communauté -cad already patch/bann)
- Choisir une approche INFORMATION ACQUISITION
- Commencer à coder (si on a deja figé environ la structure du repo)