North American Summer PDSI Reconstructions
-----------------------------------------------------------------------
               World Data Center for Paleoclimatology, Boulder
                                  and
                     NOAA Paleoclimatology Program
-----------------------------------------------------------------------
NOTE: PLEASE CITE CONTRIBUTORS WHEN USING THIS DATA!!!!!


NAME OF DATA SET: North American Summer PDSI Reconstructions
LAST UPDATE: 3/2005 (Addition of dai.txt, drought area index 
                     for the West, 800-2003 AD)

CONTRIBUTORS: Ed Cook, Lamont-Doherty Earth Observatory

IGBP PAGES/WDCA CONTRIBUTION SERIES NUMBER: 2004-045

SUGGESTED DATA CITATION: Cook, E.R., et al. 2004.
North American Summer PDSI Reconstructions. 
IGBP PAGES/World Data Center for Paleoclimatology 
Data Contribution Series # 2004-045.
NOAA/NGDC Paleoclimatology Program, Boulder CO, USA.


ORIGINAL REFERENCE: 
Cook, E.R., D.M. Meko, D.W. Stahle, and M.K. Cleaveland. 1999. 
Drought reconstructions for the continental United States. 
Journal of Climate, 12:1145-1162.	

ADDITIONAL REFERENCE: 
Cook, E.R., C.A. Woodhouse, C.M. Eakin, D.M. Meko and D.W. Stahle. 2004.
Long-Term Aridity Changes in the Western United States.
Science, Vol. 306, No. 5698, pp. 1015-1018, 5 November 2004.


FUNDING SOURCES:  
The drought reconstructions were developed through support from the
jointly managed NSF/NOAA ESH program through NOAA Project Award
NA06GP0450, "Collaborative research: Reconstruction of drought and
streamflow over the coterminous United States from tree rings, with
extensions into Mexico and Canada" (Principal Investigators: E.R. Cook,
U. Lall, C. Woodhouse, D.M. Meko). Additional support was provided by
NSF, Division of Atmospheric Sciences, Paleoclimate Program through
ATM 03-22403, "Development of a North American Drought Atlas"
(Principal Investigator: E.R. Cook).

GEOGRAPHIC REGION: North America
PERIOD OF RECORD: 1 BC - 2003 AD


DESCRIPTION: 
Text File Format of the Complete Grid-Point Data Matrix Files:

namerica-pdsi-recs.txt    the summer PDSI reconstructions
namerica-pdsi-ncrns.txt   the number of chronologies in each recon
namerica-pdsi-crsq.txt    the calibration period R-square
namerica-pdsi-vrsq.txt    the verification period r-square
namerica-pdsi-re.txt      the verification period RE
namerica-pdsi-ce.txt      the verification period CE
namerica-pdsi-act.txt     the actual summer PDSI data updated to
                          2003 for the US part of the grid
   
These complete files contain the information for all 286 grid-points
in one large martrix. There is a matrix for RECS, NCRNS, CRSQ, VRSQ,
RE, and CE, with the beginning year being -1 and the outer year 2003
in every case. For the ACT file, all data begin in 1900. As before,
missing values are indicated by -99.999 flags. The columns represent
the grid point and the rows represent years. The following FORTRAN
format specification will read these files correctly (i5,286f8.3).
The header on each file contains the grid point numbers.

There is also a netCDF file, NADApdsi04.nc, which contains all the summer PDSI
reconstructions. 

Also included are four additional files:

dai-map.pdf               a map that shows the locations of the
                          grid points by grid point number 
dai-namerica-grid.txt     the 286 longitude-latitude pairs in decimal
                          degrees
namerica-pdsi-stats.txt   a table of recon stats for the most highly
                          replicated grid point models. The time-
                          varying stats can be found in the complete
                          grid-point matrices.
                          
dai.txt                   Drought Area Index for the West 
                          Percent area occupied by drought (PDSI < -1) 


As is apparent, we used four statistics as measures of association
between the actual and estimated PDSI. For those who are not that
familiar with them, here is a brief description.

