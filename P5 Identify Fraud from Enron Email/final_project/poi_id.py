#!/usr/bin/python

import sys
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import pprint
from time import time
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data



# Define function to draw a scatter plot:
def draw_plot(data_dict, features):
    data = featureFormat(data_dict, features)
    for point in data:
        x = point[0]
        y = point[1]
        plt.scatter(x, y)
    plt.xlabel(features[0])
    plt.ylabel(features[1])
    plt.show()

# Function for explore dataset
def data_exloration(data_dict, features):
    total_data_num = len(data_dict)
    total_feature_num = len(data_dict[data_dict.keys()[0]])
    total_poi_num = 0

    for elem in data_dict.values():
        if elem['poi'] == 1:
            total_poi_num += 1

    print "Total Data Numbers: ", total_data_num
    print "Total Feature Numbers: ", total_feature_num
    print "POIs: ", total_poi_num
    print "\nInsider's Name:\n"
    pprint.pprint(data_dict.keys())

    draw_plot(data_dict, features)

    for name, value in data_dict.items():
         if value['salary'] != 'NaN' and value['salary'] > 10000000:
             print "\nExtreme outlier:", name


def remove_outliner(data_dict, features):
    data_dict.pop("TOTAL", 0)
    data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)

    # draw a scatterplot after outliner removed
    draw_plot(data_dict, features)

def grid_search(my_dataset, features_list, param_grid, clf, folds=100, do_imp=False):
    t0 = time()
    ### Task 4-1: Scale features:
    # Imputation for completing missing values
    imp = Imputer(missing_values=0, strategy='median', axis=0)

    # Preprocessing features by MinMaxScaler:
    scaler = MinMaxScaler()

    ### Task 4-2: Feature Selection
    # Use KBest to find the best features:
    selector = SelectKBest()

    if do_imp:
        pipeline = Pipeline([("imp", imp), ("scaler", scaler), ("f_select", selector), ("clf", clf)])
    else:
        pipeline = Pipeline([("scaler", scaler), ("f_select", selector), ("clf", clf)])

    grid_search = GridSearchCV(pipeline, param_grid, scoring='f1')

    test_classifier(grid_search, my_dataset, features_list, folds=folds)
    print "\n", grid_search.best_estimator_
    print "done in %0.3fs" % (time() - t0)

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
##features_list = ['poi','salary'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers

## Task 2-1: Data Exploration

features = ["salary", "bonus"]
data_exloration(data_dict, features)


### Task 2-2: Remove Outliners

# Turn out that "TOTAL" row in the dataset has extreme value, just remove it,
# and also remove the  "THE TRAVEL AGENCY IN THE PARK" from dataset.

remove_outliner(data_dict, features)


### Task 2-3: are there features with many missing values?

enron_df = pd.DataFrame(data_dict).transpose()
print "\nFeatures Statistics:\n", enron_df.describe().transpose()

        #                           count unique    top freq
        # bonus                       144     41    NaN   63
        # deferral_payments           144     39    NaN  106
        # deferred_income             144     44    NaN   96
        # director_fees               144     17    NaN  128
        # email_address               144    112    NaN   33
        # exercised_stock_options     144    101    NaN   43
        # expenses                    144     94    NaN   50
        # from_messages               144     65    NaN   58
        # from_poi_to_this_person     144     58    NaN   58
        # from_this_person_to_poi     144     42    NaN   58
        # loan_advances               144      4    NaN  141
        # long_term_incentive         144     52    NaN   79
        # other                       144     91    NaN   53
        # poi                         144      2  False  126
        # restricted_stock            144     97    NaN   35
        # restricted_stock_deferred   144     18    NaN  127
        # salary                      144     94    NaN   50
        # shared_receipt_with_poi     144     84    NaN   58
        # to_messages                 144     87    NaN   58
        # total_payments              144    124    NaN   21
        # total_stock_value           144    124    NaN   19

## Turn out the following features missing many values:
##   deferral_payments
##   director_fees
##   loan_advances
##   restricted_stock_deferred


### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

### Task 3-1: Create new features

my_dataset = data_dict

