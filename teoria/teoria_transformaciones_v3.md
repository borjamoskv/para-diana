# El modelo concreto y el precio de la teleología

### Iteración 3 — ejecución de T1, refutación de la Conjetura 1, el no-go determinista

*(Estatuto de las afirmaciones como en v2: **[T]** teorema demostrado aquí, **[E]** esbozo con literatura, **[C]** conjetura.)*

---

## §0. Qué murió y qué nació

| Ítem | Estado en v2 | Estado en v3 |
|---|---|---|
| **T1** — arquitecturas como corolario | programa («una tarde») | **ejecutado.** Modelo concreto 𝕄 con demostraciones completas y verificación ejecutable (`modelo_concreto.py`, 5/5). |
| **Conjetura 1** — alucinación = Lan | [C], «la de mayor valor y mayor coste» | **refutada en su forma ingenua por cálculo directo.** El adjunto izquierdo en Set no confabula: rehúsa o repite. Corregida a C1′ (Kleisli). |
| **T3** — no-go cognitivo | abierto | **resuelto en el caso determinista** (Myhill–Nerode leído como prohibición). El T3 real —estocástico, aproximado— queda enunciado con precisión. |
| **Problema abierto 1** — los óptimos no componen | abierto | **parcialmente resuelto.** Componen — por el producto de la mónada de selección — pero a coste exponencial, y la PSPACE-completitud indica que el coste es esencial. |

La pieza central metodológica: en v2 la prueba de fuego se aplicaba a los conceptos eliminados (estado, memoria, contexto, agente). En esta iteración se aplicó a las conjeturas de la propia teoría. **Una murió.** Una teoría que no puede matar sus propias conjeturas es un vocabulario.

---

## §1. El modelo 𝕄

Un modelo de A0–A5 en `Set` finito, elegido por ser el más pequeño donde todas las afirmaciones de v2 se vuelven decidibles.

**Datos.** Alfabeto finito *A* (eventos), salidas *O*, máquinas de Moore *(S, δ : S×A → S, o : S → O, s₀)*.

- **F(X) = 1 + X×A**, cuya álgebra inicial es **μF = A\*** — la historia libre, el event log.
- **G(X) = O × X^A**, cuya coálgebra final es **νG = O^{A\*}** — el espacio de comportamientos.
- **r : A\* → S** — el fold (catamorfismo): *r(ε) = s₀*, *r(wa) = δ(r(w), a)*. Reproducir el log.
- **b : S → O^{A\*}** — el unfold: *b(s)(v) = o(δ\*(s, v))*. Observar exhaustivamente.
- **β = b∘r** — el comportamiento: *β(w)(v) = o(δ\*(s₀, wv))*.

**Derivadas.** Para *φ : A\* → O* y *w ∈ A\**, defínase *φ_w(v) := φ(wv)*.

> **[T] Teorema 5′ — Realización mínima, con demostración completa.**
> Sea *φ = b(s₀)* el comportamiento observable. Defínase **Min_φ**: estados *{φ_w : w ∈ A\*}*, transición *δ(ψ, a) = ψ_a*, salida *o(ψ) = ψ(ε)*, inicial *φ_ε*. Entonces:
>
> 1. Min_φ es una máquina bien definida que realiza *φ*, con *r* sobreyectiva (alcanzable) y *b* inyectiva (observable).
> 2. Toda otra realización alcanzable y observable de *φ* es isomorfa a Min_φ por un **isomorfismo único** compatible con *r* y *b*.
>
> *Demostración.*
> (1) *ψ* determina *ψ_a*, luego δ está bien definida sobre derivadas. La realización: el unfold de Min_φ en *φ_w* es *v ↦ o(δ\*(φ_w, v)) = φ_{wv}(ε) = φ(wv) = φ_w(v)*, es decir, *b_min(φ_w) = φ_w*: **b_min es la inclusión en O^{A\*}**, inyectiva. Y *r_min(w) = φ_w* es sobreyectiva por construcción.
> (2) Sea *(S′, δ′, o′, s₀′)* otra realización con *r′* sobre y *b′* inyectiva. Defínase **θ := b′ : S′ → O^{A\*}**. Para *s′ = r′(w)*: *θ(s′) = b′(r′(w)) = φ_w ∈ Min_φ*. Como *r′* es sobre, θ aterriza en Min_φ y es sobreyectiva sobre él; es inyectiva porque *b′* lo es. Homomorfismo: *θ(δ′(r′(w), a)) = θ(r′(wa)) = φ_{wa} = δ_min(φ_w, a) = δ_min(θ(r′(w)), a)*; y *o_min(θ(s′)) = φ_w(ε) = b′(s′)(ε) = o′(s′)*. Unicidad: si θ̂ conmuta con las observabilidades, *b_min ∘ θ̂ = b′*; como b_min es la inclusión, *θ̂ = b′ = θ*. ∎

