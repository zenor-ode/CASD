import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

# Replace the file directory with directory of CSV
data = pd.read_csv('C:\\Users\\zulqa\\OneDrive\\Desktop\\Semester 3_URO\\CA\\Project\\Regression\\ship_data.csv')

# Extract columns needed for regression
speed = data['Speed (knots)'].values
length = data['Length (m)'].values
beam = data['Beam (m)'].values

# Reshape data for sklearn
speed_reshaped = speed.reshape(-1, 1)

# Transform speed data for quadratic regression
poly = PolynomialFeatures(degree=2)
speed_poly = poly.fit_transform(speed_reshaped)

# Quadratic Regression for Speed vs Length
model_length = LinearRegression()
model_length.fit(speed_poly, length)

# Quadratic Regression for Speed vs Beam
model_beam = LinearRegression()
model_beam.fit(speed_poly, beam)

# Generate smooth regression lines
speed_smooth = np.linspace(speed.min(), speed.max(), 500).reshape(-1, 1)  # Generate 500 evenly spaced values for speed
speed_smooth_poly = poly.transform(speed_smooth)
length_smooth = model_length.predict(speed_smooth_poly)
beam_smooth = model_beam.predict(speed_smooth_poly)

# Function to display equations and R^2 scores
def print_regression_equation(model, variable_name):
    coeff = model.coef_
    intercept = model.intercept_
    print(f"{variable_name} Regression Equation: y = {coeff[2]:.8f}x^2 + {coeff[1]:.8f}x + {intercept:.2f}")
    print(f"R^2 = {r2_score(eval(variable_name), model.predict(speed_poly)):.4f}\n")

print("Regression Equations and R^2 Scores:")
print_regression_equation(model_length, 'length')
print_regression_equation(model_beam, 'beam')

# Input for predicting Length and Beam based on Speed
user_speed = float(input("Enter ship speed (knots) for prediction: "))
user_speed_poly = poly.transform([[user_speed]])

# Predict values for Length and Beam
predicted_length = model_length.predict(user_speed_poly)[0]
predicted_beam = model_beam.predict(user_speed_poly)[0]

# Output predictions
print(f"\nPredicted Length for speed {user_speed} knots: {predicted_length:.2f} m")
print(f"Predicted Beam for speed {user_speed} knots: {predicted_beam:.2f} m")

# Plot graphs
plt.figure(figsize=(10, 5))

# Plot Speed vs Length
plt.subplot(1, 2, 1)
plt.scatter(speed, length, color='blue', label='Actual Data')
plt.plot(speed_smooth, length_smooth, color='red', label='Regression Line')  # Smooth quadratic regression line
plt.title('Speed (knots) vs Length (m)')
plt.xlabel('Speed (knots)')
plt.ylabel('Length (m)')
plt.legend()
plt.text(min(speed), max(length),
         f'Equation: y = {model_length.coef_[2]:.8f}x^2 + {model_length.coef_[1]:.8f}x + {model_length.intercept_:.2f}\n$R^2$ = {r2_score(length, model_length.predict(speed_poly)):.4f}',
         fontsize=10)

# Plot Speed vs Beam
plt.subplot(1, 2, 2)
plt.scatter(speed, beam, color='blue', label='Actual Data')
plt.plot(speed_smooth, beam_smooth, color='red', label='Regression Line')  # Smooth quadratic regression line
plt.title('Speed (knots) vs Beam (m)')
plt.xlabel('Speed (knots)')
plt.ylabel('Beam (m)')
plt.legend()
plt.text(min(speed), max(beam),
         f'Equation: y = {model_beam.coef_[2]:.8f}x^2 + {model_beam.coef_[1]:.8f}x + {model_beam.intercept_:.2f}\n$R^2$ = {r2_score(beam, model_beam.predict(speed_poly)):.4f}',
         fontsize=10)

plt.tight_layout()
plt.show()
