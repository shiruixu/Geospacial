
# coding: utf-8

# # Object Detection in Point Cloud: Lane Marking

# In[55]:


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from sklearn import linear_model
from sklearn.cluster import KMeans


# -  Data file is then read and each point is converted into (x,y,z,i) coordinates.  

# In[46]:


csv = open('final_project_data/final_project_point_cloud.fuse', 'r')
data=[]
for line in csv:
    ls=line.split(" ")
    data.append([float(ls[0]),float(ls[1]),float(ls[2]),float(ls[3][:-1])])
csv.close()
data=np.array(data)
#print(data)
x, y, z, i = data.T


# In[47]:


plt.hist(i,255)
plt.show()


# In[69]:


# range of  height
range=max(z)-min(z)
minimum=np.median(z)-0.005*range
maximum=np.median(z)+0.02*range
#mean=np.array(z).mean()
#std=np.array(z).std()
road_data=[ ]
for d in data:
    if d[2]>=minimum and d[2]<=maximum:
        road_data.append(d)
road_data=np.array(road_data)
rx, ry, rz, ri = road_data.T
counts=plt.hist(rz, 20,normed=1,color='black',alpha=0.5)
#x=[mean+2*std]*100
#x=np.array(x)
#plt.plot(x)
plt.show()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         


# In[72]:


ax.plot(rx,ry,',')
plt.show()


# In[42]:



# draw pixel picture
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(rx,ry,',')# draw pixel
plt.show()
original=[]
#intensity
si= sorted(i)[int(0.996*len(i)):int(0.9995*len(i))]
minl=min(si)
maxl=max(si)
for i in road_data:
    if i[3]>=minl and i[3]<=maxl:
        original.append(i[:-1])
original= np.array(original)
lx, ly, lz = lane.T
plt.savefig('original.png',dpi=400,bbox_inches='tight')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(rx, ry, ',')
ax.plot(lx, ly, ',', color='red')
plt.savefig('lane_rough.png',dpi=400,bbox_inches='tight')
plt.show()


# - As we ca  see from the picture, there are three lanes, the next step is to seperate lanes

# In[ ]:


kmeans = KMeans(max_iter=500000,n_clusters=3).fit(lane_data)
label = kmeans.labels_

