"""Test setup for integration and functional tests.
"""

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

#
# When ZopeTestCase configures Zope, it will *not* auto-load products in 
# Products/. Instead, we have to use a statement such as:
# 
#   ztc.installProduct('SimpleAttachment')
# 
# This does *not* apply to products in eggs and Python packages (i.e. not in
# the Products.*) namespace. For that, see below.
# 
# All of Plone's products are already set up by PloneTestCase.
# 

@onsetup
def setup_product():
    """Set up the package and its dependencies.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer. We could have created our
    own layer, but this is the easiest way for Plone integration tests.
    """
    
    fiveconfigure.debug_mode = True

    import plone.app.registry
    import plone.resource

    zcml.load_config('configure.zcml', package=plone.app.registry)
    zcml.load_config('configure.zcml', package=plone.resource)

    fiveconfigure.debug_mode = False
    
    ztc.installPackage('emas.app')
    
# The order here is important: We first call the (deferred) function which
# installs the products we need for this product. Then, we let PloneTestCase 
# set up this product on installation.

setup_product()
ptc.setupPloneSite(products=['upfront.analyticsqueue'])

class BaseTestCase(ptc.PloneTestCase):
    """
    """

class BaseFunctionalTestCase(ptc.FunctionalTestCase):
    """
    """

