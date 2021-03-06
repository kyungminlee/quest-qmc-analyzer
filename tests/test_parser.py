from __future__ import division
from unittest import TestCase
import os

import common.parser


__author__ = 'Vladimir Iglovikov'


class TestParser(TestCase):
  def setUp(self):
    self.time_indep_text = open(os.path.join(os.getcwd(), 'data', 'Lieb_1385474159.53.out')).read()
    dimension = 2
    self.tparser = common.parser.Parser(self.time_indep_text, dimension=dimension)

    self.time_indep_text = open(os.path.join(os.getcwd(), 'data', 'Lieb_1387496388.34.out')).read()
    self.tparser1 = common.parser.Parser(self.time_indep_text, dimension=dimension)

    self.time_indep_text = open(os.path.join(os.getcwd(), 'data', 'kagome_anisotropic_1397688531.07.out')).read()
    self.kagome = common.parser.Parser(self.time_indep_text, dimension=dimension)

    self.time_indep_text = open(os.path.join(os.getcwd(), 'data', 'test.out')).read()
    self.square = common.parser.Parser(self.time_indep_text, dimension=dimension)

    self.time_indep_text = open(os.path.join(os.getcwd(), 'data', 'honeycomb_1408666691.0.out')).read()
    self.honeycomb = common.parser.Parser(self.time_indep_text, dimension=dimension)

    self.time_indep_text = open(os.path.join(os.getcwd(), 'data', 'chain_1409178597.79.out')).read()
    dimension = 1
    self.chain = common.parser.Parser(self.time_indep_text, dimension=dimension)

  def test_k_points(self):
    print self.square.get_k_points()

  def test_get_t_up(self):
    self.assertAlmostEqual(1, self.tparser.get_t_up()[0])
    self.assertAlmostEqual(1, self.kagome.get_t_up()[0])

  def test_get_t_down(self):
    self.assertAlmostEqual(1, self.tparser.get_t_down()[0])
    self.assertAlmostEqual(1, self.kagome.get_t_down()[0])

  def test_get_U(self):
    self.assertAlmostEqual(0, self.tparser.get_u())
    self.assertAlmostEqual(-4, self.kagome.get_u())

  def test_get_mu_up(self):
    self.assertAlmostEqual(2, self.tparser.get_mu_up())
    self.assertAlmostEqual(0.5, self.kagome.get_mu_up())

  def test_get_mu_down(self):
    self.assertAlmostEqual(2, self.tparser.get_mu_down())
    self.assertAlmostEqual(0.5, self.kagome.get_mu_down())

  def test_get_nSites(self):
    self.assertAlmostEqual(48, self.tparser.get_nSites())

  def test_get_DO(self):
    self.assertAlmostEqual(self.tparser.get_n_up()[0] * self.tparser.get_n_down()[0], self.tparser.get_DO()[0])
    self.assertAlmostEqual(-0.39971693E+01 / self.tparser1.get_u(), self.tparser1.get_DO()[0])

  def test_get_L(self):
    self.assertEqual(4, self.tparser.get_L())

  # def test_pairing(self):
  # print self.tparser.get_pairing()

  # def test_pairing_vs_x(self):
  #   print self.tparser.get_pairing_vs_x()

  def test_num_orbits(self):
    self.assertEquals(3, self.tparser.get_num_orbits())

  def test_orbits(self):
    self.assertListEqual([0, 1, 2], self.tparser.get_orbits())

  def test_global_sites(self):
    self.assertEquals(0, self.tparser.get_global_sites())
    self.assertEquals(0, self.tparser1.get_global_sites())


  def test_get_struct_XX_F(self):
    self.assertAlmostEqual(0.97803575e-1, self.tparser.get_struct_XX_F()[0])

  # def test_get_struct_XX_AF(self):
  #   self.fail()
  #



  def test_get_density_correlation_up_up(self):
    self.assertAlmostEqual(0.75788681, self.tparser.get_density_correlation_up_up()[(0, 0, 0, 0, 0)][0])


  def test_get_rho_n1_n0_U0(self):
    self.assertAlmostEqual(self.tparser.get_rho()[0],
                           (self.tparser.get_n0()[0] + 2 * self.tparser.get_n1()[0]) / self.tparser.get_num_orbits(), 6)

  def test_n0(self):
    self.assertAlmostEqual(
      2 - self.tparser.get_green_up()[(0, 0, 0, 0, 0)][0] - self.tparser.get_green_down()[(0, 0, 0, 0, 0)][0],
      self.tparser.get_n0()[0])


  def test_kx_ky_product(self):
    self.assertEqual(self.square.get_nSites(), (len(self.square.get_kx_points()) * len(self.square.get_ky_points())))

  def test_nx(self):
    self.assertEquals(12, self.tparser1.get_nx())
    self.assertEquals(4, self.tparser.get_nx())
    self.assertEquals(2, self.square.get_nx())
    self.assertEquals(4, self.kagome.get_nx())
    self.assertEquals(8, self.chain.get_nx())
    # TODO nx_ny from non rectangular geometry is not supported
    self.assertEquals(10, self.honeycomb.get_nx())

  def test_ny(self):
    self.assertEquals(12, self.tparser1.get_ny())
    self.assertEquals(4, self.tparser.get_ny())
    self.assertEquals(48, self.square.get_ny())
    print self.square.get_nx()
    print self.square.get_ny()
    print self.square.get_u()
    print self.square.get_beta()
    self.assertEquals(4, self.kagome.get_ny())
    # TODO nx_ny from non rectangular geometry is not supported
    self.assertEquals(10, self.honeycomb.get_ny())
