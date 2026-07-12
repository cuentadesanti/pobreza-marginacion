#!/usr/bin/env python
"""
Vista F — lentes satelitales/geográficas por municipio (2,469).

Insumos (scratch dir, ver RAW_DATA_MANIFEST.md):
  ntl/*.tif                NPP-VIIRS-like 2020 v2 (Chen et al., Harvard Dataverse YGIVCD, 500m)
  gmted_*.tif              GMTED2010 media 30 arcseg (3 tiles USGS que cubren México)
  iter/conjunto_*.csv      ITER 2020 (ya en data/raw) -> ciudades >=50k para accesibilidad

Salida: data/processed/vistaF_satelital.parquet
  cvegeo (str5), ntl_mean, ntl_sum, ntl_pc, log_ntl, elev_mean, tri_mean, acc_km, [acc_min]

Accesibilidad: distancia geodésica (proyección EPSG:6372) del centroide municipal a la
localidad >=50k más cercana (fallback tabular documentado en las instrucciones §2C; el raster
de Malaria Atlas queda como upgrade opcional -> acc_min).

⚠ cvegeo SIEMPRE str.zfill(5) (bug de clave documentado).
"""
import os, sys, re, glob
import numpy as np, pandas as pd
import geopandas as gpd
import rasterio
from rasterio.merge import merge as rio_merge
from rasterstats import zonal_stats
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
SCRATCH = sys.argv[1] if len(sys.argv) > 1 else "."
MX_BBOX = (-118.6, 14.3, -86.4, 33.0)


def dms_to_dec(s):
    if not isinstance(s, str) or "°" not in s:
        return np.nan
    m = re.match(r"(\d+)°(\d+)'([\d.]+)\"?\s*([NSWEO])", s.strip())
    if not m:
        return np.nan
    d, mi, se, h = float(m[1]), float(m[2]), float(m[3]), m[4]
    v = d + mi / 60 + se / 3600
    return -v if h in ("W", "O", "S") else v


def ciudades_50k():
    f = glob.glob(os.path.join(SCRATCH, "iter/conjunto_de_datos_iter_00*.csv"))[0]
    it = pd.read_csv(f, usecols=["ENTIDAD", "MUN", "LOC", "LONGITUD", "LATITUD", "POBTOT"],
                     dtype=str)
    it = it[~it["LOC"].isin(["0000", "9998", "9999"])]
    it["POBTOT"] = pd.to_numeric(it["POBTOT"], errors="coerce")
    big = it[it["POBTOT"] >= 50000].copy()
    big["lon"] = big["LONGITUD"].map(dms_to_dec)
    big["lat"] = big["LATITUD"].map(dms_to_dec)
    big = big.dropna(subset=["lon", "lat"])
    print(f"ciudades >=50k: {len(big)}")
    return gpd.GeoDataFrame(big, geometry=gpd.points_from_xy(big.lon, big.lat), crs=4326)


def tri(dem, nodata):
    """Terrain Ruggedness Index (Riley 1999): media |z_centro - z_vecino| en 3x3."""
    z = dem.astype("float64")
    z[z == nodata] = np.nan
    acc = np.zeros_like(z); cnt = np.zeros_like(z)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == dx == 0:
                continue
            nb = np.full_like(z, np.nan)
            ys = slice(max(dy, 0), z.shape[0] + min(dy, 0))
            yd = slice(max(-dy, 0), z.shape[0] + min(-dy, 0))
            xs = slice(max(dx, 0), z.shape[1] + min(dx, 0))
            xd = slice(max(-dx, 0), z.shape[1] + min(-dx, 0))
            nb[yd, xd] = z[ys, xs]
            d = np.abs(z - nb)
            ok = ~np.isnan(d)
            acc[ok] += d[ok]; cnt[ok] += 1
    out = np.where(cnt > 0, acc / np.maximum(cnt, 1), np.nan)
    return out


