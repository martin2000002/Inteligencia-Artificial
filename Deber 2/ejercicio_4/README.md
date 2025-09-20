Requisitos
- SWI-Prolog instalado (https://www.swi-prolog.org/).

Uso desde PowerShell (Windows)
1) Abrir PowerShell y cambiar al directorio del ejercicio:
   cd "C:\Users\<tu_usuario>\...\Deber 2\ejercicio_4"

2) Ejecutar el solver que tenga `:- initialization(run, main).` en su archivo:
   swipl -q -s fwgc_solver.pl
   swipl -q -s mc_solver.pl