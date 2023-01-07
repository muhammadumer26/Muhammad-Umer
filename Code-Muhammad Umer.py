#!/usr/bin/env python
# coding: utf-8

# # Cradle-to-Gate Life Cycle Assessment for Geopolymer Concrete

# The purpose of this LCA is to

# 1- identify the most critical process (that has principal contribution in more impact categories) with less effort, less time and more accuracy, as compared to traditional stacked bar charts

# 2- Coalesce midpoint, endpoint LCA's, and process contributions in a visually appealing way to summarize LCA results (also usefull for posters and graphical abstracts of scientific publications)

# In[1]:


import pandas as pd
import uuid
import math
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
from matplotlib import rcParams
import matplotlib.patches as mpatches
import seaborn as sns
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "plotly_mimetype+notebook"
import plotly.graph_objects as go
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')


# # Goal and Scope

# The goal of this LCA is to identify the most critical process contributing to the environmental impacts of geopolymer concrete.
# The functional unit is 1m3 of concrete.
# The cradle-to-gate system boundary is selected and is presented in figure below.

# In[2]:


from PIL import Image
img = Image.open('Sys Boundary.jpg')
img


# # Life Cycle Inventory Analysis

# In[3]:


geopolymer_data = pd.read_csv('geopolymer.csv')
print("The testing matrix has been taken from experimental work by us in the lab")
geopolymer_data


# In[4]:


pip install -U olca-ipc


# In[5]:


cd C:\Users\HP\Downloads\olca-ipc.py-master


# In[6]:


import olca

params = {'mathtext.default': 'regular' }

client = olca.Client(8080)
client


# In[7]:


dt_object = datetime.fromtimestamp(datetime.timestamp(datetime.now()))


# In[8]:


#creating flows
volume = client.find(olca.FlowProperty, 'Volume')

geopolymer = olca.product_flow_of('geopolymer', volume)
geopolymer
geopolymer.description = '1 m3 Geopolymer concrete added via olca-ipc on %s.' % (dt_object)
client.insert(geopolymer) 


# In[9]:


geopolymer_data['flow'][0]
geopolymer


# In[10]:


mass = client.find(olca.FlowProperty, 'Mass')
x = [0,1,2,3,4,5]

for a in x:
    flow_name = geopolymer_data['flow'][a]
    print(flow_name)
    flow_name = olca.product_flow_of(geopolymer_data['flow'][a], volume)
    flow_name.description = 'flow for', geopolymer_data['flow'][a],'added via olca-ipc on %s.' % (dt_object)
    client.insert(flow_name) 
flow_name


# In[11]:


#Creating Processes
dt_object = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
x=[0,1,2,3,4,5,6,7]

for a in x:
    process_name = geopolymer_data['flow'][a]
    print(process_name)
    process_name = olca.process_of(geopolymer_data['flow'][a])
    process_name.description = 'Added via olca-ipc on %s.' % (dt_object)
    client.insert(process_name)
process_name
    


# In[12]:


#adding input/output flows in the geopolymer process 

target_refs = []

for a in x:
    all_obj = client.get_descriptors(olca.Flow)
    cache = [obj for obj in all_obj if geopolymer_data['flow'][a] == obj.name]
    target_refs.append(cache)


# In[13]:


process_descriptor = client.get_descriptors(olca.Process)
process_list = []
id_list = []

for process in process_descriptor:
    process_list.append(process.name)
    id_list.append(process.id)

processes_df = pd.DataFrame(list(zip(process_list,
                                   id_list)),
                            columns=['name', 'id'])
processes_df


# In[14]:


#creating product systems
product_system = client.create_product_system(processes_df['id'][processes_df.last_valid_index()],
                                              default_providers='prefer',
                                              preferred_type='UNIT_PROCESS')


# In[15]:


psID = product_system.id
psID


# # Life Cycle Impact Assessments

# The LCIA can be performed by clicking "quick calculations" button in OpenLCA, available on the product system that has been created with jupyter

# In[16]:


cd


# In[17]:


LCIA_results= pd.read_csv('LCIA.csv')
LCIA_results


# In[18]:


process_contributions= pd.read_csv('process_contribution.csv')
process_contributions


# # Interpretation/Visualization

# Visualization 1:

# This visualization indicates the most critical process (that has prinicpal contribution in more impact categories)

# The traditional stacked bar chats used in LCA visualization are intricate to analyze the most critical product and more often than not, the conclusions drawn are not accuate. For example, previously it was concluded that activators are the most critical process in impacts of geopolymer concrete, whereas this visualization indicates that both activators and fly ash are principal contributors in 3 imapct categoies, and therefore both should be deemed as critical processes

# In[19]:


