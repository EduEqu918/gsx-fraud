# -*- coding: utf-8 -*-
import json
import sys
import os
import pandas as pd

pathDir = os.listdir('data/')
list_result = []
for name in pathDir:
    print(name)    
    snapshot_time = name[20:39]    
    if name.find('.json')>=0 and snapshot_time<='2020-06-02-09:56:03':            
        with open('data/'+name,'r') as load_f:
            courses = json.load(load_f)
            #print(courses)

        enrolled_count = 0
        enrolled_count_sum = 0
        charged_enrolled_count_sum = 0
        revenue = 0
        course_count = 0 
        avg_price = 0
        for key in courses:
            #print(key)
            course = courses[key]            
            if isinstance(course,dict): 
                clazz_id = course['clazz_id']
                introduction = course['introduction']
                enrolled_count = course['enrolled_count']
                left_count = course['left_count']
                price = course['price']
                clazz_date_desc = course['clazz_date_desc']
                clazz_week_desc = course['clazz_week_desc']
                clazz_time_desc = course['clazz_time_desc']                
                lecture_desc = course['lecture_desc']
                season = course['season']
                title = course['title']
                title_grade = course['title_grade']
                grade = course['grade']
                subject_full_name = course['subject_full_name']
                teacher_list = course['teacher_list']
                for teacher in teacher_list:
                    teacher_name = teacher['name']
                    break                
                date_snapshot_time = pd.to_datetime(snapshot_time, format='%Y-%m-%d-%H:%M:%S')
                date_snapshot_time = date_snapshot_time + pd.Timedelta(hours=15)
                list_result.append([clazz_id,introduction,enrolled_count,left_count, price,clazz_date_desc,clazz_week_desc,clazz_time_desc,lecture_desc,season,title,title_grade,grade,subject_full_name,teacher_name,date_snapshot_time])
df_result = pd.DataFrame(list_result,columns=['clazz_id','introduction','enrolled_count','left_count', 'price','clazz_date_desc','clazz_week_desc','clazz_time_desc','lecture_desc','season','title','title_grade','grade','subject_full_name','teacher_name','snapshot_time'])
df_result = df_result.sort_values(by = ['clazz_id','snapshot_time'],ascending = [True,True])
df_result.to_csv("gsx_classes.csv",encoding='utf-8-sig',index=False)    
