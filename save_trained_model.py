
# Script para guardar el modelo Random Forest entrenado y el scaler.
# Con df_reduced, X_train, y_train disponibles.

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# Este código debe ejecutarse después de procesar los datos en el notebook principal.

# Preparación de datos
# Separar características y objetivo
X = df_reduced.drop("stress", axis=1)
y = df_reduced["stress"]

# Escalar características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir train/test 
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Entrenar el modelo Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# Guardar el modelo y el scaler
from stress_model import save_model
save_model(rf_model, scaler, 'stress_rf_model.pkl', 'scaler.pkl')

print("Modelo Random Forest entrenado y guardado exitosamente.")