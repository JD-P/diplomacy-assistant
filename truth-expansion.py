def possibilities(cases):
  expansion = [[]]
  for value in cases:
    if value == True or value == False:
      for expanded in expansion:
        expanded.append(value)
    elif value == 'TORF':
      for expanded in expansion[:]:
        copy = expanded[:]
        expanded.append(True)
        copy.append(False)
        expansion.append(copy)
    elif value == '*TORF':
      for expanded in expansion[:]:
        copy = expanded[:]
        copy.append(True)
        expansion.append(copy)
        copy = expanded[:]
        copy.append(False)
        expansion.append(copy)
  for expanded in expansion[:]:
    converted = tuple(expanded)
    expansion.remove(expanded)
    expansion.append(converted)
  return expansion

def overlapping(*closures):
  """Returns a dictionary of the form {closure_position:(closure, (intersected_position, intersected))...} for each overlapping set in the given closures."""
  overlaps = {}
  closure_position = 0
  for closure in closures:
    if type(closure) != set:
      closure = set(closure)
    intersected_position = 0
    for intersected in closures:
      if type(intersected) != set:
        intersected = set(intersected)
      if closure == intersected:
        None
      elif intersected_position in overlaps:
        None
      elif closure.intersection(intersected) != set():
        overlaps[closure_position] = (intersected_position, closure.intersection(intersected))
      intersected_position += 1
    closure_position += 1
  return overlaps
