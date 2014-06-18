from __future__ import division
__author__ = 'vladimir'

def divide_into_classes(datList, **kwargs):
  '''

  @param datList: list of the files that we want to divide into classes
  @param kwargs: possible parameters:
    nSites - number of sites in the spatial layer
    beta - inverse temperature
    mu - chemical potential
    u - strength of the u term
    1L - inverse of the numbers of the unit cells in one direction
    rho - electronic density
    k - versus momentum
  @return: dictionary with key - parameter of the division, values - list with files that correspond to this parameter
  '''
  result = {}
  if kwargs['parameter'] == 'nSites':
    for victim in datList:
      if victim.get_nSites() not in result:
        result[victim.get_nSites()] = [victim]
      else:
        result[victim.get_nSites()] += [victim]

  elif kwargs['parameter'] == '1L':
    for victim in datList:
      key = 1.0 / victim.get_nx()
      if key not in result:
        result[key] = [victim]
      else:
        result[key] += [victim]

  elif kwargs['parameter'] == 'beta':
    for victim in datList:
      if victim.get_beta() not in result:
        result[victim.get_beta()] = [victim]
      else:
        result[victim.get_beta()] += [victim]

  elif kwargs['parameter'] == 'mu':
    for victim in datList:
      if victim.get_mu_up() not in result:
        result[victim.get_mu_up()] = [victim]
      else:
        result[victim.get_mu_up()] += [victim]

  elif kwargs['parameter'] == 'u':
    for victim in datList:
      if victim.get_u() not in result:
        result[victim.get_u()] = [victim]
      else:
        result[victim.get_u()] += [victim]

  elif kwargs['parameter'] == 'rho':
    for victim in datList:
      # rho = round(victim.get_rho()[0], 2)
      # rho = int(50 * victim.get_rho()[0]) / 50
      rho = int(70 * victim.get_rho()[0]) / 70
      if rho not in result:
        result[rho] = [victim]
      else:
        result[rho] += [victim]

  return result