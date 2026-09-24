#!/usr/bin/env python3
"""
modelo_concreto.py — iteración 3
Modelo concreto 𝕄 de la teoría de transformaciones: máquinas de Moore en Set.

    μF  = A*        (historia libre / event log)      — álgebra inicial de F(X) = 1 + X×A
    νG  = O^(A*)    (espacio de comportamientos)      — coálgebra final de G(X) = O × X^A
    r   = fold      (reproducción del log)
    b   = unfold    (mapa de observabilidad)
    β   = b ∘ r     (comportamiento)

Verificación ejecutable de: Teorema 5' (realización mínima, unicidad salvo iso),
invariancia de gauge, lema de snapshot, teorema CQRS, clasificación CRDT por
cocientes, y el no-go determinista (Myhill–Nerode como prohibición).

Los tests verifican instancias finitas de teoremas demostrados a mano en el
documento; protegen contra errores de enunciado, no sustituyen demostraciones.
"""
import random
from math import gcd, log2


class Moore:
    def __init__(self, states, alphabet, delta, out, s0):
        self.S = list(states)
        self.A = list(alphabet)
        self.d = dict(delta)
        self.o = dict(out)
        self.s0 = s0

    # r = catamorfismo. Event Sourcing es, literalmente, materializar el argumento w.
    def run(self, w, s=None):
        s = self.s0 if s is None else s
        for a in w:
            s = self.d[(s, a)]
        return s

    def reachable(self):
        seen, front = {self.s0}, [self.s0]
        while front:
            s = front.pop()
            for a in self.A:
                t = self.d[(s, a)]
                if t not in seen:
                    seen.add(t)
                    front.append(t)
        return seen

    def classes(self, out=None, dom=None):
        """Refinamiento de particiones: la equivalencia conductual (Nerode).
        `dom` debe ser cerrado bajo δ (todo S, o el conjunto alcanzable)."""
        out = self.o if out is None else out
        dom = list(self.S) if dom is None else list(dom)
        cls = {s: repr(out[s]) for s in dom}
        while True:
            sig = {s: (cls[s], tuple(cls[self.d[(s, a)]]
                                     for a in sorted(self.A, key=repr)))
                   for s in dom}
            ids = {v: str(i) for i, v in enumerate(sorted(set(sig.values())))}
            new = {s: ids[sig[s]] for s in dom}
            if len(set(new.values())) == len(set(cls.values())):
                return new
            cls = new

    def minimize(self, out=None):
        """Teorema 5': el cociente por ~ está bien definido (los asserts SON la
        cláusula de buena definición), es alcanzable y observable, y es único
        salvo isomorfismo único."""
        out = self.o if out is None else out
        R = self.reachable()
        cls = self.classes(out=out, dom=R)
        delta, outq = {}, {}
        for s in R:
            for a in self.A:
                k, v = (cls[s], a), cls[self.d[(s, a)]]
                assert delta.get(k, v) == v, "cociente mal definido: δ no desciende"
                delta[k] = v
            if cls[s] in outq:
                assert outq[cls[s]] == out[s], "cociente mal definido: o no desciende"
            outq[cls[s]] = out[s]
        return Moore(sorted(set(cls.values())), self.A, delta, outq, cls[self.s0])

    def canonical(self):
        """Forma canónica BFS de la minimización: invariante completo de gauge."""
        M = self.minimize()
        A2 = sorted(M.A, key=repr)
        order, queue = {M.s0: 0}, [M.s0]
        while queue:
            s = queue.pop(0)
            for a in A2:
                t = M.d[(s, a)]
                if t not in order:
                    order[t] = len(order)
                    queue.append(t)
        delta = tuple(sorted(((order[s], a), order[M.d[(s, a)]])
                             for s in order for a in A2))
        outs = tuple(sorted((order[s], repr(M.o[s])) for s in order))
        return (len(order), tuple(A2), delta, outs)