for name in my_dataset:
    # Create a new financial feature: 'total_value'
    # 'total_value' = ('total_payments' + 'total_stock_value')
    insider = my_dataset[name]
    total_payments = insider['total_payments']
    total_stock = insider['total_stock_value']

    if total_payments != 'NaN' and total_stock != 'NaN':
       insider['total_value'] = total_payments + total_stock
    else:
        insider['total_value'] = 'NaN'

# create new email features: 'poi_ratio', from_poi_to_person_ratio, from_person_to_poi_ratio
    poi_to_person = insider['from_poi_to_this_person']
    person_to_poi = insider['from_this_person_to_poi']
    from_messages = insider['from_messages']
    to_messages = insider['to_messages']
    if poi_to_person != 'NaN' and person_to_poi != 'NaN' and \
       from_messages != 'NaN' and to_messages != 'NaN':

        insider['poi_ratio'] = float(poi_to_person + person_to_poi) / \
                               float(from_messages + to_messages)
        insider['poi_to_person_ratio'] = float(poi_to_person) / float(from_messages)
        insider['person_to_poi_ratio'] = float(person_to_poi) / float(to_messages)
    else:
        insider['poi_ratio'] = 'NaN'
        insider['poi_to_person_ratio'] = 'NaN'
        insider['person_to_poi_ratio'] = 'NaN'

### Task 3-2: Extract features and labels from dataset for local testing

all_features  = my_dataset[my_dataset.keys()[0]].keys()
all_features.remove('poi')
all_features.remove('email_address')
all_features.remove('loan_advances')
all_features = ['poi'] + all_features


### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

### Task 4-3: Test a variety of classifiers

### Task 4-3-1: DecisionTree Classifier:

#clf = tree.DecisionTreeClassifier()
#param_grid = dict(f_select__k=[3, 6, 9, 12])

#print "\nTrain Decision Tree Classifier... "
# print "\nWith Imputation..."
# basic_grid_search(my_dataset, all_features, param_grid, clf, do_imp=True)
# print "\nWithout Imputation..."
#grid_search(my_dataset, all_features, param_grid, clf)

## Imputation:
    # Accuracy: 0.80667
    # Precision: 0.29167
    # Recall: 0.31500
## Parameter:
    #SelectKBest: k = 3

## without imputation :
    # Accuracy: 0.79733
    # Precision: 0.25701
    # Recall: 0.27500
## Parameter:
    #SelectKBest: k = 6

### Task 4-3-2: Train Naive Bayes Classifier

#clf = GaussianNB()
#param_grid = dict(f_select__k=[3, 6, 9, 12])

#print "\nNaive Bayes Classifier:"
# print "\nWith Imputation..."
# basic_grid_search(my_dataset, all_features, param_grid, clf, do_imp=True)
#print "\nWithout Imputation..."
#grid_search(my_dataset, all_features, param_grid, clf)

## Imputation :
    # Accuracy: 0.84467
    # Precision: 0.40351
    # Recall: 0.34500
## Parameter:
    #SelectKBest: k = 3

## without imputation:
    # Accuracy: 0.84333
    # Precision: 0.39394
    # Recall: 0.32500
## Parameter:
    #SelectKBest: k = 3

### Task 4-3-3: Train KNeighbors Classifier

# clf = KNeighborsClassifier()
#
# param_grid = dict(f_select__k=[3, 6, 9, 12])
#
# print "\nKNeighbors Classifier:"
# print "\nWith Imputation..."
# basic_grid_search(my_dataset, all_features, param_grid, clf, do_imp=True)
# print "\nWithout Imputation..."
# grid_search(my_dataset, all_features, param_grid, clf)

## With imputation:
    # Accuracy: 0.86733
    # Precision: 0.50769
    # Recall: 0.16500
## Parameter:
    #SelectKBest: k = 3

## without imputation:
    # Accuracy: 0.87933
    # Precision: 0.66102
    # Recall: 0.19500
## Parameter:
    #SelectKBest: k = 12

### Task 4-3-4: Train AdaBoost Classifier

