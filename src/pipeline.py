from astropy.table import Table
import numpy as np
import pandas as pd
import os


def FitsToPandas(fits_file):
    table = Table.read(str(fits_file))
    df = table.to_pandas()
    df.drop(index=df[df['PDCSAP_FLUX'].isnull()].index, inplace=True)
    return df
    
def OneDataframe(filepath):
    directory = filepath
    main_df = pd.DataFrame()
    for file in os.listdir(directory):
        star_name = str(file).replace('tess2019331140908-s0019-000000', '')
        star_name = star_name.replace('-0164-s_lc.fits', '')
        lc_df = FitsToPandas(file)
        ind = 0
        time = 0
        flux = 0
        lst = []
        for row in lc_df:
            ind += 1
            time += row['TIME']
            flux += row['PDCSAP_FLUX']
            if ind % 32 == 0:
                avg_time = time / 32
                avg_flux = flux / 32
                lst.append(avg_time)
                lst.append(avg_flux)
                time = 0
                flux = 0
        main_df.loc[star_name] = lst
        return main_df

if __name__ == '__main__':
    df = OneDataframe('../data/light_curves/sector_19')