def equivalent(M1, M2):
    """Igualdad exacta de comportamiento β, vía BFS del producto."""
    front, seen = [(M1.s0, M2.s0)], set()
    while front:
        p = front.pop()
        if p in seen:
            continue
        seen.add(p)
        s, t = p
        if M1.o[s] != M2.o[t]:
            return False
        for a in M1.A:
            front.append((M1.d[(s, a)], M2.d[(t, a)]))
    return True


def mu(M):
    """μ(M) = |Im b|: nº de estados distinguibles. Invariante bajo isomorfismo,
    NO bajo bisimulación; su ínfimo sobre la clase de gauge es |Min|."""
    return len(set(M.classes().values()))


def scramble(Min, rng, split=3, junk=0):
    """Una realización arbitraria del mismo β: copias de estados (gauge puro)
    + estados basura inalcanzables (suben μ, nunca lo bajan)."""
    copies = {c: rng.randint(1, split) for c in Min.S}
    states = [(c, i) for c in Min.S for i in range(copies[c])]
    delta, out = {}, {}
    for (c, i) in states:
        for a in Min.A:
            c2 = Min.d[(c, a)]
            delta[((c, i), a)] = (c2, rng.randrange(copies[c2]))
        out[(c, i)] = Min.o[c]
    for j in range(junk):
        js = ('junk', j)
        states.append(js)
        for a in Min.A:
            delta[(js, a)] = rng.choice(states)
        out[js] = ('junk-out', j) if rng.random() < 0.5 else Min.o[rng.choice(Min.S)]
    return Moore(states, Min.A, delta, out, (Min.s0, 0))


# ---------- máquinas de prueba ----------

def machine_mod(p, q):
    """Contador de letras 'a' con dos vistas: n_a mod p y n_a mod q. 'b' es no-op."""
    m = p * q // gcd(p, q)
    S = list(range(m))
    delta = {**{(s, 'a'): (s + 1) % m for s in S},
             **{(s, 'b'): s for s in S}}
    out = {s: (s % p, s % q) for s in S}
    return Moore(S, ['a', 'b'], delta, out, 0)


def m_setseen():
    S = [frozenset(x) for x in ([], ['x'], ['y'], ['x', 'y'])]
    delta = {(s, a): s | {a} for s in S for a in 'xy'}
    return Moore(S, ['x', 'y'], delta, {s: s for s in S}, frozenset())


def m_counter(cap=2):
    S = [(i, j) for i in range(cap + 1) for j in range(cap + 1)]
    delta = {((i, j), 'x'): (min(i + 1, cap), j) for (i, j) in S}
    delta.update({((i, j), 'y'): (i, min(j + 1, cap)) for (i, j) in S})
    return Moore(S, ['x', 'y'], delta, {s: s for s in S}, (0, 0))


def m_last():
    S = [None, 'x', 'y']
    delta = {(s, a): a for s in S for a in 'xy'}
    return Moore(S, ['x', 'y'], delta, {s: s for s in S}, None)


def words(A, n):
    ws, layer = [''], ['']
    for _ in range(n):
        layer = [w + a for w in layer for a in A]
        ws += layer
    return ws


def commutative(M, n=5):
    """β invariante bajo permutación ⟺ toda palabra equivale a su ordenada."""
    cls = M.classes()
    return all(cls[M.run(w)] == cls[M.run(''.join(sorted(w)))]
               for w in words(M.A, n))


def duplication_insensitive(M, n=4):
    """β invariante bajo duplicación adyacente (entrega at-least-once)."""
    cls = M.classes()
    for w in words(M.A, n):
        for i in range(len(w)):
            if cls[M.run(w)] != cls[M.run(w[:i + 1] + w[i] + w[i + 1:])]:
                return False
    return True


# ---------- verificación ----------

