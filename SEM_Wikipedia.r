install.packages("lavaan",repos="http://cran.rstudio.com/")
library("lavaan")
mydata <- read.table("All_Characteristics_Comprehensive_FD.txt", header=TRUE, sep=";",row.names=NULL)
model<-"Edit_Count~Thread_Count+Comment_Count+Contributor_Count_disc+Anonymous_Contributor_Count_disc+Discussion_Period+Avg_Depth+Skewness_Depth+Avg_ReadingComplexity+Skewness_ReadingComplexity+Avg_TimeGap+Skewness_TimeGap+Gini+Acknowledgement+Others+References+Images+Format+Appreciation+Summary+Suggestion+Clarification+mean_pos+median_pos+skewness_pos+mean_neg+median_neg+skewness_neg\nFunctional_Diversity~Thread_Count+Comment_Count+Contributor_Count_disc+Anonymous_Contributor_Count_disc+Discussion_Period+Avg_Depth+Skewness_Depth+Avg_ReadingComplexity+Skewness_ReadingComplexity+Avg_TimeGap+Skewness_TimeGap+Gini+Acknowledgement+Others+References+Images+Format+Appreciation+Summary+Suggestion+Clarification+mean_pos+median_pos+skewness_pos+mean_neg+median_neg+skewness_neg\nGrade~Functional_Diversity+Edit_Count"
fit<-sem(model,data=mydata,ordered=c("Grade"))
summary(fit)
####Exploratory Factor Analysis
cor_vars<-c("Thread_Count","Comment_Count","Contributor_Count","Anonymous_Contributor_Count","Discussion_Period","Avg_Depth","Skewness_Depth","Skewness_ReadingComplexity","Avg_TimeGap","Gini","Acknowledgement","Others","References","Images_Multimedia","Format","Summary","Suggestion","Clarification","mean_pos","skewness_pos")
cor_data<-mydata[cor_vars]
cor_matrix<-cor(cor_data)
ev <- eigen(cor_matrix) # get eigenvalues
library(nFactors)
ap <- parallel(subject=nrow(cor_data),var=ncol(cor_data),rep=100,cent=.05)
nS <- nScree(x=ev$values, aparallel=ap$eigen$qevpea)
plotnScree(nS)
#
fit <- factanal(cor_data, 5, rotation="varimax")
print(fit, digits=2, cutoff=.65, sort=TRUE)
# plot factor 1 by factor 2 
load <- fit$loadings[,1:2] 
plot(load,type="n") # set up plot 
text(load,labels=names(cor_data),cex=.7) # add variable names
#PCA
library(FactoMineR)
result <- PCA(cor_data) # graphs generated automatically

#latent variable modeling
model <- '
   # latent variables
     Factor1 =~ Thread_Count+Comment_Count+Summary+Suggestion+Clarification+skewness_pos
     Factor2 =~ Acknowledgement+Others+References
     Factor3 =~ Contributor_Count+Anonymous_Contributor_Count 
	 Factor4 =~ Images_Multimedia+Format
	 
   # regressions
     Edit_Count ~ Factor1+Factor2+Factor3+Factor4
     Functional_Diversity ~ Factor1+Factor2+Factor3+Factor4
	 Grade ~ Functional_Diversity + Edit_Count'
fit <- sem(model, data=mydata,ordered=c("Grade"))
summary(fit)

###Now for 5 factors
model <- '
   # latent variables
     Factor1 =~ Thread_Count+Comment_Count+Summary+Suggestion+Clarification+skewness_pos+skewness_neg
     Factor2 =~ Acknowledgement+Others+References
     Factor3 =~ Images_Multimedia+Format+Appreciation
	 Factor4 =~ Contributor_Count+Anonymous_Contributor_Count
	 Factor5 =~ Discussion_Period + Gini
	 
   # regressions
     Edit_Count ~ Factor1 + Factor2 + Factor3 + Factor4 + Factor5
     Functional_Diversity ~ Factor1 + Factor2 + Factor3 + Factor4 + Factor5
	 Grade ~ Functional_Diversity + Edit_Count'
fit <- sem(model, data=mydata,ordered=c("Grade"))
summary(fit)

###Now for 6 factors
model <- '
   # latent variables
     Factor1 =~ Thread_Count+Comment_Count+Summary+Suggestion+Clarification+skewness_pos+skewness_neg
     Factor2 =~ Acknowledgement+Others+References
     Factor3 =~ Images_Multimedia+Format+Appreciation
	 Factor4 =~ Contributor_Count+Anonymous_Contributor_Count
	 Factor5 =~ Gini 
   # regressions
     Edit_Count ~ Factor1 + Factor2 + Factor3 + Factor4 + Factor5
     Functional_Diversity ~ Factor1 + Factor2 + Factor3 + Factor4 + Factor5
	 Grade ~ Functional_Diversity + Edit_Count'
fit <- sem(model, data=mydata,ordered=c("Grade"))
summary(fit)