La versión abstracta —sistemas de factorización (E, M), Arbib–Manes, coálgebra— es **[E]** y es el paraguas; aquí está demostrada la instancia donde todo lo demás se verifica. En el código, `minimize()` construye el cociente **con la buena definición como assert ejecutable**: el teorema corre.

La **equivalencia de Nerode** es *w ∼ w′ ⟺ φ_w = φ_{w′}*; su invariancia por la derecha (*w ∼ w′ ⟹ wa ∼ w′a*) es una línea: *φ_{wa}(v) = φ_w(av)*.

---

## §2. Las arquitecturas, ahora demostradas

### 2.1 Event Sourcing y snapshots

> **[T] Lema del snapshot.** *r(uv) = δ\*(r(u), v)*.
> *Demostración.* Inducción sobre *v*. Caso *ε*: trivial. Caso *v′a*: *r(uv′a) = δ(r(uv′), a) = δ(δ\*(r(u), v′), a) = δ\*(r(u), v′a)*. ∎

Event Sourcing es materializar *μF* y calcular el estado como el fold. Un snapshot es memoizar *r(u)* y continuar con el lema. **Lectura de gauge:** almacenar *r(u)* o recomputarlo desde el log son dos gauges del mismo invariante; el lema es la afirmación de que el invariante no depende del gauge. Verificado en 200 cortes aleatorios.

### 2.2 CQRS

> **[T] Teorema CQRS.** Sea *O = O₁ × O₂* (la observación total es el par de vistas), con equivalencias de Nerode ∼, ∼₁, ∼₂ respecto de *O*, *O₁*, *O₂*. Entonces:
>
> 1. **∼ = ∼₁ ∩ ∼₂** — la congruencia de escritura es el ínfimo de las congruencias de lectura.
> 2. Cada Minᵢ es un **cociente** de Min (proyecciones bien definidas y sobre).
> 3. Min **se embebe** en Min₁ × Min₂ vía *[w] ↦ ([w]₁, [w]₂)* — y en general la inclusión es **estricta**.
>
> *Demostración.* (1) *∀v: (o₁,o₂)(δ\*(s₀,wv)) = (o₁,o₂)(δ\*(s₀,w′v))* si y sólo si ambas coordenadas coinciden para todo *v*. (2) ∼ ⊆ ∼ᵢ hace las proyecciones bien definidas; sobreyectividad por alcanzabilidad. (3) Inyectividad es exactamente (1). ∎

CQRS deja de ser un patrón: **el modelo de escritura es el refinamiento común de las vistas, no su producto.** La estrictez importa. En la instancia verificada (*n_a* mod 4 y *n_a* mod 6): |Min| = 12, |Min₁×Min₂| = 24 — sólo la mitad de los pares de vistas son alcanzables, porque las vistas comparten el bit de paridad.

> **[T en la instancia, C en general] La redundancia es información mutua.** Con medida uniforme sobre Min:
>
> $$\log|{\textstyle\prod}_i \mathrm{Min}_i| - \log|\mathrm{Min}| \;=\; \sum_i H(V_i) - H(V) \;=\; \text{correlación total de las vistas}.$$
>
> En la instancia: log(24/12) = **1 bit** = *I(V₁;V₂)* = la paridad compartida, verificado numéricamente (2 + 2.585 − 3.585 = 1). El defecto de la inclusión —dato **algebraico**: el índice del embebimiento— coincide con una cantidad **entrópica**. Isomorfismo primero; la entropía aparece como su sombra. Éste es tu lema de cabecera, hecho literal en el ejemplo más pequeño posible.

### 2.3 CRDT: la cadena de cocientes

Hay una cadena canónica de cocientes del monoide libre:

$$A^* \;\twoheadrightarrow\; \mathcal{M}(A) \;\twoheadrightarrow\; \mathcal{P}_{\mathrm{fin}}(A)$$

(secuencias → multiconjuntos → conjuntos; el primer cociente impone conmutatividad, el segundo añade idempotencia).

