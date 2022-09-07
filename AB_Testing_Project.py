#Task 1: Preparing and Analyzing Data

#Step 1: Read the dataset ab testing data.xlsx consisting of control and test group data. Assign control and test group data to separate variables.
#!pip install openpyxl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from scipy.stats import shapiro,levene,ttest_ind
pd.set_option("display.max_columns",None)
pd.set_option("display.float_format", lambda x:"%.4f" % x)

A_=pd.read_excel("....",sheet_name="Control Group") #The dataset is not shared because it is private.
B_=pd.read_excel("......",sheet_name="Test Group") #The dataset is not shared because it is private.

#Step 2: Analyze control and test group data.
def check_df(dataframe,head=5):
    print("################### Shape #################")
    print(dataframe.shape)
    print("#################### Types ################")
    print(dataframe.dtypes)
    print("#################### Head #################")
    print(dataframe.head())
    print("################## Tail ###################")
    print(dataframe.tail())
    print("################## NA ######################")
    print(dataframe.isnull().sum())
    print("###################### Quantiles ############")
    print(dataframe.quantile([0,0.05,0.50,0.95,0.99,1]).T)
check_df(A_)
check_df(B_)

# Since we are going to combine and organize datasets, let's name them clearly.
A_.columns = [i+"_A" for i in A_.columns]
B_.columns = [i + "_B" for i in B_.columns]

#Step 3: After the analysis process, combine the control and test group data using the concat method.
df=pd.concat([A_,B_],axis=1,ignore_index=False)
df.head()

#Task 2: Defining the Hypothesis of A/B Testing

# Step 1: Define the hypothesis.

# H0 : M1 = M2 (There is no difference between the control group and test group purchasing averages.)
# H1 : M1!= M2 (There is a difference between the purchasing averages of the control group and the test group.)

#Step 2: Analyze the purchase averages for the control and test group.
df["Purchase_A"].mean()
df["Purchase_B"].mean()

#Task 3: Performing Hypothesis Testing
# Step 1: Check the assumptions before testing the hypothesis. These are Assumption of Normality and Homogeneity of Variance.
# H0: The assumption of normal distribution is provided.
# H1:Normal distribution assumption not provided.
# p < 0.05 H0 rejected
# p > 0.05 H0 not rejected
# Is the assumption of normality according to the test result provided for the control and test groups ?
# Interpret the p-values obtained.


#A)Normality Assumption

test_stat,pvalue=shapiro(df["Purchase_A"])
print("Test Stat = %.4f,p-value=%.4f" % (test_stat,pvalue))
# p-value=0.5891
# HO cannot be rejected. That is, the assumption of normality is provided for the control group..
test_stat,pvalue=shapiro(df["Purchase_B"])
print("Test Stat = %.4f,p-value=%.4f" % (test_stat,pvalue))
## Test Stat = 0.9589, p-value = 0.1541
## P-VALUE > ALFA = 0.05 for H0 cannot be rejected. THE ASSUMPTION OF NORMAL DISTRIBUTION IS PROVIDED FOR THE TEST GROUP.


#B)Variance Homogeneity.

# H0: Variances are homogeneous.
# H1: Variances Are Not Homogeneous.
# p < 0.05 H0 rejected
# p > 0.05 H0 not recejted
# Test whether the homogeneity of variance is provided for the control and test groups over the Purchase variable.
# Is the assumption of normality provided according to the test result? Interpret the p-values obtained.


test_stat,pvalue=levene(df["Purchase_A"],df["Purchase_B"])
print("Test Stat = %.4f,p-value=%.4f" % (test_stat,pvalue))

# p-value=0.1083
# HO not rejected. The values of the Control and Test groups provide the assumption of variance homogeneity..
# Variances are Homogeneous.


#Step 2: Select the appropriate test according to the Normality Assumption and Variance Homogeneity results.
# Since assumptions are provided, independent two-sample t-test (parametric test) is performed.
# H0: M1 = M2 (There is no statistically significant difference between the purchasing averages of the control group and test group.)
# H1: M1 != M2 (There is a statistically significant difference between the purchasing averages of the control group and test group.)

test_stat,pvalue=ttest_ind(df["Purchase_A"],df["Purchase_B"])
print("Test Stat = %.4f,p-value=%.4f" % (test_stat,pvalue))

#Step 3: Considering the p_value obtained as a result of the test, interpret whether there is a statistically significant difference between the control and test group purchasing averages.
# p-value=0.3493
# HO not recejted. There is no statistically significant difference between the purchasing averages of the control and test groups.


