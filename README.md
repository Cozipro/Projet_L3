# Logiciel de mesure Audio sous Python 3.7
Ce logiciel résulte du projet du 6e semestre de la licence Acoustique et Vibration de l'Université du Mans. 
Il doit être éxécuté avec une version de python 3.7.X.

Ce logiciel a pour objectif de déterminer la fonction de transfert d'un filtre se représentant sous la forme:

# Interface utilisateur

L'interface se présente de la façon suivante (version non-définitive):
![interface](images/interface.PNG)

- <ins>Interface IN:</ins> Liste pour choisir l'interface audio d'entrée
- <ins>Interface OUT:</ins> Liste pour choisir l'interface audio de sortie
- <ins>Ch mesure:</ins> Numéro de l'entrée correspondant au signal y
- <ins>Ch référence:</ins> Numéro de l'entrée correspondant au signal x (signal de référence)
- <ins>Freq min / Freq max:</ins> Fréquence de départ et de fin du chirp
- <ins>ΔF:</ins> Pas fréquentiel
- <ins>N_avg:</ins> Nombre de moyennes
- <ins>Nom:</ins> Nom de la mesure
