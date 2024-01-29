-include .creds
-include configs/process-config.env

BASEIMAGE := xycarto/wesm-surfaces
IMAGE := $(BASEIMAGE):2024-01-19

.PHONY:

RUN ?= docker run -i --rm --net=host \
	--user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	--env-file configs/process-config.env \
	-e RUN= \
	-e HOME=/work \
	-v$$(pwd):/work \
	-w /work $(IMAGE)

PHONY: 

### PROCESS
bcm: 
	$(RUN) python3  src/bcm-no-buff.py $(pc)

dsm:
	$(RUN) python3 src/dsm.py $(pc)

tin:
	$(RUN) python3 src/tin.py $(pc)


## DERIVED PRODUCTS
solar-average:
	$(RUN) python3 src/solar/solar-calc.py $(tif)

hillshade:
	$(RUN) python3 src/hillshade.py $(tif) 

reproject:
	$(RUN) python3 src/reproject.py $(tif) 

cog:
	$(RUN) python3 src/cog.py

## HELPERS
download-files:
	$(RUN) python3 src/download-files.py

vrt:
	$(RUN) python3 src/vrt.py 

## TEST EXTENTS
test-extent:
	$(RUN) python3 src/test/test-extents.py $(pc)

test-dirs:
	$(RUN) python3 src/test-dirs.py

##### DOCKER MAIN
local-test: docker/Dockerfile
	docker run -it --rm --net=host --user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	--env-file configs/process-config.env \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE) \
	bash

docker-local: docker/Dockerfile
	docker build --tag $(BASEIMAGE) - < docker/Dockerfile && \
	docker tag $(BASEIMAGE) $(IMAGE)

docker: docker/Dockerfile
	docker build --tag $(BASEIMAGE) - < docker/Dockerfile  && \
	docker tag $(BASEIMAGE) $(IMAGE) && \
	docker push $(IMAGE) && \
	touch .push

docker-pull:
	docker pull $(IMAGE)