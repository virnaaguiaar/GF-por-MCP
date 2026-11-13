
import cdsapi

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "100m_u_component_of_wind",
        "100m_v_component_of_wind"
    ],
    "year": ["2003" , "2004"],
    "month": ["03" , "04"],
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16", "17", "18",
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"
    ],
    "time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ],
    "data_format": "netcdf",
    "download_format": "zip",
    "area": [-5, -36, -6, -35]
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

ds = xr.open_dataset('era5_teste.nc')
ds_ponto = ds.sel(latitude=-5.5, longitude=-35.5, method='nearest')

u = ds_ponto['u100'].values
v = ds_ponto['v100'].values
velocidade = np.sqrt(u**2 + v**2)

plt.figure(figsize=(10, 5))
plt.plot(ds_ponto['time'].values, velocidade, marker='o')
plt.title('Velocidade do Vento a 100m (ERA5)')
plt.xlabel('Data/Hora')
plt.ylabel('Velocidade (m/s)')
plt.grid(True)
plt.tight_layout()
plt.savefig('grafico_vento.png')
print("Gráfico salvo: grafico_vento.png")

print(ds)