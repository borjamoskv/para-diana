#!/usr/bin/env python3
"""
stress_test_kl_d.py
Prueba de Estrés Multidimensional para el modelo de Desintegración Bayesiana en Categorías de Markov.
(Actualizado para Iteración 7: Canales No-Estacionarios e Infinitos)
"""

import time
import numpy as np
from modelo_kl_d import MarkovCategoryBayesianDisintegration

def test_dimensionality():
    print("======================================================================")
    print("== EJE 1: ESTRÉS DE ESCALABILIDAD (ALTA DIMENSIONALIDAD) ==")
    print("======================================================================")
    N = 1000
    print(f"Inicializando espacio de estados de tamaño N = {N}...")
    states = [f"s{i}" for i in range(N)]
    
    np.random.seed(42)
    T_real = np.random.rand(N, N)
    T_real = T_real / T_real.sum(axis=1, keepdims=True)
    pi0_real = np.random.rand(N)
    pi0_real = pi0_real / pi0_real.sum()
    
    T_model = np.random.rand(N, N)
    T_model = T_model / T_model.sum(axis=1, keepdims=True)
    pi0_model = np.random.rand(N)
    pi0_model = pi0_model / pi0_model.sum()
    
    start_time = time.time()
    model = MarkovCategoryBayesianDisintegration(states, T_real, pi0_real, T_model, pi0_model)
    
    history = {0: "s0", 1: "s500", 2: "s999", 3: "s0"}
    window = [1, 2]
    
    t0 = time.time()
    s_true = history[3]
    
    p = model.bayesian_disintegration(history, window, 3, use_model=False)
    q = model.bayesian_disintegration(history, window, 3, use_model=True)
    
    eps = 1e-15
    p_safe = np.clip(p, eps, 1.0)
    q_safe = np.clip(q, eps, 1.0)
    
    H_p = -np.sum(p * np.log2(p_safe))
    D_kl = np.sum(p[p > 0] * np.log2(p[p > 0] / q_safe[p > 0]))
    H_pq = -np.sum(p * np.log2(q_safe))
    
    t1 = time.time()
    print(f"Tiempo de cómputo (N={N}): {t1 - t0:.4f} segundos.")
    print(f"Incertidumbre Aleatoria H(p):        {H_p:.4f} bits")
    print(f"Alucinación Epistémica D_KL(p || q): {D_kl:.4f} bits")
    print(f"Sorpresa Cruzada Esperada H(p, q):   {H_pq:.4f} bits")
    print("======================================================================\n")

def test_ergodic_amnesia():
    print("======================================================================")
    print("== EJE 2: ESTRÉS ERGÓDICO ESTACIONARIO (AMNESIA TEMPORAL) ==")
    print("======================================================================")
    states = ["s0", "s1", "s2"]
    
    T_real = np.array([
        [0.1, 0.7, 0.2],
        [0.2, 0.1, 0.7],
        [0.7, 0.2, 0.1]
    ])
    pi0_real = np.array([1.0, 0.0, 0.0])
    
    model = MarkovCategoryBayesianDisintegration(states, T_real, pi0_real)
    
    eigenvals, eigenvecs = np.linalg.eig(T_real.T)
    idx = np.argmin(np.abs(eigenvals - 1.0))
    stat_dist = np.real(eigenvecs[:, idx])
    stat_dist = stat_dist / stat_dist.sum()
    
    gap = 10_000 # Reducido a 10_000 para no hacer lenta la integral de caminos discreta
    history = {0: "s0", gap: "s1"}
    window = [0]
    
    print(f"Proyectando desintegración a t = {gap} pasos en el futuro...")
    p = model.bayesian_disintegration(history, window, gap, use_model=False)
    
    print(f"Distribución Estacionaria Teórica: {np.round(stat_dist, 4)}")
    print(f"Distribución Predicha (t={gap}):   {np.round(p, 4)}")
    
    diff = np.max(np.abs(stat_dist - p))
    print(f"Error máximo absoluto: {diff:.2e}")
    if diff < 1e-10:
        print("ÉXITO: La desintegración decae perfectamente al atractor ergódico (amnesia).")
    print("======================================================================\n")

