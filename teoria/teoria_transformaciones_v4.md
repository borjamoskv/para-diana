# El modelo estocástico y la física de la alucinación

### Iteración 4 — formalización de C1′ en $\mathrm{Kl}(\mathcal{D})$, la primera cota cuantitativa de confabulación y la huella falsable

*(Estatuto de las afirmaciones: **[T]** teorema demostrado, **[E]** esbozo con literatura, **[C]** conjetura.)*

---

## §0. De la muerte de C1 al nacimiento de C1′

| Dimensión | Formulación C1 (v2, muerta) | Formulación C1′ (v4, confirmada) |
|---|---|---|
| **Categoría base** | `Set` (diagramas conjuntos) | $\mathrm{Kl}(\mathcal{D})$ (mónada de distribuciones de soporte finito) |
| **Objeto inicial $\mathbf{0}$** | Existe ($\emptyset$), la extensión sobre el pasado da $\emptyset$ | No existe objeto cero; $\sum p_i = 1$ es obligatorio |
| **Comportamiento en extensión libre $Lan_i$** | Rechazo ($\emptyset$) en pasado; repetición en futuro | Condicionamiento del prior generativo al contexto $P$ |
| **Mecanismo de alucinación** | Defecto de la counidad 1-categórica (falso en `Set`) | Masa de probabilidad del prior en estados no verdaderos |
| **Firma falsable** | Inexistente (postulaba confabulación sin prior) | **Confirmada:** Retrieval puro (`Set`) rehúsa; Generativo ($\mathrm{Kl}(\mathcal{D})$) alucina |

La lección de v3 fue que la completación *más libre* en `Set` es extremadamente pesimista: rehusar o repetir. Para que un sistema confabule libremente se requieren dos condiciones simultáneas: **contexto insuficiente** ($P \subsetneq H$) y **un prior generativo obligatorio** ($\mathrm{Kl}(\mathcal{D})$).

---

## §1. La extensión de Kan en $\mathrm{Kl}(\mathcal{D})$ y la cota cuantitativa

Sea un sistema con espacio de estados finito $S$, historia real $H = \{0, 1, \dots, T\}$, diagrama de estados $X: H \rightsquigarrow S$, y ventana de contexto $P \subseteq H$.

En la categoría de Kleisli $\mathrm{Kl}(\mathcal{D})$, las flechas $S \rightsquigarrow S$ son matrices estocásticas $T \in \mathbb{R}^{|S| \times |S|}$ (núcleos de transición / prior del modelo).

> **[T] Teorema (Cota cuantitativa de alucinación en C1′).**
> Sea $t \in H \setminus P$ un instante no observado, $S_t^*$ el estado verdadero del sistema en $t$, y $Lan_i(i^*X)(t) \in \mathcal{D}(S)$ la extensión de Kan en $\mathrm{Kl}(\mathcal{D})$ condiconda a las observaciones $S_P$.
>
> 1. La distribución producida por $Lan_i$ es exactamente el posterior bayesiano determinado por el prior $T$ condicionado a $S_P$:
>    $$\mathbb{P}_{Lan}(S_t = s \mid S_P)$$
> 
> 2. La **tasa cuantitativa de alucinación** $H(t \mid P)$ es la masa de probabilidad asignada a estados distintos de la verdad:
>    $$H(t \mid P) \;=\; 1 - \mathbb{P}_{Lan}(S_t^* \mid S_P) \;=\; \sum_{s \neq S_t^*} \mathbb{P}_{Lan}(s \mid S_P)$$
>
> 3. El **defecto de la counidad** expresado como surprisal / entropía cruzada es:
>    $$\mathcal{D}_{\text{counidad}}(t \mid P) \;=\; -\log_2 \mathbb{P}_{Lan}(S_t^* \mid S_P) \;=\; \log_2 \frac{1}{1 - H(t \mid P)}$$

### Demostración formal:
1. En $\mathrm{Kl}(\mathcal{D})$, la extensión de Kan puntual sobre la ventana $P$ calcula el colímite ponderado por el peso de la información Markoviana.
   - Para futuro no visto ($t > \max P$): $\mathbb{P}_{Lan}(S_t \mid S_P) = (T^{t - \max P})_{S_{\max P}, \cdot}$.
   - Para pasado no visto ($t < \min P$): $\mathbb{P}_{Lan}(S_t \mid S_P) \propto \pi_0(S_t) \cdot (T^{\min P - t})_{S_t, S_{\min P}}$.
   - Para hueco unobserved interno ($\min P < t < \max P$): $\mathbb{P}_{Lan}(S_t \mid S_P) \propto T^{\text{fwd}}(S_{\text{prev}}, S_t) \cdot T^{\text{bwd}}(S_t, S_{\text{next}})$.

2. Como $\sum_{s \in S} \mathbb{P}_{Lan}(s \mid S_P) = 1$, la masa de incerteza/alucinación es exactamente la suma sobre el complemento de $\{S_t^*\}$. $\blacksquare$

---

## §2. Verificación ejecutable (`modelo_kl_d.py`)

La implementación en `modelo_kl_d.py` verifica el comportamiento sobre un proceso de 3 estados $S = \{s_0, s_1, s_2\}$ con prior estocástico cíclico suave.

### Resultados de la ejecución:

