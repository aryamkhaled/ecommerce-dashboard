import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title='E-Commerce Dashboard',
    page_icon='🛍️',
    layout='wide'
)
# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7fa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('E-Commerce Sales Dashboard 🛍️')

st.markdown('**Interactive analysis of online retail data**')

st.divider()

st.sidebar.header('Navigation ')

st.success('Streamlit is working ✅')

st.info('Dashboard will be built step by step 🚧')


#Load Data
@st.cache_data
def load_data():
    df=pd.read_excel('data/Online Retail.xlsx')
    return df

df=load_data()


# Clean data
df = df[df['Quantity'] > 0] 
df = df[df['UnitPrice'] > 0] 
df = df.dropna(subset=['CustomerID'])  

#Dataset Overview
st.subheader('Dataset Overview')
col1,col2=st.columns(2)
col1.metric('Total Rows:',f'{df.shape[0]:,}')
col2.metric('Total Columns:',f'{df.shape[1]}')

# Sidebar Filters
st.sidebar.header('Filters')

countries = ['All'] + sorted(df['Country'].unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", countries)

if selected_country != 'All':
    df = df[df['Country'] == selected_country]
    

# Key Performance Indicators (KPIs)
st.divider()
st.subheader('Key Performance Indicators 📈')
#Calculate KPIs
df['total_sales']=df['Quantity']* df['UnitPrice']
total_sales=df['total_sales'].sum()

total_customers= df['CustomerID'].nunique()

total_orders=df['InvoiceNo'].nunique()

avg_order_value=total_sales/total_orders

#Display KPIs
col1,col2,col3,col4= st.columns(4)

col1.metric('Total Sales',f'{total_sales:,.0f}')
col2.metric('Total Customers',f'{total_customers:,}')
col3.metric('Total Orders',f'{total_orders:,}')
col4.metric('Avg Order Value',f'{avg_order_value:,.2f}')


# Top 10 Products 
st.divider()
st.subheader('Top 10 Products by Quantity')

top_products= df.groupby('Description')['Quantity'].sum().nlargest(10).reset_index()

fig=px.bar(
    top_products,
    x='Quantity',
    y='Description',
    orientation='h',
    color='Quantity',
    color_continuous_scale='Blues',
    #title='Top 10 Products by Quantity'
    
)

fig.update_layout(showlegend=False,height=500)
st.plotly_chart(fig,use_container_width=True)



# Monthly Sales Trend
st.divider()
st.subheader('Monthly Sales Trend')

df['Month']= df['InvoiceDate'].dt.month

monthly_sales= df.groupby('Month')['total_sales'].sum().reset_index()

fig=px.line(
    monthly_sales,
    x='Month',
    y='total_sales',
    markers=True,
   # title='Monthly Sales Trend'
)

fig.update_layout(height=500)
st.plotly_chart(fig,use_container_width=True)

# Sales by Country
if selected_country == 'All':
   st.divider()
   st.subheader('Sales by Country (Top 10)')

   country_sales= df.groupby('Country')['total_sales'].sum().nlargest(10).reset_index()

   fig= px.bar(
      country_sales,
      x='total_sales',
      y='Country',
      orientation='h',
      color='total_sales',
      color_continuous_scale='Teal',
      text='total_sales'
      #color_discrete_sequence=['#2E86AB'] (gradient from light to dark teal),
      #log_x=True (makes small values visible,but harder to read)
    
 )

   fig.update_traces(texttemplate='%{text:,.0f}',textposition='auto')
   fig.update_layout(showlegend=False,height=500,margin=dict(r=100))
   st.plotly_chart(fig,use_container_width=True)


# Top Customers
st.divider()
st.subheader('Top 10 Customers by total spent')

top_customers= df.groupby('CustomerID')['total_sales'].sum().nlargest(10).reset_index()

top_customers['CustomerID']= top_customers['CustomerID'].astype(int).astype(str)

fig= px.bar(
    top_customers,
    x='total_sales',
    y='CustomerID',
    orientation='h',
    color='total_sales',
    color_continuous_scale='Oranges'
    
)

fig.update_layout(showlegend=False,height=500,yaxis=dict(type='category'))
st.plotly_chart(fig,use_container_width=True)


# Sidebar-About
st.sidebar.divider()
st.sidebar.header(" About 📌")
st.sidebar.info(
    """
    **E-Commerce Sales Dashboard**
    
    Interactive analysis of 541,909 transactions from a UK-based online retail store.
    
    **Built with:**
    - Python
    - Streamlit
    - Plotly
    - Pandas
    
    **Author:** Aryam Khaled
    """
)


# Footer
st.divider()
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; color:#7f8c8d;'>
        <p>E-Commerce Sales Dashboard | Built with Streamlit & Plotly </p>
        <p>Created by <b> Aryam Khaled</b> | October 2026 </p>
        </div>
        
    """,
    unsafe_allow_html=True
)
