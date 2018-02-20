""" Main module """

import vat_util


def demo(argv):
  try:
    product, amount, country = argv.split(',')
    if product and amount and country:
      print calculateVat(product, int(amount), str(country).strip()), 'is the VAT'
    else:
      print 'Please enter input as 3 comma separated values (eg. bread, 1, Alaska) '
  except ValueError as e:
    print e
  
  input = raw_input('Please enter next item, amount, country: ')
  demo(input)
  

def calculateVat(product, amount, country):
  vat_model = vat_util.getVatModelByCountry(country)
  if vat_model:
    return vat_model().getVat(product, amount)
  else:
    print 'VAT cannot be calculated for', country
    return 0


def run_tests():
  # Germany
  print calculateVat('bread', 1, 'Germany')  # 0
  print 
  print calculateVat('bread', 2, 'Germany')  # .05
  print
  print calculateVat('wine', 100, 'Germany')  # 20
  print
  
  # UK
  print calculateVat('wine', 10, 'UK')  # 1
  print
  print calculateVat('wine', 100, 'UK')  # 10
  print
  print calculateVat('jeans', 20, 'UK')  # 2.5
  print
  print calculateVat('jeans', 100, 'UK')  # 2.5 + 12 = 14.5
  print
  print calculateVat('jeans', 150, 'UK')  # 2.5 + 12 + 10 = 24.5
  print 
  
  # France
  print calculateVat('bread', 2, 'France')  # .25
  print
  print calculateVat('wine', 10, 'France')  # 1.25
  print
  print calculateVat('wine', 100, 'France')  # 5.0
  print
  print calculateVat('eggs', .5, 'France')  # 0
  print 
  print calculateVat('eggs', 1, 'France')  # .0625
  print
  print calculateVat('beer', 50, 'France')  # 8.75
  print 
  print calculateVat('ale', 100, 'France')  # 17.5
  print 
  
  # Texas
  print calculateVat('bread', 2, 'Texas')  # .05
  print
  print calculateVat('wine', 100, 'Texas')  # 12.5 + 7.5 = 20
  print
  print calculateVat('beer', 100, 'Texas')  # 12.375 + 7.425 = 19.8
  print
  
  
  # Alaska
  print calculateVat('milk', 0.5, 'Alaska')  # .5
  print
  print calculateVat('milk', 8, 'Alaska')  # .5
  print
  print calculateVat('beer', 100, 'Alaska')  # 10
  print
  print calculateVat('whatever', 100, 'Alaska')
  print
  
  # Invalid cases
  print calculateVat('whatever', -1, 'NoWhere')
  print
  print calculateVat('whatever', 100, 'Scotland')


# Accept custom input
input = raw_input('Please enter item, amount, country (eg. milk, 2, UK): ')
if input == "test":
  run_tests()
demo(input)
