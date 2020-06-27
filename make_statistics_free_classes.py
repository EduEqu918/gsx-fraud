# -*- coding: utf-8 -*-
import sys
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
from matplotlib.pyplot import MultipleLocator
from matplotlib import rcParams

FREECLASS_PATH = 'freeclass/'

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['SimHei']

df = pd.read_csv("gsx_classes.csv", encoding='utf-8-sig', engine='c')
df = df [df['price'] == 0]
#df.to_csv(FREECLASS_PATH+"df_free_classes.csv",encoding='utf-8-sig',index=False)
grouped =df.groupby(['title_grade','subject_full_name'])
largest_count = 0
list_tmp = []
for name, group in grouped:
    print('name',name)
    str_name = str(name)
    df_grade_subject = group
    fig1 = plt.figure(0,figsize=(12, 12))
    plt.ylabel(u'enrolled_count')
    plt.title(str_name+'_free_class_enrolled_count')
    grouped_clazz_id = df_grade_subject.groupby('clazz_id')
    for name_clazz_id, df_clazz_id in grouped_clazz_id:        
        print(df_clazz_id.head())        
        print('plot ' + df_clazz_id.iat[0,1] + df_clazz_id.iat[0,10] + df_clazz_id.iat[0,14])
        xs = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S').date() for d in df_clazz_id['snapshot_time']]
        p1=plt.plot(xs,df_clazz_id['enrolled_count'],label=str(name_clazz_id)+' '+df_clazz_id.iat[0,1] + df_clazz_id.iat[0,10] + df_clazz_id.iat[0,14])
        list_tmp.append([name_clazz_id,df_clazz_id.iat[0,1],df_clazz_id.iat[0,10],df_clazz_id.iat[0,14],df_clazz_id.iat[0,4],df_clazz_id.iat[0,15],df_clazz_id.iat[df_clazz_id.shape[0]-1,15],df_clazz_id.iat[0,2],df_clazz_id.iat[df_clazz_id.shape[0]-1,2]])
    axes = plt.gca()
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.legend(loc='upper right',fontsize='x-large',framealpha=0.5)   
    plt.tight_layout()
    fig1.savefig(FREECLASS_PATH+str_name+'_free_class_enrolled_count.png')
    plt.close(0)
           
           
df_per_class_snapshot_duration = pd.DataFrame(list_tmp,columns=['clazz_id','title','introduction','teacher_name', 'price','first_snapshot_time','last_snapshot_time','first_snapshot_enrollment','last_snapshot_enrollment'])
df_per_class_snapshot_duration['enrollment_growth'] = df_per_class_snapshot_duration.last_snapshot_enrollment - df_per_class_snapshot_duration.first_snapshot_enrollment
df_per_class_snapshot_duration = df_per_class_snapshot_duration.sort_values(by = ['last_snapshot_time'],ascending = [True])
df_per_class_snapshot_duration.to_csv(FREECLASS_PATH+"df_per_class_snapshot_duration_orderby_last_snapshot_time.csv",encoding='utf-8-sig',index=False)    
df_per_class_snapshot_duration = df_per_class_snapshot_duration.sort_values(by = ['first_snapshot_time'],ascending = [True])
df_per_class_snapshot_duration.to_csv(FREECLASS_PATH+"df_per_class_snapshot_duration_orderby_first_snapshot_time.csv",encoding='utf-8-sig',index=False)    
fig1 = plt.figure(0,figsize=(12, 12))
plt.xlabel(u'class enrollment growth')
plt.ylabel(u'met classes')
y_major_locator=MultipleLocator(10)
ax=plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
x_major_locator=MultipleLocator(5000)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.title('Distribution of class enrollment growth count')
n, bins, patches = plt.hist(df_per_class_snapshot_duration['enrollment_growth'],bins=40)
txt = 'enrollment_growth_sum:'+str(df_per_class_snapshot_duration['enrollment_growth'].sum())
plt.text(80, 120, txt, fontsize=15,verticalalignment="top",horizontalalignment="right")
plt.tight_layout()
fig1.savefig(FREECLASS_PATH+'Distribution of free class enrollment growth count.png')
plt.close(0)
print('enrollment_growth sum:'+str(df_per_class_snapshot_duration['enrollment_growth'].sum()))
print('last_snapshot_enrollment sum:'+str(df_per_class_snapshot_duration['last_snapshot_enrollment'].sum()))
df_filter = df_per_class_snapshot_duration[df_per_class_snapshot_duration['enrollment_growth']>=10000].sort_values(by = ['enrollment_growth'],ascending = [False])
df_filter.to_csv(FREECLASS_PATH+"top_enrollment_growth_teachers.csv",encoding='utf-8-sig',index=False)
#sys.exit()
