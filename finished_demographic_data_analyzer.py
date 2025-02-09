import pandas as pd

def calculate_demographic_data(print_data=True):
    #Load dataset
    df = pd.read_csv("adult.data.csv", header=None, names=[
        "age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
        "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
        "hours-per-week", "native-country", "salary"
    ])

    #Data cleaning
    df["age"] = pd.to_numeric(df["age"], errors="coerce")  #Convert 'age' to numeric, errors to NaN
    df["hours-per-week"] = pd.to_numeric(df["hours-per-week"], errors="coerce")  #Convert 'hours-per-week to numeric, errors to NaN
    df_cleaned = df.dropna(subset=["age", "hours-per-week", "race"])  #Drop rows with NaNs

    #1. Race count
    race_count = df_cleaned["race"].value_counts()

    #2. Average age of men
    average_age_men = round(df_cleaned[df_cleaned["sex"] == "Male"]["age"].mean(), 1)

    #3. Percentage of people with a Bachelor's degree
    percentage_bachelors = round((df_cleaned["education"] == "Bachelors").mean() * 100, 1)

    #4. Advanced education: Bachelor's, Master's, Doctorate
    higher_education = df_cleaned["education"].isin(["Bachelors", "Masters", "Doctorate"])
    lower_education = ~higher_education

    higher_education_rich = round(
        (df_cleaned[higher_education & (df_cleaned["salary"] == ">50K")].shape[0] /
         df_cleaned[higher_education].shape[0]) * 100, 1
    )
    lower_education_rich = round(
        (df_cleaned[lower_education & (df_cleaned["salary"] == ">50K")].shape[0] /
         df_cleaned[lower_education].shape[0]) * 100, 1
    )

    #5. Minimum work hours
    min_work_hours = int(df_cleaned["hours-per-week"].min())

    #6. Rich percentage among minimum workers
    num_min_workers = df_cleaned[df_cleaned["hours-per-week"] == min_work_hours]
    rich_percentage = round((num_min_workers["salary"] == ">50K").mean() * 100, 1)

    #7. Country with highest percentage of rich people
    countries_rich = df_cleaned[df_cleaned["salary"] == ">50K"]["native-country"].value_counts()
    countries_total = df_cleaned["native-country"].value_counts()
    highest_earning_country_percentage = round((countries_rich / countries_total).max() * 100, 1)
    highest_earning_country = (countries_rich / countries_total).idxmax()

    #8. Top occupation in India for rich people
    top_IN_occupation = df_cleaned[(df_cleaned["native-country"] == "India") & 
                                   (df_cleaned["salary"] == ">50K")]["occupation"].mode()[0]

    if print_data:
        print("Race count:", race_count)
        print("Average age of men:", average_age_men)
        print("Percentage with Bachelors:", percentage_bachelors, "%")
        print("Higher education rich:", higher_education_rich, "%")
        print("Lower education rich:", lower_education_rich, "%")
        print("Min work hours:", min_work_hours)
        print("Rich percentage for min workers:", rich_percentage, "%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print("Highest percentage of rich in country:", highest_earning_country_percentage, "%")
        print("Top occupation in India:", top_IN_occupation)

    return {
        "race_count": race_count,
        "average_age_men": average_age_men,
        "percentage_bachelors": percentage_bachelors,
        "higher_education_rich": higher_education_rich,
        "lower_education_rich": lower_education_rich,
        "min_work_hours": min_work_hours,
        "rich_percentage": rich_percentage,
        "highest_earning_country": highest_earning_country,
        "highest_earning_country_percentage": highest_earning_country_percentage,
        "top_IN_occupation": top_IN_occupation,
    }
