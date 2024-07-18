import pandas as pd
from app import create_app, mongo

app = create_app()
app.app_context().push()

class DataLoader:
    def __init__(self, food_file_path, sport_file_path, sleep_lifestyle_file_path):
        self.food_file_path = food_file_path
        self.sport_file_path = sport_file_path
        self.sleep_lifestyle_file_path = sleep_lifestyle_file_path

    def load_food_calories(self):
        data = pd.read_excel(self.food_file_path)
        for index, row in data.iterrows():
            food_item = row['FoodItem'].lower()
            calorie_value = float(row['Cals_per100grams'].replace(' cal', ''))
            food_calorie = {'food_type': food_item, 'calories_per_100g': calorie_value}
            mongo.db.food_calories.insert_one(food_calorie)

    def load_sport_calories(self):
        data = pd.read_csv(self.sport_file_path)
        for index, row in data.iterrows():
            sport_item = row['Sport'].lower()
            calorie_value = float(row['Cals per kg'].replace(' cal', ''))
            sport_calorie = {'sport_type': sport_item, 'calories_per_kg': calorie_value}
            mongo.db.sport_calories.insert_one(sport_calorie)

    def load_sleep_lifestyle_data(self):
        data = pd.read_csv(self.sleep_lifestyle_file_path)
        for index, row in data.iterrows():
            sleep_lifestyle_data = {
                'gender': row['gender'].lower(),
                'age': row['age'],
                'sleep_duration': row['sleep duration'],
                'physical_activity_level': row['physical activity level'].lower(),
                'sleep_quality': row['quality of sleep'].lower()
            }
            mongo.db.sleep_lifestyle_data.insert_one(sleep_lifestyle_data)

    def load_all_data(self):
        self.load_food_calories()
        self.load_sport_calories()
        self.load_sleep_lifestyle_data()

if __name__ == '__main__':
    data_loader = DataLoader(
        'datasets/calories_per_100.xlsx',
        'datasets/exercise_dataset.csv',
        'datasets/Sleep_health_and_lifestyle_dataset.csv'
    )
    data_loader.load_all_data()
