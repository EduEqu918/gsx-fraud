# -*- coding: utf-8 -*-
import sys
import os
import pandas as pd
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import MultipleLocator
from matplotlib import rcParams
import bisect

from matplotlib.font_manager import FontManager
import subprocess

ENABLE_APPENEND_DATE = True
SUMMER_AUTUMN_CLASS_PATH = 'summer_autumn_charged_class/'
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['SimHei']

df = pd.read_csv("gsx_classes.csv", encoding='utf-8-sig', engine='c',  parse_dates=['snapshot_time'])
df = df [df['price'] != 0]

print('7月报名课程：',df [df['introduction'].str.startswith('07月', na=False) | df['introduction'].str.startswith('2020年07月', na=False)].shape[0])
print('8月报名课程：',df [df['introduction'].str.startswith('08月', na=False) | df['introduction'].str.startswith('2020年08月', na=False)].shape[0])
print('9月报名课程：',df [df['introduction'].str.startswith('09月', na=False) | df['introduction'].str.startswith('2020年09月', na=False)].shape[0])
df = df [df['introduction'].str.startswith('07月', na=False) | df['introduction'].str.startswith('2020年07月', na=False) \
          | df['introduction'].str.startswith('08月', na=False) | df['introduction'].str.startswith('2020年08月', na=False) \
          | df['introduction'].str.startswith('09月', na=False) | df['introduction'].str.startswith('2020年09月', na=False) ]
df.to_csv(SUMMER_AUTUMN_CLASS_PATH+"df_after_july.csv",encoding='utf-8-sig',index=False)

grouped =df.groupby(['title_grade','subject_full_name'])
largest_count = 0
list_tmp = []
for name, group in grouped:
    print('name',name)
    str_name = str(name)
    df_grade_subject = group
    fig1 = plt.figure(0,figsize=(12, 12))
    plt.ylabel(u'enrolled_count')
    plt.title(str_name+'_enrolled_count')
    grouped_season = df_grade_subject.groupby('season')
    ax = plt.subplot(grouped_season.ngroups,1,1)
    index = 1
    for season, df_grp in grouped_season:
        ax = plt.subplot(grouped_season.ngroups,1,index)
        ax.set_title('season:'+season)
        index = index +1
        grouped_clazz_id = df_grp.groupby('clazz_id')
        for name_clazz_id, df_clazz_id in grouped_clazz_id:        
            print(df_clazz_id.head())            
            print('plot ' + df_clazz_id.iat[0,1] + df_clazz_id.iat[0,10] + df_clazz_id.iat[0,14])            
            xs = [d for d in df_clazz_id['snapshot_time']]
            p1=plt.plot(xs,df_clazz_id['enrolled_count'],label=str(name_clazz_id) + df_clazz_id.iat[0,10] + df_clazz_id.iat[0,14])
            list_tmp.append([name_clazz_id,df_clazz_id.iat[0,12],df_clazz_id.iat[0,1],df_clazz_id.iat[0,10],df_clazz_id.iat[0,14],df_clazz_id.iat[0,4],df_clazz_id.iat[0,15],df_clazz_id.iat[df_clazz_id.shape[0]-1,15],df_clazz_id.iat[0,2],df_clazz_id.iat[df_clazz_id.shape[0]-1,2]])
        axes = plt.gca()
        axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        axes.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.legend(loc='upper right',fontsize='x-large',framealpha=0.5)    
    plt.tight_layout()
    fig1.savefig(SUMMER_AUTUMN_CLASS_PATH+str_name+'_enrolled_count.png')
    plt.close(0)
           
           
df_per_class_snapshot_duration = pd.DataFrame(list_tmp,columns=['clazz_id','grade','title','introduction','teacher_name', 'price','first_snapshot_time','last_snapshot_time','first_snapshot_enrollment','last_snapshot_enrollment'])
df_per_class_snapshot_duration['enrollment_growth'] = df_per_class_snapshot_duration.last_snapshot_enrollment - df_per_class_snapshot_duration.first_snapshot_enrollment
df_per_class_snapshot_duration = df_per_class_snapshot_duration.sort_values(by = ['last_snapshot_time'],ascending = [True])
df_per_class_snapshot_duration.to_csv(SUMMER_AUTUMN_CLASS_PATH+"df_per_class_snapshot_duration_orderby_last_snapshot_time.csv",encoding='utf-8-sig',index=False)    

