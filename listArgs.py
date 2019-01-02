import mic
import inspect

exp = mic.dyn_chem_experiment(sec_num = 1)
varnames =mic.dyn_chem_experiment_all.__code__.co_varnames
bullets = []
items = []

for var in varnames:
	items.append(var)
	bullets.append("*")


mic.summary("Experiment Information")
mic.summary.add("Experiment keywords", bullets, items)

