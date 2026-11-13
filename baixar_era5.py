import cdsapi
import zipfile
import os
import glob
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

def proximo_nome(prefixo="data_era5_teste", ext=".zip", pasta="."):
    existentes = glob.glob(os.path.join(pasta, f"{prefixo}*{ext}"))
    nums = set()
    for f in existentes:
        base = os.path.basename(f)[len(prefixo):-len(ext)]
        if base.isdigit():
            nums.add(int(base))
    n = 1
    while n in nums:
        n += 1
    return os.path.join(pasta, f"{prefixo}{n}{ext}")

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "100m_u_component_of_wind",
        "100m_v_component_of_wind",
    ],
    "year": ["2003"],
    "month": ["03"],
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
    "area": [-5, -36, -6, -35],
}

zip_path = proximo_nome("data_era5_teste", ".zip")
print("Baixando para:", zip_path)

client = cdsapi.Client()
client.retrieve(dataset, request).download(zip_path)

# Extrair para uma pasta com o mesmo número do zip
out_dir = zip_path.replace(".zip", "_nc")
if not os.path.isdir(out_dir):
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(out_dir)

nc_files = sorted(glob.glob(os.path.join(out_dir, "*.nc")))
ds = xr.open_mfdataset(nc_files, combine="by_coords")

lat_alvo, lon_alvo = -5.5, -35.5
ds_ponto = ds.sel(latitude=lat_alvo, longitude=lon_alvo, method="nearest")

u = ds_ponto["u100"]
v = ds_ponto["v100"]
velocidade = np.sqrt(u**2 + v**2)

time_name = "valid_time" if "valid_time" in ds_ponto.coords else "time"
tempo = ds_ponto[time_name].values

plt.figure(figsize=(12, 4))
plt.plot(tempo, velocidade.values, marker="o", ms=2, lw=0.8)
plt.xlabel("Tempo")
plt.ylabel("Velocidade do vento a 100 m (m/s)")
plt.title(f"ERA5 – vento a 100 m ({os.path.basename(zip_path)})")
plt.grid(True, alpha=0.3)
plt.tight_layout()

png_path = zip_path.replace(".zip", ".png")
plt.savefig(png_path, dpi=150)
print("Gráfico salvo em:", png_path)