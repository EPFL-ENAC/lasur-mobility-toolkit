from typing import List
import os
import json
import random
import pandas as pd
import geopandas as gpd
from importlib import resources
from typo_modal.service import TypoModalService, load_data

# load precomputed geo data
od_mm, orig_dess, dest_dess = load_data()

def setup():
  user_file = os.path.join(os.path.dirname(os.path.abspath("__file__")), 'tests/data', 'user_input.json')
  user_input = None
  with open(user_file) as f:
    user_input = json.load(f)
  
  empl_file = os.path.join(os.path.dirname(os.path.abspath("__file__")), 'tests/data', 'empl_input.json')
  empl_input = None
  with open(empl_file) as f:
    empl_input = json.load(f)
  
  input_file = os.path.join(os.path.dirname(os.path.abspath("__file__")), 'tests/data', 'input_params.json')
  input_params = None
  with open(input_file) as f:
    input_params = json.load(f)
    
  frontend_file = os.path.join(os.path.dirname(os.path.abspath("__file__")), 'tests/data', 'input_frontend.json')
  input_frontend = None
  with open(frontend_file) as f:
    input_frontend = json.load(f)
  
  file_path = resources.files('tests.data') / 'test_pts.parquet'
  with file_path.open('rb') as f:
    test_pts = gpd.read_parquet(f)
  
  return user_input, empl_input, input_params, input_frontend, test_pts

def random_input_params(data):
  constraints = ["dependent","heavy","night","disabled"]
  tps_traj = 60 + random.randint(-30, 30)#data["prelim"]["tps_traj"]
  tx_trav = 6-random.randint(0, 2)#data["prelim"]["tx_trav"]
  tx_tele = random.randint(0, 2)#data["prelim"]["tx_tele"]
  tx_pres = tx_trav-tx_tele
  fr_pro_loc = random.randint(0,12)
  fr_pro_reg = random.randint(0,8)
  fr_pro_int = random.randint(0,4)
  fm_pro_loc_voit = data["freq_trav_pro_inter"]
  fm_pro_loc_moto = data["freq_trav_pro_inter"]
  fm_pro_loc_tpu = data["freq_trav_pro_inter"]
  fm_pro_loc_train = data["freq_trav_pro_inter"]
  fm_pro_loc_velo = data["freq_trav_pro_inter"]
  fm_pro_loc_marc = data["freq_trav_pro_inter"]
  fm_pro_reg_voit = data["freq_trav_pro_inter"]
  fm_pro_reg_moto = data["freq_trav_pro_inter"]
  fm_pro_reg_train = data["freq_trav_pro_inter"]
  fm_pro_reg_avio = data["freq_trav_pro_inter"]
  fm_pro_int_voit = data["freq_trav_pro_inter"]
  fm_pro_int_train = data["freq_trav_pro_inter"]
  fm_pro_int_avio = data["freq_trav_pro_inter"]
  return constraints, tps_traj, tx_trav, tx_tele, fr_pro_loc, fr_pro_reg, fr_pro_int,fm_pro_loc_voit, fm_pro_loc_moto, fm_pro_loc_tpu, fm_pro_loc_train, fm_pro_loc_velo, fm_pro_loc_marc, fm_pro_reg_voit, fm_pro_reg_moto, fm_pro_reg_train, fm_pro_reg_avio,fm_pro_int_voit, fm_pro_int_train, fm_pro_int_avio

def read_input_frontend(data):
  input_params={}
  input_params["constraints"] = data["constraints"]
  input_params["tps_traj"] = data["travel_time"]
  input_params["tx_trav"] = data["employment_rate"]
  input_params["tx_tele"] = data["remote_work_rate"]
  input_params["fm_dt_voit"] = data["freq_mod_car"]
  input_params["fm_dt_moto"] = data["freq_mod_moto"]
  input_params["fm_dt_tpu"] = data["freq_mod_pub"]
  input_params["fm_dt_train"] = data["freq_mod_train"]
  input_params["fm_dt_velo"] = data["freq_mod_bike"]
  input_params["fm_dt_march"] = data["freq_mod_walking"]
  input_params["fm_dt_inter"] = int(data['freq_mod_combined']==True)
  input_params["fr_pro_loc"] = data["freq_trav_pro_local"]
  input_params["fr_pro_reg"] = data["freq_trav_pro_region"]
  input_params["fr_pro_int"] = data["freq_trav_pro_inter"]
  input_params["fm_pro_loc_voit"] = data["freq_mod_pro_local_car"]
  input_params["fm_pro_loc_moto"] = data["freq_mod_pro_local_moto"]
  input_params["fm_pro_loc_tpu"] = data["freq_mod_pro_local_pub"]
  input_params["fm_pro_loc_train"] = data["freq_mod_pro_local_train"]
  input_params["fm_pro_loc_velo"] = data["freq_mod_pro_local_bike"]
  input_params["fm_pro_loc_marc"] = data["freq_mod_pro_local_walking"]
  input_params["fm_pro_reg_voit"] = data["freq_mod_pro_region_car"]
  input_params["fm_pro_reg_moto"] = data["freq_mod_pro_region_moto"]
  input_params["fm_pro_reg_train"] = data["freq_mod_pro_region_train"]
  input_params["fm_pro_reg_avio"] = data["freq_mod_pro_region_plane"]
  input_params["fm_pro_int_voit"] = data["freq_mod_pro_inter_car"]
  input_params["fm_pro_int_train"] = data["freq_mod_pro_inter_train"]
  input_params["fm_pro_int_avio"] = data["freq_mod_pro_inter_plane"]
  input_params["a_voit"] = data["needs_car"]
  input_params["a_moto"] = data["needs_moto"]
  input_params["a_tpu"] = data["needs_pub"]
  input_params["a_train"] = data["needs_train"]
  input_params["a_marc"] = data["needs_walking"]
  input_params["a_velo"] = data["needs_bike"]
  input_params["i_tmps"] = data["importance_time"]
  input_params["i_prix"] = data["importance_cost"]
  input_params["i_flex"] = data["importance_flex"]
  input_params["i_conf"] = data["importance_comfort"]
  input_params["i_fiab"] = data["importance_rel"]
  input_params["i_prof"] = data["importance_most"]
  input_params["i_envi"] = data["importance_env"]
  input_params["o_lon"] = data["origin"]["lon"]
  input_params["o_lat"] = data["origin"]["lat"]
  input_params["d_lon"] = data["workplace"]["lon"]
  input_params["d_lat"] = data["workplace"]["lat"]
  return input_params#o_lon, o_lat, d_lon, d_lat, tps_traj, tx_trav, tx_tele, fm_dt_voit, fm_dt_moto, fm_dt_tpu, fm_dt_train, fm_dt_velo, fr_pro_loc, fr_pro_reg, fr_pro_int,fm_pro_loc_voit, fm_pro_loc_moto, fm_pro_loc_tpu, fm_pro_loc_train, fm_pro_loc_velo, fm_pro_loc_marc, fm_pro_reg_voit, fm_pro_reg_moto, fm_pro_reg_train, fm_pro_reg_avio,fm_pro_int_voit, fm_pro_int_train, fm_pro_int_avio, a_voit, a_moto, a_tpu, a_train, a_marc, a_velo, i_tmps, i_prix, i_flex, i_conf, i_fiab, i_prof, i_envi

