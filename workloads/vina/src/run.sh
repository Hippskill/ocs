#!/bin/sh
./vina --cpu 1 --receptor protein.pdbqt --ligand ligand.pdbqt --config config.txt --exhaustiveness 1 --log log.txt
