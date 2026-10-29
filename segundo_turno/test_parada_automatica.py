"""Teste da parada automatica do monitor de chegada (sem rede, sem criar pastas)."""
import importlib.util
import os
import unittest
from unittest import mock


def carregar():
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monitor_chegada.py")
    spec = importlib.util.spec_from_file_location("monitor_chegada_teste", caminho)
    mod = importlib.util.module_from_spec(spec)
    with mock.patch("os.makedirs"):
        spec.loader.exec_module(mod)
    return mod


M = carregar()
K = ("25/10/2026", "23:22:22")


class Parada(unittest.TestCase):
    def test_sem_resultado_nao_para(self):
        self.assertFalse(M.deve_parar(None, {}, 1000.0))

    def test_abaixo_de_100_nunca_para_e_zera_a_contagem(self):
        e = {"chave": K, "desde": 1}
        self.assertFalse(M.deve_parar((99.98, K), e, 99999.0))
        self.assertEqual(e, {})

    def test_cem_por_cento_so_para_depois_de_30_min_estavel(self):
        e = {}
        self.assertFalse(M.deve_parar((100.0, K), e, 1000.0))
        self.assertFalse(M.deve_parar((100.0, K), e, 1000.0 + 1799))
        self.assertTrue(M.deve_parar((100.0, K), e, 1000.0 + 1800))

    def test_carimbo_novo_recomeca_a_contar(self):
        e = {}
        M.deve_parar((100.0, K), e, 1000.0)
        self.assertFalse(M.deve_parar((100.0, ("25/10/2026", "23:40:00")), e, 1000.0 + 2000))
        self.assertTrue(M.deve_parar((100.0, ("25/10/2026", "23:40:00")), e, 1000.0 + 2000 + 1800))


if __name__ == "__main__":
    unittest.main()
