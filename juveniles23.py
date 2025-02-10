import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('test1201.csv')

def main():
    # Set Streamlit to wide mode
    st.set_page_config(layout="wide")

    st.title("Season 24 Juveniles")

    # Load the data
    data = load_data()

    # Sidebar filters
    st.sidebar.header("Filters")

    # Filter by archetype
    archetypes = data['archetype'].unique()
    selected_archetypes = st.sidebar.multiselect("Select Archetype(s)", archetypes, default=archetypes)

    # Filter by grade
    grades = data['grade'].unique()
    selected_grades = st.sidebar.multiselect("Select Grade(s)", grades, default=grades)

    # Filter by gender
    genders = data['gender'].unique()
    selected_genders = st.sidebar.multiselect("Select Gender(s)", genders, default=genders)

    # Filter by horse name (search)
    search_horse_name = st.sidebar.text_input("Search by Horse Name")

    # Apply filters
    filtered_data = data[
        (data['archetype'].isin(selected_archetypes)) &
        (data['grade'].isin(selected_grades)) &
        (data['gender'].isin(selected_genders))
    ]

    if search_horse_name:
        filtered_data = filtered_data[filtered_data['horse_name'].str.contains(search_horse_name, case=False, na=False)]

    # Display data
    st.dataframe(filtered_data, use_container_width=True, height=700)

    # Paginate data
    rows_per_page = 50
    total_rows = len(filtered_data)
    total_pages = max((total_rows // rows_per_page) + (total_rows % rows_per_page > 0), 1)

    # Select page
    if total_pages > 1:
        page = st.slider("Page", 1, total_pages, 1)
    else:
        page = 1

    start_row = (page - 1) * rows_per_page
    end_row = start_row + rows_per_page

    # Show paginated data
    st.write(filtered_data.iloc[start_row:end_row])

if __name__ == "__main__":
    main()