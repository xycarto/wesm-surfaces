-include .creds

BASEIMAGE := dragonflyscience/wesm-surfaces
IMAGE := $(BASEIMAGE):2023-04-22

RUN ?= docker run --rm --net=host --user=$$(id -u):$$(id -g) -e DISPLAY=$$DISPLAY --env-file .creds -e RUN= -v$$(pwd):/work -w /work $(IMAGE)

list-index:
	$(RUN) python3 list-index.py

download-laz:
	$(RUN) bash download-laz.sh

# make bcm laz=path/to/input.laz
bcm: 
	$(RUN) python3 bcm-alt.py $(laz) 

# make dsm laz=path/to/input.laz
dsm:
	$(RUN) python3 dsm.py $(laz)

# make dem laz=path/to/input.laz
dem:
	$(RUN) python3 dem.py $(laz)

# make chm laz=path/to/input.laz
chm:
	$(RUN) python3 chm.py $(laz)

# make bf-clip laz=path/to/input.laz
bf-clip:
	$(RUN) python3 clip-bf.py $(laz)

local-test: Dockerfile
	docker run -it --rm --net=host --user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE) \
	bash

docker-local: Dockerfile
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE)

docker: Dockerfile
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE) && \
	docker push $(IMAGE) && \
	touch .push

docker-pull:
	docker pull $(IMAGE)