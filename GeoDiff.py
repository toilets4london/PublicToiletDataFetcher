import PublicToiletCSVParser as loo_data
import MapPlotter as mp
import JsonParser as jp
import geopy.distance


def dist(p1,p2):
    return geopy.distance.distance(p1,p2).km


def diff(set1,set2):
    s1 = set1.copy()
    s2 = set2.copy()
    both = []
    for p1 in s1:
        for p2 in s2:
            if dist(p1,p2) < 0.01:
                both.append(p1)
                s1.remove(p1)
                s2.remove(p2)
    return {'1': s1, '2': s2, 'both': both}


def plot_camden_london_diff():
    camden_toilets = loo_data.read_camden_data()
    camden_toilet_coords = [(float(t[loo_data.LATITUDE]), float(t[loo_data.LONGITUDE])) for t in camden_toilets]
    all_toilet_coords = jp.read_json_coords(path_to_json_data="Data/data.json")
    d = diff(camden_toilet_coords, all_toilet_coords)
    mp.plot_multiple_sets([d['1'], d['2'], d['both']], ['1', '2', 'both'])

plot_camden_london_diff()