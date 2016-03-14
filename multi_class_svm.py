from scipy import interp
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from sklearn import cross_validation
#from sklearn.cross_validation import StratifiedKFold
#from sklearn.cross_validation import cross_val_predict
from sklearn import datasets
from sklearn.metrics import precision_recall_fscore_support,precision_score,recall_score,roc_curve,auc,confusion_matrix
#iris = datasets.load_iris()
#X = iris.data
#y = iris.target
#X, y = X[y != 2], y[y != 2]

file=open('C:\Users\Srikar\Dropbox\Research\ICIS 2014\Paper Extension\Data\Final_Counts\scripts\Comprehensive_article_characteristics_binary.txt','r')
data=[]
data=[[float(digit) for digit in line.split(';')] for line in file]
data=np.array(data)
y=data[:,0]
X=data[:,1:]
print y
print "Data Loaded"
cv = cross_validation.StratifiedKFold(y, n_folds=10)
classifier = svm.SVC(kernel='rbf',  probability=True, gamma=0.7, C=1)
scores = cross_validation.cross_val_score(classifier,X,y, cv=10)
predicted = cross_validation.cross_val_predict(classifier, X,y, cv=10)
print ("Predicted Values:",predicted)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print (precision_recall_fscore_support(y, predicted, average='binary'))
print (confusion_matrix(y, predicted))
mean_tpr = 0.0
mean_fpr = np.linspace(0, 1, 100)
all_tpr = []
for i, (train, test) in enumerate(cv):
    probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
    
    # Compute ROC curve and area the curve
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    mean_tpr += interp(mean_fpr, fpr, tpr)
    mean_tpr[0] = 0.0
    roc_auc = auc(fpr, tpr)
    #plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))

plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')

mean_tpr /= len(cv)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
plt.plot(mean_fpr, mean_tpr, 'k--',
         label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