> **[T] Teorema CRDT (modelo restringido).** Equivalen:
> (i) β factoriza por 𝒫_fin(A) — el comportamiento depende sólo del *conjunto* de eventos;
> (ii) existe implementación CRDT de estado: semirretículo *(L, ∨)*, *ℓ : A → L*, lectura *ρ*, con estado = ⋁ℓ(aᵢ) y merge = ∨.
>
> *Demostración.* (⇐) ∨ es asociativa, conmutativa e idempotente, luego el estado es invariante bajo permutación y duplicación del log, luego β factoriza por conjuntos. (⇒) Tómese *L = (𝒫_fin(A), ∪)*, *ℓ(a) = {a}*, *ρ = γ* donde β = γ∘set. Dos réplicas que han incorporado el mismo conjunto de eventos —en cualquier orden, con cualquier duplicación, mediante cualquier árbol de merges— tienen el mismo estado, porque la evaluación de un join de generadores no depende de la forma del árbol (leyes ACI). Eso **es** la consistencia eventual fuerte, y es la independencia del colímite respecto del diagrama de entregas. ∎

La tabla que cae de la cadena — **la semántica de entrega es el lugar de la congruencia**:

| La congruencia factoriza por | Tolera | Arquitectura |
|---|---|---|
| *A\** (nada) | nada | difusión con orden total (consenso) |
| *ℳ(A)* — conmutatividad | reorden | contadores, con entrega exactly-once |
| *𝒫(A)* — conmutatividad + idempotencia | reorden y duplicación | CRDT de estado |
| sólo idempotencia | duplicación | LWW con timestamps |

Verificado sobre tres máquinas: conjunto-visto (✓✓ → CRDT), contador (✓✗ → exactly-once), último-escribe (✗✓ → orden extra). La fila LWW enseña algo: **los timestamps compran conmutatividad extendiendo el alfabeto** — *A ↦ A×T* convierte «último» en «máximo por sello», que es un join. El truco estándar de etiquetar eventos con identificadores únicos es lo mismo **[E]**: un cambio de alfabeto que desplaza la congruencia hacia abajo en la cadena. Las técnicas de sistemas distribuidos son, una por una, morfismos de cambio de base.

**Merkle DAG** **[E]**: elección de representantes canónicos del cociente vía hash; el direccionamiento por contenido computa la clase estructuralmente; la colisión es el fallo (heurísticamente imposible) de inyectividad.

---

## §3. El no-go determinista

**Definición.** Para una máquina *M*, sea **μ(M) := |Im b|** — el número de estados *distinguibles*. Es invariante bajo isomorfismo; **no** bajo bisimulación (la basura inalcanzable lo sube). El invariante de gauge es su ínfimo sobre la clase:

> **[T] Teorema no-go (Myhill–Nerode como prohibición).** Toda máquina con comportamiento β cumple
>
> $$\mathrm{Im}\, b \;\supseteq\; \mathrm{Min}_\beta \quad(\text{como subconjuntos de } O^{A^*}), \qquad\text{luego}\qquad \mu(M) \;\geq\; |\mathrm{Min}_\beta|,$$
>
> con igualdad alcanzable (por la realización mínima). En bits: **toda realización de β necesita al menos log₂|Min_β| bits de memoria distinguible.**
>
> *Demostración.* *Im b ⊇ b(r(A\*)) = {φ_w} = Min_β*. ∎

Tres líneas. Verificado: sobre 40 realizaciones aleatorias del mismo comportamiento (copias de estados + basura), μ ∈ [12, 17], nunca por debajo de 12; el suelo se alcanza y sólo lo perfora nadie. ≈ 3.58 bits obligatorios para ese proceso, lo materialice quien lo materialice.

**La forma del resultado es la que pedía el programa:** una cota, no una descripción. Y nótese la dependencia: el invariante primario es **algebraico** —el objeto Min, único salvo iso único (Teorema 5′)—; la cantidad numérica (bits) es el logaritmo de su tamaño. La preferencia «isomorfismo antes que entropía» deja de ser metodológica: aquí es un **orden de dependencia demostrado**. Primero existe el objeto; después, su cardinal; después, su logaritmo.

**El T3 real, ahora enunciable con precisión [C]:**

> Para una clase de procesos 𝒫, error ε y coste *w*: ningún sistema con μ_w(S) < c alcanza riesgo de predicción < ε sobre 𝒫, donde *c = f(ε, E(𝒫))* y *E* es la entropía en exceso.

El caso determinista es ε = 0, μ = cardinal, *f* = umbral en |Min|: **demostrado**. El caso estocástico-aproximado es la tesis. El puente es reemplazar la igualdad de comportamientos por ε-bolas en *νG* (μ_ε := mínimo número de clases que ε-cubren las derivadas) y el cardinal por *C_μ*.

---

## §4. Refutación de la Conjetura 1

La conjetura de v2: *la confabulación es el fallo de la counidad Lan_i(i\*X) → X en ser isomorfismo; Lan genera la «continuación plausible no restringida por la verdad»*. Hice el cálculo. **El mecanismo es falso.**

