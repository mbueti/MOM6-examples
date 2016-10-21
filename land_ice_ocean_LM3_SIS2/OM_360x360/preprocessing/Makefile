SHELL=bash -f
NP=8

all: input forcing obs ocean_mosaic c48_mosaic c96_mosaic c192_mosaic
	md5sum -c md5sums.txt

showenv:
	env
	-set
	-module list
	which python
	-python --version

input: ocean_hgrid.nc topog.nc basin_codes.nc

forcing: seawifs.nc tidal_amplitude.nc 

obs: WOA05_ptemp_salt_monthly.nc WOA05_ptemp_salt_annual.nc

# Grid

ocean_hgrid.nc: 
	ulimit; source activate MIDAS; python create_grids.py
	ulimit; source activate MIDAS; python merge_grids.py
	./changeChar.py ocean_hgrid.nc tile tile1

# Topography
output_topog.nc: GEBCO_08_v2.nc bedmap2.nc ocean_hgrid.nc
	ulimit; source activate MIDAS; python create_topo.py
	ulimit; source activate MIDAS; python blend_topo.py


edit_topog.nc: output_topog.nc
	./applyTopoEdits.py --orig=output_topog.nc --edits=topo_edits --scale=-1.0 --output=edit_topog.nc

topog.nc: edit_topog.nc output_topog.nc
	./ice9.py edit_topog.nc --output topog.nc

basin_codes.nc: topog.nc
	ulimit; source activate MIDAS; python make_basin_mask.py
	source activate NCO; ncatted -h -a flag_meanings,basin,c,c,'1:Southern Ocean, 2:Atlantic Ocean, 3:Pacific Ocean, 4:Arctic Ocean, 5:Indian Ocean, 6:Mediterranean Sea, 7:Black Sea, 8:Hudson Bay, 9:Baltic Sea, 10:Red Sea, 11:Persian Gulf' basin_codes.nc
	source activate NCO;ncatted -h -a flag_values,basin,c,c,'1,2,3,4,5,6,7,8,9,10,11' basin_codes.nc

WOA05_ptemp_salt_annual.nc: WOA05_ptemp_salt_monthly.nc
	source activate NCO;ncra -h -O $< $@

WOA05_ptemp_salt_monthly.nc: ocean_hgrid.nc topog.nc /archive/gold/datasets/obs/WOA05_pottemp_salt.nc interpWOA05.py 
	ulimit; source activate MIDAS; python interpWOA05.py
	source activate NCO; ncatted -h -a modulo,TIME,c,c,' ' WOA05_ptemp_salt_monthly.nc


seawifs.nc: ocean_hgrid.nc topog.nc /archive/mjh/gold/datasets/obs/SeaWifs/SeaWiFS_Non_Elnino_clim.nc interpCHL.py 
	ulimit; source activate MIDAS; ln -s /archive/mjh/gold/datasets/obs/SeaWifs/SeaWiFS_Non_Elnino_clim.nc .;  python interpCHL.py

tidal_amplitude.nc: DATA interpTides.py 
	ulimit; source activate MIDAS; python interpTides.py



DATA: tpxo7_atlas_netcdf.tar.Z GEBCO_08_v2.nc bedmap2.nc
	tar xzvf tpxo7_atlas_netcdf.tar.Z
	touch DATA

tpxo7_atlas_netcdf.tar.Z:
#	wget ftp://ftp.oce.orst.edu/dist/tides/Global/tpxo7_atlas_netcdf.tar.Z
	ln -s  /archive/gold/datasets/obs/tpxo7_atlas_netcdf.tar.Z


GEBCO_08_v2.nc :
	ln -s /archive/gold/datasets/topography/$@ .

bedmap2.nc :
	ln -s /archive/gold/datasets/topography/$@ .

MIDAS:
	git clone https://github.com/mjharriso/MIDAS.git
	(cd MIDAS; git checkout 473c764)

