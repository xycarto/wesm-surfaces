find data/tin/${STATE}/${WORKUNIT}/hillshade -maxdepth 1 -name "*.tif" | \
    xargs -P ${CORES} -t -I % \
    make reproject tif=% in_dir=tin/hillshade workunit=$WORKUNIT state=$STATE

find data/tin/California/CA_NoCAL_Wildfires_B1_2018/hillshade -maxdepth 1 -name "*.tif" | \
    xargs -P 8 -t -I % \
    make reproject tif=% in_dir=tin/hillshade workunit=CA_NoCAL_Wildfires_B1_2018 state=California

make cog in_dir=tin/hillshade workunit=CA_NoCAL_Wildfires_B1_2018 state=California