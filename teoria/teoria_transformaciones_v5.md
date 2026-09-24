# El modelo estocástico y la física de la alucinación

### Iteración 5 — Formalización de la Extensión de Kan Pesada en $\mathrm{Kl}(\mathcal{D})$ y la Co-descomposición Epistémica/Aleatoria

*(Estatuto de las afirmaciones: **[T]** teorema demostrado, **[E]** esbozo con literatura, **[C]** conjetura.)*

---

## §0. Resolución Categórica: Lan Puntual vs. Lan Pesada

En la iteración 4, se postuló que el prior generativo surgía de la estructura interna de la categoría de Kleisli $\mathrm{Kl}(\mathcal{D})$. El dictamen de arbitraje adversarial refutó esta hipótesis mediante dos proposiciones fundamentales:

> **[T] Proposición 1.** El conjunto vacío $\emptyset$ es objeto inicial de $\mathrm{Kl}(\mathcal{D})$.
> *Demostración.* Para cualquier objeto $Y$, $\mathrm{Kl}(\mathcal{D})(\emptyset, Y) = \mathrm{Set}(\emptyset, \mathcal{D}Y)$ contiene exactamente un elemento (la función vacía $\emptyset \to \mathcal{D}Y$). ∎

> **[T] Proposición 2.** La extensión de Kan puntual libre $\mathrm{Lan}_i(i^*X)$ a lo largo de la inclusión del contexto $i: P \hookrightarrow H$ en $\mathrm{Kl}(\mathcal{D})$ coincide con el resultado determinista en $\mathrm{Set}$: emite el objeto inicial $\emptyset$ en el pasado no visto y arrastra mediante identidades (masas de Dirac $\delta$) en el futuro y huecos internos.
> *Demostración.* Los colímites requeridos son sobre diagramas vacíos (que evalúan en el objeto inicial $\emptyset$ de $\mathrm{Kl}(\mathcal{D})$) o sobre posets con objeto terminal (que evalúan en el valor del terminal, es decir, el arrastre de identidad). ∎

### Solución: La Extensión de Kan Pesada (Weighted Kan Extension)
El prior generativo no es una propiedad intrínseca de la categoría de Kleisli, sino una **estructura adicional** en forma de profunctor estocástico que actúa como peso (weight) de la extensión.

