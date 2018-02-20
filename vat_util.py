""" VAT module 

Defines VAT calculation models for each region and sub-regions, where sub-regions inherit
the tax rules from parent regions.

The sub-regions only need to define applicable tax policies eg. tax free, VAT slabs, fixed VAT etc.
and hence the rules can be modified accordingly.

The mappings of items with custom VAT rules above the base VAT are pulled from 
database, based on the region/sub-regions and sub-regions expand/override the rules defined in the
parent region.

The TODOs in the code specify further scope of improvement.
"""

class AbstractVatModel(object):
  def __init__(self):
    self._base_vat = 0
    
    # Custom mappings based on various VAT Policies
    # Models using a particular policy need to override it with their definition
    
    # Mapping of tax free products to max tax free amount
    self._tax_free_items_max_amount = {}
    
    # Mapping of flat VAT products to max VAT amount
    self._flat_vat_items_vat_amount = {}
    
    # Mapping of cusomt VAT products to custom VAT percentage
    self._custom_vat_items_vat_rate = {}
    
    # Mapping of products limited capped by a maximum VAT amount to max VAT amount
    self._max_vat_items_max_vat = {}
    
    # Mapping of products which incur additional VAT to additional VAT percentage
    self._additional_vat_items_vat_rate = {}
  
  def base_vat(self):
    raise NotImplementedError('base_vat undefined for requested model')
  
  def getVat(self):
    # TODO consider round off for vat amount and use in all implementations
    raise NotImplementedError('getVat undefined for requested model')

  
  
  
## Each region has some specific rules so each deserves a
## dedicated class representation.
  
# EU Region and sub-regions
class EuVatModel(AbstractVatModel):
  def __init__(self):
    print 'EU'
    super(EuVatModel, self).__init__()
    
    # populated from database
    self._base_vat = 12.5/100.0
    
    # populated from database
    # TODO redefine this in GBP for UK
    flat_vat_items_vat_amount = {
      'bread': .05
    }
    self._flat_vat_items_vat_amount.update(flat_vat_items_vat_amount)


class GermanyVatModel(EuVatModel):
  def __init__(self):
    print 'Germany'
    super(GermanyVatModel, self).__init__()
    self._base_vat = 15  # populated from database
    
    # populated from database
    tax_free_items_max_amount = {
      'bread': 1
    }
    self._tax_free_items_max_amount.update(tax_free_items_max_amount)

    # populated from database
    custom_vat_items_vat_rate = {
      'wine': 20.0/100.0
    }
    self._custom_vat_items_vat_rate.update(custom_vat_items_vat_rate)

  def getVat(self, product, amount):
    print product, 'amounting', amount
    vat = 0.0
    
    taxable_amount = amount
    if product in self._tax_free_items_max_amount:
      taxable_amount = amount - self._tax_free_items_max_amount.get(product, 0)
      
    if taxable_amount > 0:
      if product in self._flat_vat_items_vat_amount:
        vat = self._flat_vat_items_vat_amount.get(product)
      elif product in self._custom_vat_items_vat_rate:
        vat = taxable_amount * self._custom_vat_items_vat_rate.get(product)
      else:
        vat = taxable_amount * self._base_vat
      
    return vat


class UkVatModel(EuVatModel):
  def __init__(self):
    print 'UK'
    super(UkVatModel, self).__init__()
    
    # populated from database
    custom_vat_items_vat_rate = {
      'wine': 10.0/100.0
    }
    self._custom_vat_items_vat_rate.update(custom_vat_items_vat_rate)
    
  def getVat(self, product, amount):
    print product, 'amounting', amount
    vat = 0.0
      
    if amount > 0:
      if product in self._custom_vat_items_vat_rate:
        vat = amount * self._custom_vat_items_vat_rate.get(product)
      else:
        # TODO if slab based vat is a common policy, factor it out
        # TODO use a helper method to create slab based vat
        if amount <= 20:
          vat = float(amount) * float(self._base_vat)
        elif amount <= 100:
          vat = float(20) * float(self._base_vat) + (
            float(amount - 20) * 15.0/100.0)
        else:
          vat = float(20) * float(self._base_vat) + (
            float(80) * 15.0/100.0 +
            float(amount - 100) * 20.0/100.0)
            
    return vat
    

