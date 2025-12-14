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
    - Ruta donde guardar el modelo ('stress_rf_model.pkl')
    - Ruta donde guardar el scaler ('scaler.pkl')
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
def predict_stress(acc, bvp, temp, eda, model, scaler):
    """
    Realiza la predicción de estrés basada en los valores de los sensores.
    Parámetros:
    - acc: Magnitud del acelerómetro (sqrt(acc_x^2 + acc_y^2 + acc_z^2))
    - bvp: Señal de volumen de pulso sanguíneo
    - temp: Temperatura
    - eda: Actividad electrodérmica
    - model: Modelo RandomForestClassifier cargado
    - scaler: StandardScaler cargado

    Imprime:
    - stress = 1 (estrés) o stress = 0 (no estrés)
    """
    features = np.array([[acc, bvp, temp, eda]])

    # Escalar las características
    features_scaled = scaler.transform(features)

    # Hacer la predicción
    prediction = model.predict(features_scaled)[0]

    # Imprimir el resultado
    print(f"stress = {int(prediction)}")


if __name__ == "__main__":
    # Cargar el modelo y el scaler
    model, scaler = load_model()

    # Valores de entrada simulados (ejemplo)
    acc = 1.0  # Magnitud del acelerómetro
    bvp = 0.5  # Señal BVP
    temp = 36.5  # Temperatura
    eda = 0.2  # Actividad electrodérmica

    # Realizar la predicción
    predict_stress(acc, bvp, temp, eda, model, scaler)