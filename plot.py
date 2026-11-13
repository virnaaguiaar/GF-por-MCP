
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