import streamlit as st

def app(): 
    # Row 1: Title and Date
    st.header("PortAventura World Park Info")
    st.markdown("""
        <div style="grid-column: 4; text-align: right;">
            <h3>Date</h3>
            <p>2024-02-21</p>
        </div>
    """, unsafe_allow_html=True)

    # Row 3: Park Capacity
    st.subheader("Park Capacity")
    park_capacity_percentage = 75  # Example percentage
    st.metric(label="Capacity", value=f"{park_capacity_percentage}%", delta=0)

    # Row 5: Weather
    st.subheader("Weather")
    weather_temperature = 25  # Example temperature in Celsius
    st.metric(label="Temperature", value=f"{weather_temperature}°C", delta=0)

    # Row 7: Ride Information Subtitles
    st.subheader("Ride Information")

    # Row 8: Ride Information Grid
    # Define ride details for 10 rides
    ride_data = [
        {"name": f"Ride {i+1}", "waiting_time": (i+1) * 10, "status": "Operational" if (i+1) % 2 == 0 else "Maintenance"}
        for i in range(10)
    ]

    # Define CSS for grid layout with visible grid lines
    grid_css = """
        .ride-info-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            border: 1px solid #d3d3d3;  /* Light gray border */
            padding: 8px;
            background-color: rgba(64, 64, 64, 0.5);  /* Semi-transparent white background */
            z-index: 1;  /* Ensure text appears above the grid */
        }
    """
    st.markdown(f"<style>{grid_css}</style>", unsafe_allow_html=True)

    # Display ride information in a grid format
    for ride in ride_data:
        st.write(f"<div class='ride-info-grid'>"
                 f"<div><b>{ride['name']}</b></div>"
                 f"<div><b>Waiting Time:</b> {ride['waiting_time']} minutes</div>"
                 f"<div><b>Status:</b> {ride['status']}</div>"
                 f"</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    app()