def main():
    rng = random.Random(0)
    print("== Modelo concreto 𝕄 — verificación ejecutable (iteración 3) ==\n")

    # [1] Realización mínima + invariancia de gauge
    M = machine_mod(4, 6)
    Min = M.minimize()
    assert len(Min.S) == 12, "lcm(4,6)=12"
    assert mu(Min) == len(Min.S), "Min es observable: b es mono"
    can = Min.canonical()
    for _ in range(25):
        Sc = scramble(Min, rng, split=3, junk=rng.randint(0, 4))
        assert equivalent(Sc, Min), "el gauge rompió el comportamiento"
        assert Sc.canonical() == can, "la forma canónica no es invariante de gauge"
    print(f"[1] Realización mínima: |Min| = {len(Min.S)}; forma canónica "
          f"invariante bajo 25 gauges aleatorios. PASS")

    # [2] Lema de snapshot: r(uv) = δ*(r(u), v)
    for _ in range(200):
        w = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 20)))
        k = rng.randint(0, len(w))
        assert M.run(w) == M.run(w[k:], s=M.run(w[:k]))
    print("[2] Snapshot = memoización del fold: r(uv) = δ*(r(u),v) "
          "en 200 cortes aleatorios. PASS")

    # [3] CQRS: ~_O = ~_1 ∩ ~_2 ; vistas = cocientes de Min ; Min ↪ Min1 × Min2
    R = M.reachable()
    o1 = {s: M.o[s][0] for s in M.S}
    o2 = {s: M.o[s][1] for s in M.S}
    c = M.classes(dom=R)
    c1 = M.classes(out=o1, dom=R)
    c2 = M.classes(out=o2, dom=R)
    n, n1, n2 = (len(set(x.values())) for x in (c, c1, c2))
    for s in R:
        for t in R:
            assert ((c1[s], c2[s]) == (c1[t], c2[t])) == (c[s] == c[t]), \
                "~_O ≠ ~_1 ∩ ~_2"
    image = {(c1[s], c2[s]) for s in R}
    print(f"[3] CQRS: |Min| = {n}; vistas de tamaño {n1} y {n2}; "
          f"Min ↪ Min1×Min2 estricta: {len(image)} de {n1 * n2} pares "
          f"(redundancia = log2({n1 * n2}/{n}) = {log2(n1 * n2 / n):.0f} bit "
          f"= información mutua entre vistas). PASS")

    # [4] CRDT: dónde cae la congruencia en la cadena A* ↠ ℳ(A) ↠ 𝒫(A)
    expected = [(True, True), (True, False), (False, True)]
    rows = []
    for name, mm in [("conjunto-visto", m_setseen()),
                     ("contador", m_counter()),
                     ("último-escribe", m_last())]:
        comm, idem = commutative(mm), duplication_insensitive(mm)
        verdict = ("CRDT de estado (join)" if comm and idem
                   else "necesita exactly-once" if comm
                   else "necesita orden extra (timestamps)" if idem
                   else "necesita orden total")
        rows.append((name, comm, idem, verdict))
        print(f"[4] {name:>15}: conmutativa={str(comm):5} "
              f"idempotente={str(idem):5} → {verdict}")
    assert [(r[1], r[2]) for r in rows] == expected
    print("[4] Clasificación CRDT por cociente. PASS")

    # [5] No-go determinista: μ(realización) ≥ |Min| para TODA realización de β
    lo = []
    for _ in range(40):
        Sc = scramble(Min, rng, split=4, junk=rng.randint(0, 5))
        assert equivalent(Sc, Min)
        m_ = mu(Sc)
        assert m_ >= len(Min.S), "¡no-go violado!"
        lo.append(m_)
    print(f"[5] No-go: μ ∈ [{min(lo)}, {max(lo)}] sobre 40 realizaciones; "
          f"cota |Min| = {len(Min.S)} alcanzada "
          f"(≈ {log2(len(Min.S)):.2f} bits obligatorios). PASS")

    print("\nTodo verificado: 5/5.")


if __name__ == "__main__":
    main()