local: MIDAS 
	-rm -rf $</build/*
	mkdir -p $@
	cd $<; make -f Makefile_gfortran fms_build/libfms.a PREFIX=$(CONDA_ENV_PATH)
	touch $@

FRE_NCTOOLS = fre_nctools/tools

fre_nctools:
	echo $@
	git clone git@gitlab.gfdl.noaa.gov:fre/fre-nctools.git $@
	(cd $@; git checkout user/mjh/anaconda)
	(cd $@; cd tools;git clone git@gitlab.gfdl.noaa.gov:Krista.A.Dunne/simple_hydrography.git; cd simple_hydrography;git checkout user/mjh/anaconda)

fre_nctools/tools: fre_nctools local
fre_nctools/tools/make_hgrid/make_hgrid \
fre_nctools/tools/make_solo_mosaic/make_solo_mosaic \
fre_nctools/tools/make_quick_mosaic/make_quick_mosaic \
fre_nctools/tools/make_coupler_mosaic/make_coupler_mosaic \
fre_nctools/tools/runoff_regrid/runoff_regrid  \
fre_nctools/tools/river_regrid/river_regrid fre_nctools/tools/simple_hydrography/cp_river_vars \
fre_nctools/tools/simple_hydrography/cr_lake_files \
fre_nctools/tools/simple_hydrography/rmv_parallel_rivers: fre_nctools/tools
	(cd $(@D); source activate MIDAS; make SITE=conda PREFIX=$(CONDA_ENV_PATH) -f fre-nctools.mk $(@F) )

OCN_MOSAIC = $(foreach f,atmos_mosaic_tile1Xland_mosaic_tile1.cdl atmos_mosaic_tile1Xocean_mosaic_tile1.cdl grid_spec.cdl land_mask.cdl\
                         land_mosaic_tile1Xocean_mosaic_tile1.cdl ocean_mask.cdl ocean_mosaic.cdl,mosaic_ocean.360x360/$f)

C48_MOSAIC = $(foreach f,C48_grid.tile1.nc C48_grid.tile2.nc C48_grid.tile3.nc C48_grid.tile4.nc C48_grid.tile5.nc C48_grid.tile6.nc C48_mosaic.nc\
                         C48_mosaic_tile1XC48_mosaic_tile1.cdl C48_mosaic_tile1Xocean_mosaic_tile1.cdl C48_mosaic_tile2XC48_mosaic_tile2.cdl C48_mosaic_tile2Xocean_mosaic_tile1.cdl\
                         C48_mosaic_tile3XC48_mosaic_tile3.cdl C48_mosaic_tile3Xocean_mosaic_tile1.cdl C48_mosaic_tile4XC48_mosaic_tile4.cdl C48_mosaic_tile4Xocean_mosaic_tile1.cdl\
                         C48_mosaic_tile5XC48_mosaic_tile5.cdl C48_mosaic_tile5Xocean_mosaic_tile1.cdl C48_mosaic_tile6XC48_mosaic_tile6.cdl C48_mosaic_tile6Xocean_mosaic_tile1.cdl\
                         land_mask_tile1.cdl land_mask_tile2.cdl land_mask_tile3.cdl land_mask_tile4.cdl land_mask_tile5.cdl land_mask_tile6.cdl\
                         mosaic.cdl ocean_mask.cdl river_data.tile1.nc river_data.tile2.nc river_data.tile3.nc river_data.tile4.nc river_data.tile5.nc\
                         river_data.tile6.nc,mosaic_c48.360x360/$f)

C96_MOSAIC = $(foreach f,C96_grid.tile1.nc C96_grid.tile2.nc C96_grid.tile3.nc C96_grid.tile4.nc C96_grid.tile5.nc C96_grid.tile6.nc C96_mosaic.nc\
                         C96_mosaic_tile1XC96_mosaic_tile1.cdl C96_mosaic_tile1Xocean_mosaic_tile1.cdl C96_mosaic_tile2XC96_mosaic_tile2.cdl C96_mosaic_tile2Xocean_mosaic_tile1.cdl\
                         C96_mosaic_tile3XC96_mosaic_tile3.cdl C96_mosaic_tile3Xocean_mosaic_tile1.cdl C96_mosaic_tile4XC96_mosaic_tile4.cdl C96_mosaic_tile4Xocean_mosaic_tile1.cdl\
                         C96_mosaic_tile5XC96_mosaic_tile5.cdl C96_mosaic_tile5Xocean_mosaic_tile1.cdl C96_mosaic_tile6XC96_mosaic_tile6.cdl C96_mosaic_tile6Xocean_mosaic_tile1.cdl\
                         land_mask_tile1.cdl land_mask_tile2.cdl land_mask_tile3.cdl land_mask_tile4.cdl land_mask_tile5.cdl land_mask_tile6.cdl\
                         mosaic.cdl ocean_mask.cdl river_data.tile1.nc river_data.tile2.nc river_data.tile3.nc river_data.tile4.nc river_data.tile5.nc\
                         river_data.tile6.nc,mosaic_c96.360x360/$f)

C192_MOSAIC = $(foreach f,C192_grid.tile1.nc C192_grid.tile2.nc C192_grid.tile3.nc C192_grid.tile4.nc C192_grid.tile5.nc C192_grid.tile6.nc C192_mosaic.nc\
                         C192_mosaic_tile1XC192_mosaic_tile1.cdl C192_mosaic_tile1Xocean_mosaic_tile1.cdl C192_mosaic_tile2XC192_mosaic_tile2.cdl C192_mosaic_tile2Xocean_mosaic_tile1.cdl\
                         C192_mosaic_tile3XC192_mosaic_tile3.cdl C192_mosaic_tile3Xocean_mosaic_tile1.cdl C192_mosaic_tile4XC192_mosaic_tile4.cdl C192_mosaic_tile4Xocean_mosaic_tile1.cdl\
                         C192_mosaic_tile5XC192_mosaic_tile5.cdl C192_mosaic_tile5Xocean_mosaic_tile1.cdl C192_mosaic_tile6XC192_mosaic_tile6.cdl C192_mosaic_tile6Xocean_mosaic_tile1.cdl\
                         land_mask_tile1.cdl land_mask_tile2.cdl land_mask_tile3.cdl land_mask_tile4.cdl land_mask_tile5.cdl land_mask_tile6.cdl\
                         mosaic.cdl ocean_mask.cdl river_data.tile1.nc river_data.tile2.nc river_data.tile3.nc river_data.tile4.nc river_data.tile5.nc\
                         river_data.tile6.nc,mosaic_c192.360x360/$f)

ocean_mosaic: $(OCN_MOSAIC) basin_codes.nc
c48_mosaic: $(C48_MOSAIC)
c96_mosaic: $(C96_MOSAIC)
c192_mosaic: $(C192_MOSAIC)  


$(filter-out mosaic_ocean.360x360/grid_spec.nc mosaic_ocean.360x360/ocean_mosaic.nc,$(OCN_MOSAIC:.cdl=.nc)): mosaic_ocean.360x360/grid_spec.nc local
mosaic_ocean.360x360/ocean_mosaic.nc: ocean_hgrid.nc topog.nc $(FRE_NCTOOLS)/make_solo_mosaic/make_solo_mosaic  $(FRE_NCTOOLS)/make_quick_mosaic/make_quick_mosaic
	mkdir -p $(@D)
	(cd $(@D); ln -sf ../ocean_hgrid.nc ../topog.nc .)
	(cd $(@D); source activate MIDAS; ../$(FRE_NCTOOLS)/make_solo_mosaic/make_solo_mosaic --num_tiles 1 --dir . --mosaic_name ocean_mosaic --tile_file ocean_hgrid.nc --periodx 360.)
mosaic_ocean.360x360/grid_spec.nc: mosaic_ocean.360x360/ocean_mosaic.nc $(FRE_NCTOOLS)/make_quick_mosaic/make_quick_mosaic
	(cd $(@D); source activate MIDAS; ../$(FRE_NCTOOLS)/make_quick_mosaic/make_quick_mosaic --reproduce_siena --input_mosaic ocean_mosaic.nc --mosaic_name grid_spec --ocean_topog topog.nc )

$(filter-out mosaic_c48.360x360/mosaic.nc,$(C48_MOSAIC:.cdl=.nc)): mosaic_c48.360x360/mosaic.nc local
mosaic_c48.360x360/mosaic.nc: mosaic_ocean.360x360/ocean_mosaic.nc topog.nc $(FRE_NCTOOLS)/make_hgrid/make_hgrid $(FRE_NCTOOLS)/make_coupler_mosaic/make_coupler_mosaic  \
       $(FRE_NCTOOLS)/river_regrid/river_regrid $(FRE_NCTOOLS)/simple_hydrography/cp_river_vars $(FRE_NCTOOLS)/simple_hydrography/rmv_parallel_rivers $(FRE_NCTOOLS)/simple_hydrography/cr_lake_files
	mkdir -p $(@D)
	(cd $(@D); ln -sf ../ocean_hgrid.nc ../topog.nc .)
	(cd $(@D); ln -sf ../mosaic_ocean.360x360/ocean_mosaic.nc .)
	(cd $(@D);../$(FRE_NCTOOLS)/make_hgrid/make_hgrid --grid_type conformal_cubic_grid --nlon 96 --nratio 2)
	(cd $(@D);../$(FRE_NCTOOLS)/make_solo_mosaic/make_solo_mosaic --num_tiles 6 --dir . --mosaic_name C48_mosaic --tile_file  horizontal_grid.tile1.nc,horizontal_grid.tile2.nc,horizontal_grid.tile3.nc,horizontal_grid.tile4.nc,horizontal_grid.tile5.nc,horizontal_grid.tile6.nc)
	(cd $(@D); ../$(FRE_NCTOOLS)/make_coupler_mosaic/make_coupler_mosaic --reproduce_siena --atmos_mosaic C48_mosaic.nc --ocean_mosaic ocean_mosaic.nc --mosaic_name mosaic --ocean_topog topog.nc)
	(cd $(@D); ../$(FRE_NCTOOLS)/river_regrid/river_regrid --mosaic mosaic.nc --river_src /archive/kap/lmdt/river_network/netcdf/0.5deg/disagg/river_network_mrg_0.5deg_ad3nov_fill_coast_auto1_0.125.nc --min_frac 0.0 --land_thresh 1.e-5)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib; ../$(FRE_NCTOOLS)/simple_hydrography/cp_river_vars < ../rifs.txt)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib;../$(FRE_NCTOOLS)/simple_hydrography/rmv_parallel_rivers < ../rnfs.txt)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib;../$(FRE_NCTOOLS)/simple_hydrography/cp_river_vars < ../rnfs.txt)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib; touch input.nml;../$(FRE_NCTOOLS)/simple_hydrography/cr_lake_files < ../rnfs2.txt)
	(cd $(@D); source activate NCO; for t in 1 2 3 4 5 6; do (mv river_network.tile$${t}.nc river_data.tile$${t}.nc; ncks -A -a -v  lake_frac,lake_depth_sill,lake_tau,WaterBod,PWetland,connected_to_next,whole_lake_area,max_slope_to_next lake_frac.tile$${t}.nc river_data.tile$${t}.nc);done)
	(cd $(@D); python ../check_land.py > river_check.txt)
#	(cd $(@D); cp mosaic.nc grid_spec.nc; tar cvhf ../$(@D).tar $(wildcard C48_mosaic*.nc horizontal_grid*.nc ocean_*.nc land_mask*.nc river_data*.nc) grid_spec.nc topog.nc)

$(filter-out mosaic_c96.360x360/mosaic.nc,$(C96_MOSAIC:.cdl=.nc)): mosaic_c96.360x360/mosaic.nc local
mosaic_c96.360x360/mosaic.nc: mosaic_ocean.360x360/ocean_mosaic.nc topog.nc $(FRE_NCTOOLS)/make_hgrid/make_hgrid $(FRE_NCTOOLS)/make_coupler_mosaic/make_coupler_mosaic  \
       $(FRE_NCTOOLS)/river_regrid/river_regrid $(FRE_NCTOOLS)/simple_hydrography/cp_river_vars $(FRE_NCTOOLS)/simple_hydrography/rmv_parallel_rivers $(FRE_NCTOOLS)/simple_hydrography/cr_lake_files
	mkdir -p $(@D)
	(cd $(@D); ln -sf ../ocean_hgrid.nc ../topog.nc .)
	(cd $(@D); ln -sf ../mosaic_ocean.360x360/ocean_mosaic.nc .)
	(cd $(@D);../$(FRE_NCTOOLS)/make_hgrid/make_hgrid --grid_type conformal_cubic_grid --nlon 192 --nratio 2)
	(cd $(@D);../$(FRE_NCTOOLS)/make_solo_mosaic/make_solo_mosaic --num_tiles 6 --dir . --mosaic_name C96_mosaic --tile_file  horizontal_grid.tile1.nc,horizontal_grid.tile2.nc,horizontal_grid.tile3.nc,horizontal_grid.tile4.nc,horizontal_grid.tile5.nc,horizontal_grid.tile6.nc)
	(cd $(@D); ../$(FRE_NCTOOLS)/make_coupler_mosaic/make_coupler_mosaic --reproduce_siena --atmos_mosaic C96_mosaic.nc --ocean_mosaic ocean_mosaic.nc --mosaic_name mosaic --ocean_topog topog.nc)
	(cd $(@D); ../$(FRE_NCTOOLS)/river_regrid/river_regrid --mosaic mosaic.nc --river_src /archive/kap/lmdt/river_network/netcdf/0.5deg/disagg/river_network_mrg_0.5deg_ad3nov_fill_coast_auto1_0.125.nc --min_frac 0.0 --land_thresh 1.e-5)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib; ../$(FRE_NCTOOLS)/simple_hydrography/cp_river_vars < ../rifs.txt)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib;../$(FRE_NCTOOLS)/simple_hydrography/rmv_parallel_rivers < ../rnfs.txt)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib;../$(FRE_NCTOOLS)/simple_hydrography/cp_river_vars < ../rnfs.txt)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib; touch input.nml;../$(FRE_NCTOOLS)/simple_hydrography/cr_lake_files < ../rnfs2.txt)
	(cd $(@D); source activate NCO; for t in 1 2 3 4 5 6; do (mv river_network.tile$${t}.nc river_data.tile$${t}.nc; ncks -A -a -v  lake_frac,lake_depth_sill,lake_tau,WaterBod,PWetland,connected_to_next,whole_lake_area,max_slope_to_next lake_frac.tile$${t}.nc river_data.tile$${t}.nc);done)
	(cd $(@D); python ../check_land.py > river_check.txt)
#	(cd $(@D); cp mosaic.nc grid_spec.nc; tar cvhf ../$(@D).tar $(wildcard C48_mosaic*.nc horizontal_grid*.nc ocean_*.nc land_mask*.nc river_data*.nc) grid_spec.nc topog.nc)

$(filter-out mosaic_c192.360x360/mosaic.nc,$(C192_MOSAIC:.cdl=.nc)): mosaic_c192.360x360/mosaic.nc local
mosaic_c192.360x360/mosaic.nc: mosaic_ocean.360x360/ocean_mosaic.nc topog.nc $(FRE_NCTOOLS)/make_hgrid/make_hgrid $(FRE_NCTOOLS)/make_coupler_mosaic/make_coupler_mosaic  \
       $(FRE_NCTOOLS)/river_regrid/river_regrid $(FRE_NCTOOLS)/simple_hydrography/cp_river_vars $(FRE_NCTOOLS)/simple_hydrography/rmv_parallel_rivers $(FRE_NCTOOLS)/simple_hydrography/cr_lake_files
	mkdir -p $(@D)
	(cd $(@D); ln -sf ../ocean_hgrid.nc ../topog.nc .)
	(cd $(@D); ln -sf ../mosaic_ocean.360x360/ocean_mosaic.nc .)
	(cd $(@D);../$(FRE_NCTOOLS)/make_hgrid/make_hgrid --grid_type conformal_cubic_grid --nlon 384 --nratio 2)
	(cd $(@D);../$(FRE_NCTOOLS)/make_solo_mosaic/make_solo_mosaic --num_tiles 6 --dir . --mosaic_name C192_mosaic --tile_file  horizontal_grid.tile1.nc,horizontal_grid.tile2.nc,horizontal_grid.tile3.nc,horizontal_grid.tile4.nc,horizontal_grid.tile5.nc,horizontal_grid.tile6.nc)
	(cd $(@D); ../$(FRE_NCTOOLS)/make_coupler_mosaic/make_coupler_mosaic --reproduce_siena --atmos_mosaic C192_mosaic.nc --ocean_mosaic ocean_mosaic.nc --mosaic_name mosaic --ocean_topog topog.nc)
	(cd $(@D); ../$(FRE_NCTOOLS)/river_regrid/river_regrid --mosaic mosaic.nc --river_src /archive/kap/lmdt/river_network/netcdf/0.5deg/disagg/river_network_mrg_0.5deg_ad3nov_fill_coast_auto1_0.125.nc --min_frac 0.0 --land_thresh 1.e-5)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib; ../$(FRE_NCTOOLS)/simple_hydrography/cp_river_vars < ../rifs.txt)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib;../$(FRE_NCTOOLS)/simple_hydrography/rmv_parallel_rivers < ../rnfs.txt)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib;../$(FRE_NCTOOLS)/simple_hydrography/cp_river_vars < ../rnfs.txt)
	(cd $(@D); source activate MIDAS;export LD_LIBRARY_PATH=$(CONDA_ENV_PATH)/lib; touch input.nml;../$(FRE_NCTOOLS)/simple_hydrography/cr_lake_files < ../rnfs2.txt)
	(cd $(@D); source activate NCO; for t in 1 2 3 4 5 6; do (mv river_network.tile$${t}.nc river_data.tile$${t}.nc; ncks -A -a -v  lake_frac,lake_depth_sill,lake_tau,WaterBod,PWetland,connected_to_next,whole_lake_area,max_slope_to_next lake_frac.tile$${t}.nc river_data.tile$${t}.nc);done)
	(cd $(@D); python ../check_land.py > river_check.txt)
#	(cd $(@D); cp mosaic.nc grid_spec.nc; tar cvhf ../$(@D).tar $(wildcard C48_mosaic*.nc horizontal_grid*.nc ocean_*.nc land_mask*.nc river_data*.nc) grid_spec.nc topog.nc)

%.cdl: %.nc
	ncdump $< | egrep -v 'code_version|history' > $@


md5sums.txt: ocean_hgrid.nc topog.nc basin_codes.nc seawifs.nc tidal_amplitude.nc WOA05_ptemp_salt_monthly.nc WOA05_ptemp_salt_annual.nc 
	echo Grids > $@
	md5sum ocean_hgrid.nc >> $@
	echo >> $@
	echo Topography >> $@
	md5sum topog.nc >> $@
	md5sum basin_codes.nc >> $@
	echo >> $@
	echo Data >> $@
	md5sum seawifs.nc tidal_amplitude.nc >> $@
	echo >> $@
	echo Obs >> $@
	md5sum WOA05_ptemp_salt_{monthly,annual}.nc >> $@
	echo >> $@

