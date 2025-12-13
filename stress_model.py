# Código para guardar, cargar y hacer inferencia con el modelo de Random Forest.

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Función para guardar el modelo entrenado y el scaler
def save_model(model, scaler, model_path='stress_rf_model.pkl', scaler_path='scaler.pkl'):
    """
    Guarda el modelo Random Forest entrenado y el scaler en archivos separados.
    Parámetros:
    - model: Modelo RandomForestClassifier entrenado
    - scaler: StandardScaler ajustado
    - model_path: Ruta donde guardar el modelo (por defecto 'stress_rf_model.pkl')
    - scaler_path: Ruta donde guardar el scaler (por defecto 'scaler.pkl')
    """
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Modelo guardado en {model_path}")
    print(f"Scaler guardado en {scaler_path}")

# Función para cargar el modelo y el scaler
def load_model(model_path='stress_rf_model.pkl', scaler_path='scaler.pkl'):
    """
    Carga el modelo Random Forest y el scaler desde archivos.

    Parámetros:
    - model_path: Ruta del archivo del modelo
    - scaler_path: Ruta del archivo del scaler

    Retorna:
    - model: Modelo RandomForestClassifier cargado
    - scaler: StandardScaler cargado
    """
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    print(f"Modelo cargado desde {model_path}")
    print(f"Scaler cargado desde {scaler_path}")
    return model, scaler

# Función de inferencia
def predict_stress(acc_x, acc_y, acc_z, bvp, eda, temp, model, scaler):
    """
    Realiza la predicción de estrés basada en los valores de los sensores.
    Parámetros:
    - acc_x, acc_y, acc_z: Componentes del acelerómetro
    - bvp: Señal de volumen de pulso sanguíneo
    - eda: Actividad electrodérmica
    - temp: Temperatura
    - model: Modelo RandomForestClassifier cargado
    - scaler: StandardScaler cargado
    Imprime:
    - stress = 1 (estrés) o stress = 0 (no estrés)
    """
    features = np.array([[acc_x, acc_y, acc_z, bvp, eda, temp]])

    # Escalar las características
    features_scaled = scaler.transform(features)

    # Hacer la predicción
    prediction = model.predict(features_scaled)[0]

    # Imprimir el resultado
    print(f"stress = {int(prediction)}")