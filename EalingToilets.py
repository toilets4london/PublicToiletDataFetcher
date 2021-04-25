import requests
from bs4 import BeautifulSoup
import json


URL = "https://www.ealing.gov.uk/info/201153/street_care_and_cleaning/200/public_toilets/4"


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('tbody')
    rows = []
    for t in tables:
        rs = t.find_all('tr')
        for i, r in enumerate(rs):
            if i > 0:
                rows.append([[b.replace("*"," ") for b in c.text.replace(" ","*").split()] for c in r.find_all('td')])
    return rows


def html_to_toilets(html):
    """
    Requires filling in lat long manually
    """
    rows = parse(html)[1:]
    toilets = []
    for r in rows:
        t = {}
        t['name'] = 'Community Toilet'
        t['address'] = r[0][0]
        t['opening_hours'] = " ".join(r[0][1:])
        t['wheelchair'] = ('Y' in r[1][0].upper())
        t['baby_change'] = ('Y' in r[2][0].upper())
        t['data_source'] = "www.ealing.gov.uk"
        t['borough'] = 'Ealing'
        t['latitude'] = 0
        t['longitude'] = 0
        toilets.append(t)
    return toilets


def get_ealing_data():
    data = requests.get(URL, verify=False).text
    ts = html_to_toilets(data)
    with open('Data/processed_data_ealing.json', 'w') as dataFile:
        json.dump(ts, dataFile)




# <table class="committee">
# 	<tbody>
# 		<tr>
# 			<td class="tableTitle" scope="col"><strong>Location</strong></td>
# 			<td class="tableTitle"><strong>Disabled facilities&nbsp;</strong></td>
# 			<td class="tableTitle" scope="col"><strong>Baby changing</strong></td>
# 		</tr>
# 		<tr>
# 			<td>Al Panini Caf&eacute;, 58 Broadway, West Ealing<br />
# 			Mon to Sat 7.30am - 7pm, Sun 9am - 5pm</td>
# 			<td>No</td>
# 			<td>No</td>
# 		</tr>
# 		<tr>
# 			<td><span>DH Law Ltd, 130-132 Uxbridge Road, Hanwell<span> </span><br />
# 			Mon to Fri 9.30 am&nbsp;- 5.30 pm. Closed Saturday and Sunday</span></td>
# 			<td>Yes</td>
# 			<td>Yes</td>
# 		</tr>
# 		<tr>
# 			<td>The Lido Centre - 63 Mattock Lane, West Ealing W13 8DJ<br />
# 			Mon to Fri 10am &ndash; 5pm (please note: all visitors must sign in and out).&nbsp;Closed Saturday and Sunday</td>
# 			<td>Yes</td>
# 			<td>No</td>
# 		</tr>
# 		<tr>
# 			<td>Will to Win &ndash; The Lodge, Pitshanger Park, Woodbury Park Road W13 8DJ<br />
# 			Mon to Sun 9am &ndash; 5pm</td>
# 			<td>Yes</td>
# 			<td>Yes</td>
# 		</tr>
# 		<tr>
# 			<td>Will to Win &ndash; Lammas Park, Culmington Road, West Ealing W13 9NJ&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br />
# 			Mon to Thurs 9am &ndash; 9pm&nbsp; | Fri 9am &ndash; 8pm<br />
# 			Sat 8am &ndash; 5pm | Sun 9am &ndash; 5pm</td>
# 			<td>No</td>
# 			<td>No</td>
# 		</tr>
# 		<tr>
# 			<td><span>XXL Restaurant, 4 Ruislip Road, Greenford<br />
# 			Mon to Fri 12pm - 9pm | Sat to Sun 12pm - 10pm</span></td>
# 			<td>No</td>
# 			<td>No</td>
# 		</tr>
# 	</tbody>
# </table>