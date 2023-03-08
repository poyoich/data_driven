# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.optimize import curve_fit
from scipy import optimize


def piecewise_linear(x, x0, y0, k1, k2):
    return np.piecewise(
         x, [x < x0],
        [lambda x: k1 * x + y0 - k1 * x0, lambda x: k2 * x + y0 - k2 * x0])
 
def detectTg(df,x_col, y_col):
 
    idx = (df[x_col] - 300.0).abs().idxmin()

    x = np.array(df[x_col])
    y = np.array(df[ y_col])

    density_300 = y[idx]

    p0 = (250, 0.85, -0.0001, 0.0001)
    p, e = optimize.curve_fit(piecewise_linear, x, y, p0)
    xd = np.linspace(x.min(), x.max(), 100)

    plt.rcParams.update({'font.size': 12})
    plt.plot(x, y, "ko", fillstyle='none', markersize=8)
    plt.plot(xd, piecewise_linear(xd, *p), 'r')
    plt.ylabel(f'{y_col}$(g/cm^3)$')
    plt.xlabel(f'{x_col} ($K$)')
    plt.savefig('temp_vs_density.png', dpi=300)
    return p[0]


def detect_Tg(data, x_col, y_col):
    # Tgの初期値
   
    # 残差平方和の初期値
    residual_sum = float('inf')
    # Tgを変えながら最適な直線を探す
    for i in range(200, 600,20):
        data_low = data[data[x_col] <= i]
        data_high = data[data[x_col] >= i]

        fit_low = np.polyfit(data_low[x_col], data_low[y_col], 1)
        fit_fn_low = np.poly1d(fit_low)

        fit_high = np.polyfit(data_high[x_col], data_high[y_col], 1)
        fit_fn_high = np.poly1d(fit_high)

        # 低温側のデータに対する残差平方和
        residual_low = np.sum((fit_fn_low(data_low[x_col]) - data_low[y_col]) ** 2)

        # 高温側のデータに対する残差平方和
        residual_high = np.sum((fit_fn_high(data_high[x_col]) - data_high[y_col]) ** 2)

        # 残差平方和の合計
        residual_sum_new = residual_low + residual_high

        # 残差平方和が最小の場合、Tgを更新する
        if residual_sum_new < residual_sum:
            residual_sum = residual_sum_new
            tg = i
            fit_low_best = fit_low
            fit_high_best = fit_high
    

    # Tgの値を表示
    print('Tg =', tg)
    print('low slope =', fit_low_best[0])
    print('high slope =', fit_high_best[0])
    

    # グラフのプロット
    data_low = data[data[x_col] <= tg]
    data_high = data[data[x_col] > tg]

    fit_low = np.polyfit(data_low[x_col], data_low[y_col], 1)
    fit_fn_low = np.poly1d(fit_low)

    fit_high = np.polyfit(data_high[x_col], data_high[y_col], 1)
    fit_fn_high = np.poly1d(fit_high)

    plt.scatter(data_low[x_col], data_low[y_col], label='low',c='b')
    plt.scatter(data_high[x_col], data_high[y_col], label='high',c='b')
    plt.plot(data[x_col], fit_fn_low(data[x_col]),  label='fit_low',c='r',linestyle='--')
    plt.plot(data[x_col], fit_fn_high(data[x_col]), label='fit_high',c='orange',linestyle='--')
    plt.axvline(x=tg, color='gray', linestyle='--', label='Tg')

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend()
    plt.show()
    plt.savefig("tg_plot.png")
    return tg


# %%

# データの読み込み
data = pd.read_csv(sys.argv[1], skiprows=100,delim_whitespace=True,header=None, names=["Temp", "Density", "Volume"],)
data = data[data["Temp"] < 650]

data_new = pd.DataFrame()
temps = []
densities = []
for temp in range(200,600+1,20):
    ave_dense = data[ (temp-10<data["Temp"]) & ( data['Temp']< temp+10)]['Density'].mean()
    temps.append(temp)
    densities.append(ave_dense)

data_new['Temp'] = temps
data_new['Density'] = densities
#print(data_new)
    
#tg = detect_Tg(data_new, "Temp", "Density")
tg = detectTg(data_new, "Temp", "Density")
print(tg)

#detect_CTE(data,"Temp", "Volume",tg)



