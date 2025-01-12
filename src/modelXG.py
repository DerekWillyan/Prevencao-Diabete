from matplotlib import pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier, plot_tree
from joblib import dump

# Carregar os dados
data = pd.read_csv('diabetes_prediction_dataset.csv')  # Substitua pelo nome do arquivo

# Separar recursos e rótulo
X = data.drop(columns=['diabetes'])
y = data['diabetes']

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Aplicar o SMOTE na divisão de treino
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# Verificar a distribuição após o SMOTE
print("Distribuição de classes antes do SMOTE:")
print(y_train.value_counts())
print("\nDistribuição de classes após o SMOTE:")
print(pd.Series(y_train_smote).value_counts())

# Treinar o modelo XGBoost
model = XGBClassifier(
    n_estimators=248,
    max_depth=5,
    learning_rate=0.2,
    subsample=1.0,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train_smote, y_train_smote)

# Fazer previsões
y_pred = model.predict(X_test)

# Avaliar o modelo
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["No Diabete", "Diabete"]))

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

dump(model, 'xgboost_diabetes_model.joblib')
print("Modelo salvo com sucesso!")

# Visualizar a primeira árvore (índice 0)
plt.figure(figsize=(30, 10))  # Ajustar o tamanho da figura
plot_tree(model, num_trees=0)  # Altere 'num_trees' para visualizar outras árvores
plt.title("Tree 0")
plt.show()

# Salvar o gráfico em um arquivo
plt.savefig('tree_visualization.jpeg', dpi=300)