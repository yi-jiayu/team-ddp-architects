inp={
  "maxWeight": 5,
  "vault": [
  {"weight": 1, "value": 200},
  {"weight": 3, "value": 240},
  {"weight": 5, "value": 150},
  {"weight": 2, "value": 140}
  ]
}

def solve(maxWeight,vault):
  max = float(maxWeight)
  current = 0
  heist = 0
  valuechain = vault
  value1 = []

  for i in range(len(valuechain)):
      value = float(valuechain[i]['value'])
      weight = float(valuechain[i]['weight'])
      vpweight = value/weight
      value1.append([vpweight,weight])

  valuefinal = sorted(value1, key = lambda x:x[0])[::-1]

  for j in range(len(valuefinal)):
      if max - current >= valuefinal[j][1]:
          current += valuefinal[j][1]
          heist += valuefinal[j][0]*valuefinal[j][1]
      elif max - current < valuefinal[j][1]:
          final = max-current
          current += final
          heist += valuefinal[j][0]*final

  ans = {"heist": heist}
  return ans

print(solve(inp['maxWeight'],inp['vault']))