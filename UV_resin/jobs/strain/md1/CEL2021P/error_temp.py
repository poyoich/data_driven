import  sys
import pandas as pd
# データの読み込み
data = pd.read_csv(sys.argv[1], skiprows=100,delim_whitespace=True,header=None, names=["Temp", "Density", "Volume"],)


print(data[data['Temp']>700])