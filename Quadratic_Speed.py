import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

# Replace the file directory with directory of CSV
data = pd.read_csv('C:\\Users\\zulqa\\OneDrive\\Desktop\\Semester 3_URO\\CA\\Project\\Regression\\ship_data.csv')

# Extract columns needed for regression
capacity = data['Capacity (TEU)'].values
draft = data['Draft (m)'].values
displacement = data['Displacement (tons)'].values
block = data['Block Coefficient'].values

# Reshape data for sklearn. Sklearn is library use for Regression Analysis of given data
capacity_reshaped = capacity.reshape(-1, 1)

# Transform capacity data for quadratic regression
poly = PolynomialFeatures(degree=2)
capacity_poly = poly.fit_transform(capacity_reshaped)

# Quadratic Regression for Capacity vs Draft
model_draft = LinearRegression()  # Linear means 2nd degree regression w.r.t python library keep in mind.
model_draft.fit(capacity_poly, draft)
draft_pred = model_draft.predict(capacity_poly)

# Quadratic Regression for Capacity vs Displacement
model_displacement = LinearRegression()
model_displacement.fit(capacity_poly, displacement)
displacement_pred = model_displacement.predict(capacity_poly)

# Quadratic Regression for Capacity vs Block Coefficient
model_block = LinearRegression()
model_block.fit(capacity_poly, block)
block_pred = model_block.predict(capacity_poly)

# Function to display equations and R^2 scores
def print_regression_equation(model, variable_name):
    coeff = model.coef_
    intercept = model.intercept_
    print(f"{variable_name} Regression Equation: y = {coeff[2]:.8f}x^2 + {coeff[1]:.8f}x + {intercept:.2f}")
    print(f"R^2 = {r2_score(eval(variable_name), model.predict(capacity_poly)):.4f}\n")

print("Regression Equations and R^2 Scores:")
print_regression_equation(model_draft, 'draft')
print_regression_equation(model_displacement, 'displacement')
print_regression_equation(model_block, 'block')

# Input for predicting parameters
user_capacity = float(input("Enter ship capacity (TEU) for prediction: "))
user_capacity_poly = poly.transform([[user_capacity]])

# Predict values for Draft, Displacement, and Block Coefficient
predicted_draft = model_draft.predict(user_capacity_poly)[0]
predicted_displacement = model_displacement.predict(user_capacity_poly)[0]
predicted_block = model_block.predict(user_capacity_poly)[0]

# Output predictions
print(f"\nPredicted Draft: {predicted_draft:.2f} m")
print(f"Predicted Displacement: {predicted_displacement:.2f} tons")
print(f"Predicted Block Coefficient: {predicted_block:.2f}")

# Plot graphs
plt.figure(figsize=(15, 5))

# Plot Capacity vs Draft
plt.subplot(1, 3, 1)
plt.scatter(capacity, draft, color='blue', label='Actual Data')
plt.plot(capacity, draft_pred, color='red', label='Regression Line')
plt.title('Capacity (TEU) vs Draft (m)')
plt.xlabel('Capacity (TEU)')
plt.ylabel('Draft (m)')
plt.legend()
plt.text(min(capacity), max(draft),
         f'Equation: y = {model_draft.coef_[2]:.8f}x^2 + {model_draft.coef_[1]:.8f}x + {model_draft.intercept_:.2f}\n$R^2$ = {r2_score(draft, draft_pred):.4f}',
         fontsize=10)

# Plot Capacity vs Displacement
plt.subplot(1, 3, 2)
plt.scatter(capacity, displacement, color='blue', label='Actual Data')
plt.plot(capacity, displacement_pred, color='red', label='Regression Line')
plt.title('Capacity (TEU) vs Displacement (tons)')
plt.xlabel('Capacity (TEU)')
plt.ylabel('Displacement (tons)')
plt.legend()
plt.text(min(capacity), max(displacement),
         f'Equation: y = {model_displacement.coef_[2]:.8f}x^2 + {model_displacement.coef_[1]:.8f}x + {model_displacement.intercept_:.2f}\n$R^2$ = {r2_score(displacement, displacement_pred):.4f}',
         fontsize=10)

# Plot Capacity vs Block Coefficient
plt.subplot(1, 3, 3)
plt.scatter(capacity, block, color='blue', label='Actual Data')
plt.plot(capacity, block_pred, color='red', label='Regression Line')
plt.title('Capacity (TEU) vs Block Coefficient')
plt.xlabel('Capacity (TEU)')
plt.ylabel('Block Coefficient')
plt.legend()
plt.text(min(capacity), max(block),
         f'Equation: y = {model_block.coef_[2]:.8f}x^2 + {model_block.coef_[1]:.8f}x + {model_block.intercept_:.2f}\n$R^2$ = {r2_score(block, block_pred):.4f}',
         fontsize=10)

plt.tight_layout()
plt.show()
