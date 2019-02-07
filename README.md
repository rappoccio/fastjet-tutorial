# BOOST Conference Series Software Tutorial



## Software

You must have [Docker](https://www.docker.com/community-edition) installed (Community edition is free, so get that).

Then in a terminal:

```
docker pull srappoccio/fastjet-tutorial:latest
```

To run:

```
./runDockerX11OSX.sh srappoccio/fastjet-tutorial:latest
```

(or change ```OSX``` above to ```Ubuntu```). 

This will give you a prompt, and mount the directory ```../results``` 
(i.e., a directory named "results" up one level from this one)
in
the current working directory of the docker image. You can then use
that for communication back and forth from the docker container. Store
any results you want, and they will exist after your image is
deleted.

### With ROOT

If you want to use ROOT, then you can do everything as above, but
change ```fastjet-tutorial``` to ```fastjet-tutorial-root```.

*Important*: The python version for ROOT is still python2. Sorry. 

```
./runDockerX11OSX.sh srappoccio/fastjet-tutorial-root:latest
```

(or change ```OSX``` above to ```Ubuntu```). 


### With command line

If you want a bash shell and not a jupyter pyroot script, you can use
the "Command Line" flavors of the bash scripts, which are the same
except they have an explicit ```/bin/bash``` entry point. 

```
./runDockerX11OSXCommandLine.sh srappoccio/fastjet-tutorial-root:latest
```


## Fastjet Tutorial

You will probably want the command line version above (unless you want to use a python jupyter notebook). You have access to all of the fastjet and fastjet-contrib tutorials in your docker image. For instance:


```
cd /app/fastjet-3.3.1/example
make 01-basic
./01-basic < data/single-event.dat
```

or in fastjet-contrib:
```
cd /app/fjcontrib-1.036/
make example_softdrop
./example_softdrop < ../../fastjet-3.3.1/example/data/single-event.dat
```



## Machine Learning Tutorial

You will probably want the jupyter notebook version above. The examples live in the `lund_jet_examples` directory. 



## Notes:

- To access the notebook, go to [localhost:8888](https://localhost:8888) or [127.0.0.1:8888](https://127.0.0.1:8888). You will often be asked for a token, which can be found in the printout like this:
```
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(a084677e0088 or 127.0.0.1):8888/?token=5f2dbda0e1b14fbb9efb3fd765bea4773d62f86093afe977
```
The token is the part after the equal sign. 



