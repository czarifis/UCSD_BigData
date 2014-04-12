
# Big Data Analytics
## Regression notebook (from Stanford)
 http://nbviewer.ipython.org/github/jbpoline/bayfmri/blob/master/notebooks/005-Simple-Linear-Regression.ipynb
 

- Let's assume that we have samples of weather data from throughout the year and we try to use a set of curves to reprsent the initial data. If the curve's function is bi then f(t) = Σ (ai*bi(t))
	
- Other methods: 
	-	Bias: systematic error we had the original function, we added noise and then we got the estimation (what if we took the average?!) The initial data and the estimation is overlap perfectly so it is unbiased. If we had uniform noise then we would have bias (they don't overalp perfectly!) We always have a systematic error!!
		
	-	Variance: The variance is small in the middle because if we take these functions they are zero in the middle.
		
	- 	There is a trade of between the Bias and the flunctuation (variance) so that leaves us to the ** Ridge Regression **. First part of the equation is the sum of square error (?) and the second is the shrinkage. If you bring shirnkage to zero you just get the regular mean square, The estimator might not be entirely correct so I bring that shrinkage down to zero (see the graph it's pulled towards zero so it's not gonna have less bias but it's gonna have less variance (as we can see on the next figure))
	-	There are various methods that tell you that even though the explicit dimension of the data is huge so they would be useless we can take advantage of the internal regularity. So if a smaller set of the dimentions can explain a big percentage of the data then we basically have a significantly smaller set of dimensions that get used.
		
	
	
- sklearn (houses - income prediction)

##By Next Tuesday I should push the data on github for the weather data and eigan vector…


