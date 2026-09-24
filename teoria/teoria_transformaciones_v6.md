# El modelo estocástico y la física de la alucinación

### Iteración 6 — Formalización de C1′ en Categorías de Markov mediante Desintegración Bayesiana y Co-descomposición de Sorpresa

*(Estatuto de las afirmaciones: **[T]** teorema demostrado, **[E]** esbozo con literatura, **[C]** conjetura.)*

---

## §0. Fundamento Categórico: Categorías de Markov

La iteración 5 intentó resolver la Conjetura 1′ ($C1'$) mediante extensiones de Kan pesadas en $\mathrm{Kl}(\mathcal{D})$. Sin embargo, la formulación de colímites pesados en categorías estocásticas carece de una estructura monoidal cerrada natural y no captura el condicionamiento conjunto sobre múltiples puntos de observación.

La formalización rigurosa se obtiene tratando a $\mathrm{Kl}(\mathcal{D})$ como una **Categoría de Markov** (Fritz, 2020; Cho-Jacobs, 2019).

### Definición: Categoría de Markov
Una Categoría de Markov es una categoría monoidal simétrica $(\mathcal{C}, \otimes, \mathbf{1})$ donde cada objeto $X$ está equipado con una estructura de comonoides cocomutativa:
- **Copia (Duplicación):** $\Delta_X: X \to X \otimes X$
- **Descarte (Eliminación):** $!_X: X \to \mathbf{1}$

Sujeta a los axiomas de comonoides y a la condición de que el descarte $!_X$ sea una transformación natural, lo que exige que todo morfismo $f: X \to Y$ sea **estocástico (conservador de probabilidad)**:
$$!_Y \circ f \;=\; !_X$$

En $\mathrm{Kl}(\mathcal{D})$, esto equivale exactamente a la condición de que todas las matrices de transición tengan filas que suman exactamente 1 ($\sum_j P(s_j \mid s_i) = 1$).

---

## §1. La Desintegración Bayesiana como la Solución Categórica a C1′

Sea un sistema con espacio de estados finito $S$, historia real $H = \{0, 1, \dots, T\}$, y ventana de contexto $P \subseteq H$.

El proceso estocástico ambiente $\mathcal{P}$ se modela como un **estado conjunto** $\rho: \mathbf{1} \to S^H$ en la categoría monoidal $\mathrm{Kl}(\mathcal{D})$. 
Para cualquier instante no observado $t \notin P$, la marginalización del proceso sobre los índices de interés $P \cup \{t\}$ se obtiene descartando el resto de variables mediante el operador $!$, resultando en el estado conjunto:
$$\rho_{P \cup \{t\}}: \mathbf{1} \to S^P \otimes S$$

> **[T] Teorema (Desintegración Bayesiana de C1′).**
> La extensión de información al instante no observado $t$ condicionado a la evidencia observada en la ventana $P$ está determinada por la **desintegración bayesiana** del estado conjunto $\rho_{P \cup \{t\}}$ respecto a la proyección sobre $S^P$.
>
> Existe un canal (morfismo de Kleisli) $\rho_{t \mid P}: S^P \to S$ que satisface la ecuación de compatibilidad:
> 
> $$\rho_{P \cup \{t\}} \;=\; (\mathrm{id}_{S^P} \otimes \rho_{t \mid P}) \circ \Delta_{S^P} \circ \rho_P$$
>
> donde $\rho_P: \mathbf{1} \to S^P$ es la marginal sobre la ventana de contexto.
>
> *Demostración.* En la categoría de Kleisli $\mathrm{Kl}(\mathcal{D})$, todo estado conjunto de soporte finito admite desintegración bayesiana (Cho-Jacobs, 2019). Esta desintegración equivale a condicionar la distribución conjunta mediante la regla de Bayes, y es **única casi seguramente (c.s.)** respecto a la medida marginal $\rho_P$. ∎

### Resolución de Regímenes Temporales mediante Disolución Markoviana:
Debido a la estructura de Markov del proceso ambiente, la desintegración conjunta $\rho_{t \mid P}$ colapsa a la vecindad inmediata en $P$:
1. **Pasado no visto ($t < \min P$):** La desintegración de $\rho_{\{t, \min P\}}$ requiere el prior inicial $\pi_0$ y el canal de transición $T$, resultando en la retrodicción bayesiana (inversión en la categoría de Markov):
   $$\rho_{t \mid \min P} \;=\; T^\dagger$$
2. **Futuro no visto ($t > \max P$):** La desintegración colapsa a la propagación directa del canal desde el último estado visto:
   $$\rho_{t \mid \max P} \;=\; T^{t - \max P}$$
3. **Hueco interno ($\min P < t < \max P$):** La desintegración colapsa al puente markoviano condicionado a los extremos adyacentes $p_{\mathrm{prev}}$ y $p_{\mathrm{next}}$ de la ventana.

---

## §2. Teorema de Co-descomposición y Tres Regímenes de Falsación

El error esperado de predicción del modelo se descompone aditivamente, separando el ruido físico del universo y el sesgo de la hipótesis del modelo.

> **[T] Teorema (Descomposición de la Sorpresa Cruzada).**
> Sean $p = \rho_{t \mid P}$ la desintegración bayesiana real de la naturaleza y $q = \rho'_{t \mid P}$ la predicción emitida por el prior generativo del modelo. La sorpresa cruzada esperada de la verdad bajo la hipótesis del modelo se descompone como:
>
> $$H(p, q) \;=\; -\sum_{s \in S} p(s) \log_2 q(s) \;=\; \underbrace{H(p)}_{\text{Incertidumbre Aleatoria}} \;+\; \underbrace{D_{\mathrm{KL}}(p \,\|\, q)}_{\text{Alucinación Epistémica}}$$
>
> *Demostración.*
> $$H(p, q) = -\sum_{s} p(s) \log_2 p(s) + \sum_{s} p(s) \log_2 \frac{p(s)}{q(s)} = H(p) + D_{\mathrm{KL}}(p \,\|\, q) \quad \blacksquare$$

### Firmas Falsables Operacionales:

1. **Régimen 1: Retrieval Puro ($\mathrm{Set}$)**
   - **Mecanismo:** Extensión clásica libre en la categoría de conjuntos.
   - **Salida:** Silencio rotundo ($\emptyset$) ante falta de contexto; repetición mecánica de bordes.
   - **Métricas:** Alucinación epistémica $D_{\mathrm{KL}} = 0$. El modelo se niega a confabular.

2. **Régimen 2: Generador Calibrado ($\mathrm{Kl}(\mathcal{D})$, $q = p$)**
   - **Mecanismo:** Desintegración bayesiana con prior perfectamente ajustado al proceso real.
   - **Salida:** Distribución estocástica que refleja la incertidumbre del mundo.
   - **Métricas:** Alucinación epistémica $D_{\mathrm{KL}} = 0$. La sorpresa esperada es mínima e igual al límite físico $H(p)$.

3. **Régimen 3: Generador Desajustado / Confabulador ($\mathrm{Kl}(\mathcal{D})$, $q \neq p$)**
   - **Mecanismo:** Desintegración bayesiana con prior incorrecto o sesgado (ej. LLM alucinando facts).
   - **Salida:** Generación de estados plausibles para el modelo pero falsos o divergentes del proceso real.
   - **Métricas:** Alucinación epistémica $D_{\mathrm{KL}} > 0$. La sorpresa del sistema aumenta debido al error de representación del modelo.

---

## §3. Teorema T3 Estocástico: Cota de Sorpresa de la Verdad

El no-go determinista de Myhill-Nerode se extiende al dominio de categorías de Markov como la cota inferior de sorpresa:

> **[T] Teorema T3 (Cota de Sorpresa Mínima).**
> Para cualquier modelo de estados finitos $M$ que represente un proceso estocástico $\mathcal{P}$ en la categoría de Markov $\mathrm{Kl}(\mathcal{D})$ bajo información de contexto $S_P$, la sorpresa esperada sobre la verdad está acotada inferiormente por la entropía condicional real del proceso:
>
> $$\mathbb{E}_{S^* \sim p} [ -\log_2 \mathbb{P}_{\mathrm{model}}(S^* \mid S_P) ] \;\ge\; H_{\mathrm{true}}(S_t \mid S_P)$$
>
> La cota se satura (igualdad) si y solo si la alucinación epistémica es nula casi seguramente: $D_{\mathrm{KL}}(p \parallel q) = 0$ c.s.
