class Test:
    '''router class'''
    def __init__(self, model, name):
        self.model = model
        self.name = name
    
    def getdesc(self):
        '''this method will print the attribute of the class has'''
        desc = f'Router model: {self.model}\n'\
               f'Router name: {self.name}\n'
        return desc

class Switch(Test):
    '''This is inherited class'''
    def getdesc(self):
        desc = f' Switch Model: {self.model}\n'\
               f' Switch Name: {self.name}'
        return desc

rtr1 = Test('8500', 'SDWAN')
rtr2 = Test('ASR', 'WAN Edge')
switch = Switch('9300', 'Access Switch')
print('Swtich\n', rtr1.getdesc(), '\n', sep = '')
print ('Router\n', rtr2.getdesc(), '\n', sep = '' )
print ('Switch\n', switch.getdesc(), '\n', sep = '')