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
    grouped_obs = (
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
