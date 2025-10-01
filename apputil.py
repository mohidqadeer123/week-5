import plotly.express as px
import pandas as pd

# Exercise 1
# Analyze Titanic survival patterns by passenger class, sex, and age group.

def family_groups1():
    """
    Group the passengers by family size and passenger class
    """
    # Load Titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    df.columns = df.columns.str.lower()

    # Create family_size column: siblings/spouses + parents/children + passenger
    df['family_size'] = df['sibsp'] + df['parch'] + 1  
    out = (
         df.groupby(['family_size','pclass'])
        .agg(
            n_passengers=('survived', 'size'),
            avg_fare=('fare', 'mean'),
            min_fare=('fare', 'min'),
            max_fare=('fare', 'max')
        )
        .reset_index()  
    )
    # Return a table with these results, sorted so that the values are clear and easy to interpret (for example, by class and then family size).
    return out.sort_values(by=['pclass', 'family_size'])

def last_names():
    """
    extracts the last name of each passenger from the Name column, and returns the count for each last name
    """
    # Load Titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    df.columns = df.columns.str.lower()

    last = df['name'].str.split(',').str[0].str.strip()

    return last.value_counts()

# Create a Plotly visualization in a function named visualize_families() that directly addresses your question. 
def visualize_families():
    # Fixed function call to match the defined function name (family_groups1 instead of family_groups)
    df = family_groups1().copy()
    df['pclass'] = df['pclass'].astype(str)
    fig2 = px.bar(
        df,
        x='family_size',
        y='avg_fare',
        color='pclass',
        barmode='group',
        category_orders={
            'pclass': [1, 2, 3],
        },
        labels={
            'family_size': 'Family Size',
            'avg_fare': 'Average Fare',
            'pclass': 'Passenger Class'
        },
        title='Average fare paid by class and family size'
    )
    return fig2