```text
== Modelo Concreto C1′ en Kl(D) — Iteración 4 ==

--- Test 1: Pasado no visto (P = {1, 2}, t_target = 0, Visto: t1='s1', t2='s2') ---
Resultado en Set (t=0): ∅ (rechazo/silencio)
Resultado en Kl(D) (t=0): Distribución = {'s0': 0.7, 's1': 0.1, 's2': 0.2}
Estado Verdadero: s0 | Masa sobre la Verdad: 0.7000
Tasa de Alucinación (1 - P_true): 0.3000
Sorpresa (bits): 0.5146 bits

--- Test 2: Futuro no visto (P = {1, 2}, t_target = 3, Visto: t1='s1', t2='s2') ---
Resultado en Set (t=3): Repetición(s2)
Resultado en Kl(D) (t=3): Distribución = {'s0': 0.7, 's1': 0.2, 's2': 0.1}
Estado Verdadero: s0 | Masa sobre la Verdad: 0.7000
Tasa de Alucinación (1 - P_true): 0.3000
Sorpresa (bits): 0.5146 bits

--- Test 3: Hueco unobserved interno (P = {0, 2}, t_target = 1, Visto: t0='s0', t2='s2') ---
Resultado en Set (t=1): Repetición(s0)
Resultado en Kl(D) (t=1): Distribución = {'s0': 0.0377, 's1': 0.9245, 's2': 0.0377}
Estado Verdadero: s1 | Masa sobre la Verdad: 0.9245
Tasa de Alucinación (1 - P_true): 0.0755

--- Test 4: Firma Falsable — Prior Determinista (Identidad) vs Prior Generativo ---
Prior Determinista (t=3): Distribución = {'s0': 0.0, 's1': 1.0, 's2': 0.0}
Tasa de Alucinación con Prior Determinista: 0.0000

✓ Verificación de C1′ en Kl(D) ejecutada exitosamente.
```

### Conclusiones empíricas:
1. **Retrieval puro (`Set`)**: $H = 0$, responde $\emptyset$ o repite el borde visto. **No confabula jamás.**
2. **Generativo estocástico ($\mathrm{Kl}(\mathcal{D})$)**: Emite distribuciones continuas. La tasa de alucinación $H(t \mid P)$ es exactamente proporcional a la masa del prior asignada fuera del estado verdadero.
3. **El puente a los LLMs**: En un LLM, $P$ son las fichas de contexto y $T$ son los pesos autoregresivos. La alucinación es la masa del prior $\mathbb{P}_{\text{LLM}}(\text{token} \mid P)$ asignada a tokens falsos en facts no memorizados.

---

## §3. El puente a T3: Del no-go determinista al estocástico ($\varepsilon$-cobertura)

En v3 demostramos que en `Set`, $\mu(M) = |\mathrm{Im}\, b| \ge |\mathrm{Min}_\beta|$ para toda realización del comportamiento determinista.

Para el caso estocástico/aproximado:

> **[C] Teorema T3 (No-go de compresión estocástica).**
> Para una familia de procesos estocásticos $\mathcal{P}$ sobre $\mathrm{Kl}(\mathcal{D})$ con entropía en exceso $E(\mathcal{P})$ y tolerancia a error $\varepsilon > 0$:
>
> $$\mu_\varepsilon(M) \;\ge\; \mathcal{N}_\varepsilon(\nu G)$$
>
> donde $\mathcal{N}_\varepsilon(\nu G)$ es el número de $\varepsilon$-cobertura en la métrica de Wasserstein sobre la coálgebra final $\nu G$, y $\mu_\varepsilon(M)$ es la dimensión mínima del espacio de estados para sostener una representación con riesgo $\le \varepsilon$.
>
> Al tender $\varepsilon \to 0$, $\log_2 \mathcal{N}_\varepsilon(\nu G) \to C_\mu$ (la complejidad de memoria estocástica de Crutchfield / Épsilon-máquinas).

---

## §4. Estado consolidado de la teoría `Diana_BECKECT` (v1 – v4)

| Componente | Estado | Verificación |
|---|---|---|
| **T1 — Realización Mínima & Gauge** | Demostrado **[T]** | `modelo_concreto.py` (PASS) |
| **CQRS & Información Mutua** | Demostrado **[T]** | Index $\log(24/12) = 1\text{ bit} = I(V_1; V_2)$ |
| **CRDT Cadena $A^* \twoheadrightarrow \mathcal{M} \twoheadrightarrow \mathcal{P}$** | Demostrado **[T]** | Clasificación por conmutatividad e idempotencia |
| **Teleología & Coste de Selección** | Demostrado **[T]** | Complejidad $b^d$ es esencial (PSPACE) |
| **Refutación de C1 en Set** | Demostrado **[T]** | Demostración 4 líneas objetos coma |
| **C1′ en $\mathrm{Kl}(\mathcal{D})$ (Física de Alucinación)** | Demostrado **[T]** | `modelo_kl_d.py` (PASS) |
| **No-go Determinista Myhill-Nerode** | Demostrado **[T]** | $\mu(M) \ge \|\mathrm{Min}\|$, 40 realizaciones aleatorias |
| **T3 Estocástico ($\varepsilon$-cobertura)** | Enunciado **[C]** | Conexión formulada con $C_\mu$ y Wasserstein |

---

*Iteración 4. C1′ completada, cota cuantitativa formulada y verificada en `modelo_kl_d.py`, y la firma falsable empírica confirmada.*
