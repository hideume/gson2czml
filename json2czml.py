# coding:utf-8
import simplejson

'''
 geojson to czml
'''
class json2czml():
    def __init__(self):
        self.col="[255,255,0,128]"
    def setColor(self,str):
        self.col=str
    def load(self,fname):
        f=open(fname)
        jsn=simplejson.load(f)
        pkey=jsn['features'][0]['properties'].keys()
        out={'coordinates':[]}
        for k in pkey:
            out[k]=[]
        i=0
        for c in jsn['features']:
            #polygonもmultiPolygonも同じに加工
            if(c['geometry']['type']=='Polygon'):
                out['coordinates'].append([c['geometry']['coordinates'],[]])
            else:
                out['coordinates'].append(c['geometry']['coordinates'])
            for p in pkey:
                out[p].append(c['properties'][p])
        return out

    def check(self,dt,i,check):
        for k in check.keys():
            if(not(k in dt.keys())):
                print "check keys (%s) is not exist in json" % k
                exit()
            if(dt[k][i]!=check[k]):
                return True
        return False

    def to_czml(self,fname,checkag={}):
        c=self.load(fname)
        cz='''
        [{ "id":"document",
          "version":"1.0"
        }'''
        xx=0
        for ln in c['coordinates']:
            if(self.check(c,xx,checkag)):
                continue
            st=',{"id":"k%s"' % xx
            st+=''',"polygon":
            { "show": true
            ,"fill": true
            ,"material":
                { "solidColor":{'''
            st+='"color":{"rgba":%s}' % self.col
            st+=''' 
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

