import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT
from sc2 import position


class NN(sc2.BotAI):
    async def on_step(self, iteration):
        self.time = (self.state.game_loop/22.4) / 60
        print('Time:',self.time)

        # what to do every step
        await self.distribute_workers()  # in sc2/bot_ai.py
        await self.build_scv()			 # Build our worker who will mine minerals
        await self.build_supply_depot()  #  NEW


    async def build_scv(self):
    	for cc in self.units(COMMANDCENTER).ready.noqueue:
    		if self.can_afford(SCV) and not self.already_pending(SCV):
    			await self.do(cc.train(SCV))
    			# print('Passed conditions and train - {}'.format(self.do(cc.train(SCV))))


############################################################################################

    async def build_supply_depot(self):
        SD = self.units(COMMANDCENTER)
        SD_List = list(SD)
        if self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
            await self.build(SUPPLYDEPOT, near = SD.first.position.towards(self.game_info.map_center, 6))
            print('\t\tStart off to BUILD')
            # print('\n\t Object COMMANDCENTER:', SD)             #   [Unit(name='CommandCenter', tag=4346347521)]
            # print('\n\t TYPE OF COMMANDCENTER:', type(SD))      #   <class 'sc2.units.UnitSelection'>
            #   Curioity
            print('\n\t Object COMMANDCENTER into LIST:', SD_List)                      #   [Unit(name='CommandCenter', tag=4346347521)]
            print('\n\t TYPE OF COMMANDCENTER TYPE into list:', type(SD_List))          #   <class 'list'>

            print('\n\t Object COMMANDCENTER loop through LIST:',SD_List[0])             #    Unit(name='CommandCenter', tag=4346347521)
            print('\n\t Object COMMANDCENTER: TYPE inside loop', type(SD_List[0]))       #   <class 'sc2.unit.Unit'>
            for unit in self.units(COMMANDCENTER):
                print('\n COMMANDCENTER tag: {}'.format(unit.tag))                      #   4346347521
                print('\n COMMANDCENTER tagTYPE: {}'.format(type(unit.tag)))            #   <class 'int'>
                print('\n COMMANDCENTER name: {}'.format(unit.name))                    #   CommandCenter
                print('\n COMMANDCENTER nameTYPE: {}'.format(type(unit.name)))
                print('\n COMMANDCENTER position: {}'.format(unit.position))            #   (161.5, 21.5)
                print('\n COMMANDCENTER positionTYPE: {}'.format(type(unit.position)))  #   <class 'sc2.position.Point2'>
                for SD in self.units(SUPPLYDEPOT): 
                    print('\n SD position: {}'.format(SD.position))                                                     #   (157.0, 25.0)
                    print('\n position between CC and SP: {}'.format(unit.distance_to(SD.position)))                    #   5.70087712549569
                    print('\n TYPE of - position between CC and SP: {}'.format(type(unit.distance_to(SD.position))))    #   <class 'float'>

                
            

            # print('\n\t What is near = ... :', type(SD.first.position.towards(self.game_info.map_center, 6)))   #   <class 'sc2.position.Point2'>
            # print('\n\t near = ... TYPE:', SD.first.position.towards(self.game_info.map_center, 6))             #   (156.8629821582119, 25.30763253675283)
            print('\n\t MAP : ', self.game_info)                            #   <sc2.game_info.GameInfo object at 0x105f179e8>
            print('\n\t MAP TYPE: ', type(self.game_info))                  #   <class 'sc2.game_info.GameInfo'>
            print('\n\t MAP SIZE: ', self.game_info.map_size)               #   (200, 176)
            print('\n\t MAP SIZE TYPE: ', type(self.game_info.map_size))    #   <class 'sc2.position.Size'>
            print('\n\t MAP CENTER: ', self.game_info.map_center)           #   (100.0, 72.0)
            print('\n\t MAP CENTER TYPE: ', type(self.game_info.map_center))#   <class 'sc2.position.Point2'>

############################################################################################


run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, NN()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)