if os.path.exists(SUMMER_AUTUMN_CLASS_PATH+"df_gsx_classes_with_appended_date.csv") == False:
    sorted_snapshot_time = sorted(df['snapshot_time'].unique())
    print(sorted_snapshot_time)
    list_new_data = []
    df_new = pd.DataFrame(columns=df.columns)    
    for index, row in df_per_class_snapshot_duration.iterrows():
        #print(row['clazz_id'], row['last_snapshot_time'])
        df_tmp = df [(df['clazz_id'] == row['clazz_id']) & (df['snapshot_time'] == row['last_snapshot_time'])]            
        begin_index = bisect.bisect_right(sorted_snapshot_time, row['last_snapshot_time'])   
        list_tmp = df_tmp.iloc[0,:].tolist()
        for index in range(begin_index,len(sorted_snapshot_time)):
            x = list(list_tmp)
            x[len(x)-1] = sorted_snapshot_time[index]            
            list_new_data. append(x)
    df_append_new_date_data = pd.DataFrame(list_new_data,columns=['clazz_id','introduction','enrolled_count','left_count', 'price','clazz_date_desc','clazz_week_desc','clazz_time_desc','lecture_desc','season','title','title_grade','grade','subject_full_name','teacher_name','snapshot_time'])    
    df_append_new_date_data = pd.concat([df,df_append_new_date_data],axis=0).sort_values(by = ['clazz_id','snapshot_time'],ascending = [True,True])
    df_append_new_date_data.to_csv(SUMMER_AUTUMN_CLASS_PATH+"df_gsx_classes_with_appended_date.csv",encoding='utf-8-sig',index=False)    

df_per_class_snapshot_duration = df_per_class_snapshot_duration.sort_values(by = ['first_snapshot_time'],ascending = [True])
df_per_class_snapshot_duration.to_csv(SUMMER_AUTUMN_CLASS_PATH+"df_per_class_snapshot_duration_orderby_first_snapshot_time.csv",encoding='utf-8-sig',index=False)    
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
plt.tight_layout()
fig1.savefig(SUMMER_AUTUMN_CLASS_PATH+'Distribution of class enrollment growth count.png')
plt.close(0)
print('enrollment_growth sum:'+str(df_per_class_snapshot_duration['enrollment_growth'].sum()))
print('last_snapshot_enrollment sum:'+str(df_per_class_snapshot_duration['last_snapshot_enrollment'].sum()))


df_filter = df_per_class_snapshot_duration[df_per_class_snapshot_duration['enrollment_growth']>=500].sort_values(by = ['enrollment_growth'],ascending = [False])
df_filter.to_csv(SUMMER_AUTUMN_CLASS_PATH+"top_enrollment_growth_teachers.csv",encoding='utf-8-sig',index=False)    
df_filter = df_per_class_snapshot_duration.sort_values(by = ['last_snapshot_enrollment'],ascending = [False])
df_filter.to_csv(SUMMER_AUTUMN_CLASS_PATH+"top_enrollment_teachers.csv",encoding='utf-8-sig',index=False)    



df = pd.read_csv(SUMMER_AUTUMN_CLASS_PATH+"df_gsx_classes_with_appended_date.csv", encoding='utf-8-sig', engine='c',  parse_dates=['snapshot_time'])
df_summer = df [df['introduction'].str.startswith('07月', na=False) | df['introduction'].str.startswith('2020年07月', na=False) \
          | df['introduction'].str.startswith('08月', na=False) | df['introduction'].str.startswith('2020年08月', na=False)]
df_summer_autumn = df_summer[df_summer['season'] == '暑+秋']
df_summer = df_summer[df_summer['season'] == '暑']
df_autumn = df [df['introduction'].str.startswith('09月', na=False) | df['introduction'].str.startswith('2020年09月', na=False) ]
          
df_summer_snapshot_time = df_summer.groupby(['grade','snapshot_time'])['enrolled_count'].sum().reset_index()
df_autumn_snapshot_time = df_autumn.groupby(['grade','snapshot_time'])['enrolled_count'].sum().reset_index()
df_summer_autumn_snapshot_time = df_summer_autumn.groupby(['grade','snapshot_time'])['enrolled_count'].sum().reset_index()

