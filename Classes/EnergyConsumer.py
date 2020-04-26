class EnergyConsumer:

    def __init__(self, IDEnergyConsumer, nameEnergyConsumer, PEnergyConsumer, QEnergyConsumer, equipEnergyConsumer,
                 baseVolEnergyConsumer):
        self.tR = []
        self.tR.extend(["Y00 = 1.79246514136212-9.611369871751679j", "Y04 = -1.79246514136212+9.61136987175168j", "Y11 = 0.140203381092528-2.18317911547753j","Y12 = -0.135457287342528+2.18475920779003j", "Y21 = -0.135457287342528+2.18475920779003j", "Y22 = 0.47410059624891-6.70340518943569i", "Y24 = 0.333897215156383+4.52022607395816j", "Y33 = 0.0370940444408892-2.07004081780077j", "Y34 = -0.0370940444408892 +2.07004081780077j", "Y40 = -1.79246514136212 + 9.61136987175168j", "Y42 = 0.333897215156383 + 4.52022607395816j", "Y43 = -0.0370940444408892 + 2.07004081780077j", "Y44 = 2.16345640095939-16.2016367635106j"])
        self.IDEnergyConsumer = IDEnergyConsumer
        self.nameEnergyConsumer = nameEnergyConsumer
        self.PEnergyConsumer = PEnergyConsumer
        self.QEnergyConsumer = QEnergyConsumer
        self.equipEnergyConsumer = equipEnergyConsumer
        self.baseVolEnergyConsumer = baseVolEnergyConsumer
