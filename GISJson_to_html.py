import pydeck as pdk
import json


if __name__ == '__main__':
    # DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json" #can use this syntax to load from url
    json_file_path = 'vancouver-blocks.json'
    with open(json_file_path) as file:
        DATA = json.load(file)


    INITIAL_VIEW_STATE = pdk.ViewState(latitude=49.254, longitude=-123.13, zoom=11, max_zoom=16, pitch=45, bearing=0) #Settings for Vancouver BC
    # INITIAL_VIEW_STATE = pdk.ViewState(latitude=42.96, longitude=-85.67, zoom=11, max_zoom=16, pitch=45, bearing=0) #settings for GrandRapids MI

    polygon = pdk.Layer(
        "PolygonLayer",
        stroked=False,
        # processes the data as a flat longitude-latitude pair
        get_polygon="-",
        get_fill_color=[0, 0, 0, 20],
    )

    geojson = pdk.Layer(
        "GeoJsonLayer",
        DATA,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation="properties.valuePerSqm / 100", # Vancouver BC settings
        #get_elevation="properties.Taxable_Value / (properties.GIS_Acres * 1000)", # #settings for GrandRapids MI
        # get_fill_color="[0, 255, 255]", #Use to set color of parcels to constant value
        get_fill_color=""
                       "properties.valuePerSqm == 0.0 ? [175,171,171]:"
                       "properties.valuePerSqm < 1000 ? [162,58,51]:"
                       "properties.valuePerSqm < 2000 ? [223,157,152]:"
                       "properties.valuePerSqm < 3000 ? [159,153,187]:"
                       "properties.valuePerSqm < 4000 ? [141,190,239]:"
                       "properties.valuePerSqm < 5000 ? [122,170,177]:"
                       "properties.valuePerSqm < 10000 ? [102,149,115]:"
                       "properties.valuePerSqm < 20000 ? [83,129,53]:"
                       "[255,127,0]"
                       "", #Set parcels based on value range
        get_line_color=[255, 255, 255],
    )

    r = pdk.Deck(layers=[polygon, geojson], initial_view_state=INITIAL_VIEW_STATE)

    r.to_html("geojson_layer.html")