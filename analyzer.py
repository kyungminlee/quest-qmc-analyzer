#!/usr/bin/env python
from __future__ import division

__author__ = 'vladimir'

'''
This script will be used to analyze the data generated by the QUEST simulation

x_variables:
  u - fixed mu, beta
  mu - fixed u, beta
  beta - fixed u, mu
  T - fixed u, mu
  x - fixed u, mu, beta
  1L - plot versus 1 / L. fixed u, mu, beta
  rho - plot versus rho. fixed u, beta

y_variables:
  Energy
  m2 - square of the magnetisation
  01 - density-density correlation between 0 and 1 orbital within unit cell
  11 - density-density correlation between 0 and 1 orbital within unit cell
  m0_squared - square of the magnetisation on the 0 orbital
  m1_squares - square of the magnetisation on the 1 orbital
  C - specific heat
'''
import common.get_file_list
import common.fequals
import common.divide_into_classes
import common.merge
import common.choices
import argparse
from pylab import *
import os

execfile(os.path.join(os.getcwd(), "common", "plot_properties.py"))

parser = argparse.ArgumentParser()
parser.add_argument('-t', type=float, default=1, help="hopping strength t")
parser.add_argument('-rho', type=float, help="Electron density")
parser.add_argument('-u', type=float, help="u term")
parser.add_argument('-beta', type=float, help="inverse temperature")

parser.add_argument('-m', type=str, help="Name of the model")
parser.add_argument('-y_variable', type=str, help="variable along y axis")
parser.add_argument('-x_variable', type=str, help="variable along x axis")
parser.add_argument('-x_min', type=float, help='minimum x value')
parser.add_argument('-x_max', type=float, help='maximum x value')
parser.add_argument('-y_min', type=float, help='minimum y value')
parser.add_argument('-y_max', type=float, help='maximum y value')
parser.add_argument('-to_screen', default=False, type=bool, help='Should we print results on the screen or not.')

parser.add_argument('-T', action="store_true",
                    help="if we need graph versus temperature. By default it is versus inverse temperature.")
parser.add_argument('-legend', type=str, help='legend position. Possible values: lr, ur, ll, ul')

args = parser.parse_args(sys.argv[1:])
modelName = args.m

execfile('settings.py')

path = os.path.join(folder_with_different_models, modelName)

dataList = common.get_file_list.get_filelist(modelName, path)

#Clean up datafiles that are for sure bad. No moves were performed.
dataList = [item for item in dataList if ((item.get_global_sites() > 0 and item.get_global_accept > 0) or item.get_global_sites() == 0)]

# Clean up datafiles that are for sure bad. Electron density rho is bounded by 0 and 2.
dataList = [item for item in dataList if (item.get_rho()[0] < 2.1)]

#Not using files, that they have mu = 0 and 0 global moves, when u is not zero.
# dataList = [item for item in dataList if
#             ((
#              item.get_u() != 0 and item.get_mu_up() == 0 and item.get_global_sites() > 0) or item.get_u() == 0 or item.get_mu_up() != 0)]

if args.m == 'Lieb' or args.m == 'square':
  bipartite = True
else:
  bipartite = False

# if bipartite:
#   #We know from symmetry of the bipartite lattice that at mu = 0, rho = 1, I will assume that 0.97 - 1.03 is ok
#   if args.rho == 1:
#     dataList = [item for item in dataList if (item.get_mu_up() == 0)]
#     dataList = [item for item in dataList if (abs(item.get_rho()[0] - 1) <= 0.03)]

# We need to remove datapoints if s-wave errorbars > 20%
dataList = [item for item in dataList if (abs(item.get_s_wave()[1] / item.get_s_wave()[0]) < 0.2)]

if args.x_variable == 'u':
  xlabel(r'$U[t]$')
  title(r"{modelname}, $\rho = {rho}$, $\beta = {beta}$, $t={t}$".format(beta=args.beta, rho=args.rho, modelname=args.m, t=args.t),
        fontsize=30)
  dataList = [item for item in dataList if (common.fequals.equals(item.get_t_up(), args.t)
                                            and common.fequals.equals(item.get_beta(), args.beta)
                                            and common.fequals.equals(item.get_mu_up(), args.mu))]
elif args.x_variable == 'mu':
  xlabel(r'$\mu[t]$')
  title(r"{modelname}, $U = {u}$, $\beta = {beta}$, $t={t}$".format(beta=args.beta, u=args.u, modelname=args.m, t=args.t), fontsize=30)
  dataList = [item for item in dataList if (common.fequals.equals(item.get_t_up(), args.t)
                                            and common.fequals.equals(item.get_u(), args.u)
                                            and common.fequals.equals(item.get_beta(), args.beta))]
elif args.x_variable == 'rho':
  xlabel(r'$\rho[t]$')
  title(r"{modelname}, $U = {u}$, $\beta = {beta}$, $t={t}$".format(beta=args.beta, u=args.u, modelname=args.m, t=args.t), fontsize=30)
  dataList = [item for item in dataList if (common.fequals.equals(item.get_t_up(), args.t)
                                            and common.fequals.equals(item.get_u(), args.u)
                                            and common.fequals.equals(item.get_beta(), args.beta))]
elif args.x_variable == 'beta':
  xlabel(r'$\beta[t]$')
  title(r"{modelname}, $\rho = {rho}$, $U = {u}$, $t={t}$".format(u=args.u, rho=args.rho, modelname=args.m, t=args.t), fontsize=30)
  dataList = [item for item in dataList if (common.fequals.equals(item.get_t_up(), args.t)
                                            and common.fequals.equals(item.get_u(), args.u)
                                            and (abs(item.get_rho()[0] - args.rho)) < 0.02 + item.get_rho()[1])]

