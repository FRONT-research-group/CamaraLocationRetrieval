import folium
from app.schemas.location_retrieval import Point

def create_map(point_list : list[Point]) -> None:
    """
    Create a folium map with a polygon overlay.
    
    Returns:
        folium.Map: A folium map object with a polygon.
    """
    # Initialize the map centered around Tokyo, Japan
    m = folium.Map(location=[23.75, 37.78], zoom_start=13)

    # # Define the polygon locations
    # locations = [
    #     [35.6762, 139.7795],
    #     [35.6718, 139.7831],
    #     [35.6767, 139.7868],
    #     [35.6795, 139.7824],
    #     [35.6787, 139.7791],
    # ]
    
    locations = [[point.latitude, point.longitude] for point in point_list]

    # Create and add the polygon to the map
    folium.Polygon(
        locations=locations,
        color="blue",
        weight=6,
        fill_color="red",
        fill_opacity=0.5,
        fill=True,
        popup="Greece Athens",
        tooltip="Click me!",
    ).add_to(m)

    m.save("./map.html")