**Montaje.** Tiempo *H = [n]* (poset lineal), ventana de contexto *P = {n−k, …, n} ⊆ H*, estado *X : H → Set* (diagrama con las dinámicas como flechas). Contexto := *i\*X*. Las extensiones de Kan a lo largo de la inclusión plenamente fiel *i : P ↪ H* existen puntualmente (Set es bicompleta).

> **[T] Proposición (cálculo de Lan y Ran sobre la ventana).**
>
> | región | Lan_i(i\*X)(t) | Ran_i(i\*X)(t) |
> |---|---|---|
> | *t < min P* (pasado no visto) | **∅** | *X(min P)* (constante hacia atrás) |
> | *t ∈ P* (ventana) | *X(t)* | *X(t)* |
> | *t > max P* (futuro) | *X(max P)* (constante hacia delante) | **1** |
>
> *Demostración.* Puntualmente, *Lan_i Y(t) = colim{Y(p) : p ∈ P, p ≤ t}* sobre la categoría coma, y *Ran_i Y(t) = lim{Y(p) : p ≥ t}*. Si la coma tiene objeto terminal (resp. inicial), el colímite (resp. límite) es el valor en él: para *t ≥ min P* el poset *{p ≤ t}* tiene máximo; para *t ≤ max P* el poset *{p ≥ t}* tiene mínimo; en la ventana ese extremo es el propio *t* (plenitud de *i*). Los casos restantes son el colímite vacío (= inicial = ∅) y el límite vacío (= terminal = 1). ∎
>
> El cálculo no usa que *P* sea contiguo: para *P* disperso (retrieval, RAG) Lan arrastra «el último fragmento recuperado antes de *t*». La conclusión no cambia.

**Lectura.** En Set, el adjunto izquierdo —la completación *más libre* compatible con el fragmento— **no confabula jamás**: sobre el pasado no visto responde ∅ («imposible, me niego»), y sobre el futuro repite la última cosa vista. Libertad universal produce *rechazo o repetición*, nunca fabricación fluida. La identificación v2 de la alucinación con el defecto de la counidad 1-categórica está muerta: el defecto existe (∅ ≠ X(t)), pero su modo de fallo es el silencio, no la invención.

**Corrección [C] — Conjetura 1′.** La confabulación requiere **dos** ingredientes, no uno: contexto insuficiente **y un prior generativo**. El hábitat correcto es la extensión de Kan en la categoría de Kleisli de una mónada de distribuciones *D* (o en profunctores pesados): allí la extensión a lo largo de *i* no puede responder ∅ —debe emitir una distribución— y la «completación libre» es *el prior condicionado a la ventana*. Confabular = masa del prior fuera de la completación verdadera; el defecto de la counidad se convierte en una divergencia, y la tasa de alucinación quedaría acotada por ella.

**Huella falsable de C1′:** un sistema *sin* prior (nivel Set: recuperación estricta, sin generación) debe rehusar en lugar de confabular. Es exactamente lo que hacen los sistemas de sólo-retrieval. La conjetura corregida ya toca suelo empírico.

Esto es lo que debía pasar: la prueba de fuego, apuntada hacia dentro, mató el mecanismo y dejó uno más afilado. El coste de publicar la v2 sin este cálculo habría sido exactamente el que anticipamos.

---

## §5. El precio de la teleología

En v2, A6 (selección) quedó como axioma independiente y el Problema abierto 1 decía: *la optimalidad no compone*. Precisión nueva:

> **[E] La teleología sí compone — por el producto de selección.** Las funciones de selección *J X = (X → Q) → X* forman una mónada fuerte, y su **producto monoidal** computa exactamente la inducción hacia atrás: equilibrios perfectos en subjuegos de juegos secuenciales (Escardó–Oliva). Sobre esto están construidos los juegos abiertos. Luego los agentes componen teleológicamente; el operador existe y es canónico.

> **[T en 𝕄] Coste del producto.** Sobre un horizonte de profundidad *d* con ramificación *b*, la evaluación exhaustiva del producto de selección visita las *b^d* hojas del árbol.

> **[E] El coste es esencial.** Resolver juegos generales es PSPACE-completo (QBF, Generalized Geography). No hay atajo polinómico general salvo colapso de clases.

De modo que en la misma categoría conviven **dos regímenes de composición**:

$$\underbrace{w(g \circ f) \;\leq\; w(g) \otimes w(f)}_{\text{dinámica: subaditiva}} \qquad\qquad \underbrace{\mathrm{cost}(\pi_1 \circledast \cdots \circledast \pi_d) \;\sim\; b^{\,d}}_{\text{teleología: exponencial}}$$

