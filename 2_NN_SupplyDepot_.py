import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT


class NN(sc2.BotAI):
    async def on_step(self, iteration):
        self.time = (self.state.game_loop/22.4) / 60
        print('Time:',self.time)

        # what to do every step
        await self.distribute_workers()  # in sc2/bot_ai.py
        await self.build_scv()			 # Build our worker who will mine minerals


######################################
        await self.build_supply_depot()
######################################


    async def build_scv(self):
    	for cc in self.units(COMMANDCENTER).ready.noqueue:
    		if self.can_afford(SCV) and not self.already_pending(SCV):
    			await self.do(cc.train(SCV))
    			# print('Passed conditions and train - {}'.format(self.do(cc.train(SCV))))


######################################
    async def build_supply_depot(self):
        SD = self.units(COMMANDCENTER)

        if self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
            await self.build(SUPPLYDEPOT, near = SD.first.position.towards(self.game_info.map_center, 6))
            print('\t\tStart off to BUILD')
######################################



run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, NN()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)