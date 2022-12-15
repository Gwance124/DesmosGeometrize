import os 
import sys
import getopt

def get_cli_parameters(argv):
    input = ''
    resolution = 256
    alpha = 128
    iterations = 400
    shapesPerStep = 30
    mutationsPerStep = 100
    
    # gets user input and resolution parameters
    try:
        opts, args = getopt.getopt(argv, "hi:r:a:I:s:m:", ["i=", "r=", "a=", "I=", "s=", "m="])
    except getopt.GetoptError:
        print('geodeezmos.py -i <input> -r <resolution> -a <alpha> -I <iterations> -s <shapes per step> -m <mutations per step>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print('geodeezmos.py -i <input> -r <resolution> -a <alpha> -I <iterations> -s <shapes per step> -m <mutations per step>')
            sys.exit()
        elif opt == "-i":
            input = arg
        elif opt == "-r":
            resolution = int(arg)
        elif opt == "-a":
            alpha = int(arg)
        elif opt ==  "-I":
            iterations = int(arg)
        elif opt == "-s":
            shapesPerStep = int(arg)
        elif opt ==  "-m":
            mutationsPerStep = int(arg)

    if not os.path.exists(input):
        print('Input path is not valid')
        sys.exit()

    print('Input is: ', input)
    print('Resolution is: ', resolution)
    print('Alpha is: ', alpha)
    print('Iterations is: ', iterations)
    print('Shapes per Step is: ', shapesPerStep)
    print('Mutations per Step is: ', mutationsPerStep)
    
    return input, resolution, alpha, iterations, shapesPerStep, mutationsPerStep