**La dinámica compone barata; la teleología compone cara, y la dureza es de complejidad, no de implementación.** El Problema abierto 1 queda reformulado: lo que no existe no es la composición de óptimos — es la composición *barata* de óptimos.

**Definición (racionalidad acotada).** El producto de selección truncado a profundidad *k* (lookahead-*k*, con heurística en la frontera). Los agentes reales no son instancias del producto: son sus truncamientos. **[C]** Cuantificar la pérdida de optimalidad como función de *(k, b, w)* — la conjetura conectaría racionalidad acotada con la geometría del árbol de juego, y daría al marco su segunda cota.

---

## §6. Estado del programa

| Ítem | v2 | v3 | Siguiente acción |
|---|---|---|---|
| T1 — arquitecturas como corolario | programa | **hecho [T] + verificado** | — |
| T3 — no-go | programa | **determinista hecho [T]**; estocástico enunciado | μ_ε y el puente a C_μ |
| C1 — alucinación | [C] | **refutada**; C1′ [C] | calcular Lan en Kl(D) sobre un mundo juguete: primera cota *cuantitativa* de confabulación |
| C2 — cripticidad como defecto de factorización | [C] | [C], sin cambio | categorías de Markov con pesos (la tesis) |
| OP1 — composición de óptimos | abierto | **parcial**: producto de selección + coste esencial | cota de truncamiento |
| Redundancia CQRS = información mutua | — | [T instancia / C general] | demostrar en general con medida uniforme |

**Recomendación para la iteración 4:** el juguete de C1′. Es barato (un mundo de tres estados, la mónada de distribuciones, la extensión calculada a mano), es decisivo (o produce la primera cota cuantitativa de alucinación del marco, o mata también a C1′ — ambos resultados valen), y es el único ítem de la tabla que toca datos empíricos de inmediato. T2/C2 sigue siendo el objetivo de calibre tesis; no conviene gastarlo sin el músculo del caso juguete.

---

## §7. Verificación ejecutable

`modelo_concreto.py` (adjunto). Salida real:

```text
== Modelo concreto 𝕄 — verificación ejecutable (iteración 3) ==

[1] Realización mínima: |Min| = 12; forma canónica invariante bajo 25 gauges aleatorios. PASS
[2] Snapshot = memoización del fold: r(uv) = δ*(r(u),v) en 200 cortes aleatorios. PASS
[3] CQRS: |Min| = 12; vistas de tamaño 4 y 6; Min ↪ Min1×Min2 estricta: 12 de 24 pares
    (redundancia = log2(24/12) = 1 bit = información mutua entre vistas). PASS
[4]  conjunto-visto: conmutativa=True  idempotente=True  → CRDT de estado (join)
[4]        contador: conmutativa=True  idempotente=False → necesita exactly-once
[4]  último-escribe: conmutativa=False idempotente=True  → necesita orden extra (timestamps)
[4] Clasificación CRDT por cociente. PASS
[5] No-go: μ ∈ [12, 17] sobre 40 realizaciones; cota |Min| = 12 alcanzada
    (≈ 3.58 bits obligatorios). PASS

Todo verificado: 5/5.
```

Qué es y qué no es esto: los tests ejecutan instancias finitas de teoremas demostrados a mano en §§1–3 — protegen contra errores de enunciado y de cálculo, no sustituyen demostraciones. La excepción parcial es [4], donde la conmutatividad/idempotencia se comprueba sobre palabras acotadas; para las tres máquinas del test la propiedad universal es demostrable a mano en una línea cada una.

Dos detalles del código que son teoría y no ingeniería: los `assert` de `minimize()` **son** la cláusula de buena definición del Teorema 5′ (si el cociente no descendiera, el teorema fallaría en tiempo de ejecución), y `canonical()` es un invariante completo de gauge computable — la versión ejecutable de «único salvo isomorfismo único».

---

## §8. Bibliografía añadida sobre la de v2

- **Escardó–Oliva**, *Selection functions, bar recursion and backward induction* (2010) — §5.
- **Shapiro–Preguiça–Baquero–Zawirski**, *Conflict-free Replicated Data Types* (2011) — §2.3; el teorema de SEC allí es la forma sistemas del colímite ACI.
- **Hopcroft; Moore** — minimización por refinamiento de particiones (el algoritmo de `classes()` lleva, apropiadamente, el nombre de Moore).

---

*Iteración 3. Un teorema de realización con demostración completa, cuatro arquitecturas demostradas, un no-go, una conjetura muerta, una conjetura nueva con huella falsable, y 5/5 en la máquina.*
