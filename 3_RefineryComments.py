import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT, REFINERY, VESPENEGEYSER, MINERALFIELD
from sc2 import position


class NN(sc2.BotAI):
    async def on_step(self, iteration):
        self.time = (self.state.game_loop/22.4) / 60
        print('Time:',self.time)

        # what to do every step
        await self.distribute_workers()  # in sc2/bot_ai.py
        await self.build_scv()			 # Build our worker who will mine minerals
        await self.build_supply_depot()


######################################
        await self.build_refinery()
        # await self.checking_resources() # Learn how to extract Units(MineralFIeld and VespenGeyser) - Name, Tag, Position, Distance_to
######################################


    async def build_scv(self):
    	for cc in self.units(COMMANDCENTER).ready.noqueue:
    		if self.can_afford(SCV) and not self.already_pending(SCV):
    			await self.do(cc.train(SCV))


    async def build_supply_depot(self):
        SD = self.units(COMMANDCENTER)
        if self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
            await self.build(SUPPLYDEPOT, near = SD.first.position.towards(self.game_info.map_center, 6))
            print('\t\tStart off to BUILD')


#############################################################
#   Specific Architecture for - finding spot and building Geyser

    async def build_refinery(self):
        if self.can_afford(REFINERY) and self.time > 0.43 and len(self.units(REFINERY)) <= 4:
            for cc in self.units(COMMANDCENTER):
                #   Found Geyser near CommandCenter
                vgs = self.state.vespene_geyser.closer_than(20.0, cc)
                print('\n vgs', vgs)                                    #   [Unit(name='VespeneGeyser', tag=4299948033), Unit(name='VespeneGeyser', tag=4299685889)]
                print('\n TYPE', type(vgs))                             #   class 'sc2.units.Units'>
                    #   Iterate through Geyser near CC
                for vg in vgs:
                    print('\n vg', vg)                                  #   Unit(name='VespeneGeyser', tag=4299948033)
                    print('\n Type', type(vg))                          #   <class 'sc2.unit.Unit'>
                    #   Check If REFINERY already exists on Geyser Spot, If so break
                    if self.units(REFINERY).closer_than(1.0,vg).exists:
                        break
                    #   If not exists, then select worker and use him for building Refinery
                    worker = self.select_build_worker(vg.position)
                    print('\n worker', worker)                          #   Unit(name='SCV', tag=4348706817)
                    print('\n Type', type(worker))                      #   <class 'sc2.unit.Unit'>
                    await self.do(worker.build(REFINERY, vg))
                    print('\n self.do(worker.build(REFINERY, vg))', self.do(worker.build(REFINERY, vg)))    #   <coroutine object BotAI.do at 0x105b410a0>
                    print('\n TYPEC', type(self.do(worker.build(REFINERY, vg))))                            #   <class 'coroutine'>
                    break
                print('\n\t\t\t Building')

    # async def checking_resources(self):
        # first_CC = self.units(COMMANDCENTER).first
        # # print('\n\t\t   Inside CHECKING_RESOURCES()')

        # #       self.minerals --- self.vespene --- self.state --- self.state.vespene_geyser --- self.state.mineral_field

        # # print('\n Minerals: {}'.format(self.minerals))              #   Minerals: 70
        # # print('\n Type Minerals: {}'.format(type(self.minerals)))   #   <class 'int'>
        # # print('\n Vespene: {}'.format(self.vespene))                #   Vespene: 0   
        # # print('\n Type Vespene: {}'.format(type(self.vespene)))     #   <class 'int'>
        # # print('\n State: {}'.format(self.state))                    #   <sc2.game_state.GameState object at 0x105bd7710>
        # # print('\n Type State: {}'.format(type(self.state)))         #   <class 'sc2.game_state.GameState'>
        # # print('\n Minerals: {}'.format(self.state.mineral_field))       #   Minerals: [Unit(name='MineralField', tag=8796504067), ... Unit(name='MineralField', tag=4296278017)]
        # # print('\n Minerals: {}'.format(type(self.state.mineral_field))) #   <class 'sc2.units.Units'>
        # # print('\n Minerals: {}'.format(self.state.vespene_geyser))      #   Geyser: [Unit(name='VespeneGeyser', tag=8807514114), ... Unit(name='VespeneGeyser', tag=4297064449)]
        # # print('\n Minerals: {}'.format(type(self.state.vespene_geyser)))#   <class 'sc2.units.Units'>

        # for MF in self.state.vespene_geyser:
        # # for MF in self.units(VESPENEGEYSER):          #   It's not working
        # #     print('\n\t VespeneGeyser name: {}'.format(MF))                                  #   Unit(name='VespeneGeyser', tag=8798273539)
        # #     print('\n\t VespeneGeyser name: {}'.format(MF.name))                             #   VespeneGeyser
        # #     print('\n\t VespeneGeyser tag: {}'.format(MF.tag))                               #   8798273539
        # #     print('\n\t VespeneGeyser position: {}'.format(MF.position))                     #   (158.5, 14.5)
        # #     print('\n\t VespeneGeyser position: {}'.format(type(MF.position)))               #   <class 'sc2.position.Point2'>
        # #     print('\n\t VespeneGeyser distance_to CC: {}'.format(MF.distance_to(first_CC.position)))#   161.44348856488452
        # #     print('\n\t VespeneGeyser TYPE: {}'.format(type(MF.distance_to(first_CC.position))))    #   <class 'float'>
        # # print('\n FINISH Geyser Loop \n')
        # for VG in self.state.units.mineral_field:
        # #     print('\n\t MineralField name: {}'.format(VG))                                  #   Unit(name='MineralField750', tag=8793554947)
        # #     print('\n\t MineralField name: {}'.format(VG.name))                             #   MineralField750
        # #     print('\n\t MineralField tag: {}'.format(VG.tag))                               #   8793554947
        # #     print('\n\t MineralField position: {}'.format(VG.position))                     #   (162.0, 14.5)
        # #     print('\n\t MineralField distance_to CC: {}'.format(VG.distance_to(first_CC.position))) #   164.06172618865133
        # #     print('\n\t MineralField TYPE: {}'.format(type(VG.distance_to(first_CC.position))))     #   <class 'float'>
        # # print('\n FINISH Minerals Loop \n')

#############################################################


run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, NN()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)