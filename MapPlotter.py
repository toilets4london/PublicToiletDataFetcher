import JsonParser as jp
import folium
import itertools


def get_marker_color(i):
    colors = [
        'red',
        'blue',
        'gray',
        'darkred',
        'lightred',
        'orange',
        'beige',
        'green',
        'darkgreen',
        'lightgreen',
        'darkblue',
        'lightblue',
        'purple',
        'darkpurple',
        'pink',
        'cadetblue',
        'lightgray',
        'black'
    ]
    return colors[i%(len(colors)-1)]


def avg_lat_lon(points):
    ave_lat = sum(p[0] for p in points) / len(points)
    ave_lon = sum(p[1] for p in points) / len(points)
    return [ave_lat, ave_lon]


def plot_points(points,  map_file_name="Data/map.html"):
    my_map = folium.Map(location=avg_lat_lon(points), zoom_start=14)
    for point in points:
        folium.Marker(point,icon=folium.Icon(color='green')).add_to(my_map)
    my_map.save(map_file_name)


def plot_multiple_sets(sets, category_names=None, map_file_name="Data/compare.html"):
    if not category_names:
        category_names = ["Category %d"%i for i in range(1,len(sets)+1)]
    all_points = list(itertools.chain.from_iterable(sets))
    my_map = folium.Map(location=avg_lat_lon(all_points), zoom_start=14)
    for i, point_set in enumerate(sets):
        for point in point_set:
            folium.Marker(point, icon=folium.Icon(color=get_marker_color(i)), popup=category_names[i]).add_to(my_map)
    my_map.save(map_file_name)


def plot_json(path_to_json_data="Data/data.json", map_file_name="Data/map.html"):
    points = jp.read_json_coords(path_to_json_data)
    plot_points(points, map_file_name=map_file_name)


def plot_jsons(paths, map_file_name="Data/compare.html"):
    sets = [jp.read_json_coords(path) for path in paths]
    plot_multiple_sets(sets, map_file_name=map_file_name)


plot_json()