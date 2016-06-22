Télécharger le packet depuis le répertoire git:
```bash
git clone git@github.com:gropax/dysto.git
```

installer le packet en mode developpement
```bash
cd dysto
sudo python3 setup.py develop
```

Pour executer les scripts d'exemple, il faut d'abord ajouter le corpus (`estrep-694882.parsed_bonsai3_2_malt.conll`) dans le dossier `data`:
```bash
bash bag_of_word.bash
```

Pour évaluer la précision d'un thésaurus sur une série de tests:
```bash
dysto-test /path/to/thesaurus_NC /data/tests_N
dysto-test /path/to/thesaurus_V /data/tests_V
```
