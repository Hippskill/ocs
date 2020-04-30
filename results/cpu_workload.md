# Simulation
## Coordinate descent
best coordinates is {'n_cpu': 8, 'n_ram_gb': 1}

best instance is Instance(name=custom, n_cpu=8, n_ram_gb=1, cost_per_second=0.0008100000000000001)

best instance metrics instance: Instance(name=custom, n_cpu=8, n_ram_gb=1, cost_per_second=0.0008100000000000001) failure: False mean_cost: 0.01177055743932724 mean_elapsed: 14.531552394231161

cost 0.6834031151628496

elapsed time 937.8239307403564

## Random search

best instance is Instance(name=custom, n_cpu=8, n_ram_gb=8, cost_per_second=0.00088)

best instance metrics instance: Instance(name=custom, n_cpu=8, n_ram_gb=8, cost_per_second=0.00088) failure: False mean_cost: 0.013155595811208091 mean_elapsed: 14.949540694554647

cost 0.6248558017945288

elapsed time 947.2764048576355

## Full search

best instance is Instance(name=custom, n_cpu=8, n_ram_gb=8, cost_per_second=0.00088)

best instance metrics instance: Instance(name=custom, n_cpu=8, n_ram_gb=8, cost_per_second=0.00088) failure: False mean_cost: 0.009064132067362467 mean_elapsed: 10.300150076548258

cost 2.6544458959651003

elapsed time 4254.68715763092

## Scout
best instance is Instance(name=custom, n_cpu=10, n_ram_gb=10, cost_per_second=0.0011)

best instance metrics instance: Instance(name=custom, n_cpu=10, n_ram_gb=10, cost_per_second=0.0011) failure: False mean_cost: 0.011059841187795003 mean_elapsed: 10.054401079813639

cost 0.08218208559513092

elapsed time 157.74241662025452


# Azure
## Coordinate descent
best instance is Instance(name=Standard_DS3_v2, n_cpu=4, n_ram_gb=14, cost_per_second=7.750000000000001e-05)

best instance metrics instance: Instance(name=Standard_DS3_v2, n_cpu=4, n_ram_gb=14, cost_per_second=7.750000000000001e-05) failure: False mean_cost: 0.0017329374308586124 mean_elapsed: 22.360482978820798

cost 0.045855036999252106

elapsed time 893.8057196617126

## Random search
best instance is Instance(name=Standard_DS2_v2, n_cpu=2, n_ram_gb=7, cost_per_second=3.888888888888889e-05)

best instance metrics instance: Instance(name=Standard_DS2_v2, n_cpu=2, n_ram_gb=7, cost_per_second=3.888888888888889e-05) failure: False mean_cost: 0.001435837024052938 mean_elapsed: 36.92152347564697

cost 0.022694643210503792

elapsed time 1181.617150449753

## Scout
best instance is Instance(name=Standard_DS3_v2, n_cpu=4, n_ram_gb=14, cost_per_second=7.750000000000001e-05)

best instance metrics instance: Instance(name=Standard_DS3_v2, n_cpu=4, n_ram_gb=14, cost_per_second=7.750000000000001e-05) failure: False mean_cost: 0.0016078097249865534 mean_elapsed: 20.74593193531036

cost 0.0906267943558362

elapsed time 3398.7146716833113
