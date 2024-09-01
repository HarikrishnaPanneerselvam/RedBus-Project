from matplotlib import pyplot as plt
import pandas as pd
import mysql.connector
from tabulate import tabulate
import streamlit as st

# Establish a connection to your MySQL database
cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Hari@4444",
    database="redbus"
)

# Create a cursor object
cursor = cnx.cursor()

# Create a title for the page
st.title("RedBus Project")

# Create a sidebar container
with st.sidebar:


    # Attach the logo image to the side bar container
    st.sidebar.image(r"C:\Users\USER\Desktop\RedBusProject\th.jpg", width=300)
    st.sidebar.markdown("<h1 style='text-align: center'>RedBus Project</h1>", unsafe_allow_html=True)

    # Add a header to the sidebar
    st.header("Navigation")
    
    # Create a button for each page
    page = st.selectbox("Choose a page", ["Home", "Bus Routes", "Analysis"])


# Use a conditional statement to display the selected page
if page == "Home":
    st.write("Welcome to the home page!")

    st.subheader("Project Overview")
    st.write("This project aimed to extract relevant data from the Redbus website using the Selenium web scraping framework, store the extracted data in a MySQL database, and then present the data in a user-friendly interface using the Streamlit web application framework.")
    st.subheader("Objectives")
    st.subheader("Data Extraction:")
    st.write(" Scrape bus information, including bus number, departure/arrival time, price, and availability, from the Redbus website.")
    st.subheader("Data Storage:")
    st.write(" Store the extracted data in a MySQL database for efficient retrieval and analysis.")
    st.subheader("Data Visualization:")
    st.write(" Create a Streamlit application to visualize the extracted data in an interactive and informative manner.")
elif page == "Bus Routes":
    # Query to fetch DepartureCity column from the database
    query = "SELECT DISTINCT DepartureCity FROM bus_detail"

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    departure_cities = [row[0] for row in cursor.fetchall()]

    # Create a selectbox with the departure cities
    selected_city = st.selectbox("Choose a departure city", departure_cities)

    # Display the selected city
    st.write(f"You selected: {selected_city}")

    # Query to fetch Destination column from the database
    query = "SELECT DISTINCT Destination FROM bus_detail"

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    destinations = [row[0] for row in cursor.fetchall()]

    # Create a selectbox with the destinations
    selected_destination = st.selectbox("Choose a destination", destinations)

    # Display the selected destination
    st.write(f"You selected: {selected_destination}")

    # Create a selectbox for price
    price_options = ["Filter Off", "Under 200", "200-500", "500-1000", "Above 1000"]
    selected_price = st.selectbox("Choose a price range", price_options)

    # Display the selected price
    st.write(f"You selected: {selected_price}")

    # Create a selectbox for bus rating
    rating_options = ["Filter Off", "3-4", "4-5"]
    selected_rating = st.selectbox("Choose a bus rating", rating_options)

    # Display the selected rating
    st.write(f"You selected: {selected_rating}")

    # Create a selectbox for start time
    time_options = ["Filter Off", "04:00-12:00", "12:00-17:00", "17:00-21:00", "21:00-04:00"]
    selected_time = st.selectbox("Choose a start time range", time_options)

    # Display the selected time
    st.write(f"You selected: {selected_time}")

    # Query to fetch the matched values based on the selected city, destination, price, rating, and start time
    query = """
        SELECT *
        FROM bus_detail
        WHERE DepartureCity = %s AND Destination = %s
    """
    params = (selected_city, selected_destination)

    conditions = []

    if selected_price != "Filter Off":
        if selected_price == "Under 200":
            conditions.append("Price < 200")
        elif selected_price == "200-500":
            conditions.append("Price BETWEEN 200 AND 500")
        elif selected_price == "500-1000":
            conditions.append("Price BETWEEN 500 AND 1000")
        elif selected_price == "Above 1000":
            conditions.append("Price > 1000")

    if selected_rating != "Filter Off":
        if selected_rating == "3-4":
            conditions.append("Bus_Rating BETWEEN 3 AND 4")
        elif selected_rating == "4-5":
            conditions.append("Bus_Rating BETWEEN 4 AND 5")

    if selected_time != "Filter Off":
        if selected_time == "04:00-12:00":
            conditions.append("Start_Time BETWEEN '04:00:00' AND '12:00:00'")
        elif selected_time == "12:00-17:00":
            conditions.append("Start_Time BETWEEN '12:00:00' AND '17:00:00'")
        elif selected_time == "17:00-21:00":
            conditions.append("Start_Time BETWEEN '17:00:00' AND '21:00:00'")
        elif selected_time == "21:00-04:00":
            conditions.append("(Start_Time BETWEEN '21:00:00' AND '23:59:59' OR Start_Time BETWEEN '00:00:00' AND '04:00:00')")

    if conditions:
        query += " AND " + " AND ".join(conditions)

    # Execute the query
    cursor.execute(query, params)

    # Fetch the results
    matched_values = cursor.fetchall()

    # Get the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Create a DataFrame from the matched values
    df = pd.DataFrame(matched_values, columns=column_names)
        

    # Display the matched values in a table format
    st.write("Matched Values:")
    st.table(df)
elif page == "Analysis":
    st.subheader("Redbus Data Analysis")

    import plotly.graph_objs as go
    import pandas as pd

    # Fetch the data from the MySQL table
    query = "SELECT Price, Bus_Rating FROM bus_detail"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(rows, columns=['Price', 'Bus_Rating'])

    # Plot the scatter plot
    fig = go.Figure(data=[go.Scatter(x=df['Price'], y=df['Bus_Rating'], mode='markers')])
    fig.update_layout(title='Scatter Plot of Price vs Bus Rating', xaxis_title='Price', yaxis_title='Bus Rating')

    # Display the plot in the Streamlit app
    st.plotly_chart(fig)
    st.write("The scatter plot shows the relationship between the price of a bus and its rating. It can be observed that most buses are priced under 2000 and have a rating between 3 to 4. A few buses are priced higher with a rating between 3 to 4. There is a bus with a rating of 3.5 which is priced at almost 9000.")

# Close the cursor and connection
cursor.close()

cnx.close()