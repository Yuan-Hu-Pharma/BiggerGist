# BiggerGist
repository for containing code that enables users to run GIST on large regions of interest via a massively serial approach

This code is in a developmental stage and is not ready for prime time

The structure of this code will be a wrapper script that will take a users input command for GIST and break it into n number of GIST processes, then run the gistpp cat command to combine the regions of interest such that the user can analyze a region of interest that would otherwise be too large.

The wrapper script will require a functioning version of gistpp with the cat command. 

FAQ:

Why do the smaller regions created by BiggerGist overlap slightly?

GIST ignores the outer layer of the region of interest for entropic calculations due to the need for neigboring waters in the nearest neighbor approximation. To accomodate that please be sure to include one extra dimension in each direction (2 for each of x,y,z). This should also explain why the smaller regions of interest overlap slightly.

Why does the code expect only 2, 4, or 8 subregions?

The idea here is that cpu's come with an even number of threads and to keep the entire process simple I stopped at 8...this was intended as a quick fix script to enable end users to handle larger systems with greater ease, if runtime is not significantly increased by dividing the region of interest into eighths the code will have to be manually changed to handle larger numbers of subvolumes.

What if I don't have a version of GISTPP that contains the cat function?

You can download an up-to-date version of GISTPP here: https://github.com/gosldorf/gist-post-processing 
