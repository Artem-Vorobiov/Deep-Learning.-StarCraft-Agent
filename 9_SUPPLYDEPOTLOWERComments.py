import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.ids.ability_id import AbilityId
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT, SUPPLYDEPOTLOWERED, MORPH_SUPPLYDEPOT_LOWER, MORPH_SUPPLYDEPOT_RAISE

###############################################################################################
#   How to affect on Ability using SUPPLYDEPOT as an example
#   How to make up SUPPLYDEPOTLOWERED (UnitTypeId)
#   How to make up MORPH_SUPPLYDEPOT_RAISE (AbilityId)
###############################################################################################


class NN(sc2.BotAI):
    def __init__(self):
        self.ch_time = 0

    async def on_step(self, iteration):
        self.time = (self.state.game_loop/22.4) / 60
        print('Time:',self.time)

        # what to do every step
        await self.distribute_workers()  # in sc2/bot_ai.py
        await self.build_scv()			 # Build our worker who will mine minerals


######################################
        await self.build_supply_depot()
        await self.supplydepot_lower()
######################################


    async def build_scv(self):
    	for cc in self.units(COMMANDCENTER).ready.noqueue:
    		if self.can_afford(SCV) and not self.already_pending(SCV):
    			await self.do(cc.train(SCV))
    			# print('Passed conditions and train - {}'.format(self.do(cc.train(SCV))))



    async def build_supply_depot(self):
        CC = self.units(COMMANDCENTER)

        if self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT) and \
        self.units(SUPPLYDEPOT).amount < 1 and self.units(SUPPLYDEPOTLOWERED).amount < 1:
            await self.build(SUPPLYDEPOT, near = CC.first.position.towards(self.game_info.map_center, 6))
            print('\t\tStart off to BUILD')


    async def supplydepot_lower(self):

######################################
#   First way to affect: using   unit_typeid.py   class UnitTypeId(enum.Enum)
#   self.do(sd.build(SUPPLYDEPOTLOWERED))

        for sd in self.units(SUPPLYDEPOT).ready:
            print('\n ', sd.tag)
            await self.do(sd.build(SUPPLYDEPOTLOWERED))
            self.ch_time = self.time
            print('\n\n\n\n\n\n\n                       LOWED                    \n\n\n\n\n')
######################################


######################################
#   First way to affect: using   ability_id.py   class AbilityId(enum.Enum)

        if self.time > self.ch_time  + 2:
            for depo in self.units(SUPPLYDEPOTLOWERED).ready:
                await self.do(depo(MORPH_SUPPLYDEPOT_RAISE))
                print('\n\n\n\n\n\n\n                   RAISED                    \n\n\n\n\n')
######################################


        # if self.units(SUPPLYDEPOT).ready:
        #     for xxx in self._game_data.abilities.values():
        #         print('\n', xxx)
        #         print('\n', xxx.id)
        #         if xxx.id == AbilityId.MORPH_SUPPLYDEPOT_LOWER:
        #             print('YYeepp...\n\n\n\n')



run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, NN()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=False)