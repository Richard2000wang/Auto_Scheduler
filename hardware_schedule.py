from hardware_var import *
from schools_var import *
l1_robots = [dash, codey, sphero, irobot, snapcircuit]
l2_robots = [qtruck, alienbot, clickbot, ev3, hand, inventor]
l1_schools = [Bonaccord]

from ortools.linear_solver import pywraplp

# Current issue: How to track robots used previously and to generate solution without
## Alternate solution
## Each school has a certain number of kids and we have a certain amount of robots
# For each new generation, robots are assigned to schools and the total number is subtracted
# Solution ends when all schools have robots
# Next iteration only succeeds if NOT current robot 
# Generate new solution
# Best solution is the one with the most iterations, cap at a certain amount. 
# Use dictionaries to keep track of robots and schools 

def main():
    data = {}
    datastore =[]
    weeks = input("Enter the number of weeks you need a schedule for")
    for i in l1_robots:
        datastore.append(i)
    data['l1_robots'] =  datastore
    data['values'] = datastore
    datastore = []
    data['num_robots'] = len(data['l1_robots'])
    data['all_robots'] = range(data['num_robots'])

    for i in l1_schools:
        datastore.append(i)
    data['l1_schools'] = datastore
    datastore = []
    data['num_schools'] = len(data['l1_schools'])
    data['all_schools'] = range(data['num_schools'])

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        print('SCIP solver unavailable.')
        return

    # Variables.
    # x[i, b] = 1 if school i is using in robot b.
    x = {}
    for i in data['all_robots']:
        for b in data['all_schools']:
            x[i, b] = solver.BoolVar(f'x_{i}_{b}')

    # Constraints.
    # Each school is assigned to at most one type of robot.
    for i in data['all_robots']:
        solver.Add(sum(x[i, b] for b in data['all_schools']) <= 1)

    # Robots used can not exceed robots owned.
    for b in data['all_robots']:
        solver.Add(
            sum(x[i, b] * data['l1_schools'][i]
                for i in data['all_schools']) <= data['l1_robots'][b])

    # Robots used must be different every week
    # For loop
    # For each week
    # Give solution where:
    # If all_schools[i] != l1_robots[i]

    # Objective.
    # Maximize total value of robots.
    # Work in Progress
    objective = solver.Objective()
    for i in data['all_items']:
        for b in data['all_bins']:
            objective.SetCoefficient(x[i, b], data['values'][i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f'Total packed value: {objective.Value()}')
        total_weight = 0
        for b in data['all_bins']:
            print(f'Bin {b}')
            bin_weight = 0
            bin_value = 0
            for i in data['all_items']:
                if x[i, b].solution_value() > 0:
                    print(
                        f"Item {i} weight: {data['weights'][i]} value: {data['values'][i]}"
                    )
                    bin_weight += data['weights'][i]
                    bin_value += data['values'][i]
            print(f'Packed bin weight: {bin_weight}')
            print(f'Packed bin value: {bin_value}\n')
            total_weight += bin_weight
        print(f'Total packed weight: {total_weight}')
    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    main()