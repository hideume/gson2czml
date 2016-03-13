import simplejson

def load(fname):
    f=open(fname)
    jsn=simplejson.load(f)
    pkey=jsn['features'][0]['properties'].keys()
    out={'coordinates':[]}
    for k in pkey:
        out[k]=[]
    i=0
    for c in jsn['features']:
        if(c['geometry']['type']=='Polygon'):
            out['coordinates'].append([c['geometry']['coordinates'],[]])
        else:
            out['coordinates'].append(c['geometry']['coordinates'])
        for p in pkey:
            out[p].append(c['properties'][p])
    return out

def json2czml(fname):
    c=load(fname)
    cz='''
    [{ "id":"document",
      "version":"1.0"
    }'''
    xx=0
    for ln in c['coordinates']:
        st=',{"id":"k%s"' % xx
        st+=''',"polygon":
        { "show": true
        ,"fill": true
        ,"material":
            { "solidColor":{
             "color":{"rgba":[255,255,0,128]}
                }
            }
          ,"positions": 
          {"cartographicDegrees":['''
        ii=0
        for ln2 in ln[0][0]:
            if(ii==0):
                st+="%f, %f, 0.0\n" % (ln2[0],ln2[1])
            else:
                st+=",%f, %f, 0.0\n" % (ln2[0],ln2[1])
            ii+=1
        st+="]}}}"
        cz+=st
        xx+=1
    return cz+"]"

c=json2czml('tokyo.geojson')
print c
