'''
Created on 17 Aug 2013

@author: Aleksandra
'''
import cProfile


from pyrcpsp import GeneticAlgorithmSolver
from pyrcpsp import SingleModeClasses


activity1=SingleModeClasses.Activity("a1",3,{1:2})
activity2=SingleModeClasses.Activity("a2",4,{1:3})
activity3=SingleModeClasses.Activity("a3",2,{1:4})
activity4=SingleModeClasses.Activity("a4",2,{1:4})
activity5=SingleModeClasses.Activity("a5",1,{1:3})
activity6=SingleModeClasses.Activity("a6",4,{1:2})
        
activity_graph = {SingleModeClasses.Activity.DUMMY_START:[activity1,activity2],
                  activity1:[activity3], 
                  activity3:[activity5], 
                  activity2:[activity4],
                  activity4:[activity6],
                  activity5:[SingleModeClasses.Activity.DUMMY_END],
                  activity6:[SingleModeClasses.Activity.DUMMY_END]}

resources = {1:4}
problem = SingleModeClasses.Problem(activity_graph, resources)

solver = GeneticAlgorithmSolver(problem)
toolbox = solver.generate_toolbox_for_problem()
cProfile.run('solver.solve()')
#print problem.compute_makespan(solution)