def test_compute_geo():
  user_input, empl_input, input_params, input_frontend, test_pts = setup()
  assert user_input != None, "user_input empty"
  assert empl_input != None, "empl_input empty"
  assert input_params != None, "input_params empty"
  assert input_frontend != None, "input_frontend empty"
  input_params = read_input_frontend(input_frontend['data'])
  service = TypoModalService(od_mm, orig_dess, dest_dess)
  t_traj_mm = service.compute_geo(o_lon = input_params["o_lon"], o_lat = input_params["o_lat"], d_lon = input_params["d_lon"], d_lat = input_params["d_lat"])
  #print(t_traj_mm)
  assert t_traj_mm != None, "no travel time found for these coords"
  assert isinstance(t_traj_mm, dict), "travel time not dict"
  assert t_traj_mm == {'t_tim': 10, 't_tp': 21, 't_velo': 21, 'oid': 2715, 'did': 281}, "wrong travel times"

def test_compute_reco():
  user_input, empl_input, input_params, input_frontend, test_pts = setup()
  input_params = read_input_frontend(input_frontend['data'])
  # print(input_params)
  service = TypoModalService(od_mm, orig_dess, dest_dess)

  t_traj_mm = service.compute_geo(o_lon = input_params["o_lon"], o_lat = input_params["o_lat"], d_lon = input_params["d_lon"], d_lat = input_params["d_lat"])

  reco_dt, scores = service.compute_reco_dt(t_traj_mm,
                                 input_params['tps_traj'],
                                 input_params['tx_trav'],
                                 input_params['tx_tele'],
                                 input_params['fm_dt_voit'],
                                 input_params['fm_dt_moto'],
                                 input_params['fm_dt_tpu'],
                                 input_params['fm_dt_train'],
                                 input_params['fm_dt_velo'], 
                                 input_params['a_voit'],
                                 input_params['a_moto'],
                                 input_params['a_tpu'],
                                 input_params['a_train'],
                                 input_params['a_marc'],
                                 input_params['a_velo'],
                                 input_params['i_tmps'],
                                 input_params['i_prix'],
                                 input_params['i_flex'],
                                 input_params['i_conf'],
                                 input_params['i_fiab'],
                                 input_params['i_prof'],
                                 input_params['i_envi'])
  #print(reco_dt)
  assert reco_dt != None, "reco is none"
  assert isinstance(reco_dt, str) , "reco not a string"
  assert reco_dt == 'tpu', "wrong reco"

  reco_pro_loc, reco_pro_reg, reco_pro_int = service.compute_reco_pro(scores, 
                                                                      input_params['fr_pro_loc'], 
                                                                      input_params['fr_pro_reg'], 
                                                                      input_params['fr_pro_int'], 
                                                                      input_params['fm_pro_loc_voit'], 
                                                                      input_params['fm_pro_loc_moto'], 
                                                                      input_params['fm_pro_loc_tpu'], 
                                                                      input_params['fm_pro_loc_train'], 
                                                                      input_params['fm_pro_loc_velo'], 
                                                                      input_params['fm_pro_loc_marc'], 
                                                                      input_params['fm_pro_reg_voit'], 
                                                                      input_params['fm_pro_reg_moto'], 
                                                                      input_params['fm_pro_reg_train'], 
                                                                      input_params['fm_pro_reg_avio'], 
                                                                      input_params['fm_pro_int_voit'], 
                                                                      input_params['fm_pro_int_train'], 
                                                                      input_params['fm_pro_int_avio'])
  mesure_dt1, mesure_dt2, mesure_pro_loc, mesure_pro_regint = service.compute_mesu_empl(empl_input, reco_dt, reco_pro_loc, reco_pro_reg, reco_pro_int)
  #print(mesure_dt1)
  #print(mesure_dt2)
  print(mesure_pro_loc)
  print(mesure_pro_regint)
  assert mesure_dt1 == "t"
  assert mesure_dt2 == "p"
  assert mesure_pro_loc == ["ebike_fleet"]
  assert mesure_pro_regint == ["train_pro"]