grouped_summer = df_summer_snapshot_time.groupby('grade')
grouped_autumn = df_autumn_snapshot_time.groupby('grade')
grouped_summer_autumn = df_summer_autumn_snapshot_time.groupby('grade')
fig1 = plt.figure(0,figsize=(18, 12))
plt.ylabel(u'enrolled_count_sum')
plt.title('enrolled_count_sum_by_grade')

ax = plt.subplot(331)
list_tmp = [grouped_summer,grouped_autumn,grouped_summer_autumn]
title_index = ['Summer Classes','Autumn Classes','Summer+Autumn Classes']
for index in range(3):
    grouped = list_tmp[index]
    for name, df_tmp in grouped:
        if (name >= 1) and (name <= 6) :
            ax = plt.subplot(3,3,index+1)
            ax.set_title('Primary School '+title_index[index])
        elif (name == 7) or (name == 8) or (name == 9):
            ax = plt.subplot(3,3,index+4)
            ax.set_title('Junior Middle School '+title_index[index])
        else:        
            ax = plt.subplot(3,3,index+7)
            ax.set_title('Senior Middle School '+title_index[index])
                
        xs = [d for d in df_tmp['snapshot_time']]
        p1=plt.plot(xs,df_tmp['enrolled_count'],label='Grade '+str(name))
        plt.legend(loc='upper right',fontsize='x-large',framealpha=0.5)
        axes = plt.gca()
        axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        axes.xaxis.set_major_locator(mdates.AutoDateLocator())


df_summer_primary_school = df_summer[(df_summer['grade'] >=1) & (df_summer['grade'] <=6)].groupby(['snapshot_time'])['enrolled_count'].sum().reset_index()
df_summer_middle_school = df_summer[(df_summer['grade'] >=7) & (df_summer['grade'] <=9) ].groupby(['snapshot_time'])['enrolled_count'].sum().reset_index()
df_summer_middle_school.to_csv(SUMMER_AUTUMN_CLASS_PATH+"junior_middle_school_enrolled_count.csv",encoding='utf-8-sig',index=False)    
df_summer_high_school = df_summer[(df_summer['grade'] >=10) & (df_summer['grade'] <=12) ].groupby(['snapshot_time'])['enrolled_count'].sum().reset_index()
df_autumn_primary_school = df_autumn[(df_autumn['grade'] >=1) & (df_autumn['grade'] <=6) ].groupby(['snapshot_time'])['enrolled_count'].sum().reset_index()
df_autumn_middle_school = df_autumn[(df_autumn['grade'] >=7) & (df_autumn['grade'] <=9) ].groupby(['snapshot_time'])['enrolled_count'].sum().reset_index()
df_autumn_high_school = df_autumn[(df_autumn['grade'] >=10) & (df_autumn['grade'] <=12) ].groupby(['snapshot_time'])['enrolled_count'].sum().reset_index()
df_summer_autumn_primary_school = df_summer_autumn[(df_summer_autumn['grade'] >=1) & (df_summer_autumn['grade'] <=6) ].groupby(['snapshot_time'])['enrolled_count'].sum().reset_index()
df_summer_autumn_middle_school = df_summer_autumn[(df_summer_autumn['grade'] >=7) & (df_summer_autumn['grade'] <=9) ].groupby(['snapshot_time'])['enrolled_count'].sum().reset_index()
df_summer_autumn_high_school = df_summer_autumn[(df_summer_autumn['grade'] >=10) & (df_summer_autumn['grade'] <=12) ].groupby(['snapshot_time'])['enrolled_count'].sum().reset_index()
list_tmp = [df_summer_primary_school,df_autumn_primary_school,df_summer_autumn_primary_school,df_summer_middle_school,df_autumn_middle_school,df_summer_autumn_middle_school,df_summer_high_school,df_autumn_high_school,df_summer_autumn_high_school]
for index in range(9):
    df_tmp = list_tmp[index]
    if df_tmp.shape[0] !=0:
        ax = plt.subplot(3,3,index+1)                
        xs = [d for d in df_tmp['snapshot_time']]    
        p1=plt.plot(xs,df_tmp['enrolled_count'],label='All')
        plt.legend(loc='upper right',fontsize='x-large',framealpha=0.5)
        axes = plt.gca()
        axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        axes.xaxis.set_major_locator(mdates.AutoDateLocator())
plt.tight_layout()
fig1.savefig(SUMMER_AUTUMN_CLASS_PATH+'enrolled_count_sum_by_grade.png')
plt.close(0)
