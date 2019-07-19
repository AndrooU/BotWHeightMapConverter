@echo off
if not exist "terrain" mkdir "terrain"
for %%x in (*.hght.sstera) do (
wszst dec %%x --dest %%~nx.stera
sarc x %%~nx.stera -C "terrain"
del %%~nx.stera
)