class FranceVatModel(EuVatModel):
  def __init__(self):
    print 'France'
    super(FranceVatModel, self).__init__()
    
    # populated from database
    tax_free_items_max_amount = {
      'eggs': 0.5
    }
    self._tax_free_items_max_amount.update(tax_free_items_max_amount)
    
    # populated from database
    custom_vat_items_vat_rate = {
      'ale': 17.5/100.0,
      'beer': 17.5/100.0,
    }
    self._custom_vat_items_vat_rate.update(custom_vat_items_vat_rate)
    
    # populated from database
    max_vat_items_max_vat = {
      'wine': 5.0
    }
    self._max_vat_items_max_vat.update(max_vat_items_max_vat)
    
  def getVat(self, product, amount):
    print product, 'amounting', amount
    vat = 0.0
    
    taxable_amount = amount
    if product in self._tax_free_items_max_amount:
      taxable_amount = amount - self._tax_free_items_max_amount.get(product, 0)
      
    if taxable_amount > 0:
      if product in self._custom_vat_items_vat_rate:
        vat = taxable_amount * self._custom_vat_items_vat_rate.get(product)
      else:
        vat = float(taxable_amount) * float(self._base_vat)
        
    if product in self._max_vat_items_max_vat and vat > self._max_vat_items_max_vat.get(product):
      vat = self._max_vat_items_max_vat.get(product)
      
    return vat


# US Region and sub-regions
class UsVatModel(AbstractVatModel):
  def __init__(self):
    print 'US'
    super(UsVatModel, self).__init__()
    
    # populated from database
    self._base_vat = 10.0/100.0
    
    # populated from database
    # TODO redefine this in GBP for UK
    custom_vat_items_vat_rate = {
      'dairy': 5.0/100.0,  # TODO consider product categories. eg. dairy to include milk, cheese, cream etc.
      'milk': 5.0/100.0,
    }
    self._custom_vat_items_vat_rate.update(custom_vat_items_vat_rate)
    
    # populated from database
    additional_vat_items_vat_rate = {
      'alcohol': 7.5/100.0, # TODO product categories like in dairy
      'beer': 7.5/100.0,
      'wine': 7.5/100.0,
    }
    self._additional_vat_items_vat_rate.update(additional_vat_items_vat_rate)
    
    
class TexasVatModel(UsVatModel):
  def __init__(self):
    print 'Texas'
    super(TexasVatModel, self).__init__()
    
    # populated from database
    self._base_vat = 12.5/100.0
    
    # populated from database
    tax_free_items_max_amount = {
      'beer': 1
    }
    self._tax_free_items_max_amount.update(tax_free_items_max_amount)
    
    flat_vat_items_vat_amount = {
      'bread': .05
    }
    self._flat_vat_items_vat_amount.update(flat_vat_items_vat_amount)
  
  
  def getVat(self, product, amount):
    print product, 'amounting', amount
    vat = 0.0
    
    taxable_amount = amount
    if product in self._tax_free_items_max_amount:
      taxable_amount = amount - self._tax_free_items_max_amount.get(product, 0)
      
    if taxable_amount > 0:
      if product in self._flat_vat_items_vat_amount:
        vat = self._flat_vat_items_vat_amount.get(product)
      else:
        vat = float(taxable_amount) * float(self._base_vat)
        
      if product in self._additional_vat_items_vat_rate:
        vat += taxable_amount * self._additional_vat_items_vat_rate.get(product)
      
    return vat
    
    
class AlaskaVatModel(UsVatModel):
  def __init__(self):
    print 'Alaska'
    super(AlaskaVatModel, self).__init__()
    
    # populated from database
    max_vat_items_max_vat = {
      'milk': 0.5
    }
    self._max_vat_items_max_vat.update(max_vat_items_max_vat)
    
  def getVat(self, product, amount):
    print product, 'amounting', amount
    vat = 0.0
      
    if amount > 0:
      vat = float(amount) * float(self._base_vat)
        
    if product in self._max_vat_items_max_vat and vat > self._max_vat_items_max_vat.get(product):
      vat = self._max_vat_items_max_vat.get(product)
      
    return vat


class NewYorkVatModel(UsVatModel):
  pass



def getVatModelByCountry(country):
  # TODO cache/memoize model so that we do not need to init for each call
  return _VAT_MODEL_MAP.get(country.upper())
  
  
_VAT_MODEL_MAP = {
  # Regions
  'EU': EuVatModel, 
  'US': UsVatModel, 
  
  # Sub-regions (countries/states)
  'GERMANY': GermanyVatModel,
  'UK': UkVatModel,
  'FRANCE': FranceVatModel,
  'TEXAS': TexasVatModel,
  'ALASKA': AlaskaVatModel
}

# TODO Currency conversion models for scenarios like GBP - EUR and various currencies in Africa/Asia etc.
# _CURRENCY_MAP = {
#   'Germany': 'EUR',
#   'UK': 'GBP',
#   'France': 'EUR',
#   'Texas': 'USD', 
#   'Alaska': 'USD',
#   'Colorado': 'USD',
# }
  
  
# TODO Use region map for sub-regions that do not need special overriding, and hence
# can use parent region VAT rules.
# _REGION_MAP = {
#   'Germany': 'EU',
#   'UK': 'EU',
#   'France': 'EU',
#   'Texas': 'US', 
#   'Alaska': 'US',
#   'Colorado': 'US',
#   # 'NotFound': 'Default',
# }

