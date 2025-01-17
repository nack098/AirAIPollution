import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
import tensorflow as tf

data = pd.read_csv("merged_data.csv", index_col=0)

features = ['year', 'dayFraction', 'season', 'temp', 'lat', 'long']
X = data[features]
y = np.array(data['pm2.5']) 

scaler = StandardScaler()
scaler = scaler.fit(X)
X_scaled = scaler.transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3)

# Build Neural Network
model = tf.keras.models.Sequential([
  tf.keras.layers.Input(shape=(6,)),
  tf.keras.layers.Dense(16, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(1, activation='linear')
])

# Compile Model
model.compile(optimizer='adam', loss='mse', metrics=['r2_score', 'mae'])

# Train Model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=32)

# Evaluate Model
model.evaluate(X_test, y_test, verbose = 2)

#predict me!
new_data = np.array([[2025, 0.04657, 1, 30, 13.7369, 100.5333]])
new_data = scaler.transform(new_data)
print(new_data.shape)
predictions = model.predict(new_data)
print(new_data, "->", predictions)

#export model
model.save("model.keras")
#export standardscaler
dump(scaler, 'std_scaler.bin', compress=True)