`mvf(1)` -- format names and move files
===

## SYNOPSIS

    mvf [-s <re>] [-S] [-X] [-P] [-f <format>] [-y <filenames>] [-x <sep>] [-z <num>] [-Z <num>]
    
    # transformations -- if none are specified, -S is assumed
    -s <re>       split filenames on regex (groups will be saved in terms)
    -S            same as -s '[\s-_.]+'
    
    # options
    -X            do not extract extensions
    -x <sep>      extension separator (default = '.')
    -z <num>      extension segment size limit (default = 4)
    -Z <num>      extension segment count limit (default = 99999)
    -P            do not extract path
    
    # target files
    -f <format>   target filename format
    -y            execute the move

## USAGE

### step 1
```
mvf *
```

Create the dictionary of terms to be used to build target filenames.
This step will execute your transformation extraction steps and print
the resulting dictionary.

### step 2
```
mvf * -f '{p10:03d}.{ext}'
```

Print the original and formatted filenames to confirm your work.

### step 3
```
mvf * -f '{p10:03d}.{ext}' -y
```

Execute the moves.

## COPYRIGHT

Copyright (c) 2019 James Andariese
