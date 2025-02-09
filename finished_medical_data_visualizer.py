import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#1. Load the data
df = pd.read_csv("medical_examination.csv")

#2. Add 'overweight' column
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

#3. Normalize cholesterol and glucose
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

#4. Categorical Plot
def draw_cat_plot():
    #5. Melt the DataFrame for categorical plot
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    #6. Group and reformat data
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).size().rename(columns={'size': 'total'})

    #7. Draw the catplot
    fig = sns.catplot(data=df_cat, x='variable', y='total', hue='value', col='cardio', kind='bar').fig

    #8. Save the figure
    fig.savefig('catplot.png')
    return fig

#10. Heat Map
def draw_heat_map():
    #11. Clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    #12. Calculate the correlation matrix
    corr = df_heat.corr()

    #13. Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    #14. Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 8))

    #15. Draw the heat map
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', cmap='coolwarm', square=True, cbar_kws={'shrink': 0.5}, ax=ax)

    #16. Save the figure
    fig.savefig('heatmap.png')
    return fig
