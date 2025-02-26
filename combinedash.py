import pandas as pd
import streamlit as st
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title='Business Insights Dashboard', layout='wide')

# Custom CSS for larger text and better styling
st.markdown(
    """
    <style>
        .big-font {
            font-size:60px !important;
            font-weight: bold;
            color: #0B5394;
        }
        .medium-font {
            font-size:36px !important;
            font-weight: bold;
            color: #0B5394;
            margin-bottom: 10px;
        }
        .card {
            background-color: #E8F5FE;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            color: #0B5394;
            text-align: center;
            font-size: 32px;
        }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar navigation
menu = st.sidebar.radio("Select Dashboard", ["Manufacturing Companies", "Investors"])

if menu == "Manufacturing Companies":
    # Manufacturing Companies Dashboard
    st.markdown('<div class="big-font">Manufacturing Companies</div>', unsafe_allow_html=True)
    
    # Load company data
    file_path_companies = r'C:\Users\EliteBook 840 G4\Downloads\companies_cleaned.xlsx'
    df_companies = pd.read_excel(file_path_companies)

    # Key Metrics as cards
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="card">Total Companies<br>{len(df_companies)}</div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">Total CB BANK COMPANY Value<br>{df_companies["CB BANK COMPANY"].sum():,.0f}</div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card">Top Industry<br>{df_companies["INDUSTRIES"].value_counts().idxmax()}</div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="card">Top City<br>{df_companies["LOCATION"].value_counts().idxmax()}</div>', unsafe_allow_html=True)

    # Visualization: Companies
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="medium-font">Which Cities Host the Most Manufacturing Companies?</div>', unsafe_allow_html=True)
        city_counts = df_companies['LOCATION'].value_counts().reset_index().head(5)
        city_counts.columns = ['City', 'Count']
        city_pie_chart = px.pie(city_counts, names='City', values='Count', color_discrete_sequence=px.colors.sequential.Blues[::-1])
        city_pie_chart.update_layout(title='', font=dict(size=24))
        st.plotly_chart(city_pie_chart)

    with col2:
        st.markdown('<div class="medium-font">Which Companies Generate the Highest CB BANK COMPANY Value?</div>', unsafe_allow_html=True)
        top_cb_df = df_companies[['ORGANIZATION NAME', 'LOCATION', 'INDUSTRIES', 'CB BANK COMPANY']].sort_values(by='CB BANK COMPANY', ascending=False).head(15)
        st.dataframe(top_cb_df.style.background_gradient(cmap='Blues').set_table_styles([{'selector': 'td, th', 'props': [('font-size', '24px')]}]), height=600)

    st.markdown('<div class="medium-font">Which Industries Contribute the Most to CB BANK COMPANY?</div>', unsafe_allow_html=True)
    cb_industry_df = df_companies.groupby('INDUSTRIES')['CB BANK COMPANY'].sum().reset_index().sort_values(by='CB BANK COMPANY', ascending=False).head(20)
    cb_industry_chart = px.bar(cb_industry_df, x='INDUSTRIES', y='CB BANK COMPANY', color='CB BANK COMPANY', color_continuous_scale='Blues')
    cb_industry_chart.update_layout(title='', font=dict(size=24))
    st.plotly_chart(cb_industry_chart)

    st.markdown('<div class="medium-font">Top Companies in Manufacturing-related Industries</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    manufacturing_industries = ['Manufacturing', 'Industrial Manufacturing', 'Machinery Manufacturing']
    for col, industry in zip(cols, manufacturing_industries):
        top_industry_df = df_companies[df_companies['INDUSTRIES'] == industry].sort_values(by='CB BANK COMPANY', ascending=False).head(5)
        if not top_industry_df.empty:
            with col:
                st.markdown(f"<div class='medium-font'>{industry}</div>", unsafe_allow_html=True)
                st.dataframe(top_industry_df[['ORGANIZATION NAME', 'CB BANK COMPANY']].style.background_gradient(cmap='Blues'), height=300, width=400)

elif menu == "Investors":
    # Investor Insights Dashboard
    st.markdown('<div class="big-font">Investors</div>', unsafe_allow_html=True)

    # Load investor data
    file_path_investors = r'C:\Users\EliteBook 840 G4\Downloads\cleaned_investors_list.xlsx'
    df_investors = pd.read_excel(file_path_investors)

    # Key Metrics as cards
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="card">Total Investors<br>{len(df_investors)}</div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">Total Number of Investments<br>{df_investors["NUMBER OF INVESTEMENTS"].sum():,.0f}</div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card">Total Number of Exits<br>{df_investors["NUMBER OF EXITS"].sum():,.0f}</div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="card">Top Country<br>{df_investors["COUNTRY"].value_counts().idxmax()}</div>', unsafe_allow_html=True)

    # Visualization: Side-by-side Top Investors by Investments and Exits
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="medium-font">Who are the Top Investors by Number of Investments?</div>', unsafe_allow_html=True)
        top_investors_df = df_investors[['NAME', 'NUMBER OF INVESTEMENTS', 'COUNTRY']].sort_values(by='NUMBER OF INVESTEMENTS', ascending=False).head(10)
        st.dataframe(top_investors_df.style.background_gradient(cmap='Blues'), height=400)

    with col2:
        st.markdown('<div class="medium-font">Who are the Top Investors by Number of Exits?</div>', unsafe_allow_html=True)
        top_exits_df = df_investors[['NAME', 'NUMBER OF EXITS', 'COUNTRY']].sort_values(by='NUMBER OF EXITS', ascending=False).head(10)
        st.dataframe(top_exits_df.style.background_gradient(cmap='Blues'), height=400)

    # Visualization: Side-by-side Most Common Funding Statuses and Types of Investors
    col3, col4 = st.columns([1, 1])
    with col3:
        st.markdown('<div class="medium-font">What are the Most Common Funding Statuses?</div>', unsafe_allow_html=True)
        funding_status_counts = df_investors['FUNDING STATUS'].value_counts().reset_index()
        funding_status_counts.columns = ['Funding Status', 'Count']
        funding_status_chart = px.pie(funding_status_counts, names='Funding Status', values='Count', color_discrete_sequence=px.colors.sequential.Blues[::-1])
        funding_status_chart.update_layout(title='', font=dict(size=24))
        st.plotly_chart(funding_status_chart)

    with col4:
        st.markdown('<div class="medium-font">What are the Most Common Types of Investors?</div>', unsafe_allow_html=True)
        investor_type_counts = df_investors['INVESTOR TYPE'].value_counts().reset_index().head(5)
        investor_type_counts.columns = ['Investor Type', 'Count']
        investor_type_chart = px.pie(investor_type_counts, names='Investor Type', values='Count', color_discrete_sequence=px.colors.sequential.Blues[::-1])
        investor_type_chart.update_layout(title='', font=dict(size=24))
        st.plotly_chart(investor_type_chart)