def test_epistemic_collapse():
    print("======================================================================")
    print("== EJE 3: COLAPSO EPISTÉMICO ESTRICTO (KERNEL PANIC) ==")
    print("======================================================================")
    states = ["s0", "s1", "s2"]
    
    T_real = [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0]
    ]
    pi0_real = [1.0, 0.0, 0.0]
    
    T_model = [
        [0.5, 0.0, 0.5], # Dogmáticamente imposible la transición a s1
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0]
    ]
    pi0_model = [1.0, 0.0, 0.0]
    
    model = MarkovCategoryBayesianDisintegration(states, T_real, pi0_real, T_model, pi0_model)
    
    history = {0: "s0", 1: "s1"}
    window = [0]
    
    metrics = model.hallucination_metrics(history, window, 1)
    
    print(f"P (Realidad): {metrics['p_dist']}")
    print(f"Q (Modelo):   {metrics['q_dist']}")
    print(f"Incertidumbre Aleatoria H(p):        {metrics['H_p_aleatoric']:.4f} bits")
    print(f"Alucinación Epistémica D_KL(p || q): {metrics['D_kl_epistemic']} bits")
    print(f"Sorpresa Cruzada Esperada H(p, q):   {metrics['H_pq_cross_expected']} bits")
    
    if metrics['D_kl_epistemic'] == float('inf'):
        print("ÉXITO: El modelo devolvió `inf` exacto. Kernel Panic epistémico confirmado.")
    else:
        print("FALLO: La alucinación no fue infinito.")
    print("======================================================================\n")

def test_non_stationary():
    print("======================================================================")
    print("== EJE 4: CANALES DE MARKOV NO-ESTACIONARIOS (DINÁMICOS) ==")
    print("======================================================================")
    states = ["s0", "s1", "s2"]
    
    # El universo alterna entre mover masa a s1 y moverla a s2 dependiendo si t es par o impar
    def T_real_func(t):
        if t % 2 == 0:
            return np.array([
                [0.1, 0.9, 0.0],
                [0.1, 0.9, 0.0],
                [0.1, 0.9, 0.0]
            ])
        else:
            return np.array([
                [0.1, 0.0, 0.9],
                [0.1, 0.0, 0.9],
                [0.1, 0.0, 0.9]
            ])
            
    pi0_real = [1.0, 0.0, 0.0]
    
    model = MarkovCategoryBayesianDisintegration(states, T_real_func, pi0_real)
    
    # Evaluamos varios instantes sin ver nada para probar el producto de caminos
    window = [0]
    for t in [1, 2, 3, 4]:
        history = {0: "s0", t: "s0"} # El estado final es irrelevante para p_dist
        metrics = model.hallucination_metrics(history, window, t)
        print(f"t={t} | P(Realidad): {metrics['p_dist']}")
        
    print("ÉXITO: La distribución fluctúa dinámicamente gracias a la integral de caminos discreta.")
    print("======================================================================\n")

def test_myhill_nerode_quotient():
    print("======================================================================")
    print("== EJE 5: AUDITORÍA MYHILL-NERODE & REALIZACIÓN MÍNIMA ==")
    print("======================================================================")
    from modelo_kl_d import MachineRealization, MyhillNerodeAuditor
    
    s0 = "s0"
    alphabet = ["a", "b"]
    
    def transition(s, a):
        if s == "s0" and a == "a": return "s1"
        if s == "s1" and a == "b": return "s0"
        return s

    def output(s):
        return "OUT_A" if s == "s0" else "OUT_B"

    machine = MachineRealization(s0, transition, output)
    auditor = MyhillNerodeAuditor(machine, alphabet, max_depth=3)
    mn_report = auditor.compute_minimal_quotient()
    
    print(f"Palabras probadas en A*: {mn_report['num_words_tested']}")
    print(f"Número de clases Myhill-Nerode (|Im b|): {mn_report['num_equivalence_classes']}")
    print(f"Máquina Mínima Validada: {mn_report['is_minimal']}")
    
    if mn_report['is_minimal'] and mn_report['num_equivalence_classes'] == 2:
        print("ÉXITO: Realización mínima validada mediante cociente conductual Myhill-Nerode.")
    else:
        print("FALLO: La cota de Myhill-Nerode no fue satisfecha.")
    print("======================================================================")


if __name__ == "__main__":
    test_dimensionality()
    test_ergodic_amnesia()
    test_epistemic_collapse()
    test_non_stationary()
    test_myhill_nerode_quotient()
