#!/bin/sh
tar xvzf anis.tar.gz > /dev/null
./anis-grid.exe SYN SYN-GRID.an $1 $2 > result-$1-$2
tar czf result.tar.gz result-$1-$2
rm SYN*
rm anis-grid.exe
rm result-$1-$2