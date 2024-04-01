# MIX MEASURE BUDDY FIRMWARE

## BUILD MICROPYTHON FIRMWARE WITH CUSTOM MMB CODE USING DOCKER

```bash
# BUILD DOCKER IMAGE
$ docker build -t docker.io/library/mixmeasurebuddyfirmwarebuilder .

# RUN BUILD PROCESS
$ cd _THIS_FOLDER_
$ docker run -v "$PWD:/var/build/src" docker.io/library/mixmeasurebuddyfirmwarebuilder

# FIRMWARE FILES FOR EACH SET MANIFEST
ls -la $PWD/build
```


##
