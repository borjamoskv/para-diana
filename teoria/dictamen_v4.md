# Dictamen sobre la iteración 4

### Arbitraje adversarial de `teoria_transformaciones_v4.md` y `modelo_kl_d.py`

*(Estatuto: **[T]** demostrado aquí, **[E]** esbozo con literatura, **[C]** conjetura.)*

---

## §0. Veredicto

1. **La probabilidad es correcta y reproducible.** Re-ejecuté `modelo_kl_d.py` en entorno independiente: salida idéntica bit a bit. Además rederivé a mano la matriz *T* y el prior π₀ **desde las salidas publicadas, antes de leer el código** (los outputs sobredeterminan el modelo: circulante doblemente estocástica (0.1, 0.7, 0.2), π₀ uniforme; el puente del Test 3 da 0.49/0.53 = 0.9245 ✓). El juguete es honesto y está bien construido.

2. **La identificación categórica es falsa tal y como está enunciada.** Lo que el código computa no es la extensión de Kan de *i\*X* en Kl(𝒟). Es suavizado bayesiano del proceso ambiente — correcto como probabilidad, mal firmado como matemática.

3. **El estatuto [T] de C1′ queda revocado a [C] con instancia computada.** Y la fila «Teleología [T]» y la fila «CQRS-información-mutua [T]» de la matriz consolidada también están infladas respecto de v3; se restauran abajo.

El veredicto en una frase: **v4 hace bien la física y mal la firma — y la firma era precisamente lo que había que demostrar.**

---

## §1. Refutación del mecanismo enunciado

v4, §0: *«No existe objeto cero [en Kl(𝒟)]; ∑pᵢ = 1 es obligatorio»* — y de ahí que la extensión «se vea estructuralmente obligada a emitir una distribución».

> **[T] Proposición 1.** ∅ es objeto inicial de Kl(𝒟).
> *Demostración.* Kl(𝒟)(∅, Y) = Set(∅, 𝒟Y) tiene exactamente un elemento (la función vacía). ∎
> (Lo que sí es cierto: 𝒟(∅) = ∅ —ninguna distribución suma 1 sobre el vacío—, luego no hay morfismos *hacia* ∅ desde objetos no vacíos. Pero la inicialidad no necesita eso.)

> **[T] Proposición 2.** La Lan puntual a lo largo de *i : P ↪ [n]* en Kl(𝒟) existe y da **el mismo resultado que en Set**: ∅ en el pasado no visto, arrastre por identidad de Kleisli (masa puntual δ) en el futuro y en los huecos.
> *Demostración.* Los colímites requeridos son: el vacío (= objeto inicial = ∅, existe por Prop. 1) y colímites sobre posets con objeto terminal (= valor en el terminal, válido en cualquier categoría). La identidad de Kleisli es la unidad de la mónada: la masa puntual. ∎

**Consecuencia:** la refutación de v3 **sobrevive intacta al cambio de categoría**. La completación libre 1-categórica rehúsa o repite también en Kl(𝒟). El mecanismo «la conservación de masa prohíbe el ∅» es falso: la conservación de masa prohíbe *entrar* en ∅, no *producirlo* como valor de un colímite vacío.

**La prueba del delito está en el propio código.** La rama Set de `modelo_kl_d.py` calcula la Lan puntual correctamente (∅ / repetición / arrastre — coincide con la Proposición 2). La rama Kl(𝒟) calcula otra cosa, y se ve en qué datos usa:

| Test | Lan puntual de *i\*X* (lo enunciado) | Lo computado | Dato importado que **no** está en *i\*X* |
|---|---|---|---|
| 1 — pasado | ∅ | retrodicción bayesiana | **π₀** (prior inicial) y **T** |
| 2 — futuro | δ en s₂ (repetición) | T^(t−max P) aplicada | **T** (el kernel hacia el futuro fue olvidado por la restricción) |
| 3 — hueco | arrastre de X(0) = δ en s₀ | puente markoviano (0.9245) | **T** en ambos tramos |

La restricción *i\*X* sólo retiene los kernels compuestos **entre elementos de la ventana**. Todo lo que supera la repetición proviene de reimportar el proceso ambiente 𝒫 = (T, π₀). Cambiar Set por Kl(𝒟) no cambió la Lan; lo que cambió es el algoritmo.

---

## §2. Dónde vive C1′ de verdad

Lo anterior no mata la conjetura — la **localiza**. La tesis de dos ingredientes de v3 (contexto insuficiente **y** prior generativo) sale confirmada, pero el prior no es una propiedad de la categoría: es **estructura adicional del problema de extensión**. Candidatos formales, en orden de plausibilidad:

- **[C] Extensión de Kan pesada**, con peso el profunctor inducido por el proceso 𝒫 (enriquecimiento en probabilidades / profunctores estocásticos). La «demostración formal» de v4 dice literalmente *«el colímite ponderado por el peso de la información Markoviana»* — la palabra *ponderado* introduce de contrabando exactamente lo que hay que definir y demostrar: qué peso, en qué sentido enriquecido, y por qué el colímite pesado coincide con el condicionamiento.
- **[E] Desintegración / inversión bayesiana en categorías de Markov con condicionales** (Cho–Jacobs, *Disintegration and Bayesian inversion via string diagrams*; Fritz). El Test 3 es literalmente la desintegración del kernel compuesto T²: dado X₀ ⇝ X₁ ⇝ X₂ con el compuesto fijado, recuperar el término medio. El Test 1 es inversión bayesiana de T^k, que **requiere π₀** — la inversión bayesiana es relativa al prior, otra confirmación de que el prior es estructural.
- Nota abierta: ni siquiera está claro que sea **Lan** y no **Ran** — condicionar tiene sabor conservador (adjunto derecho), y en categorías de Markov con condicionales el cuasi-dagger difumina la distinción. En v2 las vistas materializadas eran Ran; el suavizado podría serlo también.

