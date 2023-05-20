import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load data from CSV files
walking_data = pd.read_csv('walking_data.csv')
running_data = pd.read_csv('running_data.csv')
cycling_data = pd.read_csv('cycling_data.csv')

# # Assign labels to the datasets
# walking_data['label'] = 'walking'
# running_data['label'] = 'running'
# cycling_data['label'] = 'cycling'
# TODO will the lable be in the data sent by the client? if so no need to add it here 
# maybe replace lables with numbers? 0,1,2?s

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
y_pred = classifier.predict(X_test)

# Evaluate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Save the trained model
joblib.dump(classifier, 'model.joblib')

print('Trained model saved as model.joblib')
