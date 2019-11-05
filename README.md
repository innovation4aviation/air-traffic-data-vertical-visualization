# Trajectory-Data-Analysis
This project is created to analyze the air traffic data in one FIR during one specific day(24h). The analysis of trajectory information includes two parts: Vertical visualization (flight distribution along the altitude) and trajectory clustering (a coarse one only concentrating on the overflights).
ADS-B data of three consecutive days is used and since the format of data file may vary, the data processing and filtering method (regular expression) adopted here may not be applicable in some cases. More detailed explanation can be found in corresponding program comments.
Please make sure the path name is changed when read/write files.
