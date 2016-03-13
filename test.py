from json2czml import json2czml
c=json2czml()
c.setColor("[0,255,0,255]")
print c.to_czml('tokyo.geojson',{'area_en':'Tokubu'})
