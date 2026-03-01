println("Updating Julia packages.. this will take a few minutes!")

import Pkg
using Pkg 
# Note that the IDE executes code from teh root and not respective to the file
packages = readlines("src/DATA/Julia_packages.txt", keep=true) 

for i in 1:length(packages)
    line = packages[i] # take next line, for example: "[5789e2e9] FileIO v1.4.3"
    line = line[14:end] # cut off the first 14 characters, i.e. the package [id]
    last_space = findlast(" ", line)[1]  # find last space, take the first dimention
    cut2 = last_space - 1 # one character before the last space
    package = line[1:cut2]
    println("# Pkg.add(\"", package,"\") ")
    println("# using ", package )
    println(" " )
    Pkg.add( package )
end

Pkg.resolve()
Pkg.update()