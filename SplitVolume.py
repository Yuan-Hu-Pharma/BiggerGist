#!/usr/bin/env python

#
# Written by M. Aldeghi
#

import os
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter


# =============
# Input Options
# =============
def parseOptions():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter,
                            description='''
A script to split the GIST volume into many small boxes for parallel analysis.

The following inputs are required:
  --numboxes: the number of small boxes the large box is to be split into.
              this should match the number of cores you plan to use for the
              analysis, since each small box can be analysed separately.
  --gridcntr, --griddim: these are inputs needed by GIST.

The spacing (--gridspacn) and reference water density (--refdens) are optional
arguments, which will default to 0.5 and 0.03344 (units as in cpptraj).

If you want the script to print out a full cpptraj input file, so that you
can run the analysis simply by doing "cpptraj -i gist.in" you will need to
also provide the relative path to the topology and trajectory files. Residues
to be stripped (e.g. ions) are optional and can be specified with the -s flag.
Similarly, you can select which frames to analyse with the -t flag, otherwise
all available frames will be analysed.
''')
    parser.add_argument('--numboxes', metavar='int', dest='numboxes',
                        help='Number of cuboids to split the box into.',
                        required=True, type=int)
    parser.add_argument('--gridcntr', metavar=('x', 'y', 'z'), dest='center',
                        help='Center of the box.',
                        required=True, nargs=3, type=float)
    parser.add_argument('--griddim', metavar=('x', 'y', 'z'), dest='size',
                        help='Dimensions of the box.',
                        required=True, nargs=3, type=float)
    parser.add_argument('--gridspacn', metavar='float', dest='spacing',
                        help='Grid resolution (angstrom). Default is 0.5.',
                        default=0.5, type=float)
    parser.add_argument('--refdens', metavar='float', dest='refdens',
                        help='Reference water number density. '
                             'Default is 0.0334.',
                        default=0.0334, type=float)
    parser.add_argument('-p', metavar='top', dest='topology',
                        help='Relative path to the topology file.',
                        default=None, type=str)
    parser.add_argument('-x', metavar='trj', dest='trajectory',
                        help='Relative path to the trajectory file.',
                        default=None, type=str)
    parser.add_argument('-s', metavar='strip', dest='strip',
                        help='Residues to strip from trajectory. '
                             'E.g. Na and Cl ions.',
                        default=[], type=str, nargs='+')
    parser.add_argument('-t', metavar=('int'), dest='trjslice',
                        help='First and last frames of the trajectory to '
                             'analyse. Default is all.',
                        default=None, type=int, nargs=2)
    args = parser.parse_args()
    return args


