# Simulation

## Scout
best instance is Instance(name=custom, n_cpu=10, n_ram_gb=14, cost_per_second=0.00114)

best instance metrics instance: Instance(name=custom, n_cpu=10, n_ram_gb=14, cost_per_second=0.00114) failure: False mean_cost: 0.12764285375118253 mean_elapsed: 111.96741557121277

cost 0.7910803410434721

elapsed time 703.348646402359

## Random Search
best instance is Instance(name=custom, n_cpu=6, n_ram_gb=11, cost_per_second=0.00071)

best instance metrics instance: Instance(name=custom, n_cpu=6, n_ram_gb=11, cost_per_second=0.00071) failure: False mean_cost: 0.08245068489472072 mean_elapsed: 116.12772520383199

cost 0.8055365913716953

elapsed time 1814.6032005151112

## Coordinate Descent

best coordinates is {'n_ram_gb': 12, 'n_cpu': 7}

best instance is Instance(name=custom, n_cpu=7, n_ram_gb=12, cost_per_second=0.00082)

best instance metrics instance: Instance(name=custom, n_cpu=7, n_ram_gb=12, cost_per_second=0.00082) failure: False mean_cost: 0.09026380156834919 mean_elapsed: 110.07780679066975

cost 3.1663697307236993

elapsed time 7225.254738171895

# Azure

## Scout

best instance is Instance(name=Standard_DS3_v2, n_cpu=4, n_ram_gb=14, cost_per_second=7.750000000000001e-05)


best instance metrics instance: Instance(name=Standard_DS3_v2, n_cpu=4, n_ram_gb=14, cost_per_second=7.750000000000001e-05) failure: False mean_cost: 0.007761907555162906 mean_elapsed: 100.15364587306973

cost 0.15387534992694854

elapsed time 1985.4883861541746

## Random Search

best instance not found :(

## Coordinate Descent

best coordinates is {'n_cpu': 4, 'n_ram_gb': 14}

best instance is Instance(name=Standard_DS3_v2, n_cpu=4, n_ram_gb=14, cost_per_second=7.750000000000001e-05)

best instance metrics instance: Instance(name=Standard_DS3_v2, n_cpu=4, n_ram_gb=14, cost_per_second=7.750000000000001e-05) failure: False mean_cost: 0.007761907555162906 mean_elapsed: 100.15364587306973

cost 0.06751917437598441

elapsed time 1822.7409686247508
