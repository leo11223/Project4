import pandas as pd
import streamlit as st
import plotly_express as px
df = pd.read_csv('/vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])
#For is_4wd, 1 means is and NaN means not, change Nan to 0
df['is_4wd'] = df['is_4wd'].fillna(0)
# create a text header above the dataframe
st.header('Data viewer') 
# display the dataframe with streamlit
st.dataframe(df)
st.header('Vehicle types by manufacturer')
# create a plotly histogram figure
fig = px.histogram(df, x='manufacturer', color='type')
# display the figure with streamlit
st.write(fig)
st.header('Histogram of `condition` vs `model_year`')
fig = px.histogram(df, x='model_year', color='condition')
st.write(fig)
st.header('Compare price distribution between manufacturers')
# get a list of car manufacturers
manufac_list = sorted(df['manufacturer'].unique())
# get user's inputs from a dropdown menu
manufacturer_1 = st.selectbox(
                              label='Select manufacturer 1', # title of the select box
                              options=manufac_list, # options listed in the select box
                              index=manufac_list.index('chevrolet') # default pre-selected option
                              )
# repeat for the second dropdown menu
manufacturer_2 = st.selectbox(
                              label='Select manufacturer 2',
                              options=manufac_list, 
                              index=manufac_list.index('hyundai')
                              )
# filter the dataframe 
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]

# add a checkbox if a user wants to normalize the histogram
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay')
# display the figure with streamlit
st.write(fig)

#Header for the graph
st.header('Odometer and Price')
# Odometer vs price under different  condition
fig = px.scatter(df, x='odometer', y='price', color='condition')
#display with streamlit
st.write(fig)

#Data prep
df_year_price = df.groupby(['model_year', 'condition', 'is_4wd']).mean('price')
df_year_price = df_year_price.reset_index()
#Header for the graph
st.header('Model Year and Price')
#checkbox for 4wd or not
test = st.checkbox('4wd', value=True)
if test:
    test_condition = 1
else:
    test_condition = 0
# Odometer vs price under different  condition
df_year_price2 = df_year_price.loc[df_year_price['is_4wd'] == test_condition]
fig = px.histogram(df_year_price2, x='model_year', y='price', color='condition')
#display with streamlit
st.write(fig)