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
        await self.build_scv()           # Build our worker who will mine minerals
        await self.build_supply_depot()
        await self.build_refinery()
        await self.expand()

    async def expand(self):
        if self.units(COMMANDCENTER).amount < 4:
            if self.can_afford(COMMANDCENTER) and not self.already_pending(COMMANDCENTER):
                print('\n EXPANDING ... ')
                await self.expand_now()


#   ЕСТЬ ПРОБЛЕМА - когда постороено 2 СС выскакивает ошибка касательно строительства REFINERY

#   Specific Architecture for - finding spot and building Geyser
    async def build_refinery(self):
        if self.can_afford(REFINERY) and self.time > 1 and len(self.units(REFINERY)) <= 2 and not self.already_pending(REFINERY):
            for cc in self.units(COMMANDCENTER):
                #   Found Geyser near CommandCenter
                vgs = self.state.vespene_geyser.closer_than(20.0, cc)
                    #   Iterate through Geyser near CC
                for vg in vgs:
                    #   Check If REFINERY already exists on Geyser Spot, If so break
                    if self.units(REFINERY).closer_than(1.0,vg).exists:
                        break
                    #   If not exists, then select worker and use him for building Refinery
                    worker = self.select_build_worker(vg.position)
                    await self.do(worker.build(REFINERY, vg))
                    break


    async def build_scv(self):
        for cc in self.units(COMMANDCENTER).ready.noqueue:
            if self.can_afford(SCV) and not self.already_pending(SCV):
                await self.do(cc.train(SCV))


    async def build_supply_depot(self):
        SD = self.units(COMMANDCENTER)
        if self.supply_used > 0.65*self.supply_cap:
            if self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
                await self.build(SUPPLYDEPOT, near = SD.first.position.towards(self.game_info.map_center, 6))






run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, NN()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)