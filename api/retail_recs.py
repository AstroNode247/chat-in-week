import pandas as pd
import numpy as np

def recommend_stuff(user_id):
    purchase_df = pd.read_csv('../data/kz.csv', dtype={'category_id': 'Int64', 'user_id': 'Int64'})
    product_df = pd.read_csv('../data/product_features.csv')
    
    # Extract user data
    content_user = purchase_df[purchase_df['user_id']==user_id]['product_id'].values
    user_product = product_df[product_df['product_id'].isin(content_user)]

    # Build the user profile
    user_prof = user_product.drop('product_id', axis=1).sum()

    # Create a subset of only the non read books
    non_user_movies = product_df[~product_df['product_id'].isin(user_product['product_id'])]

    # Calculate the dot product between all rows
    user_prof_sim = np.dot(user_prof.values, non_user_movies.drop('product_id', axis=1).values.T)

    # Wrap in a DataFrame for ease of use
    user_prof_sim_df = pd.DataFrame(user_prof_sim, columns=['dot_product'])
    user_prof_sim_df['product_id'] = non_user_movies['product_id']

    # Recommends for user
    recommended_products = user_prof_sim_df.sort_values(by='dot_product', ascending=False)[:10].product_id
    recommended_products = purchase_df[purchase_df['product_id'].isin(recommended_products)].drop_duplicates(subset=['product_id'])
    recommended_products = recommended_products[['brand', 'price', 'category_code']]
    return recommended_products
