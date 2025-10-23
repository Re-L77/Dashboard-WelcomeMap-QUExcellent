#!/usr/bin/env python
"""Script de diagnóstico para el modelo ML."""
import joblib
import numpy as np

# Cargar modelos
lgb_model = joblib.load('app/models/lgb_model.joblib')
scaler = joblib.load('app/models/scaler.joblib')
le_dict = joblib.load('app/models/le_dict-2.joblib')

print("=" * 60)
print("INFORMACIÓN DEL MODELO")
print("=" * 60)

# Info del modelo
print(f"\n🔹 LightGBM Model:")
print(f"   - Classes: {lgb_model.classes_}")
print(f"   - N features: {lgb_model.n_features_in_}")
print(f"   - Feature names: {getattr(lgb_model, 'feature_names_', 'No disponible')}")

# Info del scaler
print(f"\n🔹 StandardScaler:")
print(f"   - N features: {scaler.n_features_in_}")
print(f"   - Feature names: {getattr(scaler, 'feature_names_in_', 'No disponible')}")
print(f"   - Mean (primeros 5): {scaler.mean_[:5]}")
print(f"   - Scale (primeros 5): {scaler.scale_[:5]}")

# Label encoders
print(f"\n🔹 Label Encoders:")
for key, le in le_dict.items():
    print(f"   - {key}: {le.classes_}")

# Crear datos de prueba (como en el JSON)
print("\n" + "=" * 60)
print("PRUEBA DE PREDICCIÓN")
print("=" * 60)

# Datos de prueba (30 features numéricos + 4 categóricos = 34)
test_features = [
    28,    # edad
    3,     # experiencia_previa
    20,    # tiempo_proceso_reclutamiento_dias
    2,     # num_entrevistas
    4.2,   # calificacion_entrevista
    1,     # oferta_inicial_aceptada
    1,     # asistencia_curso_induccion
    4.1,   # puntuacion_induccion
    1,     # materiales_entregados
    1,     # sesion_bienvenida
    5,     # dias_hasta_primer_proyecto
    1,     # asignacion_mentor
    4,     # reunion_equipo_realizadas
    6,     # actividades_integracion
    4.3,   # satisfaccion_lider
    4.5,   # compatibilidad_equipo
    35,    # horas_capacitacion
    5,     # cursos_completados
    78,    # evaluacion_tecnica
    1,     # plan_entrenamiento_formal
    72,    # conocimiento_herramientas
    4.5,   # encuesta_satisfaccion_reclutamiento
    4.3,   # encuesta_satisfaccion_induccion
    4.2,   # encuesta_satisfaccion_integracion
    8,     # nps_primer_mes
    12,    # cantidad_feedback_recibido
    8,     # tamanio_equipo
    5,     # participacion_eventos
    25,    # conexiones_linkedin
    12,    # interaccion_comunidad_interna
]

# Agregar categorías codificadas
genero_encoded = int(le_dict['genero'].transform(['M'])[0])
area_encoded = int(le_dict['area_departamento'].transform(['IT'])[0])
contrato_encoded = int(le_dict['tipo_contrato'].transform(['Indefinido'])[0])
seniority_encoded = int(le_dict['nivel_seniority'].transform(['Semi-Senior'])[0])

test_features.extend([genero_encoded, area_encoded, contrato_encoded, seniority_encoded])

X = np.array(test_features).reshape(1, -1)

print(f"\n🔹 Features generados:")
print(f"   - Shape: {X.shape}")
print(f"   - Primeros 5: {X[0][:5]}")
print(f"   - Últimos 4 (categóricos): {X[0][-4:]}")
print(f"   - Min: {X.min()}, Max: {X.max()}")

# Escalar
X_scaled = scaler.transform(X)
print(f"\n🔹 Features escalados:")
print(f"   - Shape: {X_scaled.shape}")
print(f"   - Primeros 5: {X_scaled[0][:5]}")
print(f"   - Últimos 4: {X_scaled[0][-4:]}")

# Predicción
pred_proba = lgb_model.predict_proba(X_scaled)
pred = lgb_model.predict(X_scaled)

print(f"\n🔹 Predicción:")
print(f"   - Clase predicha: {pred[0]}")
print(f"   - Probabilidades: {pred_proba[0]}")
print(f"   - Prob. Clase 0: {pred_proba[0][0]:.4f}")
print(f"   - Prob. Clase 1: {pred_proba[0][1]:.4f}")

# Diagnosticar
print("\n" + "=" * 60)
print("DIAGNÓSTICO")
print("=" * 60)

if pred[0] == 0 and pred_proba[0][1] < 0.1:
    print("⚠️  El modelo siempre predice clase 0 con muy baja probabilidad de éxito.")
    print("   Posibles causas:")
    print("   1. El modelo fue entrenado con datos desequilibrados (overfitting a clase 0)")
    print("   2. Los valores de entrada están fuera del rango esperado")
    print("   3. El modelo necesita recalibrarse")
else:
    print("✅ El modelo está funcionando correctamente")
