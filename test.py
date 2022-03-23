import pandas as pd
import logging

startcol = "Descrizione"
findcol = "RASAERBA 4850 SB"
relcol = "Codice"
rel2col = "Listino iva compresa"

df = pd.read_excel('./listini/Active2021.xlsx')
df2 = df.loc[df[startcol] == findcol, relcol].item()
df3 = df.loc[df[startcol] == findcol, rel2col].item()
print(df2, df3)