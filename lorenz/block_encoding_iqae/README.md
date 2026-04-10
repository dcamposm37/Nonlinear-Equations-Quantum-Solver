# Block Encoding con IQAE - Lorenz System

## Descripción General

Esta carpeta implementa la simulación del **atractor de Lorenz** utilizando **Block Encoding** con **Iterative Quantum Amplitude Estimation (IQAE)**. Este enfoque representa una demostración de concepto para computación cuántica tolerante a fallas (fault-tolerant).

El sistema de Lorenz es un sistema dinámico tridimensional caótico descrito por:

```
dx/dt = σ(y - x)
dy/dt = x(ρ - z) - y
dz/dt = xy - βz
```

Donde:
- `σ` = 10.0 (número de Prandtl)
- `ρ` = 28.0 (número de Rayleigh)
- `β` = 8/3 ≈ 2.667 (proporción física)

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `block_encoding_iqae.py` | Simulación con estimación de amplitud iterativa (proof-of-concept fault-tolerant) |

## Principio del Algoritmo

### 1. Discretización de Euler

El método de Euler explícito linealiza el sistema:

```
x[n+1] = x[n] + dt·σ·(y[n] - x[n])
y[n+1] = y[n] + dt·(x[n]·(ρ - z[n]) - y[n])
z[n+1] = z[n] + dt·(x[n]·y[n] - β·z[n])
```

Esta discretización se codifica en una **matriz de evolución A** de 8×8 que incluye términos auxiliares para las no linealidades (productos xy y xz).

### 2. Transformación de Similaridad

Para mejorar la estabilidad numérica, se aplica una transformación de escala:

```
W = diag[1/20, 1/30, 1/50, 1/1000, 1/600, 1, 1, 1]
A_scaled = W · A · W⁻¹
```

Esto evita la "inanicición de precisión" (precision starvation) en los estados cuánticos.

### 3. Block Encoding Estándar

La matriz normalizada `A_norm = A_scaled / ‖A‖₂` se codifica en una unitaria extendida:

```
U = [ A_norm      √(I - A_norm·A_normᵀ) ]
    [ √(I - A_normᵀ·A_norm)    -A_normᵀ ]
```

Esta es la construcción estándar de block encoding que requiere **1 qubit ancilla** adicional.

### 4. Iterative Quantum Amplitude Estimation (IQAE)

En lugar de usar mediciones directas con ruido de shot, este método **simula IQAE** calculando las probabilidades exactas del statevector:

1. **Probabilidades extraídas**: 
   - `P(0...0) = |x|²`
   - `P(0...1) = |y|²`
   - `P(1...0) = |z|²`
   
2. **Estimación de recursos**: Calcula cuántas consultas al oráculo serían necesarias para lograr un error relativo del 1%:
   ```
   N_oracle ≈ π / (4 · ε)  donde ε = 0.01 · √P
   ```

3. **Magnitudes reconstruidas**:
   ```
   |x| = √(P_x) · α · ‖state‖
   ```

### 5. Heurística de Continuidad (Sign Trick)

Como IQAE solo proporciona magnitudes (no fases), se usa una heurística clásica para determinar los signos:

```
dx = dt·σ·(y_prev - x_prev)
sign_x = +1 si (x_prev + dx) ≥ 0, sino -1
```

Esto asume continuidad temporal (la inercia de Euler).

## Características Clave

- **Sin ruido de shot**: Simula el límite de precisión infinita de IQAE
- **Estimación de recursos**: Calcula consultas teóricas al oráculo para cada paso
- **Fault-tolerant POC**: Demuestra el costo potencial en hardware cuántico tolerante a fallas
- **1 qubit ancilla**: Requiere solo un qubit adicional para el block encoding

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
python -m lorenz.block_encoding_iqae.block_encoding_iqae
```

## Salidas

Los resultados se guardan en:
- `figures/lorenz_be_iqae_3d.png` - Visualización 3D del atractor
- `figures/lorenz_be_iqae_2d.png` - Proyecciones 2D (XY, XZ, YZ)
- `figures/lorenz_be_iqae_error_log.png` - Gráfico de divergencia de error

## Comparación con Block Encoding Estándar

| Aspecto | Block Encoding | Block Encoding + IQAE |
|---------|---------------|----------------------|
| Mediciones | Directas (con ruido) | Estimadas (sin ruido) |
| Hardware | NISQ | Fault-tolerant |
| Precisión | Limitada por shots | Limitada por algoritmo |
| Costo | O(1/ε²) shots | O(1/ε) consultas oráculo |
| Fases | Requiere QPE | IQAE proporciona magnitudes |

## Limitaciones

1. **Heurística de signo**: Requiere pasos de tiempo pequeños para mantener continuidad
2. **Dimensión fija**: Limitado a 8 dimensiones (3 variables + 5 auxiliares)
3. **Linealización**: El método de Euler introduce error de truncamiento

## Referencias

1. **Nielsen, M. A. & Chuang, I. L.** (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
2. **Suzuki, Y., et al.** (2020). *Amplitude Estimation without Phase Estimation*. Quantum Information Processing.
3. **Lorenz, E. N.** (1963). *Deterministic Nonperiodic Flow*. Journal of the Atmospheric Sciences.
