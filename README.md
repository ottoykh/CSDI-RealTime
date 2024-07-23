# CSDI-RealTime

This API aims to create a seamless integration of weather station data from the Hong Kong Observatory (HKO) and the Common Spatial Data Infrastructure (CSDI). The goal is to georeference the weather station data and transform it into a GeoJSON format for real-time fetching, visualization, and analysis.

### Concept

Bring the unusable, to a georeferenced usable data

### Problem statement
The current CSDI is “directed” based data, they are spatial but not spatial with the data itself, especially the real-time HKO weather dataset. Most of the data in geojson or csv are directing the user to download the real time data in a csv format, this creating a lot of barriers and make the real time data has limited usability and interchangeability. Then, this trial is to make an integration from the HKO data to the CSDI, with this API, the real time data can be merged together and do the fetching and getting the “whole picture” of the data instead of currently “redirecting” based approaches.  

### Methods

* Data collection and merging
* Download each of the subset of every weather station from CSDI and HKO
* Merge all the subset and clear other duplicate field 
* Output the merged data in a geojson based respond API
* Data release with geojson format 
* Online API deployment with modular based programming
