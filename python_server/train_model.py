import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load data from CSV files
# TODO change this to actual files from the server
walking_data = pd.read_csv('training_data/data_2023-05-20_22-30-53_Walking.csv')
running_data = pd.read_csv('training_data/data_2023-05-20_22-38-15_Running.csv')
cycling_data = pd.read_csv('training_data/data_2023-05-20_22-45-57_Cycling.csv')


# Concatenate the datasets into a single DataFrame
data = pd.concat([walking_data, running_data, cycling_data], ignore_index=True)

# Split the data into training and testing sets
X = data.drop('label', axis=1) # vsi razn lable
Y = data['label'] # sam label
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Train the RandomForestClassifier
classifier = RandomForestClassifier()
classifier.fit(X_train, y_train) 

# Make predictions on the test set
print('Making predictions on the test set...')
print(X_test)
y_pred = classifier.predict(X_test)

# Evaluate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Save the trained model
joblib.dump(classifier, 'model.joblib')

print('Trained model saved as model.joblib')

#print one prediction
print(classifier.predict(X_test[0]))
# print(y_test.iloc[[0]])
