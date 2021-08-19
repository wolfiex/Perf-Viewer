import re,json
import pandas as pd

data = open('data.txt','r').read().split('\n')

desc = ''
nodez = []
linkd = []

dummy = []


spaced = re.compile('\s+')
pcs = re.compile('([\d\.]+)%')

for item in data:
    if not item: continue
    
    if item[0] == '#':
        if 'Event count' in item:
            print(item)
            counts = int(re.search('\d+',item).group())
        desc += item + '\n'
        continue
    
    elif item.count('%') == 2:
        print(item)
        percent,name = item.rsplit('[.] ') 
        name = name.split()[0]
        vals = [float(i) for i in pcs.findall(percent)]  
        nodez.append({'id':name,'children':vals[0],'self':vals[1],'shared':spaced.split(percent)[-2] })
        
        
        
        dummy.append(item)
    else:
        time,path = item.split()[:2]
        pc = int(time)/counts
        spath = path.split(';')
        try: target = spath[1].split()[0]
        except: target = name
        linkd.append({'source':name,'target':target,'%':pc,'count':int(time)})
    

nodes = pd.DataFrame(nodez)         
        
links = pd.DataFrame(linkd).groupby(['source','target']).sum().sort_values('%',ascending=False).reset_index()

graph = {'nodes':nodes.T.to_dict(),'links':links.T.to_dict()}

json.dump(graph,open('graph.json','w'))