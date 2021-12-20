Filename: state_p16_sov_data_by_p16_srprec.dbf, state_p16_sov_data_by_p16_srprec.csv

File URL: http://statewidedatabase.org/pub/data/P16/state/state_p16_sov_data_by_p16_srprec.zip

Dataset: 2016 Primary Election Precinct Data

Description: Statewide Statement of Vote data file containing precinct level voting results for statewide races.

Unit of analysis: SR precincts are derived from consolidated precincts and are a geographic unit constructed for statistical merging purposes by the Statewide Database.

Data source:	Statewide Database - University of California, Berkeley

Technical documentation:	http://statewidedatabase.org/d10/Creating%20CA%20Official%20Redistricting%20Database.pdf

Codebooks:	The 58 Statement of Vote data county codebooks can be accessed from the election's precinct data page,
http://statewidedatabase.org/d10/p16.html

Note about SOV data codebooks and candidate names: 

SOV data file codebooks are county and election specific. The names of the candidates that ran in Assembly, Senate, Congressional and Board of Equalization 
district based races vary by county for each election depending on which districts fall within the county.

The Assembly, Congressional, Senate and Board of Equalization districts that each precinct is located in can be found
in the fields labeled ADDIST, CDDIST, SDDIST and BOEDIST. In order to determine the candidates that were on a ballot in a given
precinct, retrieve the district number from the SOV data table for that precinct record and then look up the candidate's name in the sov data codebook for that count.
 
For example in the 2012 Primary Election, Sonoma County svprec 1001 was located in the 5th Congressional distric according to the state_p12_sov_data_by_p12_svprec.dbf. Refering to 2012 Primary Sonoma County sov data codebook, 097.codes allows one to determine that the cngdem01 candidate that ran in the 5th congressional district i.e. CNG05DEM01 corresponds to the candidate Mike Thompson while the cngdem01 candidate running in svprec 1048, located in the 2nd Congressional corresponds to CNG02dem01, Susan  Adams. In cases where there was no party candidate running in the race, the records in the sov data table will be all zeros. Please see the 2012 Primary 2nd Congressional Green Party candidate, cnggrn01 in the state_p12_sov_data_by_p12_svprec.dbf for an example of this. 

Date last modified:  Mon,02/Aug/2021

Previous versions:	none			
  Wed,21/Oct/2020
  Fri,18/Oct/2019
	01/08/2018 

County records not available or unavailable at time of file creation:	none