def main():
    geo = gpd.read_file(os.path.join(HERE, "spatial", "municipios_2020.geojson"))[
        ["cvegeo", "geometry"]]
    geo["cvegeo"] = geo["cvegeo"].astype(str).str.zfill(5)
    print(f"geometrías: {len(geo)}")

    # ---------- NTL ----------
    ntl_tif = sorted(glob.glob(os.path.join(SCRATCH, "ntl", "*.tif")))[0]
    print("NTL:", ntl_tif)
    zs = zonal_stats(geo, ntl_tif, stats=["mean", "sum"], all_touched=False, nodata=None)
    geo["ntl_mean"] = [z["mean"] for z in zs]
    geo["ntl_sum"] = [z["sum"] for z in zs]

    # ---------- DEM: merge tiles, clip MX, elev + TRI ----------
    tiles = [rasterio.open(p) for p in sorted(glob.glob(os.path.join(SCRATCH, "gmted_*.tif")))]
    print("DEM tiles:", [os.path.basename(t.name) for t in tiles])
    dem, tr = rio_merge(tiles, bounds=MX_BBOX)
    dem = dem[0]
    nod = tiles[0].nodata if tiles[0].nodata is not None else -32768
    prof = dict(driver="GTiff", height=dem.shape[0], width=dem.shape[1], count=1,
                dtype="float32", crs=tiles[0].crs, transform=tr, nodata=-9999)
    dem_p = os.path.join(SCRATCH, "dem_mx.tif"); tri_p = os.path.join(SCRATCH, "tri_mx.tif")
    demf = dem.astype("float32"); demf[dem == nod] = -9999
    with rasterio.open(dem_p, "w", **prof) as dst:
        dst.write(demf, 1)
    t = tri(dem, nod).astype("float32"); t[np.isnan(t)] = -9999
    with rasterio.open(tri_p, "w", **prof) as dst:
        dst.write(t, 1)
    geo["elev_mean"] = [z["mean"] for z in zonal_stats(geo, dem_p, stats=["mean"], nodata=-9999)]
    geo["tri_mean"] = [z["mean"] for z in zonal_stats(geo, tri_p, stats=["mean"], nodata=-9999)]

    # ---------- accesibilidad: distancia a ciudad >=50k ----------
    cities = ciudades_50k().to_crs(6372)
    cent = geo.to_crs(6372).geometry.centroid
    tree = cKDTree(np.c_[cities.geometry.x, cities.geometry.y])
    d, _ = tree.query(np.c_[cent.x, cent.y])
    geo["acc_km"] = d / 1000

    # ---------- ensamble ----------
    pob = pd.read_parquet(os.path.join(PROC, "vistaD_v1.parquet"),
                          columns=["cvegeo", "pob_tot"])
    pob["cvegeo"] = pob["cvegeo"].astype(str).str.zfill(5)
    out = geo.drop(columns="geometry").merge(pob, on="cvegeo", how="left")
    assert len(out) >= 2450, out.shape
    out["ntl_pc"] = out["ntl_sum"] / out["pob_tot"]
    out["log_ntl"] = np.log1p(out["ntl_mean"])
    out = out[["cvegeo", "ntl_mean", "ntl_sum", "ntl_pc", "log_ntl",
               "elev_mean", "tri_mean", "acc_km", "pob_tot"]]
    out.to_parquet(os.path.join(PROC, "vistaF_satelital.parquet"), index=False)
    print(f"\nvistaF_satelital.parquet: {out.shape}, NaN por columna:")
    print(out.isna().sum().to_string())

    # sanity (§8.1): log_ntl debe correlacionar NEGATIVO con z_monetario y loc_peq
    z = pd.read_csv(os.path.join(HERE, "outputs", "zscores_rung3_K3.csv"))
    z["cvegeo"] = z["cvegeo"].astype(str).str.zfill(5)
    d5 = pd.read_parquet(os.path.join(PROC, "vistaD_v1.parquet"), columns=["cvegeo", "loc_peq_pct"])
    d5["cvegeo"] = d5["cvegeo"].astype(str).str.zfill(5)
    m = out.merge(z, on="cvegeo").merge(d5, on="cvegeo")
    assert len(m) >= 2450, m.shape
    for c in ["monetario_mean", "material_mean", "loc_peq_pct"]:
        print(f"corr(log_ntl, {c}) = {np.corrcoef(m.log_ntl, m[c])[0,1]:+.3f}")
    print(f"corr(tri_mean, material_mean) = {np.corrcoef(m.dropna(subset=['tri_mean']).tri_mean, m.dropna(subset=['tri_mean']).material_mean)[0,1]:+.3f}")
    print(f"corr(acc_km, material_mean)  = {np.corrcoef(m.acc_km, m.material_mean)[0,1]:+.3f}")


if __name__ == "__main__":
    main()
