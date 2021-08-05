import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

global Results
Results = ["WorkDesk", "Fridge", "Bed", "Main-Entrance", "Living", "Sofa", "Balcony", "Master-Entrance"]

# iterations: 1000
# accuracy: 89%
# Test SIZE: 75%
# random_state: 12
class MLP_model_WRK_FRD_BED_1000_89:
    def __init__(self):
        df = pd.read_csv('dataset/combined_csv.csv')
        dataset = df.values
        X = dataset[:,0:3]
        Y = dataset[:, 3]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.75, random_state = 12)

        self.model = MLPClassifier(random_state=1, max_iter=1000).fit(X_train, Y_train)

        print(self.model.score(X_test, Y_test))

    def estimate(self, lis):
        if len(lis) == 3:
            index = self.model.predict([lis])
            return Results[int(index) - 1]

# iterations: 1000
# accuracy: 91%
# Test SIZE: 65%
# random_state: 1
class MLP_model_WRK_FRD_BED_ENTR_LIV_1000_91:

    def __init__(self):
        df = pd.read_csv('dataset/combined_csv_5.csv')
        dataset = df.values
        X = dataset[:,0:3]
        Y = dataset[:, 3]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.65, random_state = 1)

        self.model = MLPClassifier(random_state=1, max_iter=1000).fit(X_train, Y_train)

        print(self.model.score(X_test, Y_test))

    def estimate(self, lis):
        if len(lis) == 3:
            index = self.model.predict([lis])
            return Results[int(index) - 1]

# iterations: 1000
# accuracy: 90%
# Test SIZE: 75%
# random_state: 12
class MLP_model_WRK_FRD_BED_ENTR_LIV_SOF_BAL_MAS_1000_90:

    def __init__(self):
        df = pd.read_csv('dataset/combined_csv_8.csv')
        dataset = df.values
        X = dataset[:,0:3]
        Y = dataset[:, 3]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.75, random_state = 12)

        self.model = MLPClassifier(random_state=13, max_iter=1000).fit(X_train, Y_train)

        print(self.model.score(X_test, Y_test))

    def estimate(self, lis):
        if len(lis) == 3:
            index = self.model.predict([lis])
            return Results[int(index) - 1]
