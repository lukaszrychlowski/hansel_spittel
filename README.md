# compression_test
Compression tests of alloys, performed at elevated temperatures and varying strain rates, allow for mathematical description of materials rheological behavior by derivation of Hansel-Spittel equation coefficients. 

Challenge lies in complexicity of the formula - with 9 constant coeficents to be derived in a function with variable temperature, strain, strain rate and stress. Since alloys tested exhibit viscoplastic behavior during strain the equation is simplified and only 6 coefficients are to be estimated.

Brute force approach is used - set of constants is randomized in a loop and fitted to the equation. Estimated stress level is calculated for given strain rate and temperature and compared to the experimental data. 

Ref:

https://engineering.stackexchange.com/questions/36218/hansel-spittel-equation-parameter-determination


<img width="1682" alt="bez nazwy" src="https://user-images.githubusercontent.com/90209348/161439559-e3057586-1184-4432-9474-38028663d625.png">

![hansel](https://user-images.githubusercontent.com/90209348/162443121-4401f8ce-78f0-441f-b3e9-19dc90499fa3.png)


