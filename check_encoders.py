import joblib

le_dict = joblib.load('app/models/le_dict-2.joblib')

for key, le in le_dict.items():
    print(f"\n{key}:")
    print(f"  Classes: {le.classes_}")
    print(f"  Transform mapping:")
    for idx, cls in enumerate(le.classes_):
        print(f"    '{cls}' -> {idx}")
