import joblib
import pandas as pd
from django.shortcuts import render
from .forms import UserProfileForm
import re
import numpy as np

model = joblib.load(r"C:/Users/BhumikaMallapur/djangoprojects/ecommerce_proj/smart_nutri/nutrition/data/new_optimized_random_forest.pkl")

recipes_df = pd.read_csv(r"C:/Users/BhumikaMallapur/djangoprojects/ecommerce_proj/smart_nutri/nutrition/data/IndianFoodDataset (5).csv")
recipes_df['Diet'] = recipes_df['Diet'].str.strip().str.lower()
print(recipes_df.columns)

def predict_diet(request):
    form = UserProfileForm(request.POST or None, request.FILES or None)
    recommended_recipes = None
    print(recipes_df.columns)
    if request.method == 'POST' and form.is_valid():
        user_profile = form.save()
        physical_activity = user_profile.physical_activity
        health_condition_preferences = user_profile.health_condition_preferences.lower()
        print(health_condition_preferences)
        dietary_preferences = user_profile.dietary_preferences.lower()
        family_history = user_profile.family_history.lower()
        print(family_history)
        print(dietary_preferences)
        glucose = user_profile.daily_insulin_level or 0
        bmi = user_profile.weight / ((user_profile.height / 100) ** 2)
        age = user_profile.age
        print((glucose,bmi,age))
        input_data = pd.DataFrame([[glucose, bmi, age]], columns=['Glucose', 'BMI', 'Age'])
        predicted_outcome = model.predict(input_data)[0]
        print(predicted_outcome)

        is_diabetic = (
            predicted_outcome == 1 or
            family_history=='diabetic' or
            health_condition_preferences=='diabetes'
        )
        print(is_diabetic)

        '''if is_diabetic:  # Check if the user is diabetic
            print("eneter")
            if dietary_preferences=='vegeatarian':  # Vegetarian
                  print("herree")
                  recommended_recipes = recipes_df[
                         (recipes_df['Diet'] == 'vegetarian') &  # Vegetarian diet
                    (recipes_df['carb_g_x'] <= 50) | # Low-carb
                    print(recipes_df['carb_g_x'],recipes_df['fibre_g_x'],recipes_df['fat_g_x'],recipes_df['protein_g_x'])
                        (recipes_df['fat_g_x'] <= 20) | # Low-fat
                        (recipes_df['fibre_g_x'] >= 5) | # High-fiber
                        (recipes_df['protein_g_x'] >= 10) # Moderate protein
                        
                    ]
            elif dietary_preferences=='vegan':  # Vegan
                    recommended_recipes = recipes_df[
                         (recipes_df['Diet'] == 'vegan') &  # Vegan diet
                        (recipes_df['carb_g_x'] <= 50) &  # Low-carb
                        (recipes_df['fat_g_x'] <= 20) &  # Low-fat
                        (recipes_df['fibre_g_x'] >= 5) &  # High-fiber
                        (recipes_df['protein_g_x'] >= 10)  # Moderate protein
                        
                    ]
            elif dietary_preferences=='non vegetarian':  # Non-Vegetarian
              recommended_recipes = recipes_df[
                    (recipes_df['Diet'] == 'non vegetarian') &  # Non-vegetarian diet
                    (recipes_df['carb_g_x'] <= 50) &  # Low-carb
                    (recipes_df['fat_g_x'] <= 25) &  # Low-fat
                    (recipes_df['fibre_g_x'] >= 5) &  # High-fiber
                    (recipes_df['protein_g_x'] >= 15) # High protein
                    
                ]
    '''
   
            
        if is_diabetic==False:
            if dietary_preferences=='vegetarian':
                recommended_recipes = recipes_df[recipes_df["Diet"].isin(["vegetarian","high protein vegetarian"])]
            elif dietary_preferences=='vegan':
                recommended_recipes = recipes_df[recipes_df['Diet']== 'vegan']
            elif dietary_preferences=='non vegetarian':
                print("here")
                print(recipes_df[recipes_df["Diet"].isin(["non vegetarian"])])
                print("hey")
                recommended_recipes =recipes_df[np.logical_not(recipes_df["Diet"].isin(["vegetarian",'vegan','high protein vegetarian']))]
                print("recc",recommended_recipes)

            else:
                 recommended_recipes = recipes_df[recipes_df['Diet'].isin(['vegetarian', 'non vegetarian', 'vegan'])]

        
        recommended_recipes = (
            recommended_recipes[['RecipeName', 'TotalTimeInMins', 'Diet']]
            .head(12)
            .to_dict('records')
        )

    return render(request, 'predict.html', {'form': form, 'recipes': recommended_recipes})



def home(request):
    trending_recipes = recipes_df.sort_values(by='TotalTimeInMins', ascending=True).head(5)
    trending_recipes = trending_recipes[['RecipeName', 'TotalTimeInMins', 'Diet']].to_dict('records')

    return render(request, 'home.html', {'trending_recipes': trending_recipes})
