#パワースペクトルを求める関数を定義
def signal_fft(data, fs):
    import numpy as np
    from scipy import fftpack

    n = len(data)-1
    y = fftpack.fft(data) / n
    y = y[0:round(n/2)]
    power = 2 * (np.abs(y)**2)
    power = 10 * np.log10(power)
    f = np.arange(0, fs/2, fs/n)
    return power, f
