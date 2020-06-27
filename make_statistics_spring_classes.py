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

SPRING_CLASS_PATH = 'spring_charged_class/'
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['SimHei']

df = pd.read_csv("gsx_classes.csv", encoding='utf-8-sig', engine='c')
df = df [df['price'] != 0]

#print('1月报名课程：',df [df['introduction'].str.startswith('01月', na=False) | df['introduction'].str.startswith('2020年01月', na=False)].shape[0])
#print('2月报名课程：',df [df['introduction'].str.startswith('02月', na=False) | df['introduction'].str.startswith('2020年02月', na=False)].shape[0])
#print('3月报名课程：',df [df['introduction'].str.startswith('03月', na=False) | df['introduction'].str.startswith('2020年03月', na=False)].shape[0])
print('4月报名课程：',df [df['introduction'].str.startswith('04月', na=False) | df['introduction'].str.startswith('2020年04月', na=False)].shape[0])
print('5月报名课程：',df [df['introduction'].str.startswith('05月', na=False) | df['introduction'].str.startswith('2020年05月', na=False)].shape[0])
#print('6月报名课程：',df [df['introduction'].str.startswith('06月', na=False) | df['introduction'].str.startswith('2020年06月', na=False)].shape[0])
df = df [df['introduction'].str.startswith('04月', na=False) | df['introduction'].str.startswith('2020年04月', na=False) \
          | df['introduction'].str.startswith('05月', na=False) | df['introduction'].str.startswith('2020年05月', na=False) ]
df.to_csv(SPRING_CLASS_PATH+"df_april_may.csv",encoding='utf-8-sig',index=False)
       
grouped =df.groupby(['grade'])
largest_count = 0
list_tmp = []
for name, group in grouped:
    print('name',name)
    str_name = str(name)
    df_grade_subject = group
    fig1 = plt.figure(0,figsize=(12, 12))
    plt.ylabel(u'enrolled_count')
    plt.title('Grade'+str_name+'_enrolled_count')
    grouped_clazz_id = df_grade_subject.groupby('clazz_id')
    for name_clazz_id, df_clazz_id in grouped_clazz_id:        
        print(df_clazz_id.head())        
        print('plot ' + df_clazz_id.iat[0,1] + df_clazz_id.iat[0,10] + df_clazz_id.iat[0,14])
        xs = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S').date() for d in df_clazz_id['snapshot_time']]
        p1=plt.plot(xs,df_clazz_id['enrolled_count'],label=str(name_clazz_id) + df_clazz_id.iat[0,10] + df_clazz_id.iat[0,14])
        list_tmp.append([name_clazz_id,df_clazz_id.iat[0,1],df_clazz_id.iat[0,10],df_clazz_id.iat[0,14],df_clazz_id.iat[0,4],df_clazz_id.iat[0,15],df_clazz_id.iat[df_clazz_id.shape[0]-1,15],df_clazz_id.iat[0,2],df_clazz_id.iat[df_clazz_id.shape[0]-1,2]])
    axes = plt.gca()
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.legend(loc='upper right',fontsize='x-large',framealpha=0.5)    
    fig1.savefig(SPRING_CLASS_PATH+str_name+'_enrolled_count.png')
    plt.close(0)
           
           
df_per_class_snapshot_duration = pd.DataFrame(list_tmp,columns=['clazz_id','title','introduction','teacher_name', 'price','first_snapshot_time','last_snapshot_time','first_snapshot_enrollment','last_snapshot_enrollment'])
df_per_class_snapshot_duration['enrollment_growth'] = df_per_class_snapshot_duration.last_snapshot_enrollment - df_per_class_snapshot_duration.first_snapshot_enrollment
df_per_class_snapshot_duration = df_per_class_snapshot_duration.sort_values(by = ['last_snapshot_time'],ascending = [True])
df_per_class_snapshot_duration.to_csv(SPRING_CLASS_PATH+"df_per_class_snapshot_duration_orderby_last_snapshot_time.csv",encoding='utf-8-sig',index=False)    
df_per_class_snapshot_duration = df_per_class_snapshot_duration.sort_values(by = ['first_snapshot_time'],ascending = [True])
df_per_class_snapshot_duration.to_csv(SPRING_CLASS_PATH+"df_per_class_snapshot_duration_orderby_first_snapshot_time.csv",encoding='utf-8-sig',index=False)    
fig1 = plt.figure(0,figsize=(12, 12))
plt.xlabel(u'class enrollment growth')
plt.ylabel(u'met classes')
y_major_locator=MultipleLocator(10)
ax=plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.title('Distribution of class enrollment growth count')
n, bins, patches = plt.hist(df_per_class_snapshot_duration['enrollment_growth'],bins=20)
txt = 'enrollment_growth_sum:'+str(df_per_class_snapshot_duration['enrollment_growth'].sum())
plt.text(120, 120, txt, fontsize=15,verticalalignment="top",horizontalalignment="right")
fig1.savefig(SPRING_CLASS_PATH+'Distribution of class enrollment growth count.png')
plt.close(0)
print('enrollment_growth sum:'+str(df_per_class_snapshot_duration['enrollment_growth'].sum()))
print('last_snapshot_enrollment sum:'+str(df_per_class_snapshot_duration['last_snapshot_enrollment'].sum()))
df_filter = df_per_class_snapshot_duration[df_per_class_snapshot_duration['enrollment_growth']>=500].sort_values(by = ['enrollment_growth'],ascending = [False])
df_filter.to_csv(SPRING_CLASS_PATH+"top_enrollment_growth_teachers.csv",encoding='utf-8-sig',index=False)
