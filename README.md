# BiggerGist
repository for containing code that enables users to run GIST on large regions of interest via a massively serial approach

Huge thanks to Matteo Aldeghi (from the Max Planck Institute) for contributing the code which allows end-users to divide GIST into sub-volumes!



Contained here are three python scripts that will assist end-users in performing GIST analysis on large sub-volumes:

FindCentroid.py -- Given a pdb structure file determine the centroid and suggest a GIST region of interest to encompass it.

SplitVolume.py -- Given information defining the large region of interest create gist.in cpptraj scripts to peform GIST on a user specified number of sub-volumes (Written and provided by: Matteo Aldeghi from the Max Planck Institute)

MergeGistDX.py -- Provided overlapping sub-volume GIST .dx outputi files produces a combined .dx file equivalent to a GIST performed on the combined volume. (Written and provided by: Matteo Aldeghi)

FAQ:

Why do the smaller regions created by BiggerGist overlap slightly?

GIST ignores the outer layer of the region of interest for entropic calculations due to the need for neigboring waters in the nearest neighbor approximation. To accommodate this SplitVolume.py creates sub-volumes that overlap by one layer. 

