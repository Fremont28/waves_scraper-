#import libraries 
import numpy as np 
import pandas as pd
import sklearn 
import matplotlib.pyplot as plt
import seaborn as sns 
from pylab import rcParams
import scipy 
import scipy.stats

class SurfLine():
    def __init__(self):
        pass
    
    def surf_visuals(self,df):
        df=pd.read_table(df,delim_whitespace=True)
        df=df.iloc[1:df.shape[0]]
        cols=df.columns 
        df[cols]=df[cols].apply(pd.to_numeric,errors='coerce')

        #assign number for each month 
        def month_viz(x):
            if x==1:
                return "January"
            if x==2:
                return "February"
            if x==3:
                return "March"
            if x==4:
                return "April"
            if x==5:
                return "May"
            if x==6:
                return "June"
            if x==7:
                return "July"
            if x==8:
                return "August"
            if x==9:
                return "September"
            if x==10:
                return "October"
            if x==11:
                return "November"
            if x==12:
                return "December"
        df['month']=df['MM'].apply(month_viz) 

        #histogram waveheight 
        plt.figure()
        df.WVHT.hist(color="orange")
        rcParams['figure.figsize'] = 15, 10
        plt.title('Average Wave Height Histogram')
        plt.xlabel('wave height (feet)')
        plt.ylabel('Frequency')
        plt.savefig('fig_surf1.png')

        #median wave metrics by month (units feet and seconds)
        avg_waves_M=df.groupby('month')[['WVHT','GST','DPD','WSPD','WDIR']].median() 
        waves_one=avg_waves_M[["WVHT","GST","WSPD"]]*3.28 
        waves_two=avg_waves_M[["DPD","WDIR"]]
        avg_waves_M=pd.concat([waves_one,waves_two],axis=1)
        avg_waves_M.to_csv("waves_xx.csv")
        print(avg_waves_M)
    
        #append csv files 
        file=pd.read_csv("waves_xx.csv") #csv file ("waves_xx.csv")
        file1=avg_waves_M 
        file1.reset_index(level=0,inplace=True)
        file=file.append(avg_waves_M)
        file.to_csv("waves_xx.csv")

        fig = plt.figure() 
        ax = fig.add_subplot(111) 
        ax2 = ax.twinx() 
        width = 0.4
        avg_waves_M.WVHT.plot(kind='bar', color='red', ax=ax, width=width, position=1)
        avg_waves_M.GST.plot(kind='bar', color='blue', ax=ax2, width=width, position=0)
        ax.set_ylabel('Wave Height (feet)')
        ax2.set_ylabel('Gust Speed (feet/s)')
        plt.savefig('fig_surf2.png')

        #wwp vs. wwh
        fig = plt.figure()  
        ax = fig.add_subplot(111)  
        ax2 = ax.twinx()  
        width = 0.4
        avg_waves_M.WDIR.plot(kind='bar', color='orange', ax=ax, width=width, position=1)
        avg_waves_M.WSPD.plot(kind='bar', color='green', ax=ax2, width=width, position=0)
        ax.set_ylabel('Wind Direction')
        ax2.set_ylabel('Wind Speed (feet/s)')
        plt.savefig('fig_surf3.png')

        #convert meters to feet 
        df1=df 
        #df1[['SwH','SwP','WWH','WWP']]=df1[['SwH','SwP','WWH','WWP']]
        df1=df1.drop('month',1)
        df1.rename(columns={'#YY':'year'}, inplace=True)
        df1.rename(columns={'MM':'month'}, inplace=True)
        df1.rename(columns={'DD':'day'}, inplace=True)
        df1['date']=pd.to_datetime(df1[['year', 'month', 'day']])

        df1=df1.set_index('date')

        #plot time series of swell period 
        fig=plt.figure() 
        df1.WVHT.plot(linewidth=0.5)
        plt.ylabel('wave height (feet)')
        plt.savefig('fig_surf4.png')
        
if __name__=='__main__':
    surf=SurfLine()
    surf.surf_visuals("https://www.ndbc.noaa.gov/data/realtime2/46235.txt") 
