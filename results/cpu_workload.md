# Simulation
## Coordinate descent
best coordinates is {'n_cpu': 9, 'n_ram_gb': 8}

best instance is Instance(name=custom, n_cpu=9, n_ram_gb=8, cost_per_second=0.0009800000000000002)

best instance metrics instance: Instance(name=custom, n_cpu=9, n_ram_gb=8, cost_per_second=0.0009800000000000002) failure: False mean_cost: 0.012806962724208833 mean_elapsed: 13.068329310417177

cost 2.1738009927897455

elapsed time 3243.0626256227492

## Random search
best instance is Instance(name=custom, n_cpu=10, n_ram_gb=9, cost_per_second=0.00109)

best instance metrics instance: Instance(name=custom, n_cpu=10, n_ram_gb=9, cost_per_second=0.00109) failure: False mean_cost: 0.01421616909503937 mean_elapsed: 13.042356967926025

cost 2.023633663759232

elapsed time 3739.4945554733276

## Full search

best instance is Instance(name=custom, n_cpu=10, n_ram_gb=10, cost_per_second=0.0011)

best instance metrics instance: Instance(name=custom, n_cpu=10, n_ram_gb=10, cost_per_second=0.0011) failure: False mean_cost: 0.013194640209674837 mean_elapsed: 11.99512746334076

cost 7.727198932571405

elapsed time 11276.093375706672

## Scout
best instance is Instance(name=custom, n_cpu=10, n_ram_gb=10, cost_per_second=0.0011)

best instance metrics instance: Instance(name=custom, n_cpu=10, n_ram_gb=10, cost_per_second=0.0011) failure: False mean_cost: 0.013194640209674837 mean_elapsed: 11.99512746334076

cost 4.256209577229028

elapsed time 15109.011092448234

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
