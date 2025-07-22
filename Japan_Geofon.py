import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://geofon.gfz.de/eqinfo/list.php?datemin=2025-04-16&datemax=2025-07-16&latmax=46&lonmin=123&lonmax=146&latmin=24&magmin=4.0&fmt=html&nmax=1000"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
#finding mag
total_mag = []
find_mag = soup.find_all("span",{'class':"magbox"})
for mag in find_mag:
    total_mag.append(mag.text.strip())
#finding locations
total_loc = []
find_loc = soup.find_all("strong")
for loc in find_loc:
    total_loc.append(loc.text.strip())
#finding and cleaning time
temp_time = []
findtime = soup.find_all("div",{'class':"col-xs-12"})
for time in findtime:
    temp_time.append(time.text.strip())
total_time = []
for time in temp_time:
    if "\n" in time:
        time = total_time.append(time.split("\n")[0])
total_time.pop(0)
total_time.pop(0)
total_time.pop(0)
total_time.pop(161)
#finding and cleaning depth
temp_depth = []
find_depth = soup.find_all("span",{'class':"pull-right"})
for depth in find_depth:
    temp_depth.append(depth.text.strip())
temp_depth.pop(0)
temp_depth.pop(0)
temp_depth.pop(0)
temp_depth.pop(161)
total_depth = []
for depth in temp_depth:
    depth = total_depth.append(depth.split("*")[0])

data = {'mag': total_mag,'place': total_loc, 'time': total_time, 'depth': total_depth}
df = pd.DataFrame(data)
df.to_csv('C:/Users/Yahoo/Desktop/Bootcamp HW/Project2/JAPAN_GEOFON.csv', index=False, encoding='utf-8')
