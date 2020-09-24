# Turgot's thesis
import pandas as pd
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
import scipy.stats




root = '/Users/berker/Desktop/TURGOR/excel_for_R.xlsx'
df = pd.read_excel(root)




### Data preparation
df.rename(columns = {'Unnamed: 0':'direction', 'Unnamed: 1':'identity', "ANGLE":"angle", "LENGTH":"length", "DURATION":"duration", "WAGGLES":"waggles"}, inplace = True)
df.drop([0], inplace = True)
df_stat = df[["identity", "angle", "length", "duration", "waggles"]].copy()




### Statistics on individuals
stats_out_mean = pd.DataFrame(columns = ["identity", "angle", "length", "duration", "waggles"])
stats_out_var = pd.DataFrame(columns = ["identity", "angle", "length", "duration", "waggles"])
stats_out_stdev = pd.DataFrame(columns = ["identity", "angle", "length", "duration", "waggles"])
angle_array = []
length_array = []
duration_array = []
waggle_array = []
k = 0

for i in range(1, len(df)-2):
    if df_stat.loc[i, "identity"] == df_stat.loc[i+1, "identity"]:
        angle_array.append(df_stat.loc[i, "angle"])
        length_array.append(df_stat.loc[i, "length"])
        duration_array.append(df_stat.loc[i, "duration"])
        waggle_array.append(df_stat.loc[i, "waggles"])
        
    else:
        angle_array.append(df_stat.loc[i, "angle"])
        length_array.append(df_stat.loc[i, "length"])
        duration_array.append(df_stat.loc[i, "duration"])
        waggle_array.append(df_stat.loc[i, "waggles"])
        
        stats_out_mean.loc[k, "identity"] = df_stat.loc[i, "identity"]
        stats_out_mean.loc[k, "angle"] = stat.mean(angle_array)
        stats_out_mean.loc[k, "length"] = stat.mean(length_array)
        stats_out_mean.loc[k, "duration"] = stat.mean(duration_array)
        stats_out_mean.loc[k, "waggles"] = stat.mean(waggle_array)

        stats_out_var.loc[k, "identity"] = df_stat.loc[i, "identity"]
        stats_out_var.loc[k, "angle"] = stat.variance(angle_array)
        stats_out_var.loc[k, "length"] = stat.variance(length_array)
        stats_out_var.loc[k, "duration"] = stat.variance(duration_array)
        stats_out_var.loc[k, "waggles"] = stat.variance(waggle_array)    
    
        stats_out_stdev.loc[k, "identity"] = df_stat.loc[i, "identity"]
        stats_out_stdev.loc[k, "angle"] = stat.stdev(angle_array)
        stats_out_stdev.loc[k, "length"] = stat.stdev(length_array)
        stats_out_stdev.loc[k, "duration"] = stat.stdev(duration_array)
        stats_out_stdev.loc[k, "waggles"] = stat.stdev(waggle_array)
        
        angle_array = []
        length_array = []
        duration_array = []
        waggle_array = []
        k = k + 1

stats_out_mean.to_excel("mean.xlsx", index = False)
stats_out_var.to_excel("variance.xlsx", index = False)
stats_out_stdev.to_excel("stdev.xlsx", index = False)




### Correlation of length, duration and waggles


# Pearson
scipy.stats.pearsonr(df_stat["length"], df_stat["duration"])
# (0.5146637807400295, 1.8800753719292625e-80)
scipy.stats.pearsonr(df_stat["length"], df_stat["waggles"])
#(0.5025222500382647, 3.37421869084273e-76)
scipy.stats.pearsonr(df_stat["waggles"], df_stat["duration"])
# (0.940536040525263, 0.0)


# Spearman
scipy.stats.spearmanr(df_stat["length"], df_stat["duration"])
# SpearmanrResult(correlation=0.45821881513667195, pvalue=4.725917992836518e-62)
scipy.stats.spearmanr(df_stat["length"], df_stat["waggles"])
# SpearmanrResult(correlation=0.4298961153678399, pvalue=4.845314776147002e-54)
scipy.stats.spearmanr(df_stat["waggles"], df_stat["duration"])
# Out[84]: SpearmanrResult(correlation=0.9025616948322301, pvalue=0.0)


# Kendell Tau
scipy.stats.kendalltau(df_stat["length"], df_stat["duration"])
# KendalltauResult(correlation=0.32596072913766594, pvalue=5.37271426123179e-61)
scipy.stats.kendalltau(df_stat["length"], df_stat["waggles"])
# KendalltauResult(correlation=0.31218957727157465, pvalue=5.133393758829858e-53)
scipy.stats.kendalltau(df_stat["waggles"], df_stat["duration"])
# KendalltauResult(correlation=0.7864298207213447, pvalue=0.0)




### Scatter plots
fig, ax = plt.subplots()
plt.figure(figsize=(10,8))
ax.scatter(df_stat["length"], df_stat["duration"], c = "r", marker = "1")
ax.set_xlabel("Length")
ax.set_ylabel("Duration")
ax.set_title("Scatter plot of length versus duration")
plt.show()
fig.savefig("length_duration")

fig2, ax2 = plt.subplots()
plt.figure(figsize=(10,8))
ax2.scatter(df_stat["length"], df_stat["waggles"], c = "r", marker = "1")
ax2.set_xlabel("Length")
ax2.set_ylabel("Waggles")
ax2.set_title("Scatter plot of length versus waggles")
plt.show()
fig2.savefig("length_waggle")

fig3, ax3 = plt.subplots()
plt.figure(figsize=(10,8))
ax3.scatter(df_stat["waggles"], df_stat["duration"], c = "r", marker = "1")
ax3.set_xlabel("waggles")
ax3.set_ylabel("Duration")
ax3.set_title("Scatter plot of waggles versus duration")
plt.show()
fig3.savefig("waggle_duration")




### Histogram
df_stat2.hist(column = "length", bins = 40)
df_stat2.hist(column = "duration", bins = 50)
df_stat2.hist(column = "waggles", bins = 15)




### Dance and solar angle
root1 = '/Users/berker/Desktop/TURGOR/daytime1.xlsx'
root2 = '/Users/berker/Desktop/TURGOR/daytime2.xlsx'
root3 = '/Users/berker/Desktop/TURGOR/daytimetotal.xlsx'

df1 = pd.read_excel(root1)
df2 = pd.read_excel(root2)
df_total =  pd.read_excel(root3)




### Regression
y = np.array(df1['dance'].dropna().values, dtype=float)
x = np.array(pd.to_datetime(df1['dance'].dropna()).index.values, dtype=float)
slope, intercept, r_value, p_value, std_err =scipy.stats.linregress(x,y)
xf = np.linspace(min(x),max(x),100)
xf1 = xf.copy()
xf1 = pd.to_datetime(xf1)
yf = (slope*xf)+intercept




### Plot
fig, ax = plt.subplots(1,1)
df1.plot(ax = ax)
ax.plot(ax, yf, Label = "Linear fit")
plt.ylabel("Degree")
ax.legend()
plt.legend()

