1)  Calibration R-SQuare (CRSQ). This statistic measures the percent
PDSI variance explained by the tree-ring chronologies at each grid point
over the 1928-1978 calibration period, based on a regression modeling
procedure described in Cook et al. (1999). As defined here, CRSQ is
equivalent to the "coefficient of multiple determination" found in
standard statistic texts. It ranges from 0 (no calibrated variance) to
1.0 (perfect agreement between instrumental PDSI and the tree-ring
estimates). The former represents complete failure to estimate PDSI
from tree rings and the latter is not plausible if the model is not
seriously over-fit. In our case here, the median (middle or 50th
percentile value) CRSQ over all 286 grid points is 0.514. This means
that approximately 1/2 of the PDSI variance is being explained by tree-
ring chronologies when viewed over the entire 286 grid point domain.
In dendroclimatology, this level of calibrated variance is considered
to be, in general, quite good.

2)  Verification R-SQuare (VRSQ). This statistic measures the percent
PDSI variance in common between actual and estimated PDSI in the
1900-1927 verification period. It is calculated as the square of the
Pearson correlation coefficient, which is a well known measure of
association between two variables. VRSQ also ranges from 0 to 1.0
(VRSQ is assigned a 0 value if the correlation is negative). Roughly
speaking, VRSQ>0.11 is statistically significant at the 1-tailed 95% level
using our 28 year verification period data. In our case, the median VRSQ
over all 286 grid points is 0.445. This drop from 0.514 in the calibration
period is expected, but relatively modest. Thus, the overall fidelity of
the reconstructions is verified well when compared with withheld PDSI
data.

3)  Verification reduction of error (RE). This statistic was originally
derived by Edward Lorenz as a test of meteorological forecast skill.
Unlike CRSQ and VRSQ, RE has a theoretical range of -infinity to 1.0.
Over the range 0-1.0, RE expresses the degree to which the estimates
over the verification period are better than "climatology", i.e. the
calibration period mean of the actual data. So, a positive RE means that
the PDSI estimates are better than just using the calibration period mean
as a reconstruction of past PDSI behavior. A negative RE is generally
interpreted as meaning that the estimates are worse than the calibration
period mean and, therefore, have no skill. The use of the calibration
period mean as the "yardstick" for assessing reconstruction skill makes
this statistic more difficult to pass than VRSQ. However, it is also less
robust, meaning that it is very sensitive to even a few bad estimates in
the verification period. Therefore, RE>0 is interpreted as evidence for
a reconstruction that contains some skill over that of climatology. In
our case, the median RE over all 286 grid points is 0.419. This is
strong evidence for meaningful reconstruction skill over the PDSI grid.

4)  Verification coefficient of efficiency (CE). This statistic comes from
the hydrology literature and is very similar to the RE. It too has a
theoretical range of -infinity to 1.0. The crucial difference is that the
CE uses the verification period mean of the withheld actual data as the
"yardstick" for assessing the skill of the estimates. This seemingly minor
difference is important because it results in the CE being even more
difficult than the RE to pass (i.e., a CE>0). Consequently, CE is never
greater than RE (see Cook et al., 1999 for why this is so) and is often
significantly smaller. In our case, the median CE over all 286 grid points
is 0.357, strongly positive but smaller than RE as expected. This result
is again strong evidence for meaningful reconstruction skill over the
PDSI grid.

Overall, the North American PDSI grid is very well calibrated and
verified. However, the calibration/verification statistics typically
weaken back in time at each grid point. This occurs because increasingly
longer, and smaller, subsets of chronologies are used to extend the
reconstructions back as far as possible. The calibration and verification
statistics described thus far are for grid point models that are based on
the largest number of (and shortest common length) chronologies. Each time
a longer (and smaller) subset was used to extend the PDSI reconstruction
farther back in time at each grid point, a new set of calibration and
verification statistics was produced. This resulted in a time-varying set
of statistics for each reconstruction. This being the case, is there a
hard-and-fast rule for determining when the reliability of a PDSI
reconstructions becomes too poor to use? The answer is "No!" The chosen
"rule" will depend on how much uncertainty is acceptable for each
individual who uses these reconstructions. Regardless, one must
always keep in mind the changing uncertainty in each PDSI reconstruction
when using it for whatever purposes. This caveat is especially true for
the weakly reconstructed areas of Canada and Mexico.

Any questions concerning these PDSI reconstructions should be directed to
Ed Cook at drdendro@ldeo.columbia.edu.