Y una degradación anticipada en v2 (§7, objeción 2) que aquí se materializa: los condicionales en categorías de Markov son únicos **casi seguramente**, no únicamente. El «isomorfismo único» del mundo determinista baja a «único c.s.». Es la concesión exacta a la entropía que la teoría ya tenía contabilizada.

---

## §3. La corrección conceptual: la métrica mezcla dos cosas

Éste es el punto más importante del dictamen, más que el categórico.

> **[T] Descomposición del defecto.** Sea *p* el posterior verdadero del proceso y *q* el posterior del modelo, ambos condicionados a S_P. Entonces la sorpresa esperada de la verdad se descompone:
>
> $$\mathbb{E}_{S^*\sim p}\big[-\log q(S^*\mid S_P)\big] \;=\; \underbrace{H\big(p(\cdot\mid S_P)\big)}_{\text{incertidumbre aleatoria}} \;+\; \underbrace{D_{\mathrm{KL}}\big(p \,\|\, q\big)}_{\text{alucinación epistémica}}$$
>
> *Demostración.* Regla de la cadena de la entropía cruzada. ∎

La «tasa de alucinación» H(t|P) = 1 − masa-sobre-la-verdad de v4 **mezcla ambos términos**. En el juguete, el prior del modelo ES el proceso generador (q = p), luego KL = 0: **el 0.3 medido no es confabulación — es el suelo aleatorio irreducible del propio proceso.** Un oráculo perfectamente calibrado exhibiría exactamente el mismo 0.3. Llamar a eso «alucinación» es acusar al modelo del ruido del mundo.

La definición correcta que C1′ necesita:

- **Alucinación (epistémica)** := D_KL(posterior verdadero ‖ posterior del modelo) — cero sii el modelo está calibrado con el proceso.
- **Incertidumbre (aleatoria)** := H(posterior verdadero) — irreducible, no imputable al modelo.

Consecuencia para el puente a LLMs de v4 §2: un LLM que responde «probablemente X» sobre un hecho objetivamente incierto **no está alucinando**. La firma falsable se refina: retrieval puro rehúsa (Set); generativo calibrado reparte el suelo aleatorio (KL = 0); generativo desajustado confabula (KL > 0). Tres regímenes, no dos.

**Encargo ejecutable inmediato:** repetir el juguete con un kernel desajustado T′ ≠ T y mostrar la separación de los dos términos. El juguete actual, con q = p, no puede distinguirlos por construcción.

---

## §4. Matriz de estatutos, restaurada

| Componente | v4 decía | Estatuto correcto |
|---|---|---|
| C1′ en Kl(𝒟) | [T] Demostrado | **[C]** con instancia computada y verificada; la identificación con una construcción universal (peso/desintegración) es el trabajo pendiente |
| «Teorema» de §1 v4 (puntos 2–3) | [T] | **definiciones** (normalización y −log de la misma cantidad); un diccionario, no un teorema |
| Mecanismo «no hay ∅ en Kl(𝒟)» | implícito [T] | **falso** (Proposiciones 1–2) |
| Teleología b^d | [T] Demostrado | **[T en 𝕄]** el conteo + **[E]** la esencialidad (condicional a P ≠ PSPACE), como en v3 |
| CQRS = información mutua | [T] Demostrado | **[T instancia / C general]**, como en v3 |
| T3 estocástico (ε-cobertura, Wasserstein) | [C] | [C] ✓ bien enunciado; falta fijar la métrica sobre νG |
| Refutación de C1 en Set | [T] | [T] ✓ — y ahora reforzada: vale también en Kl(𝒟) (Prop. 2) |
| Terminología | «surprisal / entropía cruzada» | la entropía cruzada es la **esperanza** del surprisal; no son sinónimos |

---

## §5. Encargo para la iteración 5

Tres entregables, en orden:

1. **El peso, enunciado y demostrado en finito.** Definir el peso W inducido por 𝒫 y demostrar, en el caso finito, que la extensión pesada (Lan o Ran — decidirlo es parte del trabajo) reproduce filtrado hacia delante / suavizado hacia atrás. Con Cho–Jacobs y Fritz como andamiaje, es abordable y convertiría C1′ en [T].
2. **La separación aleatorio/epistémico en el juguete.** T′ desajustada, medir H_true y KL por separado, exhibir los tres regímenes (rehúsa / calibrado / confabula). Una tarde.
3. **La cota como teorema central.** La descomposición de §3 ya da la forma: *la sorpresa esperada de la verdad está acotada inferiormente por la entropía condicional verdadera, con exceso exactamente KL(p‖q)*. Es el análogo estocástico del no-go determinista: allí «no puedes almacenar menos que |Min|»; aquí «no puedes sorprenderte menos que H(p)». El mismo patrón: un suelo algebraico-informacional que ninguna implementación perfora.

---

*Dictamen de la iteración 4. La instancia sobrevive; el mecanismo muere; la conjetura se degrada con honor a [C] y sale mejor localizada de lo que entró. La alucinación queda descompuesta en la parte del mundo y la parte del modelo — y sólo la segunda es alucinación.*