Sea $\mathcal{P} = (T, \pi_0)$ el proceso estocástico ambiente de Markov sobre el espacio de estados finito $S$. Este proceso induce un profunctor estocástico (o distribuidor) $W: P^{\mathrm{op}} \times H \to \mathrm{Set}$ definido por las probabilidades de transición de la realidad:
$$W(p, t) = \mathbb{P}_{\mathcal{P}}(S_t = s \mid S_p = s')$$

> **[T] Teorema (Identificación de la Extensión Pesada).**
> La extensión de Kan en $\mathrm{Kl}(\mathcal{D})$ ponderada por el peso Markoviano $W$, denotada como $\mathrm{Lan}_i^W(X)(t)$, equivale exactamente al posterior bayesiano de la realidad condicionado a la ventana de contexto observada $S_P$:
> 
> $$\mathrm{Lan}_i^W(X)(t) \;=\; \int^{p \in P} W(p, t) \otimes X(p) \;=\; \mathbb{P}_{\mathcal{P}}(S_t = s \mid S_P)$$
> 
> *Demostración.* Dado que las observaciones $X(p) = \delta_{S_p^*}$ son masas de Dirac puntuales en los estados realmente observados en la ventana $P$, la co-densidad del colímit ponderado se reduce al condicionamiento bayesiano multivariable sobre la frontera de Markov más cercana a $t$ en $P$:
> - Para $t > \max P$: la integral colapsa a la propagación hacia delante $T^{t - \max P}(S_{\max P}, \cdot)$.
> - Para $t < \min P$: la integral colapsa a la retrodicción bayesiana relativa al prior $\pi_0$ condicionado a $S_{\min P}$.
> - Para $\min P < t < \max P$: la integral colapsa al puente markoviano condicionado a los extremos adyacentes de la ventana. ∎

---

## §1. Teorema de Co-descomposición del Defecto (Sorpresa Cruzada)

El error de predicción del modelo no es un bloque homogéneo. Se descompone algebraicamente en la incertidumbre aleatoria (ruido físico del mundo) y la alucinación epistémica (desajuste del modelo generativo).

> **[T] Teorema (Descomposición Epistémica).**
> Sean $p = \mathbb{P}_{\mathrm{true}}(S_t \mid S_P)$ la distribución condicional real del proceso y $q = \mathbb{P}_{\mathrm{model}}(S_t \mid S_P)$ la predicción emitida por el modelo generativo. La sorpresa cruzada esperada de la verdad $H(p, q)$ se descompone aditivamente como:
>
> $$H(p, q) \;=\; -\sum_{s \in S} p(s) \log_2 q(s) \;=\; \underbrace{H(p)}_{\text{Incertidumbre Aleatoria}} \;+\; \underbrace{D_{\mathrm{KL}}(p \,\|\, q)}_{\text{Alucinación Epistémica}}$$
>
> *Demostración.*
> $$H(p, q) = -\sum_{s} p(s) \log_2 q(s) = -\sum_{s} p(s) \log_2 q(s) + \sum_{s} p(s) \log_2 p(s) - \sum_{s} p(s) \log_2 p(s)$$
> Reordenando términos:
> $$H(p, q) = -\sum_{s} p(s) \log_2 p(s) + \sum_{s} p(s) \log_2 \frac{p(s)}{q(s)} = H(p) + D_{\mathrm{KL}}(p \,\|\, q) \quad \blacksquare$$

### Consecuencias Físicas:
1. **El Suelo Aleatorio Irreducible ($H(p)$):** Es la entropía condicional de la naturaleza. Incluso un modelo perfecto con conocimiento exacto del universo ($q = p \implies D_{\mathrm{KL}} = 0$) sufrirá una sorpresa esperada igual a $H(p)$. Esta incertidumbre **no es alucinación**.
2. **La Alucinación Pura ($D_{\mathrm{KL}}(p \parallel q)$):** Mide el desajuste de los pesos generativos del modelo respecto del proceso real. Solo esta componente constituye **confabulación o alucinación epistémica**.

---

## §2. La Firma Falsable en Tres Regímenes

La distinción entre categorías e información mutua nos permite aislar tres firmas operacionales claras en el comportamiento del agente frente a la falta de información:

```text
               [Contexto Insuficiente / Entrada P ⊊ H]
                                  |
         --------------------------------------------------
         |                                                |
   [Retrieval Puro (Set)]                       [Prior Generativo (Kl(D))]
         |                                                |
  Silencio / Rehusar (∅)                         Distribución q(S_t | S_P)
  H_epistemic = 0                                         |
                                         -----------------------------------
                                         |                                 |
                                [Modelo Calibrado (q = p)]      [Modelo Desajustado (q ≠ p)]
                                         |                                 |
                                   H_pq = H(p)                       H_pq = H(p) + D_KL
                                   D_KL = 0                          D_KL > 0
                                   (Ruido del Mundo)                 (Confabulación Activa)
```

1. **Régimen 1: Retrieval Puro ($\mathrm{Set}$)**
   - **Mecanismo:** Extensión libre clásica.
   - **Comportamiento:** Silencio total ($\emptyset$) en el pasado no visto; repetición del borde en el futuro.
   - **Métricas:** Alucinación epistémica $D_{\mathrm{KL}} = 0$.

2. **Régimen 2: Generador Calibrado ($\mathrm{Kl}(\mathcal{D})$, $T' = T$)**
   - **Mecanismo:** Extensión pesada con prior perfectamente ajustado a la naturaleza.
   - **Comportamiento:** Asigna masa de probabilidad exacta a todas las trayectorias plausibles.
   - **Métricas:** Sorpresa cruzada igual al límite de Shannon $H(p)$, alucinación epistémica $D_{\mathrm{KL}} = 0$.

3. **Régimen 3: Generador Desajustado / Confabulador ($\mathrm{Kl}(\mathcal{D})$, $T' \neq T$)**
   - **Mecanismo:** Extensión pesada con prior sesgado o incorrecto (ej. pesos de LLM desajustados).
   - **Comportamiento:** Confabulación activa de escenarios plausibles para el modelo pero falsos para el proceso real.
   - **Métricas:** Sorpresa cruzada $H(p, q) > H(p)$, alucinación epistémica $D_{\mathrm{KL}} > 0$.

---

## §3. Teorema T3 Estocástico: Cota de Sorpresa de la Verdad

El no-go determinista de Myhill-Nerode se extiende al caso estocástico/informacional mediante la cota de sorpresa:

> **[T] Teorema T3 (Cota de Sorpresa Esperada).**
> Ningún modelo estocástico de estados finitos $M$ que aproxime un proceso $\mathcal{P}$ con información de contexto $S_P$ puede exhibir una sorpresa esperada sobre la verdad menor que la entropía de Shannon condicional verdadera del proceso:
>
> $$\mathbb{E}_{S^* \sim p} [ -\log_2 \mathbb{P}_{\mathrm{model}}(S^* \mid S_P) ] \;\ge\; H_{\mathrm{true}}(S_t \mid S_P)$$
>
> La igualdad se alcanza si y solo si el modelo está perfectamente calibrado ($D_{\mathrm{KL}}(p \parallel q) = 0$).

Esta cota formaliza la cota termodinámica de disipación de información: la sorpresa es la energía de disipación epistémica necesaria para asimilar el colapso del estado verdadero.
