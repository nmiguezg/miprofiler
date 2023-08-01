import joblib
from sklearn import metrics
from modaresi.preprocessor import Preprocessor
from train import load_train_and_test_sets

_, X, _, _,y_test, _ = load_train_and_test_sets("../../datasets/2016/Training", "../../datasets/2016/Test")
Xt = Preprocessor('gender').preproccess(X)
with open("models/modaresi/gender.joblib", 'rb') as file:
    gender_model = joblib.load(file)
    
y_predicted = gender_model.predict(Xt)

print(f"Classification report:\n%s", metrics.classification_report(y_test, y_predicted))

# Log the confusion matrix
confusion_matrix = metrics.confusion_matrix(y_test, y_predicted)
print(f"Confusion matrix:\n%s", confusion_matrix)