from Products.PloneTestCase import ptc
import collective.testcaselayer.ptc

ptc.setupPloneSite()

class IntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):
        super(IntegrationTestLayer, self).afterSetUp()

Layer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])
