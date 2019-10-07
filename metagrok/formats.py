import random
import os
_FIXED_SEED_PKMN = ']'.join([
  'Volbeat||leftovers|H|tailwind,substitute,thunderwave,bugbuzz||81,,85,85,85,85||,0,,,,||83|',
  'Pangoro||choiceband|1|gunkshot,superpower,knockoff,icepunch||85,85,85,85,85,85||||79|',
  'Serperior||leftovers|H|substitute,hiddenpowerfire,leafstorm,leechseed||85,,85,85,85,85||,0,,,,||77|',
  'Conkeldurr||flameorb||bulkup,icepunch,machpunch,drainpunch||85,85,85,85,85,85||||76|',
  'Starmie||leftovers|1|thunderbolt,rapidspin,recover,scald||85,85,85,85,85,85||||77|',
  'Carbink||custapberry|H|stealthrock,explosion,lightscreen,powergem||85,85,85,85,85,85||||83|',
])

_ZOROARKS_PKMN = ']'.join([
  'Zoroark||leftovers|0|nastyplot,knockoff,focusblast,flamethrower||85,85,85,85,85,85||||78|',
  'Pangoro||choiceband|1|gunkshot,superpower,knockoff,icepunch||85,85,85,85,85,85||||79|',
  'Serperior||leftovers|H|substitute,hiddenpowerfire,leafstorm,leechseed||85,,85,85,85,85||,0,,,,||77|',
  'Conkeldurr||flameorb||bulkup,icepunch,machpunch,drainpunch||85,85,85,85,85,85||||76|',
  'Starmie||leftovers|1|thunderbolt,rapidspin,recover,scald||85,85,85,85,85,85||||77|',
  'Carbink||custapberry|H|stealthrock,explosion,lightscreen,powergem||85,85,85,85,85,85||||83|',
])

def _1_coverage(level = ''):
  return ']'.join([
    'Mimikyu||lifeorb||swordsdance,shadowclaw,shadowsneak,playrough|Jolly|,252,,,4,252||||%s|' % level,
    'Medicham-Mega||medichamite||icepunch,firepunch,poweruppunch,zenheadbutt|Jolly|,252,,,4,252||||%s|' % level,
    'Garchomp||leftovers|H|crunch,dragonclaw,firefang,earthquake|Jolly|,252,,,4,252||||%s|' % level,
    'Volcarona||buginiumz||quiverdance,bugbuzz,fierydance,uturn|Modest|,,,252,4,252||||%s|' % level,
    'Toxapex||leftovers||toxicspikes,recover,scald,poisonjab|Impish|252,4,252,,,||||%s|' % level,
    'Magnezone||airballoon||flashcannon,thunderbolt,hiddenpowerfire,toxic|Bold|248,,252,8,,||,0,,,,||%s|' % level,
  ])

def _2_psyspam(level = ''):
  return ']'.join([
    'Alakazam-Mega||alakazite|magicguard|psychic,focusblast,shadowball,hiddenpowerfire|Timid|,,,252,4,252||,0,,,,||%s|' % level,
    'Tapu Lele||psychiumz||calmmind,psyshock,moonblast,hiddenpowerfire|Timid|,,,252,4,252||,0,,,,||%s|' % level,
    'Kartana||choicescarf||leafblade,knockoff,sacredsword,defog|Jolly|,252,4,,,252||||%s|' % level,
    'Greninja-Ash||choicespecs||spikes,watershuriken,hydropump,darkpulse|Timid|,,,252,4,252||||%s|' % level,
    'Landorus-Therian||rockyhelmet||stealthrock,earthquake,hiddenpowerice,uturn|Impish|248,,200,,,60||,30,30,,,||%s|' % level,
    'Magearna||assaultvest||fleurcannon,ironhead,hiddenpowerfire,voltswitch|Sassy|248,,52,,208,||,,,,,20||%s|' % level,
  ])

def _3_trickroom(level = ''):
  return ']'.join([
    'Marowak-Alola||thickclub|H|shadowbone,flareblitz,swordsdance,bonemerang|Adamant|248,252,,,8,||,,,,,0||%s|' % level,
    'Cresselia||mentalherb||trickroom,icebeam,moonlight,lunardance|Relaxed|248,,252,,8,||,0,,,,0||%s|' % level,
    'Mawile||mawilite||playrough,suckerpunch,thunderpunch,firefang|Adamant|248,252,,,8,||,,,,,0||%s|' % level,
    'Uxie||mentalherb||trickroom,stealthrock,memento,magiccoat|Bold|252,,116,,140,||,0,,,,0||%s|' % level,
    'Crawdaunt||lifeorb|H|knockoff,crabhammer,aquajet,swordsdance|Adamant|252,252,,,4,||,,,,,0||%s|' % level,
    'Magearna||fairiumz||trickroom,fleurcannon,focusblast,thunderbolt|Quiet|252,,,252,4,||,0,,,,0||%s|' % level,
  ])

