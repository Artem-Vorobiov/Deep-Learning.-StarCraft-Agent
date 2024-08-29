# A StarCraft II API Client for Python 3

This is library for writing AI Bots for StarCraft II in Python 3. 

Documentation is in [the Wiki](https://github.com/Dentosal/python-sc2/wiki).


## Installation

You'll need Python 3.6 or newer.

```
pip3 install --user --upgrade sc2
```

You can see latest released versions from [tags page](https://github.com/Dentosal/python-sc2/tags).

You'll  need an StarCraft II executable. If you are running Windows or macOS, just install the normal SC2 from blizzard app. [The free starter edition works too.](https://us.battle.net/account/sc2/starter-edition/). Linux users get the best experience by installing the Windows version of StarCraft II with [Wine](https://www.winehq.org). Linux user can also use the [Linux binary](https://github.com/Blizzard/s2client-proto#downloads), but it's headless so you cannot actually see the game.

You probably want some maps too. Official map downloads are available from [Blizzard/s2client-proto](https://github.com/Blizzard/s2client-proto#downloads). Notice: the map files are to be extracted into *subdirectories* of the `install-dir/Maps` directory.

### Running

After installing the library, a StarCraft II executable, and some maps, you're ready to get started. Simple bot that follows my strategy you can check it out.

```
python3.6 Terran_AI-master/20_3_predicting.py
```
1. Collect the games required to train the neural network (NN). At the end of the file, it counts the number of games that will be run one after another.
2. After the games are collected, run the file 18_keras.py to train your model.
3. Evaluate your model. If needed, collect more games with 20_3_predicting.py or tune the hyperparameters.
4. Run 20_3_predicting.py with the uploaded model and observe your model fighting against the computer agent.

### Conclusion

Last version is   `Terran_AI-master/20_3_predicting.py` we'll be calling it *A*. The second to last version is `Terran_AI-master/20_2_predicting.py` we'll be calling it *B*. The *B* played 92 games and got 25% accuracy. Then I've trained another model based on these 92 games and old model. So, now I'm going to play 92 games with new model and check what accuracy I'll get.
