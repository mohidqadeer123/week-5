import plotly.express as px
import pandas as pd

# Exercise 1
# Analyze Titanic survival patterns by passenger class, sex, and age group.

def survival_demographics():
    """
    Returns a DataFrame with passenger counts, survivors, and survival rates.
    """

   # Load Titanic dataset and standardize column names
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    df.columns = df.columns.str.lower()

    # Drop rows without age (since we need age to form groups)
    df = df.dropna(subset=['age']).copy()

    # Define age bins and labels
    age_bins = [0, 12, 19, 59, float('inf')]
    age_labels = ['Child', 'Teen', 'Adult', 'Senior']

    # Create categorical age group column
    df['age_group'] = pd.cut(
        df['age'],
        bins=age_bins,
        labels=age_labels,
        right=True,
        include_lowest=True
    )

    # Aggregate actual passenger counts and survivors
    grouped = (
        df.groupby(['pclass', 'sex', 'age_group'])
        .agg(
              n_passengers=('survived', 'size'),
              n_survivors=('survived', 'sum')
            ) 
        .reset_index()
    )

    # Build all possible combinations (3 classes × 2 sexes × 4 age groups = 24 rows)
    all_combos = pd.DataFrame(
        [(c, s, a) for c in [1, 2, 3] 
                   for s in ['female', 'male'] 
                   for a in age_labels],
        columns=['pclass', 'sex', 'age_group']
    )

    # Ensure column types match
    all_combos['pclass'] = all_combos['pclass'].astype(int)
    grouped_obs['pclass'] = grouped_obs['pclass'].astype(int)

    # Merge observed data with all possible combinations
    grouped = all_combos.merge(grouped_obs, on=['pclass', 'sex', 'age_group'], how='left')

    # Fill missing values with zeros
    grouped[['n_passengers', 'n_survivors']] = (
        grouped[['n_passengers', 'n_survivors']].fillna(0).astype(int)
    )

    # Calculate survival rate
    grouped['survival_rate'] = grouped['n_survivors'] / grouped['n_passengers']
    grouped['survival_rate'] = grouped['survival_rate'].fillna(0.0)

    # Ensure proper ordering of age groups
    grouped['age_group'] = pd.Categorical(grouped['age_group'], categories=age_labels, ordered=True)

    # Sort results for readability
    grouped = grouped.sort_values(by=['pclass', 'sex', 'age_group'])

    return grouped

    # Create a Plotly visualization in a function named visualize_demographic() that directly addresses your question by returning a Plotly figure (e.g., fig = px. ...).

 def visualize_demographic():
     '''
    Returns ploty figure for question

    '''
    df = survival_demographics()
    fig = px.bar(
        df,
        x='age_group',
        y='survival_rate',
        color='sex',
        barmode='group',
        facet_col='pclass',
        category_orders={
        'age_group': ['Child', 'Teen', 'Adult', 'Senior'],
        'pclass': [1, 2, 3],
        },
        labels={
            'age_group': 'Age Group',
            'survival_rate': 'Survival Rate',}
        )

    return fig

# Exercise 2
# Using the Titanic dataset, write a function named family_groups() to explore the relationship between family size, passenger class, and ticket fare.

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

    df = family_groups().copy()
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
    
