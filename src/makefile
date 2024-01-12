-include .creds

DOCKER_PW := ${DOCKER_PW}

BASEIMAGE := xycarto/wesm-surfaces
IMAGE := $(BASEIMAGE):2024-01-12

TFBASEIMAGE := xycarto/xycarto-terraform
TFIMAGE := $(TFBASEIMAGE):2024-01-12

RUN ?= docker run --rm --net=host \
	--user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= \
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

list-index:
	$(RUN) python3 src/list-index.py

# make download-pc workunit=CA_NoCAL_Wildfires_B1_2018 state=California
download-pc:
	$(RUN) python3 download/download-pc.py $(workunit) $(state)

# make bcm pc=data/point-clouds/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2021n2057.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# make bcm pc=data/point-clouds/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2051.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
bcm: 
	$(RUN) python3  -W ignore process/bcm-alt.py $(pc) $(workunit) $(state)

# make dsm pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2021n2057.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
dsm:
	$(RUN) python3 process/dsm.py $(pc) $(workunit) $(state)

# make dem pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2021n2057.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# make dem pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2051.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
dem:
	$(RUN) python3 process/dem.py $(pc) $(workunit) $(state)

# make dem-gdal pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2051.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
dem-gdal:
	$(RUN) python3 process/dem-gdal.py $(pc) $(workunit) $(state)

# make tin pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2021n2057.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# make tin pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2051.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
tin:
	$(RUN) python3 process/tin.py $(pc) $(workunit) $(state)

# make hexbin pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2021n2057.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# make hexbin pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2051.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California
# make hexbin pc=data/bcm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2054.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California

hexbin:
	$(RUN) python3 process/hexbin.py $(pc) $(workunit) $(state)

# make vrt in_dir=dsm workunit=CA_NoCAL_Wildfires_B1_2018 state=California
vrt:
	$(RUN) python3 process/vrt.py $(in_dir) $(workunit) $(state)

# make hillshade tif=data/dsm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2051.tif in_dir=dsm workunit=CA_NoCAL_Wildfires_B1_2018 state=California
hillshade:
	$(RUN) python3 process/hillshade.py $(tif) $(in_dir) $(workunit) $(state)

# make reproject tif=data/dsm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2051.tif in_dir=dsm workunit=CA_NoCAL_Wildfires_B1_2018 state=California
reproject:
	$(RUN) python3 process/reproject.py $(tif) $(in_dir) $(workunit) $(state)

# make cog in_dir=dsm workunit=CA_NoCAL_Wildfires_B1_2018 state=California
cog:
	$(RUN) python3 process/cog.py $(in_dir) $(workunit) $(state)

# make chm laz=path/to/input.laz
chm:
	$(RUN) python3 chm.py $(laz)

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

##### DOCKER TERRAFORM #####

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

###### TERRAFORM RUN ######

# time make tf-build-surface workunit=CA_NoCAL_Wildfires_B1_2018 state=California
tf-build-surface:
	$(TFRUN) bash build-infra.sh $(workunit) $(state)