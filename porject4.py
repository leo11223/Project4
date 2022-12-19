import pandas as pd
import streamlit as st
import plotly_express as px
import statistics as stat
df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])
#For is_4wd, 1 means is and NaN means not, change Nan to 0. Fix datatype to int as well.
df['is_4wd'] = df['is_4wd'].fillna(0)
df['is_4wd'] = df['is_4wd'].astype('int')
#Fixing missing value for cylinders, odometer and paint color. 
#fill NAN in model year with median value of year by model since year need to be integer
df['model_year'] = df['model_year'].fillna(df.groupby('model')['model_year'].transform('median'))
df['model_year'] = df['model_year'].astype('int')
#fill missing value in cylinders with median value of cylinders by model for cylinders have to be integers. Then, fix the data type to integer
df['cylinders'] = df['cylinders'].fillna(df.groupby('model')['cylinders'].transform('median'))
df['cylinders'] = df['cylinders'].astype('int')
#fill missing value in color with no_info
df['paint_color'] = df['paint_color'].fillna('no_info')
#For missing value of odometer, fill with mean odometer value by year
df['odometer'] = df['odometer'].fillna(df.groupby('model_year')['odometer'].transform('mean'))
avg = stat.mean(df.loc[df['model'] == 'ford f-150']['odometer'].dropna())
df['odometer'] = df['odometer'].fillna(avg)

# create a text header above the dataframe
st.header('Data viewer') 
# display the dataframe with streamlit
st.dataframe(df)
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

#Transmission vs price
#Data prep for vehicle type and Price. 
df_type_price = df.groupby(['transmission', 'condition', 'is_4wd']).mean('price')
df_type_price = df_type_price.reset_index()

#Header for the graph
st.header('Transmission type and Price')
# Transmission type vs price under different  condition
fig = px.histogram(df_type_price, x='transmission', y='price', color='condition', histfunc='avg')
#display with streamlit
st.write(fig)

#Cylinder vs price
#Data prep for vehicle type and Price. 
df_type_price = df.groupby(['cylinders', 'condition', 'is_4wd']).mean('price')
df_type_price = df_type_price.reset_index()

#Header for the graph
st.header('cylinders and Price')
# Cylinders vs price under different  condition
fig = px.histogram(df_type_price, x='cylinders', y='price', color='condition', histfunc='avg')
#display with streamlit
st.write(fig)