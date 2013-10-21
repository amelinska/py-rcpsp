from GenericEvolutionaryRcpspAlgorithmSolver import GenericGeneticAlgorithmSolver
from GeneticAlgorithmSolver import find_lowest_index_non_existing_in, mutate_sgs
from MultiModeClasses import MultiModeSgsMaker

__author__ = 'bartek'
'''
Created on 17 Aug 2013

@author: Aleksandra
'''

from MultiModeClasses import Solution
from deap import creator, base, tools, algorithms
from copy import copy
from random import random, randint, choice


def negative_leftover(problem, mode_assignment):
    leftovers = [leftover_capacity(problem, resource, mode_assignment) for resource in problem.nonrenewable_resources]
    return sum(-leftover for leftover in leftovers if leftover < 0 )

def leftover_capacity(problem, resource, mode_assignment):
    return problem.nonrenewable_resources[resource] - sum(mode.demand[resource] for mode in mode_assignment)

def evaluate_sgs_function(SolutionClass, problem_instance, sgs):
    #TODO: make test of evaluation function
    """

    :param SolutionClass: used to generation the solution from problem_instance and sgs
    :param problem_instance: instance of the problem
    :type problem_instance: MultiModeClasses.Problem
    :param sgs: serial generation scheme, list of tuples of form: (activity:MultiModeClasses.Activity, mode: MultiModeClasses.Mode)
    :type sgs: list [tuple]
    :return: single element tuple containing value of evaluation function of sgs (value,)
    """
    solution = SolutionClass.generate_solution_from_serial_schedule_generation_scheme(sgs, problem_instance)
    #unpack activities and modes list to the separate lists
    activities, modes = zip(*sgs)
    total_negative_leftover = negative_leftover(problem_instance, modes)
    maximal_makespan = sum(act.maximal_duration() for act in activities)
    if total_negative_leftover > 0:
        return (maximal_makespan + total_negative_leftover,)
    else:
        return (problem_instance.compute_makespan(solution),)

class GeneticAlgorithmSolverMultimode(GenericGeneticAlgorithmSolver):
    def __init__(self, *args, **kwargs):
        #TODO: implement crossover and mutate functions
        self.crossover_sgs = crossover_sgs_multimode
        self.mutate_sgs = mutate_sgs_multimode
        if not 'number_of_retries' in kwargs:
            retries = 4
        else:
            retries = kwargs['number_of_retries']
        self.SgsMaker = lambda problem : MultiModeSgsMaker(problem, retries)
        self.Solution = Solution
        super(GeneticAlgorithmSolverMultimode, self).__init__(*args) # wywoluje konstruktor klasy bazowej

    def evaluate_sgs(self, sgs):
        """
        evaluation of an genotype of a solution to multimode rcpsp.
        sgs is defined as a list of tuples of (assignment, corresponding mode).
        evaluation takes into account nonrenewable resources infeasibility,
        see [Sonke Hartmann Project Scheduling under limited constraints chapter 7.1.1]
        """
        return evaluate_sgs_function(self.Solution, self.problem, sgs)

def modified_crossover_sgs_multimode(sgs_mum, sgs_dad):
    q = randint(0,len(sgs_mum))
    r = randint(0,len(sgs_mum))
    return modified_crossover_sgs_nonrandom_multimode(sgs_mum, sgs_dad, q, r)

def crossover_sgs_multimode(sgs_mum, sgs_dad):
    q = randint(0,len(sgs_mum))
    r = randint(0,len(sgs_mum))
    return crossover_sgs_nonrandom_multimode(sgs_mum, sgs_dad, q, r)