label = ["Activator", "GGBFS", "Fly Ash",  "Activator", "GGBFS", "Fly Ash",  "Activator", "Fly Ash", "GGBFS", "Fly Ash", "GGBFS", "Activator", "Fly Ash", "Activator", "GGBFS", "Activator", "Fly Ash", "GGBFS"]
source = [0,0,0, 1,1,1, 2,2,2, 3,3,3, 4,4,4, 5,5,5, 6,6,6, 7,7,7, 8,8,8, 9,9,9, 10,10,10, 11,11,11, 12,12,12, 13,13,13, 14,14,14]  #3 source nodes
target = [3,4,5, 3,4,5, 3,4,5, 6,7,8, 6,7,8, 6,7,8, 9,10,11, 9,10,11,  9,10,11, 12,13,14, 12,13,14, 12,13,14, 15,16,17, 15,16,17, 15,16,17]  # 4 target nodes 
value = [1,0,0, 0,1,0, 0,0,1, 1,0,0, 0,0,1, 0,1,0, 0,0,1, 1,0,0, 0,1,0, 1,0,0, 0,0,1, 0,1,0, 0,1,0, 1,0,0, 0,0,1]
link = dict(source=source, target=target, value=value, color = ['rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)','rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)', 'rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)','rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)',
          'rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)', 'rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)','rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)',
         'rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)','rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)', 'rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(230, 126, 34,0.5)','rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)','rgba(52, 152, 219,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)','rgba(34, 153, 84,0.5)'],)
node = dict(label=label, x=[0.1,0.1,0.1, 0.25,0.25,0.25, 0.4,0.4,0.4, 0.55,0.55,0.55, 0.7,0.7,0.7, 0.85,0.85,0.85], y= [0.1,0.5,0.9, 0.9,0.5,0.1, 0.1,0.5,0.9, 0.1,0.5,0.9, 0.1,0.5,0.9, 0.1,0.5,0.9] ,pad = 0, thickness = 60, color = ['#FF7F50','#2ECC71','#6495ED', '#FF7F50','#2ECC71','#6495ED', '#FF7F50','#6495ED','#2ECC71', '#6495ED','#2ECC71','#FF7F50', '#6495ED','#FF7F50','#2ECC71', '#FF7F50','#6495ED','#2ECC71'])
data= go.Sankey(link=link, node=node)
fig = go.Figure(data)
fig.update_layout(
    hovermode = 'x',
    font=dict(size = 10, color = 'black')
)
fig.add_annotation(
    x= 0.1,
    y=1.065,
    text = "Climate Change",
    font=dict(size = 12, color = 'black')
)
fig.add_annotation(
    x= 0.25,
    y=1.065,
    text = "Ionizing Radiation",
    font=dict(size = 12, color = 'black')
)
fig.add_annotation(
    x= 0.4,
    y=1.065,
    text = "Ozone Depletion",
    font=dict(size = 12, color = 'black')
)
fig.add_annotation(
    x= 0.55,
    y=1.065,
    text = "Particulate Matter",
    font=dict(size = 12, color = 'black')
)
fig.add_annotation(
    x= 0.7,
    y=1.065,
    text = "Acidification",
    font=dict(size = 12, color = 'black')
)
fig.add_annotation(
    x= 0.85,
    y=1.065,
    text = "Eutrophication",
    font=dict(size = 12, color = 'black')
)

fig.show()


# Visualization 2:

# This visualization coalesce midpoint lca, endpoint lca and process contributions in a visually appealing way to summarize lca in one figure (also usefull in posters and graphical abstracts of scientific publications)

# In[20]:


label = ["Gravel", "Sand", "Fly ash", "GGBFS", "Sodium Silicate", "Sodium Hydroxide", "Climate Change", "Ozone Depletion", "Particulate Matter Formation", "Acidification", "Ecosystem Quality", "Human Health", "Resources"]
source = [0,0,0,0, 1,1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4, 5,5,5,5, 6,6,6, 7,7,7, 8,8,8, 9,9,9]  #3 source nodes
target = [6,7,8,9, 6,7,8,9, 6,7,8,9, 6,7,8,9, 6,7,8,9,  6,7,8,9, 10,11,12, 10,11,12, 10,11,12, 10,11,12 ]  # 4 target nodes 
value = [6,2,4,0.5, 3,1,2,0.3, 12,3,84,63, 15,40,6,13, 26,25,1,1, 38,29,1,20, 30,35,23, 12,35,32, 20,32,0, 30,0,0]
link = dict(source=source, target=target, value=value)
node = dict(label=label, pad = 35, thickness = 50)
data= go.Sankey(link=link, node=node)


# In[21]:


fig = go.Figure(data)
fig.update_layout(
    hovermode = 'x',
    font=dict(size = 12, color = 'black')
)
fig.add_annotation(
    x= 0.03,
    y=1,
    text = "Processes",
    font=dict(size = 15, color = 'black')
)
fig.add_annotation(
    x= 0.5,
    y=0.82,
    text = "Midpoint LCA",
    font=dict(size = 15, color = 'black')
)
fig.add_annotation(
    x= 0.97,
    y=0.62,
    text = "Endpoint LCA",
    font=dict(size = 15, color = 'black')
)
fig.show()


# # Acknowledgments

# I would like to thank Mr. Julian Rickert for his amazing tutorials in integrating open LCA and Jupyter Notebooks

# I am gratefull to open LCA for providing open source software license

# I thank ecoinvent for providing academic license of ecoinvent database
