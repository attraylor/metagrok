import argparse
import json
import logging
import math
import os
import textwrap
import random

import gevent

from metagrok import battlelogs
from metagrok import config
from metagrok import formats
from metagrok import torch_policy
from metagrok import utils
from metagrok import mail
from metagrok.pkmn.games import Game
from metagrok.pkmn.engine.player import EnginePkmnPlayer
from metagrok import team_choice

from metagrok import team_generation as tg

def start(args):
  logger = utils.default_logger_setup(logging.INFO)
  logger.info('Writing to ' + args.outdir)

  config.set_cuda(args.cuda)
  p1dir = os.path.join(args.outdir, 'p1')
  p2dir = os.path.join(args.outdir, 'p2')

  utils.mkdir_p(p1dir)
  utils.mkdir_p(p2dir)

  prog = os.path.join(
      config.get('showdown_root'),
      config.get('showdown_server_dir'),
      'pokemon-showdown')

  #game = Game(options = formats.get(args.format), prog = prog)
  policy_1 = torch_policy.load(args.p1)
  policy_2 = torch_policy.load(args.p2)

  wins = [0, 0]

  logger.info('starting...')
  # TODO: make multithreaded. Maybe integrate this with RL experiment
  p1_teams, p2_teams = tg.init_lc_thunderdome()
  strategy_agent = team_choice.AgentStrategyProfile(p1_teams, p2_teams)
  for i in range(args.num_matches):
    #team1_ind = team_choice.teamchoice_random(formats.ou_teams)
    team1_ind = strategy_agent.select_action()
    team2_ind = strategy_agent.select_action_p2()
    game = Game(options = strategy_agent.get_teams(team1_ind, team2_ind), prog = prog)
    p1 = EnginePkmnPlayer(policy_1, '%s-p1' % i,
      play_best_move = args.play_best_move in ['p1', 'both'])
    p2 = EnginePkmnPlayer(policy_2, '%s-p2' % i,
      play_best_move = args.play_best_move in ['p2', 'both'])
    game.play(p1, p2)

    for j in [0, 1]:
      player = [p1, p2][j]
      dirname = [p1dir, p2dir][j]

      bogger = battlelogs.BattleLogger(player.gid, dirname)
      for block in player.blocks:
        bogger.log(block)
      bogger.close()
      if j == 0:
         if player.result == 'winner':
           strategy_agent.update(team1_ind, team2_ind, p1_win=True)
         else:
           strategy_agent.update(team1_ind, team2_ind, p1_win=False)
      if player.result == 'winner':
        wins[j] += 1
      else:
        assert player.result in ['loser', 'tie']
  print(strategy_agent.get_utility_matrix())
  with open("lc_thunderdome_results.txt", "w+") as wf:
	  for ct, team in enumerate(strategy_agent.p1_teams):
		  wf.write("{}\t{}\n".format(ct, team))
	  for ct, team in enumerate(strategy_agent.p2_teams):
		  wf.write("{}\t{}\n".format(ct, team))
	 # wf.write(strategy_agent.get_utility_matrix())
	  wf.write("\n")
	  wf.flush()
	  wf.close()
  return wins

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--p1')
  parser.add_argument('--p2')
  parser.add_argument('--outdir', default = 'data/evals/head2head/%s' % utils.iso_ts())
  parser.add_argument('--num-matches', type = int)
  parser.add_argument('--play-best-move', choices = ['p1', 'p2', 'both'])
  parser.add_argument('--progress-type', choices = ['bar', 'log'], default = 'log')
  parser.add_argument('--format', default = 'gen7randombattle')
  parser.add_argument('--cuda', action = 'store_true')
  return parser.parse_args()

def main():
  args = parse_args()
  utils.mkdir_p(args.outdir)

  params = vars(args)
  params['_format_details'] = formats.get(args.format)
  #print(params['_format_details'])
  #sys.exit(1)


  with open(os.path.join(args.outdir, 'args.json'), 'w') as fd:
    json.dump(params, fd)

  p1wins, p2wins = gevent.spawn(start, parse_args()).get()

  subject = 'head2head evaluation finished: ' + args.outdir
  mean = float(p1wins) / args.num_matches
  print(args.num_matches)
  var = mean * (1. - mean)
  sem = math.sqrt(var / args.num_matches)
  z = (mean - 0.5) / (1e-8 + sem)

  fmt_args = (args.p1, p1wins, args.p2, p2wins, mean, sem, z, json.dumps(params, indent = 2))

  text = textwrap.dedent('''\
  Results:
    p1 (%s) num wins: %s
    p2 (%s) num wins: %s

    mean: %s
    sem: %s
    z-score: %s

  Arguments:
  %s''') % fmt_args
  print(text)
  mail.send(subject, text)

if __name__ == '__main__':
  main()