def crossover_activity_list_multimode(sgs_mum, sgs_dad, q):
    len_of_sgs_mum = len(sgs_mum)
    sgs_daughter = []
    sgs_son = []
    for i in xrange(q):
        sgs_daughter.append(sgs_mum[i])
        sgs_son.append(sgs_dad[i])
    for i in xrange(q,len_of_sgs_mum):
        j = find_lowest_index_non_existing_in(sgs_dad, sgs_daughter)
        sgs_daughter.append(sgs_dad[j])
        j = find_lowest_index_non_existing_in(sgs_mum, sgs_son)
        sgs_son.append(sgs_mum[j])
    return (sgs_daughter, sgs_son)

def create_dictionary_of_modes(list_of_tuples):
    result = {}
    for tup in list_of_tuples:
        result[tup[0]] = tup[1]
    return result

def modified_crossover_mode_list(sgs_mum, sgs_dad, r):
    mode_dict_daugther = {}
    mode_dict_son ={}
    len_of_sgs_mum = len(sgs_mum)
    for i in range(r):
        mode_dict_daugther[sgs_mum[i][0]] = sgs_mum[i][1]
        mode_dict_son[sgs_dad[i][0]] = sgs_dad[i][1]
    for activity, mode in sgs_dad:
        if not activity in mode_dict_daugther:
            mode_dict_daugther[activity] = mode

    for activity, mode in sgs_mum:
        if not activity in mode_dict_son:
            mode_dict_son[activity] = mode

    return mode_dict_daugther, mode_dict_son


def modified_crossover_sgs_nonrandom_multimode(sgs_mum, sgs_dad, q, r):
    activity_list_mum = [t[0] for t in sgs_mum]
    activity_list_dad = [t[0] for t in sgs_dad]

    daughter_activity_list, son_activity_list = crossover_activity_list_multimode(activity_list_mum, activity_list_dad, q)
    mode_dict_daughter, mode_dict_son = modified_crossover_mode_list(sgs_mum, sgs_dad, r)
    result_daughter = creator.Individual()
    result_son = creator.Individual()

    for activity in daughter_activity_list:
        result_daughter.append((activity, mode_dict_daughter[activity]))

    for activity in son_activity_list:
        result_son.append((activity, mode_dict_son[activity]))

    return result_daughter, result_son

def crossover_mode_dict(child_activity_list, ancestor_dict1, ancestor_dict2, r):
    result_mode_list = []
    for i in range(r):
        child_activity = child_activity_list[i]
        child_mode = ancestor_dict1[child_activity]
        result_mode_list.append(child_mode)
    for i in range(r,len(child_activity_list)):
        child_activity = child_activity_list[i]
        child_mode = ancestor_dict2[child_activity]
        result_mode_list.append(child_mode)
    return result_mode_list

def crossover_sgs_nonrandom_multimode(sgs_mum, sgs_dad, q, r):
    activity_list_mum = [t[0] for t in sgs_mum]
    activity_list_dad = [t[0] for t in sgs_dad]
    sgs_mum_dict = create_dictionary_of_modes(sgs_mum)
    sgs_dad_dict = create_dictionary_of_modes(sgs_dad)

    daughter_activity_list, son_activity_list = crossover_activity_list_multimode(activity_list_mum, activity_list_dad, q)
    daughter_mode_list = crossover_mode_dict(daughter_activity_list, sgs_mum_dict, sgs_dad_dict, r)
    son_mode_list = crossover_mode_dict(son_activity_list, sgs_dad_dict, sgs_mum_dict, r)
    daugher_sgs = creator.Individual()
    son_sgs = creator.Individual()
    for el in zip(daughter_activity_list, daughter_mode_list):
        daugher_sgs.append(el)
    for el in zip(son_activity_list, son_mode_list):
        son_sgs.append(el)

    return daugher_sgs, son_sgs


def mutate_sgs_multimode(problem, sgs, prob = 0.05):
    (sgs,) = mutate_sgs(problem, sgs, prob)
    result = creator.Individual()
    for t in sgs:
        activity = t[0]
        if random() < prob:
            mode = choice(activity.mode_list)
        else:
            mode = t[1]
        result.append((activity, mode))
    return (result,)