stat = {"HP":0, "Atk":1, "Def":2, "SpA":3,"SpD":4, "Spe":5}
def parse_file(file,max_level = 100):
  newline = ""
  with open(file) as teamfile:
    team = []
    for i in range (0, 6):
      #LINE 1: Name
      #TODO: Handle Nicknames
      gender = ""
      while newline.strip() == "":
        newline = teamfile.readline()
      name = newline.split(" @ ")[0].strip()
      if "(M)" in name:
          gender = "M"
          name = name.split("(M)")[0].strip()
      if "(F)" in name:
          gender = "F"
          name = name.split("(F)")[0].strip()
      item = newline.split(" @ ")[1].strip()
      #LINE 2: Ability
      abilityline = teamfile.readline()
      ability = abilityline.split(": ")[1].strip()
      #LINE 3: Level
      newline = teamfile.readline()
      if "Level" in newline:
        level = max(int(newline.split(": ")[1].strip()), max_level)
        newline = teamfile.readline()
      else:
        level = max_level
      #LINE 4: EVs
      #EVs: 156 Def / 116 SpA / 236 Spe
      evs = newline.split(": ")[1].strip()
      ev_arr = [0, 0, 0, 0, 0, 0]
      for i in evs.split(" / "):
        ev_split = i.split(" ")
        ev_num = int(ev_split[0])
        ev_arr[stat[ev_split[1]]] = ev_num
      newline = teamfile.readline()
      #LINE 6: NATURE
      nature = newline.split(" ")[0].strip()
      newline = teamfile.readline()
      iv_arr = [0, 0, 0, 0, 0, 0]
      if newline[0:3] == "IVs":
        #LINE 5? IVs?
        ivs = newline.split(": ")[1].strip()
        iv_arr = [0, 0, 0, 0, 0, 0]
        for i in ivs.split(" / "):
          iv_split = i.split(" ")
          iv_num = int(iv_split[0])
          iv_arr[stat[iv_split[1]]] = iv_num
        newline = teamfile.readline()
      #LINES 7-10: MOVES?
      moves = []
      while newline[0:2] == "- ":
        moves.append(newline[2:].strip())
        newline = teamfile.readline()
      #print('Magearna||fairiumz||trickroom,fleurcannon,focusblast,thunderbolt|Quiet|252,,,252,4,||,0,,,,0||%s|')
      item = item.replace(" ", "").replace("-", "").lower()
      moves = ",".join([move.replace(" ", "").replace("-", "").replace("[", "").replace("]", "").lower() for move in moves])
      ev_arr = ",".join([str(i) if i > 0 else "" for i in ev_arr])
      iv_arr = ",".join([str(i) if i > 0 else "" for i in iv_arr])
      team.append("{}||{}|{}|{}|{}|{}||{}|{}|{}|".format(name,item, ability, moves, nature, ev_arr, iv_arr,gender,level))
      print(team[-1])
    return "]".join(team)
ou_teams = []
team_path = "metagrok/teams/ou"
for file in os.listdir(team_path):
    if ".txt" in file:
        ou_teams.append(parse_file(os.path.join(team_path,file)))
        print("")
sys.exit(1)
print("done loading ou teams")
_MATRIX_GRID_TEAMS = {1: _1_coverage(), 2: _2_psyspam(), 3: _3_trickroom()}

_NAME_TO_OPTIONS = dict(
  gen7randombattle = dict(
    formatid = 'gen7randombattle',
    p1 = {'name': 'p1'},
    p2 = {'name': 'p2'},
  ),
  gen7fixedseed01abcdef = dict(
    formatid = '',
    p1 = {'name': 'p1', 'team': _FIXED_SEED_PKMN},
    p2 = {'name': 'p2', 'team': _FIXED_SEED_PKMN},
  ),
  gen7zoroarks = dict(
    formatid = '',
    p1 = {'name': 'p1', 'team': _ZOROARKS_PKMN},
    p2 = {'name': 'p2', 'team': _ZOROARKS_PKMN},
  ),
  gen7matrix = dict(
    formatid = 'gen7ou',
    p1 = lambda: random_matrix_team('p1'),
    p2 = lambda: random_matrix_team('p2'),
  ),
)

for i in [1, 2, 3]:
  for j in [1, 2, 3]:
    _NAME_TO_OPTIONS['gen7ouc{}v{}'.format(i, j)] = dict(
      formatid = 'gen7ou',
      p1 = {'name': 'p1', 'team': _MATRIX_GRID_TEAMS[i]},
      p2 = {'name': 'p2', 'team': _MATRIX_GRID_TEAMS[j]},
    )

def get_teams(p1_ind, p2_ind):
  #Used for initial team matchup experiments.
  team_1 = ou_teams[p1_ind]
  team_2 = ou_teams[p2_ind]
  return dict(
        formatid="gen7ou",
        p1= {'name': 'p1', 'team': team_1},
        p2 = {'name': 'p2', 'team': team_2},
    )





def _make_fixed_team_p1_meta(p1_team):
  return dict(
    formatid = 'gen7ou',
    p1 = {'name': 'p1', 'team': p1_team},
    p2 = {'name': 'p2'},
  )

_NAME_TO_OPTIONS['gen7c1'] = _make_fixed_team_p1_meta(_1_coverage(81))
_NAME_TO_OPTIONS['gen7c2'] = _make_fixed_team_p1_meta(_2_psyspam(81))
_NAME_TO_OPTIONS['gen7c3'] = _make_fixed_team_p1_meta(_3_trickroom(81))

_pfx_to_team = dict(
  gen7c1 = _1_coverage,
  gen7c2 = _2_psyspam,
  gen7c3 = _3_trickroom,
)

def get(name):
  name = name.lower()
  if ':' in name:
    pfx, level = name.split(':')
    team_ctor = _pfx_to_team[pfx]
    return _make_fixed_team_p1_meta(team_ctor(int(level)))

  fmt = _NAME_TO_OPTIONS[name]
  rv = {}
  for k, v in fmt.items():
    if callable(v):
      v = v()
    rv[k] = v
  return rv

def random_matrix_team(name):
  rv = {'name': name}
  rv['team'] = random.choice(list(_MATRIX_GRID_TEAMS.values()))
  return rv

def default():
  return get('gen7zzzzz')

def all():
  return list(_NAME_TO_OPTIONS.keys())