# ====
# Main
# ====
def main(args):

    # ----------
    # Input info
    # ----------
    numboxes = args.numboxes
    spacing = args.spacing
    center = {'x': args.center[0],
              'y': args.center[1],
              'z': args.center[2]}
    size = {'x': args.size[0],
            'y': args.size[1],
            'z': args.size[2]}
    origin = {'x': center['x'] - spacing*(size['x']/2.),
              'y': center['y'] - spacing*(size['y']/2.),
              'z': center['z'] - spacing*(size['z']/2.)}

    # ---------------------------------
    # Calculate how to split the volume
    # ---------------------------------
    div_x, div_y, div_z = findBoxPartitions(numboxes,
                                            size['x'], size['y'], size['z'])

    sboxes_size = {'x': size['x']/div_x,
                   'y': size['y']/div_y,
                   'z': size['z']/div_z}

    sboxes_centers = []
    # in the order of filling z first, then y, then x
    for x in range(div_x):
        for y in range(div_y):
            for z in range(div_z):
                center_x = (origin['x'] +
                            spacing*(sboxes_size['x']/2.) +
                            spacing*(sboxes_size['x']*x))
                center_y = (origin['y'] +
                            spacing*(sboxes_size['y']/2.) +
                            spacing*(sboxes_size['y']*y))
                center_z = (origin['z'] +
                            spacing*(sboxes_size['z']/2.) +
                            spacing*(sboxes_size['z']*z))

                sbox_center = {'x': center_x,
                               'y': center_y,
                               'z': center_z}
                sboxes_centers.append(sbox_center)

    # -----------
    # Write files
    # -----------
    idx = 1
    for center in sboxes_centers:
        os.mkdir('gist%i' % idx)

        with open('gist{0}/gist{0}.in'.format(idx), 'w') as f:

            if args.topology is not None and args.trajectory is not None:
                f.write('parm ../%s\n' % args.topology)

                if args.trjslice is not None:
                    f.write('trajin ../%s %i to %i\n' % (args.trajectory,
                                                         args.trjslice[0],
                                                         args.trjslice[1]))
                else:
                    f.write('trajin ../%s\n' % args.trajectory)

                for res in args.strip:
                    f.write('strip @%s\n' % res)

                f.write('gist refdens {0:.4f} '.format(args.refdens))
                f.write('gridcntr '
                        '{0:.3f} {1:.3f} {2:.3f} '.format(center['x'],
                                                          center['y'],
                                                          center['z']))
                f.write('griddim '
                        '{0:d} {1:d} {2:d} '.format(int(sboxes_size['x']+2),
                                                    int(sboxes_size['y']+2),
                                                    int(sboxes_size['z']+2)))
                f.write('gridspacn {0} '.format(spacing))
                f.write('out gist.dat\n')
                f.write('go\nquit\n')
            else:
                f.write('gist refdens {0:.4f} '.format(args.refdens))
                f.write('gridcntr '
                        '{0:.3f} {1:.3f} {2:.3f} '.format(center['x'],
                                                          center['y'],
                                                          center['z']))
                f.write('griddim '
                        '{0:d} {1:d} {2:d} '.format(int(sboxes_size['x']+2),
                                                    int(sboxes_size['y']+2),
                                                    int(sboxes_size['z']+2)))
                f.write('gridspacn {0} '.format(spacing))
                f.write('out gist.dat\n')

            idx += 1

    print('\nAll input files written in "gistX" folders.\n')


# =========
# Functions
# =========
def findBoxPartitions(num_boxes, dimx, dimy, dimz):
    '''
    Find how the x,y, and z dimensions can be split in order to obtain a
    predefined number of cuboids, then pick the combination in order to
    minimise the number of surface voxels.
    '''
    fx = factors(int(dimx))
    fy = factors(int(dimy))
    fz = factors(int(dimz))

    combi = findCombination(num_boxes, fx, fy, fz)
    best_comb = findMinArea(combi, dimx, dimy, dimz)
    return best_comb[0], best_comb[1], best_comb[2]


def factors(x):
    '''
    Find all numbers an integer can be divided by.
    '''
    factors = []
    for i in range(1, x + 1):
        if x % i == 0:
            factors.append(i)
    return factors


def findCombination(num, x_list, y_list, z_list):
    '''
    Find which values of x,y,z can be used so that x*y*z is equal to
    a predefined number of cuboids.
    '''
    combinations = []
    for x in x_list:
        for y in y_list:
            for z in z_list:
                if x*y*z == num:
                    combination = [x, y, z]
                    combinations.append(combination)

    if len(combinations) == 0:
        exit('ERROR: No combination of integers can return the desired\n'
             'number of sub-volumes given the [x, y, z] dimensions provided.')

    print("\nCombinations returning the desired number of boxes:")

    for c in combinations:
        print '%i x %i x %i' % (c[0], c[1], c[2])
    return combinations


def findMinArea(list_of_combinations, dimx, dimy, dimz):
    '''
    list_of_combinations contains a list of [x,y,z] integer values.
    Find the combination that minimise the number of surface voxels
    '''
    for i, combi in enumerate(list_of_combinations):
        a = dimx/combi[0]
        b = dimy/combi[1]
        c = dimz/combi[2]
        # number of voxels on the surface:
        A = a*b*2 + b*(c-2)*2 + (a-2)*(c-2)*2

        # initialise min_A
        if i == 0:
            min_A = A

        if A < min_A:
            min_A = A
            min_combi = [combi[0], combi[1], combi[2]]

    print('\nThe following combination provides equal-size boxes with the\n'
          'lowest number of surface voxels:')
    print '%i x %i x %i' % (min_combi[0], min_combi[1], min_combi[2])
    return min_combi


if __name__ == "__main__":
    args = parseOptions()
    main(args)
