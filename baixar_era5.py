import cdsapi
import zipfile
import os
import glob
import time
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
client = cdsapi.Client()

# Divide o mês em 3 segmentos de ~10 dias para evitar o limite de custo do CDS
segmentos = [
    [f"{d:02d}" for d in range(1, 11)],
    [f"{d:02d}" for d in range(11, 21)],
    [f"{d:02d}" for d in range(21, 32)],
]

zip_paths = []

for seg in segmentos:
    request = {
        "product_type": ["reanalysis"],
        "variable": [
            "100m_u_component_of_wind",
            "100m_v_component_of_wind",
        ],
        "year": ["2003"],
        "month": ["03"],
        "day": seg,
        "time": [f"{h:02d}:00" for h in range(24)],
        "data_format": "netcdf",
        "download_format": "zip",
        "area": [-5, -36, -6, -35],
    }

    zip_path = proximo_nome("data_era5_teste", ".zip")
    print(f"Baixando segmento {seg[0]}-{seg[-1]} para: {zip_path}")

    try:
        client.retrieve(dataset, request).download(zip_path)
        zip_paths.append(zip_path)
        print("  Concluído")
    except Exception as e:
        print(f"  Falhou: {e}")

    time.sleep(10)  # Pausa entre requisições para não sobrecarregar o servidor

# Extrair cada zip para uma pasta própria
nc_files = []
for zp in zip_paths:
    out_dir = zp.replace(".zip", "_nc")
    if not os.path.isdir(out_dir):
        with zipfile.ZipFile(zp) as z:
            z.extractall(out_dir)
    nc_files.extend(sorted(glob.glob(os.path.join(out_dir, "*.nc"))))

# Abrir e concatenar todos os NetCDFs baixados
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
plt.title("ERA5 – vento a 100 m (2003-03, baixado em 3 segmentos)")
plt.grid(True, alpha=0.3)
plt.tight_layout()

png_path = "grafico_vento_2003_03.png"
plt.savefig(png_path, dpi=150)
print("Gráfico salvo em:", png_path)