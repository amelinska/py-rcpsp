'''
Created on 17 Aug 2013

@author: Aleksandra
'''

#from pyrcpsp.GenericEvolutionaryRcpspAlgorithmSolver import GenericGeneticAlgorithmSolver
#from pyrcpsp.GeneticAlgorithmSolver import crossover_sgs, mutate_sgs
#from pyrcpsp.MultiModeClasses import MultiModeSgsMaker, Solution

from pyrcpsp import GeneticAlgorithmSolver
from pyrcpsp import GeneticAlgorithmSolverMultimode
from pyrcpsp import MultiModeClasses
from pyrcpsp import GenericEvolutionaryRcpspAlgorithmSolver



class NaiveGeneticAlgorithmSolverMultiMode(GenericEvolutionaryRcpspAlgorithmSolver.GenericGeneticAlgorithmSolver):
    def __init__(self, *args, **kwargs):
        self.crossover_sgs = GeneticAlgorithmSolver.crossover_sgs
        self.mutate_sgs = GeneticAlgorithmSolver.mutate_sgs
        if not 'number_of_retries' in kwargs:
            retries = 4
        else:
            retries = kwargs['number_of_retries']
        self.SgsMaker = lambda problem : GeneticAlgorithmSolverMultimode.MultiModeSgsMaker(problem, retries)
        self.Solution = MultiModeClasses.Solution
        super(NaiveGeneticAlgorithmSolverMultiMode, self).__init__(*args)



                
