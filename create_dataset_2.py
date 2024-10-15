import pandas as pd
import json

with open('protein_csvs/mealid_to_title.json', 'r') as file:
    mealid_to_title = json.load(file)

users_with_rules = pd.read_csv('protein_csvs/users_with_rules.csv')
weekly_meal_plan_dataset = pd.read_csv('protein_csvs/weekly_meal_plan_dataset.csv')

output_file = 'generated_jsonls/dataset_created_from_weekly_plans_2.jsonl'
with open(output_file, 'w') as f:
    user_counter = 0
    meal_counter = 0
    counter = 0
    breakfast = 0
    morning_snack = 0
    lunch = 0
    afternoon_snack = 0
    dinner = 0
    supper = 0

    breakfast_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    morning_snack_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    lunch_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    afternoon_snack_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    dinner_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    supper_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    for user in users_with_rules["USER ID"]:
        user_info = users_with_rules[users_with_rules['USER ID'] == user]
        user_id = user_info["USER ID"][user_counter]
        weight = user_info['Weight'].values[0]
        height = user_info['Height'].values[0]
        pal = user_info['PAL'].values[0]
        bmi = user_info['BMI'].values[0]
        bmr = user_info['BMR'].values[0]
        age = user_info['Age'].values[0]
        subgroup = ""
        if user_info['Subgroup'].values[0] == 1:
            subgroup = " the user is a healthy adult"
        if user_info['Subgroup'].values[0] == 2:
            subgroup = " the user is a healthy adolecent"
        if user_info['Subgroup'].values[0] == 3:
            subgroup = " the user is a healthy older adult"
        if user_info['Subgroup'].values[0] == 4:
            subgroup = " the user is an overweight adult"
        if user_info['Subgroup'].values[0] == 5:
            subgroup = " the user is an athlete"
        if user_info['Subgroup'].values[0] == 6:
            subgroup = " the user is an adult with obesity"
        if user_info['Subgroup'].values[0] == 7:
            subgroup = " the user is an adult with cardiovasculat disease"
        if user_info['Subgroup'].values[0] == 8:
            subgroup = " the user is an adult with Type 2 Diabetes"
        if user_info['Subgroup'].values[0] == 9:
            subgroup = " the user is an adult with iron deficiency"
        if user_info['Subgroup'].values[0] == 10:
            subgroup = " the user is an adalut with low fruits and vegetables"
        EI = user_info['EI'].values[0]
        protein_min = user_info['Protein_min'].values[0]
        protein_max = user_info['Protein_max'].values[0]
        sfa_min = user_info['SFA_min'].values[0]
        sfa_max = user_info['SFA_max'].values[0]
        iron_equal = user_info['Iron_equal'].values[0]
        vitamin_c_equal = user_info['Vit C_equal'].values[0]
        fibre_min = user_info['Fibre_g_min'].values[0]
        fibre_max = user_info['Fibre_g_max'].values[0]
        fruit_min = user_info['Fruit_portion_min'].values[0]
        fruit_max = user_info['Fruit_portion_max'].values[0]
        veg_min = user_info['Veg_portion_min'].values[0]
        veg_max = user_info['Veg_portion_max'].values[0]
        cho_min = user_info['CH0_min'].values[0]
        cho_max = user_info['CH0_max'].values[0]
        fat_min = user_info['Fat_min'].values[0]
        fat_max = user_info['Fat_max'].values[0]
        
        for meal in weekly_meal_plan_dataset["USER ID"]:
            daily_meal_temp = weekly_meal_plan_dataset[weekly_meal_plan_dataset['USER ID'] == meal]        
            for day in daily_meal_temp["DATE_OF_MONTH"]:
                daily_meal = daily_meal_temp[daily_meal_temp['DATE_OF_MONTH'] == day]

                #print("For the user: ", user_id)
                #print("For the date: ", day)
                #print(daily_meal["DATE_OF_MONTH"])

                if daily_meal["BREAKFAST"][meal_counter] == 0:
                    meal_counter += 1
                    counter += 1
                    continue
                breakfast_id = daily_meal["BREAKFAST"][meal_counter]
                breakfast_kcal = daily_meal["BREAKFAST KCAL"][meal_counter]
                breakfast_protein = daily_meal["BREAKFAST TOTAL PROTEIN"][meal_counter]
                breakfast_carb = daily_meal["BREAKFAST TOTAL CARBOHYDRATE"][meal_counter]
                breakfast_fat = daily_meal["BREAKFAST TOTAL FAT"][meal_counter]
                breakfast_sfa = daily_meal["BREAKFAST TOTAL SFA"][meal_counter]
                breakfast_iron = daily_meal["BREAKFAST TOTAL IRON"][meal_counter]
                breakfast_vitamin_c = daily_meal["BREAKFAST TOTAL VIT C"][meal_counter]
                breakfast_fibre = daily_meal["BREAKFAST TOTAL FIBRE"][meal_counter]
                breakfast_fruits = daily_meal["BREAKFAST TOTAL FRUITS"][meal_counter]
                breakfast_vegs = daily_meal["BREAKFAST TOTAL VEGS"][meal_counter]

                for key in mealid_to_title:
                    if key == "0" or key == "-1":
                        continue
                    else:
                        if int(key) == int(breakfast_id):
                            breakfast_title = mealid_to_title[key]
                            break
                #print(breakfast_id, breakfast_title, breakfast_kcal, breakfast_protein, breakfast_carb, breakfast_fat, breakfast_sfa, breakfast_iron, breakfast_vitamin_c, breakfast_fibre, breakfast_fruits, breakfast_vegs)

                if daily_meal["MORNING SNACK"][meal_counter] == 0:
                    meal_counter += 1
                    counter += 1
                    continue
                morning_snack_id = daily_meal["MORNING SNACK"][meal_counter]
                morning_snack_kcal = daily_meal["MORNING SNACK KCAL"][meal_counter]
                morning_snack_protein = daily_meal["MORNING SNACK TOTAL PROTEIN"][meal_counter]
                morning_snack_carb = daily_meal["MORNING SNACK TOTAL CARBOHYDRATE"][meal_counter]
                morning_snack_fat = daily_meal["MORNING SNACK TOTAL FAT"][meal_counter]
                morning_snack_sfa = daily_meal["MORNING SNACK TOTAL SFA"][meal_counter]
                morning_snack_iron = daily_meal["MORNING SNACK TOTAL IRON"][meal_counter]
                morning_snack_vitamin_c = daily_meal["MORNING SNACK TOTAL VIT C"][meal_counter]
                morning_snack_fibre = daily_meal["MORNING SNACK TOTAL FIBRE"][meal_counter]
                morning_snack_fruits = daily_meal["MORNING SNACK TOTAL FRUITS"][meal_counter]
                morning_snack_vegs = daily_meal["MORNING SNACK TOTAL VEGS"][meal_counter]

                for key in mealid_to_title:
                    if key == "0" or key == "-1":
                        continue
                    else:
                        if int(key) == int(morning_snack_id):
                            morning_snack_title = mealid_to_title[key]
                            break
                #print(morning_snack_id, morning_snack_title, morning_snack_kcal, morning_snack_protein, morning_snack_carb, morning_snack_fat, morning_snack_sfa, morning_snack_iron, morning_snack_vitamin_c, morning_snack_fibre, morning_snack_fruits, morning_snack_vegs)

                if daily_meal["LUNCH"][meal_counter] == 0:
                    meal_counter += 1
                    counter += 1
                    continue
                lunch_id = daily_meal["LUNCH"][meal_counter]
                lunch_kcal = daily_meal["LUNCH KCAL"][meal_counter]
                lunch_protein = daily_meal["LUNCH TOTAL PROTEIN"][meal_counter]
                lunch_carb = daily_meal["LUNCH TOTAL CARBOHYDRATE"][meal_counter]
                lunch_fat = daily_meal["LUNCH TOTAL FAT"][meal_counter]
                lunch_sfa = daily_meal["LUNCH TOTAL SFA"][meal_counter]
                lunch_iron = daily_meal["LUNCH TOTAL IRON"][meal_counter]
                lunch_vitamin_c = daily_meal["LUNCH TOTAL VIT C"][meal_counter]
                lunch_fibre = daily_meal["LUNCH TOTAL FIBRE"][meal_counter]
                lunch_fruits = daily_meal["LUNCH TOTAL FRUITS"][meal_counter]
                lunch_vegs = daily_meal["LUNCH TOTAL VEGS"][meal_counter]

                for key in mealid_to_title:
                    if key == "0" or key == "-1":
                        continue
                    else:
                        if int(key) == int(lunch_id):
                            lunch_title = mealid_to_title[key]
                            break
                #print(lunch_id, lunch_title, lunch_kcal, lunch_protein, lunch_carb, lunch_fat, lunch_sfa, lunch_iron, lunch_vitamin_c, lunch_fibre, lunch_fruits, lunch_vegs)

                if daily_meal["AFTERNOON SNACK"][meal_counter] == 0:
                    meal_counter += 1
                    counter += 1
                    continue
                afternoon_snack_id = daily_meal["AFTERNOON SNACK"][meal_counter]
                afternoon_snack_kcal = daily_meal["AFTERNOON SNACK KCAL"][meal_counter]
                afternoon_snack_protein = daily_meal["AFTERNOON SNACK TOTAL PROTEIN"][meal_counter]
                afternoon_snack_carb = daily_meal["AFTERNOON SNACK TOTAL CARBOHYDRATE"][meal_counter]
                afternoon_snack_fat = daily_meal["AFTERNOON SNACK TOTAL FAT"][meal_counter]
                afternoon_snack_sfa = daily_meal["AFTERNOON SNACK TOTAL SFA"][meal_counter]
                afternoon_snack_iron = daily_meal["AFTERNOON SNACK TOTAL IRON"][meal_counter]
                afternoon_snack_vitamin_c = daily_meal["AFTERNOON SNACK TOTAL VIT C"][meal_counter]
                afternoon_snack_fibre = daily_meal["AFTERNOON SNACK TOTAL FIBRE"][meal_counter]
                afternoon_snack_fruits = daily_meal["AFTERNOON SNACK TOTAL FRUITS"][meal_counter]
                afternoon_snack_vegs = daily_meal["AFTERNOON SNACK TOTAL VEGS"][meal_counter]

                for key in mealid_to_title:
                    if key == "0" or key == "-1":
                        continue
                    else:
                        if int(key) == int(afternoon_snack_id):
                            afternoon_snack_title = mealid_to_title[key]
                            break
                #print(afternoon_snack_id, afternoon_snack_title, afternoon_snack_kcal, afternoon_snack_protein, afternoon_snack_carb, afternoon_snack_fat, afternoon_snack_sfa, afternoon_snack_iron, afternoon_snack_vitamin_c, afternoon_snack_fibre, afternoon_snack_fruits, afternoon_snack_vegs)

                if daily_meal["DINNER"][meal_counter] == 0:
                    meal_counter += 1
                    counter += 1
                    continue
                dinner_id = daily_meal["DINNER"][meal_counter]
                dinner_kcal = daily_meal["DINNER KCAL"][meal_counter]
                dinner_protein = daily_meal["DINNER TOTAL PROTEIN"][meal_counter]
                dinner_carb = daily_meal["DINNER TOTAL CARBOHYDRATE"][meal_counter]
                dinner_fat = daily_meal["DINNER TOTAL FAT"][meal_counter]
                dinner_sfa = daily_meal["DINNER TOTAL SFA"][meal_counter]
                dinner_iron = daily_meal["DINNER TOTAL IRON"][meal_counter]
                dinner_vitamin_c = daily_meal["DINNER TOTAL VIT C"][meal_counter]
                dinner_fibre = daily_meal["DINNER TOTAL FIBRE"][meal_counter]
                dinner_fruits = daily_meal["DINNER TOTAL FRUITS"][meal_counter]
                dinner_vegs = daily_meal["DINNER TOTAL VEGS"][meal_counter]

                for key in mealid_to_title:
                    if key == "0" or key == "-1":
                        continue
                    else:
                        if int(key) == int(dinner_id):
                            dinner_title = mealid_to_title[key]
                            break
                #print(dinner_id, dinner_title, dinner_kcal, dinner_protein, dinner_carb, dinner_fat, dinner_sfa, dinner_iron, dinner_vitamin_c, dinner_fibre, dinner_fruits, dinner_vegs)

                if daily_meal["SUPPER"][meal_counter] == 0:
                    supper_list[8] += 1
                    meal_counter += 1
                    counter += 1
                    continue
                supper_id = daily_meal["SUPPER"][meal_counter]
                supper_kcal = daily_meal["SUPPER KCAL"][meal_counter]
                supper_protein = daily_meal["SUPPER TOTAL PROTEIN"][meal_counter]
                supper_carb = daily_meal["SUPPER TOTAL CARBOHYDRATE"][meal_counter]
                supper_fat = daily_meal["SUPPER TOTAL FAT"][meal_counter]
                supper_sfa = daily_meal["SUPPER TOTAL SFA"][meal_counter]
                supper_iron = daily_meal["SUPPER TOTAL IRON"][meal_counter]
                supper_iron = daily_meal["SUPPER TOTAL IRON"][meal_counter]
                supper_vitamin_c = daily_meal["SUPPER TOTAL VIT C"][meal_counter]
                supper_fibre = daily_meal["SUPPER TOTAL FIBRE"][meal_counter]
                supper_fruits = daily_meal["SUPPER TOTAL FRUITS"][meal_counter]
                supper_vegs = daily_meal["SUPPER TOTAL VEGS"][meal_counter]

                for key in mealid_to_title:
                    if key == "0" or key == "-1":
                        continue
                    else:
                        if int(key) == int(supper_id):
                            supper_title = mealid_to_title[key]
                            break
                #print(supper_id, supper_title, supper_kcal, supper_protein, supper_carb, supper_fat, supper_sfa, supper_iron, supper_vitamin_c, supper_fibre, supper_fruits, supper_vegs)
                
                entry = {
                    "instruction":
                        "Generate a daily meal plan of breakfast, morning snack, lunch, afternoon snack, dinner, and supper for the following user.",
                    "input":
                        "User profile: Energy intake="+str(EI)+", weight="+str(weight)+", height="+str(height)+", pal="+str(pal)+", bmi="+str(bmi)+", age="+str(age)+", and "+subgroup+".",
                    #"output":
                        #"Based on the above information the user needs: minimum grams of protein: "+str(protein_min)+" maximum grams of protein: "+str(protein_max)+" minimum grams of SFA: "+str(sfa_min)+", maximum grams of SFA: "+str(sfa_max)+", grams of iron: "+str(iron_equal)+", grams of vitamin C: "+str(vitamin_c_equal)+", minimum grams of fibre:"+str(fibre_min)+", maximum grams of fibre: "+str(fibre_max)+", minimum portions of fruit: "+str(fruit_min)+", maximum portions of fruit: "+str(fruit_max)+", minimum portions of vegetables: "+str(veg_min)+", maximum portions of vegetables: "+str(veg_max)+", minimum grams of carbohydrates: "+str(cho_min)+", maximum grams of carbohydrates: "+str(cho_max)+", minimum grams of fats: "+str(fat_min)+", maximum grams of fats: "+str(fat_max)+". Therefore, here is a daily meal plan: Breakfast, "+str(breakfast_title)+" ("+str(breakfast_kcal)+"kcal, "+str(breakfast_protein)+"g protein, "+str(breakfast_carb)+"g of carbohydrate, "+str(breakfast_fat)+"g of fat, "+str(breakfast_sfa)+"g of SFA, "+str(breakfast_iron)+"g of iron, "+str(breakfast_vitamin_c)+"g of vitamin c, "+str(breakfast_fibre)+"g of fibre, "+str(breakfast_fruits)+" number of fruits, "+str(breakfast_vegs)+" number of vegetables. Morning snack, "+str(morning_snack_title)+" ("+str(morning_snack_kcal)+"kcal, "+str(morning_snack_protein)+"g protein, "+str(morning_snack_carb)+"g of carbohydrate, "+str(morning_snack_fat)+"g of fat, "+str(morning_snack_sfa)+"g of SFA, "+str(morning_snack_iron)+"g of iron, "+str(morning_snack_vitamin_c)+"g of vitamin c, "+str(morning_snack_fibre)+"g of fibre, "+str(morning_snack_fruits)+" number of fruits, "+str(morning_snack_vegs)+" number of vegetables. Lunch, "+str(lunch_title)+" ("+str(lunch_kcal)+"kcal, "+str(lunch_protein)+"g protein, "+str(lunch_carb)+"g of carbohydrate, "+str(lunch_fat)+"g of fat, "+str(lunch_sfa)+"g of SFA, "+str(lunch_iron)+"g of iron, "+str(lunch_vitamin_c)+"g of vitamin c, "+str(lunch_fibre)+"g of fibre, "+str(lunch_fruits)+" number of fruits, "+str(lunch_vegs)+" number of vegetables. Afternoon snack, "+str(afternoon_snack_title)+" ("+str(afternoon_snack_kcal)+"kcal, "+str(afternoon_snack_protein)+"g protein, "+str(afternoon_snack_carb)+"g of carbohydrate, "+str(afternoon_snack_fat)+"g of fat, "+str(afternoon_snack_sfa)+"g of SFA, "+str(afternoon_snack_iron)+"g of iron, "+str(afternoon_snack_vitamin_c)+"g of vitamin c, "+str(afternoon_snack_fibre)+"g of fibre, "+str(afternoon_snack_fruits)+" number of fruits, "+str(afternoon_snack_vegs)+" number of vegetables. Dinner, "+str(dinner_title)+" ("+str(dinner_kcal)+"kcal, "+str(dinner_protein)+"g protein, "+str(dinner_carb)+"g of carbohydrate, "+str(dinner_fat)+"g of fat, "+str(dinner_sfa)+"g of SFA, "+str(dinner_iron)+"g of iron, "+str(dinner_vitamin_c)+"g of vitamin c, "+str(dinner_fibre)+"g of fibre, "+str(dinner_fruits)+" number of fruits, "+str(dinner_vegs)+" number of vegetables. Supper, "+str(supper_title)+" ("+str(supper_kcal)+"kcal, "+str(supper_protein)+"g protein, "+str(supper_carb)+"g of carbohydrate, "+str(supper_fat)+"g of fat, "+str(supper_sfa)+"g of SFA, "+str(supper_iron)+"g of iron, "+str(supper_vitamin_c)+"g of vitamin c, "+str(supper_fibre)+"g of fibre, "+str(supper_fruits)+" number of fruits, "+str(supper_vegs)+" number of vegetables.",
                    "output":
                        "Here is a daily meal plan:\nBreakfast, "+str(breakfast_title)+" ("+str(breakfast_kcal)+"kcal, "+str(breakfast_protein)+" grams protein, "+str(breakfast_carb)+" grams of carbohydrate, "+str(breakfast_fat)+" grams of fat, "+str(breakfast_sfa)+" grams of SFA, "+str(breakfast_iron)+" grams of iron, "+str(breakfast_vitamin_c)+" grams of vitamin c, "+str(breakfast_fibre)+" grams of fibre, "+str(breakfast_fruits)+" number of fruits, "+str(breakfast_vegs)+" number of vegetables.\nMorning snack, "+str(morning_snack_title)+" ("+str(morning_snack_kcal)+"kcal, "+str(morning_snack_protein)+" grams protein, "+str(morning_snack_carb)+" grams of carbohydrate, "+str(morning_snack_fat)+" grams of fat, "+str(morning_snack_sfa)+" grams of SFA, "+str(morning_snack_iron)+" grams of iron, "+str(morning_snack_vitamin_c)+" grams of vitamin c, "+str(morning_snack_fibre)+" grams of fibre, "+str(morning_snack_fruits)+" number of fruits, "+str(morning_snack_vegs)+" number of vegetables.\nLunch, "+str(lunch_title)+" ("+str(lunch_kcal)+"kcal, "+str(lunch_protein)+" grams protein, "+str(lunch_carb)+" grams of carbohydrate, "+str(lunch_fat)+" grams of fat, "+str(lunch_sfa)+" grams of SFA, "+str(lunch_iron)+" grams of iron, "+str(lunch_vitamin_c)+" grams of vitamin c, "+str(lunch_fibre)+" grams of fibre, "+str(lunch_fruits)+" number of fruits, "+str(lunch_vegs)+" number of vegetables.\nAfternoon snack, "+str(afternoon_snack_title)+" ("+str(afternoon_snack_kcal)+"kcal, "+str(afternoon_snack_protein)+" grams protein, "+str(afternoon_snack_carb)+" grams of carbohydrate, "+str(afternoon_snack_fat)+" grams of fat, "+str(afternoon_snack_sfa)+" grams of SFA, "+str(afternoon_snack_iron)+" grams of iron, "+str(afternoon_snack_vitamin_c)+" grams of vitamin c, "+str(afternoon_snack_fibre)+" grams of fibre, "+str(afternoon_snack_fruits)+" number of fruits, "+str(afternoon_snack_vegs)+" number of vegetables.\nDinner, "+str(dinner_title)+" ("+str(dinner_kcal)+"kcal, "+str(dinner_protein)+" grams protein, "+str(dinner_carb)+" grams of carbohydrate, "+str(dinner_fat)+" grams of fat, "+str(dinner_sfa)+" grams of SFA, "+str(dinner_iron)+" grams of iron, "+str(dinner_vitamin_c)+" grams of vitamin c, "+str(dinner_fibre)+" grams of fibre, "+str(dinner_fruits)+" number of fruits, "+str(dinner_vegs)+" number of vegetables.\nSupper, "+str(supper_title)+" ("+str(supper_kcal)+"kcal, "+str(supper_protein)+" grams protein, "+str(supper_carb)+" grams of carbohydrate, "+str(supper_fat)+" grams of fat, "+str(supper_sfa)+" grams of SFA, "+str(supper_iron)+" grams of iron, "+str(supper_vitamin_c)+" grams of vitamin c, "+str(supper_fibre)+" grams of fibre, "+str(supper_fruits)+" number of fruits, "+str(supper_vegs)+" number of vegetables.",
                }
                f.write(json.dumps(entry) + '\n')
                
                if str(breakfast_kcal) == "0.0":
                    breakfast_list[0] += 1
                if str(breakfast_protein) == "0.0":
                    breakfast_list[1] += 1
                if str(breakfast_carb) == "0.0":
                    breakfast_list[2] += 1
                if str(breakfast_fat) == "0.0":
                    breakfast_list[3] += 1
                if str(breakfast_sfa) == "0.0":
                    breakfast_list[4] += 1
                if str(breakfast_iron) == "0.0":
                    breakfast_list[5] += 1
                if str(breakfast_vitamin_c) == "0.0":
                    breakfast_list[6] += 1
                if str(breakfast_fibre) == "0.0":
                    breakfast_list[7] += 1
                if str(breakfast_id) == "0.0":
                    breakfast_list[8] += 1
                
                if str(morning_snack_kcal) == "0.0":
                    morning_snack_list[0] += 1
                if str(morning_snack_protein) == "0.0":
                    morning_snack_list[1] += 1
                if str(morning_snack_carb) == "0.0":
                    morning_snack_list[2] += 1
                if str(morning_snack_fat) == "0.0":
                    morning_snack_list[3] += 1
                if str(morning_snack_sfa) == "0.0":
                    morning_snack_list[4] += 1
                if str(morning_snack_iron) == "0.0":
                    morning_snack_list[5] += 1
                if str(morning_snack_vitamin_c) == "0.0":
                    morning_snack_list[6] += 1
                if str(morning_snack_fibre) == "0.0":
                    morning_snack_list[7] += 1
                if str(morning_snack_id) == "0.0":
                    morning_snack_list[8] += 1

                if str(lunch_kcal) == "0.0":
                    lunch_list[0] += 1
                if str(lunch_protein) == "0.0":
                    lunch_list[1] += 1
                if str(lunch_carb) == "0.0":
                    lunch_list[2] += 1
                if str(lunch_fat) == "0.0":
                    lunch_list[3] += 1
                if str(lunch_sfa) == "0.0":
                    lunch_list[4] += 1
                if str(lunch_iron) == "0.0":
                    lunch_list[5] += 1
                if str(lunch_vitamin_c) == "0.0":
                    lunch_list[6] += 1
                if str(lunch_fibre) == "0.0":
                    lunch_list[7] += 1
                if str(lunch_id) == "0.0":
                    lunch_list[8] += 1

                if str(afternoon_snack_kcal) == "0.0":
                    afternoon_snack_list[0] += 1
                if str(afternoon_snack_protein) == "0.0":
                    afternoon_snack_list[1] += 1
                if str(afternoon_snack_carb) == "0.0":
                    afternoon_snack_list[2] += 1
                if str(afternoon_snack_fat) == "0.0":
                    afternoon_snack_list[3] += 1
                if str(afternoon_snack_sfa) == "0.0":
                    afternoon_snack_list[4] += 1
                if str(afternoon_snack_iron) == "0.0":
                    afternoon_snack_list[5] += 1
                if str(afternoon_snack_vitamin_c) == "0.0":
                    afternoon_snack_list[6] += 1
                if str(afternoon_snack_fibre) == "0.0":
                    afternoon_snack_list[7] += 1
                if str(afternoon_snack_id) == "0.0":
                    afternoon_snack_list[8] += 1

                if str(dinner_kcal) == "0.0":
                    dinner_list[0] += 1
                if str(dinner_protein) == "0.0":
                    dinner_list[1] += 1
                if str(dinner_carb) == "0.0":
                    dinner_list[2] += 1
                if str(dinner_fat) == "0.0":
                    dinner_list[3] += 1
                if str(dinner_sfa) == "0.0":
                    dinner_list[4] += 1
                if str(dinner_iron) == "0.0":
                    dinner_list[5] += 1
                if str(dinner_vitamin_c) == "0.0":
                    dinner_list[6] += 1
                if str(dinner_fibre) == "0.0":
                    dinner_list[7] += 1
                if str(dinner_id) == "0.0":
                    dinner_list[8] += 1

                if str(supper_kcal) == "0.0":
                    supper_list[0] += 1
                if str(supper_protein) == "0.0":
                    supper_list[1] += 1
                if str(supper_carb) == "0.0":
                    supper_list[2] += 1
                if str(supper_fat) == "0.0":
                    supper_list[3] += 1
                if str(supper_sfa) == "0.0":
                    supper_list[4] += 1
                if str(supper_iron) == "0.0":
                    supper_list[5] += 1
                if str(supper_vitamin_c) == "0.0":
                    supper_list[6] += 1
                if str(supper_fibre) == "0.0":
                    supper_list[7] += 1
                if str(supper_id) == "0.0":
                    supper_list[8] += 1
                
                counter += 1
                #if counter == 22:
                #    quit()
                #print("check point 4", counter)
                meal_counter += 1
            meal_counter = 0
            break
        user_counter += 1
    #print(breakfast, morning_snack, lunch, afternoon_snack, dinner, supper)
    print(breakfast_list, morning_snack_list, lunch_list, afternoon_snack_list, dinner_list, supper_list)