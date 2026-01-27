import streamlit as st
import pandas as pd
import plotly.express as px
from adops_logic import AdsTxtParser

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AdOps Shield | Validator",
    layout="wide"
)

# --- MAIN HEADER ---
st.title("AdOps Shield: App-Ads.txt Analyzer")
st.markdown("""
Professional tool for validating, analyzing, and visualizing `ads.txt` and `app-ads.txt` files.
Checks for IAB syntax compliance, identifies errors, and visualizes partner distribution.
""")

# --- SIDEBAR (INPUT) ---
with st.sidebar:
    st.header("Data Source")
    input_method = st.radio("Select Method:", ["Load from URL", "Upload File"])
    
    raw_content = None
    source_name = "Unknown"

    if input_method == "Load from URL":
        url_input = st.text_input("Enter Domain or URL", placeholder="example.com")
        if st.button("Fetch Data"):
            if url_input:
                parser = AdsTxtParser()
                with st.spinner('Fetching file...'):
                    content, msg = parser.fetch_from_url(url_input)
                    if content:
                        raw_content = content
                        source_name = msg
                        st.success(f"Successfully loaded from {msg}")
                    else:
                        st.error(f"Error fetching data: {msg}")
    
    else: # File Upload
        uploaded_file = st.file_uploader("Upload .txt file", type="txt")
        if uploaded_file:
            raw_content = uploaded_file.getvalue().decode("utf-8")
            source_name = uploaded_file.name

# --- MAIN LOGIC ---
if raw_content:
    parser = AdsTxtParser()
    df, errors = parser.parse_content(raw_content)
    stats = parser.get_stats(df)

    # --- SECTION 1: KPI METRICS ---
    st.divider()
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    if stats:
        kpi1.metric("Total Lines", stats['total_lines'])
        kpi2.metric("Unique Partners (SSPs)", stats['unique_partners'])
        kpi3.metric("DIRECT", stats['direct_count'])
        kpi4.metric("RESELLER", stats['reseller_count'])

    # --- SECTION 2: VISUALIZATION ---
    st.subheader("Partner Analytics")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Pie Chart: Direct vs Reseller
        if not df.empty:
            fig_pie = px.pie(df, names='Account_Type', title='Account Type Distribution', 
                             color='Account_Type', 
                             color_discrete_map={'DIRECT':'#00CC96', 'RESELLER':'#636EFA'})
            st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Bar Chart: Top 10 Domains
        if not df.empty:
            top_domains = df['Domain'].value_counts().nlargest(10).reset_index()
            top_domains.columns = ['Domain', 'Count']
            fig_bar = px.bar(top_domains, x='Count', y='Domain', orientation='h', 
                             title='Top 10 Advertising Networks (SSPs)',
                             text='Count')
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- SECTION 3: ERROR LOGGING ---
    if errors:
        st.error(f"Syntax Errors Found: {len(errors)}")
        with st.expander("View Error Details"):
            error_df = pd.DataFrame(errors)
            st.dataframe(error_df, use_container_width=True)
    else:
        st.success("No IAB syntax errors found.")

    # --- SECTION 4: DATA EXPLORER ---
    st.divider()
    st.subheader("Data Explorer")
    
    search_term = st.text_input("Search by ID or Domain", "")
    
    if not df.empty:
        if search_term:
            filtered_df = df[
                df['Domain'].str.contains(search_term, case=False) | 
                df['Publisher_ID'].str.contains(search_term, case=False)
            ]
        else:
            filtered_df = df
        
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Download Button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"cleaned_{source_name}.csv",
            mime='text/csv',
        )

elif not raw_content and input_method == "Load from URL":
    st.info("Enter a domain or URL in the sidebar to begin.")
elif not raw_content:
    st.info("Upload an ads.txt file in the sidebar to begin.")
