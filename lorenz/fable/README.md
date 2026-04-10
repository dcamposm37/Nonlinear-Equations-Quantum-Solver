# FABLE - Fast Approximate Block Encoding for Lorenz System

## Descripción General

Esta carpeta implementa la simulación del **atractor de Lorenz** utilizando **FABLE** (Fast Approximate Block Encoding), una técnica eficiente para codificar matrices en circuitos cuánticos. FABLE es particularmente útil para matrices que son aproximadamente unitarias o tienen bloques unitarios.

El sistema de Lorenz caótico tridimensional:

```
dx/dt = σ(y - x)
dy/dt = x(ρ - z) - y
dz/dt = xy - βz
```

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `fable_statevector.py` | Simulación exacta usando statevector con la librería FABLE |

## ¿Qué es FABLE?

**FABLE** (Fast Approximate Block Encoding) es un algoritmo que construye circuitos cuánticos para codificar matrices de forma eficiente, especialmente cuando la matriz tiene estructura especial (como ser dispersa o aproximadamente unitaria).

### Ventajas de FABLE

- **Eficiencia**: Menor profundidad de circuito que block encoding estándar
- **Sin qubits ancilla adicionales**: Usa solo los qubits necesarios para la matriz
- **Aproximación controlada**: Permite establecer umbrales de corte para elementos pequeños

## Principio del Algoritmo

### 1. Codificación del Sistema de Lorenz

La matriz de evolución de Euler de 8×8 se construye como:

```
A = [1-dt·σ   dt·σ      0       0     0  0  0  0]
    [dt·ρ     1-dt      0     -dt     0  0  0  0]
    [0        0     1-dt·β     0    dt  0  0  0]
    [0        0         0       1     0  0  0  0]
    [0        0         0       0     1  0  0  0]
    ...
```

Incluye variables auxiliares para capturar las no linealidades (xz y xy).

### 2. Transformación de Similaridad

Se aplica un escalado diagonal para estabilidad numérica:

```
W = diag[1/20, 1/30, 1/50, 1/1000, 1/600, 1, 1, 1]
A_scaled = W · A · W⁻¹
```

### 3. Construcción del Circuito FABLE

```python
from fable import fable
fable_circ, alpha_fable = fable(A_normalized)
```

FABLE construye automáticamente un circuito cuántico que implementa el block encoding aproximado de la matriz.

### 4. Evolución Paso a Paso

Para cada paso de tiempo:

1. **Preparar estado**: `|ψ₀⟩ = scaled_state / ‖scaled_state‖`
2. **Aplicar FABLE**: `|ψ'⟩ = FABLE(A) |0...0⟩ ⊗ |ψ₀⟩`
3. **Extraer amplitudes**: Del statevector donde ancillas = |0...0⟩
4. **Rescaling**: `x_new = |x_sv| · 2ⁿ · ‖A‖ · ‖state‖`

### 5. Heurística de Signo (Estructural)

FABLE proporciona magnitudes absolutas. Los signos se determinan por continuidad:

```
dx = dt·σ·(y_prev - x_prev)
sign_x = +1 si (x_prev + dx) ≥ 0
```

Luego se aplican los signos a las variables auxiliares:
- `xz = sign_x · sign_z · |xz_raw|`
- `xy = sign_x · sign_y · |xy_raw|`

### 6. Restricción Geométrica

Después de cada paso, se reimponen las relaciones no lineales:

```
state[3] = state[0] · state[2]  # xz = x·z
state[4] = state[0] · state[1]  # xy = x·y
```

Esto garantiza consistencia con la física del sistema.

## Características Clave

- **Sin ruido de medición**: Usa statevector exacto
- **Eficiencia de circuito**: FABLE optimiza la profundidad del circuito
- **Protección contra "origin trap"**: Estados inicializados con padding en ceros
- **Compresión automática**: FABLE puede ignorar elementos menores a un umbral

## Parámetros

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `DT` | 0.01 | Paso de tiempo |
| `SIGMA` | 10.0 | Número de Prandtl |
| `RHO` | 28.0 | Número de Rayleigh |
| `BETA` | 8/3 | Proporción geométrica |
| `X0, Y0, Z0` | (1, 1, 1) | Condiciones iniciales |
| `T_FINAL` | 10.0 | Tiempo total de simulación |

## Uso

```bash
python -m lorenz.fable.fable_statevector
```

## Salidas

Los resultados se guardan en:
- `figures/lorenz_fable_sv_3d.png` - Visualización 3D del atractor
- `figures/lorenz_fable_sv_2d.png` - Proyecciones 2D (XY, XZ, YZ)
- `figures/lorenz_fable_sv_error_log.png` - Gráfico de divergencia de error

## Comparación: Block Encoding vs FABLE

| Aspecto | Block Encoding Estándar | FABLE |
|---------|------------------------|-------|
| Qubits ancilla | 1+ | 0 (solo qubits de datos) |
| Profundidad | Mayor | Menor (optimizada) |
| Precisión | Exacta (unitaria) | Aproximada (con umbral) |
| Construcción | Manual (matriz extendida) | Automática (librería) |
| Compresión | No | Sí (umbrales de corte) |

## Variante: S-FABLE

Existe una variante **S-FABLE** (Sparse FABLE) que:
- Transforma la matriz a la base de Walsh-Hadamard: `M = Hⁿ · A · Hⁿ`
- Aplica FABLE a M (más disperso en esta base)
- Recupera el estado aplicando Hⁿ al final

Esto puede ofrecer mejor compresión para matrices dispersas. Ver `lorenz/sfable/`.

## Dependencias

```bash
pip install fable-circuits
```

Librería oficial de FABLE para Python.

## Limitaciones

1. **Heurística de signo**: Requiere continuidad temporal
2. **Heurística estructural**: Requiere reimposición manual de xz = x·z
3. **Complejidad**: Aunque optimizado, sigue siendo exponencial en el número de qubits

## Referencias

1. **Camps, E., et al.** (2022). *FABLE: Fast Approximate Block Encodings*. arXiv preprint.
2. **Lorenz, E. N.** (1963). *Deterministic Nonperiodic Flow*. Journal of the Atmospheric Sciences.
3. **Qiskit Contributors.** (2023). *Qiskit: An open-source framework for quantum computing*.
