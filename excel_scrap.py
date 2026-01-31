import pandas as pd
import os
current_dir=os.getcwd()
file_name_list=["Backend_men_makeup_data.xlsx","Backend_men_spa_data.xlsx","Backend_parlour_men_data.xlsx", "Backend_women_makeup.xlsx","Backend_women_spa_data.xlsx","Backend_parlour_women_data.xlsx"]
#file_name_list=["Backend_women_makeup.xlsx"]
for file_name in file_name_list:
    file_path=os.path.join(current_dir,file_name)
    df=pd.read_excel(file_path)
    df["opening_hours"]=df["opening_hours"].astype(str)
    df["opening_hours"]=df["opening_hours"].apply(lambda x:x.split(";")[0])
    df["opening_hours"]=df["opening_hours"].str.replace("Monday:","Monday-Friday:")
    df.to_excel(file_path,index=False)