elif args.x_variable == 'T':
  xlabel(r'$T[t]$')
  title(r"{modelname}, $\rho = {rho}$, $U = {u}$, $t={t}$".format(u=args.u, rho=args.rho, modelname=args.m, t=args.t), fontsize=30)
  dataList = [item for item in dataList if (common.fequals.equals(item.get_t_up(), args.t)
                                            and common.fequals.equals(item.get_u(), args.u)
                                            and common.fequals.equals(item.get_mu_up(), args.mu))]
elif args.x_variable == '1L':
  xlabel(r'$1 / L$')
  title(r"{modelname}, $\rho = {rho}$, $u = {u}$, $\beta = {beta}$, $t={t}$".format(u=args.u, rho=args.rho, beta=args.beta,
                                                                           modelname=args.m, t=args.t), fontsize=30)
  dataList = [item for item in dataList if (common.fequals.equals(item.get_t_up(), args.t)
                                            and common.fequals.equals(item.get_u(), args.u)
                                            and common.fequals.equals(item.get_rho()[0], args.rho)
                                            and common.fequals.equals(item.get_beta(), args.beta))]

#divide into classes, corresponding to different number of sites
into_nSites_dict = common.divide_into_classes.divide_into_classes(dataList, parameter='nSites')

for element in dataList:
  print element.get_rho()
#We choose what lattice sizes are we interested in
nSites_list = common.choices.list_choice(into_nSites_dict.keys())

for nSites in nSites_list:
  splitted = common.divide_into_classes.divide_into_classes(into_nSites_dict[nSites], parameter=args.x_variable)
  xList, yList, yErr = common.merge.merge(splitted, args.y_variable)

  if args.x_variable == 'T':
    xList = [1 / tx for tx in xList]

  errorbar(xList, yList, yerr=yErr, fmt='D-', label='nSites = {nSites}'.format(nSites=nSites), linewidth=3,
           markersize=15)
  if args.to_screen:
    print 'xList = ', xList
    print 'yList = ', yList
    print 'yErr = ', yErr

if args.y_variable == 'Energy' and args.t == 0:
  ylabel(r'$Energy$')

if args.y_variable == 'Energy_hop' and args.t != 0:
  ylabel(r'$Energy_{hop}[t]$')
elif args.y_variable == 'Energy_hop' and args.t == 0:
  ylabel(r'$Energy_{hop}$')

if args.y_variable == 'X_F' and args.t != 0:
  ylabel(r'$struct_xx_f[t]$')
elif args.y_variable == 'X_F' and args.t == 0:
  ylabel(r'$struct_xx_f$')

if args.y_variable == 'rho' and args.t != 0:
  ylabel(r'$\rho[t]$')
elif args.y_variable == 'rho' and args.t == 0:
  ylabel(r'$\rho$')

if args.y_variable == 'DO' and args.t != 0:
  ylabel(r'$\left<N_{up} N_{down}\right>[t]$')
elif args.y_variable == 'rho' and args.t == 0:
  ylabel(r'$\left<N_{up} N_{down}\right>[t]$')

if args.y_variable == 's-wave' and args.t != 0:
  ylabel(r'$P_s[t]$')
elif args.y_variable == 's-wave' and args.t == 0:
  ylabel(r'$P_s[t]$')

if args.y_variable == '01':
  ylabel(r'$\left<n_0 n_1\right>[t]$')

if args.y_variable == '12':
  ylabel(r'$\left<n_1 n_2\right>[t]$')

if args.y_variable == '00':
  ylabel(r'$\left<n_{0,(0,0)} n_{0, (1, 0)}\right>[t]$')

if args.y_variable == 'm2' and args.t != 0:
  ylabel(r'$\left<m^2\right>[t]$')
elif args.y_variable == 'm2' and args.t == 0:
  ylabel(r'$\left<m^2\right>[t]$')

if args.y_variable == 'm0_squared' and args.t != 0:
  ylabel(r'$\left<m_0^2 \right>[t]$')
elif args.y_variable == 'm0_squared' and args.t == 0:
  ylabel(r'$\left<m_0^2 \right>[t]$')

if args.y_variable == 'm1_squared' and args.t != 0:
  ylabel(r'$\left<m_1^2 \right>[t]$')
elif args.y_variable == 'm1_squared' and args.t == 0:
  ylabel(r'$\left<m_1^2 \right>[t]$')

if args.y_variable == 'C' and args.t != 0:
  ylabel(r'$C[t]$')
elif args.y_variable == 'm1_squared' and args.t == 0:
  ylabel(r'$C[t]$')

if args.legend == 'lr' or args.legend == 'rl':
  legend(loc='lower right', fancybox=True, shadow=True)
elif args.legend == 'ur' or args.legend == 'ru':
  legend(loc='upper right', fancybox=True, shadow=True)
elif args.legend == 'll' or args.legend == 'll':
  print 'here'
  legend(loc='lower left', fancybox=True, shadow=True)
elif args.legend == 'ul' or args.legend == 'lu':
  legend(loc='upper left', fancybox=True, shadow=True)
elif args.legend == 'best':
  legend(loc='best', fancybox=True, shadow=True)
else:
  legend(fancybox=True, shadow=True)

if '-x_min' in sys.argv:
  xlim(xmin=args.x_min)

show()