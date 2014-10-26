from __future__ import division
import numpy
import re

__author__ = 'Vladimir Iglovikov'


def extract_geometry(victim, **kwargs):
  parameter = kwargs['parameter']
  result = {}
  if parameter == 'coordinates':
    tm = re.search(r'(?<=Z)[0-9\s s\.]*', victim).group()
    for line in tm.strip().split("\n"):
      tp = line.strip().split()
      index, label, type, x, y, z = int(tp[0]), tp[1], int(tp[2]), float(tp[3]), float(tp[4]), float(tp[5])
      result[index] = (label, type, x, y, z)
    return result


def extract_tdm_data(victim, **kwargs):
  parameter = kwargs['parameter']

  if parameter == 'ld_xx_real':
    result = {}
    tm = re.findall(r'(?<=xx Current)([\s 0-9\.E+-]*)', victim.replace('+-', ''))
    for element in tm:
      key = element.strip().split('\n')[0].split()
      i = int(key[0])
      j = int(key[1])
      for line in element.strip().split('\n')[1:]:
        tl = line.strip().split()
        result[(i, j, float(tl[0]))] = (float(tl[1]), float(tl[2]))
    return result




  else:
    temp = victim.strip().split('====================================')
    temp1 = []
    for i, item in enumerate(temp):
      if parameter in item and 'k' not in item:
        tt = item.replace('=', '').strip()

        temp1 += [tt]

    result = {}
    for item in temp1:
      temp = item.split('\n')
      key = temp[0].replace(parameter, '').strip().split()

      key = (int(key[0]), int(key[1]), float(key[2]), float(key[3]))

      yList = []
      yErr = []
      for i in xrange(1, len(temp) - 1):
        temp3 = temp[i].replace('+-', '').strip().split()
        yList += [float(temp3[1])]
        yErr += [float(temp3[2])]

      result[key] = (numpy.mean(yList), numpy.mean([tx ** 2 for tx in yErr]))
    return result


def extract_non_tdm_data(victim, **kwargs):
  parameter = kwargs['parameter']

  if parameter == 'k_points':
    result = []
    tm = re.search(r'(?<=Class)[\s 0-9\.-]*', victim).group()
    for line in tm.strip().split('\n'):
      tl = line.strip().split()
      if len(tl) == 3:
        result += [(float(tl[1]), float(tl[2]))]
      elif len(tl) == 2:
        result += [(float(tl[0]), float(tl[1]))]
    return result
  elif parameter == "Mean Equal time Green's function":
    result = []
    tm = re.search(r"(?<=Mean Equal time Green's function:)[\s 0-9\.E+-]*", victim).group()
    tm = tm.replace('+-', '').strip().split("\n")
    for line in tm:
      tl = line.strip().split()
      orbit1, orbit2, x, y, z, symmetry, value, err = int(tl[0]), int(tl[1]), float(tl[2]), float(tl[3]), float(
        tl[4]), int(tl[5]), float(tl[6]), float(tl[7])
      result += [orbit1, orbit2, x, y, z, symmetry, value, err]
    return result


    # temp = victim.strip().split('====================================')
    # temp1 = []
    # for i, item in enumerate(temp):
    # if parameter in item:
    #       tt = item.replace('=', '').strip()
    #       temp1 += [tt]
    #
    #   result = {}
    #
    # elif 'FT' not in kwargs and 'k_grid' not in kwargs:  # We work with non Fourier transform
    #   for item in temp1:
    #     if (parameter in item and "FT" not in item and "Eigenvalues" not in item and "Eigenmodes" not in item):
    #       temp = item.replace(parameter, '').strip().split('\n')
    #       for line in temp:
    #         temp2 = line.replace('+-', '').replace('-', ' -').replace('E -', 'E-').strip().split()
    #         result[(int(temp2[0]), int(temp2[1]), float(temp2[3]), float(temp2[4]), float(temp2[5]))] = (
    #           float(temp2[6]), float(temp2[7]))
    # elif 'k_grid' not in kwargs and kwargs['FT'] == True: # We work with Fourier transform
    #   temp = temp1[0].replace('+-', '').replace(parameter, '').strip().split('\n')
    #   temp1 = []
    #   for line in temp:
    #     tx = []
    #     for ttx in line.split():
    #       tx += [float(ttx)]
    #     temp1 += [tx]
    #   result = []
    #   for line in temp1:
    #     if len(line) == 5:
    #       key = int(line[0])
    #       result += [(key, line[1], line[2], line[3], line[4])]
    #     elif len(line) == 4:
    #       result += [(key, line[0], line[1], line[2], line[3])]
    #     else:
    #       print 'we should not be here'
    #
    # elif 'k_grid' in kwargs and 'FT' not in kwargs: # We work with k points
    #   # temp = temp1[0].replace(parameter, '').replace('K-points', '').replace('Class', '').strip().split('\n')
    #   temp = temp1[0].replace(parameter, '').replace('K-points', '').replace('Class', '')
    #
    #   temp1 = []
    #   for line in temp.strip().split('\n'):
    #     tx = []
    #     for ttx in line.split():
    #       tx += [float(ttx)]
    #     temp1 += [tx]
    #
    #   key = 'temp'
    #
    #   result = {}
    #   if dimension == 1:
    #     for line in temp1:
    #       if len(line) == 2:
    #         key = int(line[0])
    #         result[key] = [line[1]]
    #       elif len(line) == 1:
    #         result[key] += [line[0]]
    #   elif dimension == 2:
    #     for line in temp1:
    #       if len(line) == 3:
    #         key = int(line[0])
    #         result[key] = [(line[1], line[2])]
    #       elif len(line) == 2:
    #         result[key] += [(line[0], line[1])]
    # return result
    #
