## Example application of hypothesis testing

* Null hypothesis is that it doesn't matter. The fatality probability is 1% regardless of wearing a seatbelt or not.
  * We have the mean and standard deviation (=3.16). p value is the Probability that what you saw happened by chance given that the null-hypothesis is in fact true. (In the medical field 5% is the probability that an event would have and it would have been acceptable. )
  
* (reminder!)Correlation is the normalized version of the covariance!


</br>

* Pearson correlation. null hyp: X,Y are jointly normal and uncorrelated. Suppose I took N samples from this joint distribution and calculated the correlation r (this r is supposed to have mean=0 since they are uncorrelated, but we want to see how much it flunctuated). We check if this thing can be represented by the student t distribution (is like a normal distribution but it is affected by the number of degrees of freedom (=number of samples). The tail of this thing is the p-value, it tells you which is the chance that this will happen randomly)
* Spearman correlation. different "kind" of correlation. We take all the X values and replace them by their order (check profs notes). These numbers go from 0 to the number of values we have . If we have outliers they will be put near the other set of values.

###Multiple hypothesis test

We have many areas that might reject the null hypothesis. Each one has a p-value of 1% but we don't know if these areas overlap. (check out bonferroni correction) 