#clf = AdaBoostClassifier()
#param_grid = dict(f_select__k=[3, 6, 9, 12])

# print "\nAdaBoost Classifier:"
# print "\nWith Imputation..."
# basic_grid_search(my_dataset, all_features, param_grid, clf, do_imp=True)
#print "\nWithout Imputation..."
#grid_search(my_dataset, all_features, param_grid, clf)

## Imputation:
    # Accuracy: 0.83267
    # Precision: 0.34545
    # Recall: 0.28500
## Parameter:
    #SelectKBest: k = 12

## without imputation:
    # Accuracy: 0.84067
    # Precision: 0.37255
    # Recall: 0.28500
## Parameter:
    #SelectKBest: k = 9

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

#Task 5-1: Tune AdaBoost and Naive Bayes classifiers

#Task 5-1-1: AdaBoost Classifier

# clf = AdaBoostClassifier()
# param_grid = dict(f_select__k=[6, 9, 12],
#                   f_select__score_func=[f_classif, chi2],
#                   clf__n_estimators=[20, 50, 100],
#                   clf__algorithm=["SAMME", "SAMME.R"],
#                   clf__learning_rate=[.3, .5, .7, 1, 1.2])
#
#
# print "\nTune AdaBoost Classifier..."
# grid_search(my_dataset, all_features, param_grid, clf)
## Result:
    # Accuracy: 0.85733
    # Precision: 0.43269
    # Recall: 0.22500
    # F1: 0.29605
    # F2: 0.24899
## Parameter:
    # SelectKBest: k = 9, score_func = chi2
    # n_estimators = 50,
    # algorithm= "SAMME.R"
    # learning_rate= 0.3

# done in 7007.551s


#Task 5-1-2: Tune Naive Bayers Classifier


# clf = GaussianNB()
#
# param_grid = dict(f_select__k=range(3, 16),
#                   f_select__score_func=[chi2, f_classif])
#
# print "\nTune Naive Bayes Classifier..."
# grid_search(my_dataset, all_features, param_grid, clf, folds=1000, do_imp=True)
# grid_search(my_dataset, all_features, param_grid, clf, folds=1000)

## With Imputation:
    # Accuracy: 0.84940
    # Precision: 0.40609
    # Recall: 0.28000
    # F1: 0.33146
    # F2: 0.29854
## Parameter:
    #SelectKBest: k = 4, score_func = chi2


## Without Imputation:
    # Accuracy: 0.83740
    # Precision: 0.36737
    # Recall: 0.30400
    # F1: 0.33269
    # F2: 0.31486
## Parameter:
    #SelectKBest: k = 4, score_func = chi2


# Task 5-2: Choose Naive Bayes as my final Classifier

# Get three best features from SelectKBest
data = featureFormat(my_dataset, all_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

fs = Pipeline([("scaler", MinMaxScaler()), ("f_select", SelectKBest(chi2))])
fs.fit(features, labels)

# #Get features' scores, sorted and saved into KB_scores
KB_scores = fs.named_steps["f_select"].scores_
KB_scores = zip(all_features[1:], KB_scores)
KB_scores = sorted(KB_scores, key=lambda x:x[1], reverse=True)
print "\nFeatures Scores:\n"
pprint.pprint(KB_scores)

all_features_sorted = [list(k) for k in zip(*KB_scores)][0]

features_list = ['poi'] + all_features_sorted[:4]
print "\n Top 4 features selected for final algorithm"
print "\n", features_list
## Fearures_list: ['poi', 'exercised_stock_options', 'total_stock_value', 'bonus', 'total_value']


clf = GaussianNB()

test_classifier(clf, my_dataset, features_list)

## Final result:
    # Accuracy: 0.85200
    # Precision: 0.52914
    # Recall: 0.34500
    # F1: 0.41768
    # F2: 0.37081


# ### Task 6: Dump your classifier, dataset, and features_list so anyone can
# ### check your results. You do not need to change anything below, but make sure
# ### that the version of poi_id.py that you submit can be run on its own and
# ### generates the necessary .pkl files for validating your results.
#
dump_classifier_and_data(clf, my_dataset, features_list)