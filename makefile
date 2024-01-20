-include .creds

DOCKER_PW := ${DOCKER_PW}

BASEIMAGE := xycarto/wesm-surfaces
IMAGE := $(BASEIMAGE):2024-01-19

TFBASEIMAGE := xycarto/xycarto-terraform
TFIMAGE := $(TFBASEIMAGE):2024-01-12

.PHONY:

RUN ?= docker run -i --rm --net=host \
	--user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= \
	-e HOME=/work \
	-v$$(pwd):/work \
	-w /work $(IMAGE)

TFRUN ?= docker run -it --rm  \
	-u $$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= \
	-v$$(pwd):/work \
	--net=host \
	-w /work $(TFIMAGE)


PHONY: test-process tf-test-process

##### BUILDS
# time make tf-build workunit=CA_NoCAL_Wildfires_B1_2018 state=California process=surfaces ec2=t2.large volume_size=20 type=test 
tf-build:
	$(TFRUN) bash build-infra.sh -w $(workunit) -s $(state) -p $(process) -e $(ec2) -v $(volume_size) -t $(type) -l remote

tf-build-help:
	$(TFRUN) bash build-infra.sh -h

# time make test process=bcm
tf-test-process:
	$(TFRUN) bash build-infra.sh $(process)

test-process:
	$(RUN) bash build-infra.sh $(process)

### PROCESS
download-files:
	$(RUN) python3 src/download-files.py

bcm: 
	$(RUN) python3  src/bcm-combined.py $(pc)

dsm:
	$(RUN) python3 src/dsm.py $(pc)

tin:
	$(RUN) python3 src/tin.py $(pc)

vrt:
	$(RUN) python3 src/vrt.py 

hillshade:
	$(RUN) python3 process/hillshade.py $(tif) $(in_dir) $(workunit) $(state)

reproject:
	$(RUN) python3 process/reproject.py $(tif) $(in_dir) $(workunit) $(state)

cog:
	$(RUN) python3 process/cog.py $(in_dir) $(workunit) $(state)


## DERIVED PRODUCTS
solar-average:
	$(RUN) python3 process/solar/solar-calc.py $(tif) $(workunit) $(state) $(type)

##### DOCKER MAIN
local-test: docker/Dockerfile
	docker run -it --rm --net=host --user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE) \
	bash

docker-local: docker/Dockerfile
	docker build --tag $(BASEIMAGE) - < docker/Dockerfile && \
	docker tag $(BASEIMAGE) $(IMAGE)

docker: docker/Dockerfile
	echo $(DOCKER_PW) | docker login --username xycarto --password-stdin
	docker build --tag $(BASEIMAGE) - < docker/Dockerfile  && \
	docker tag $(BASEIMAGE) $(IMAGE) && \
	docker push $(IMAGE) && \
	touch .push

docker-pull:
	echo $(DOCKER_PW) | docker login --username xycarto --password-stdin
	docker pull $(IMAGE)

##### DOCKER TERRAFORM 
tf-docker-local: docker/Dockerfile.terraform
	docker build --tag $(TFBASEIMAGE) - < docker/Dockerfile.terraform && \
	docker tag $(TFBASEIMAGE) $(TFIMAGE)

tf-docker: docker/Dockerfile.terraform
	echo $(DOCKER_PW) | docker login --username xycarto --password-stdin
	docker build --tag $(TFBASEIMAGE) - < docker/Dockerfile.terraform && \
	docker tag $(TFBASEIMAGE) $(TFIMAGE) && \
	docker push $(TFIMAGE)

tf-docker-pull:
	echo $(DOCKER_PW) | docker login --username xycarto --password-stdin
	docker pull $(TFIMAGE)







############# UNUSED
# # time make tf-build-test workunit=CA_NoCAL_Wildfires_B1_2018 state=California process=infra ec2=t2.micro volume_size=20 
# tf-build-test:
# 	$(TFRUN) bash build-infra.sh -w $(workunit) -s $(state) -p $(process) -e $(ec2) -v $(volume_size) -t test -l remote

# # time make build-test-local workunit=CA_NoCAL_Wildfires_B1_2018 state=California process=infra ec2=t2.micro volume_size=20 
# build-test-local:
# 	$(RUN) bash build-infra.sh -w $(workunit) -s $(state) -p $(process) -e $(ec2) -v $(volume_size) -t test -l local


# # make download-pc workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# download-pc:
# 	$(RUN) python3 download/download-pc.py $(workunit) $(state)

# # make download-bcm workunit=CA_NoCAL_Wildfires_B1_2018 state=California type=test
# download-bcm:
# 	$(RUN) python3 download/download-bcm.py $(workunit) $(state) $(type)

# # make download-dsm workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# download-dsm:
# 	$(RUN) python3 download/download-dsm.py $(workunit) $(state)

# # make dem pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2051.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# dem:
# 	$(RUN) python3 process/dem.py $(pc) $(workunit) $(state)

# # make dem-gdal pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2051.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# dem-gdal:
# 	$(RUN) python3 process/dem-gdal.py $(pc) $(workunit) $(state)

# # make hexbin pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2054.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# hexbin:
# 	$(RUN) python3 process/hexbin.py $(pc) $(workunit) $(state)

# # time make hexbin-merge workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# hexbin-merge:
# 	$(RUN) bash process/merge-hexbin.sh $(workunit) $(state)

# # time make hexbin-vt workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# hexbin-vt:
# 	$(RUN) python3 process/make-vector-tiles-hexbin.py $(workunit) $(state)

# # make chm laz=path/to/input.laz
# chm:
# 	$(RUN) python3 chm.py $(laz)

# # time make tf-build-bcm workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# tf-build-bcm:
# 	$(TFRUN) bash build-infra-bcm.sh $(workunit) $(state)

# # time make tf-build-surface workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# tf-build-surface:
# 	$(TFRUN) bash build-infra-surfaces.sh $(workunit) $(state)

# # time make tf-build-solar workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# tf-build-solar:
# 	$(TFRUN) bash build-infra-solar.sh $(workunit) $(state)

# list-index:
# 	$(RUN) python3 src/list-index.py