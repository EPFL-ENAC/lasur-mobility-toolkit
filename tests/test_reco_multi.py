import pytest
from typo_modal.service import TypoModalService, load_data

@pytest.fixture
def service():
  od_mm, orig_dess, dest_dess = load_data()
  return TypoModalService(od_mm, orig_dess, dest_dess)

def test_compute_reco_dt_case_1(service):
  t_traj_mm = {'t_tp': 20, 't_velo': 10, 'oid': 2795, 'did': 367}
  reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 5, 5, 5, 5, 5, 5, 5)
  assert reco_dt2 == ['tpu','velo'] # 
  # reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 5, 5, 5, 5, 5, 5, 5)
  # assert reco_dt2 == ['tpu','velo'] #

def test_compute_reco_dt_case_2(service):
  t_traj_mm = {'t_tp': 20, 't_velo': 10, 'oid': 2795, 'did': 367}
  reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 5, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1)
  # reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1)
  assert reco_dt2 == ['tpu','train'] 

def test_compute_reco_dt_case_3(service):
  t_traj_mm = {'t_tp': 30, 't_velo': 35, 'oid': 2795, 'did': 367}
  reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 20, [], 5, 0, 0, 0, 0, 0, 0, 5, 1, 1, 1, 5, 5, 5, 3, 5, 3, 5, 1, 3)
  # reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3)
  assert reco_dt2 == ['vae','elec'] 

def test_compute_reco_dt_case_4(service):
  t_traj_mm = {'t_tp': 20, 't_velo': 5, 'oid': 2795, 'did': 367}
  reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 3, 0, 0, 0, 1, 1, 0, 1, 1, 1, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4)
  # reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 4, 4, 4, 4, 4, 4, 4)
  assert reco_dt2 == ['marche','velo'] 

def test_compute_reco_dt_case_5(service):
  t_traj_mm = {'t_tp': 20, 't_velo': 10, 'oid': 2795, 'did': 367}
  reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, ["dependent","heavy","night","disabled"], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 2, 2, 2, 2, 2, 2, 2)
  reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, ["dependent","heavy","night","disabled"], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 2, 2, 2, 2, 2, 2, 2)
  assert reco_dt2 == ['covoit','elec'] 

def test_compute_reco_dt_case_6(service):
  t_traj_mm = {'t_tp': 10, 't_velo': 5, 'oid': 2795, 'did': 367}
  reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 4, 4, 4, 4, 4, 4, 4)
  # reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, ["disabled"], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 4, 4, 4, 4, 4, 4, 4)
  print(reco_dt2)
  assert reco_dt2 == ['marche','tpu'] 

def test_compute_reco_dt_case_7(service):
  t_traj_mm = {'t_tp': 20, 't_velo': 30, 'oid': 2760, 'did': 367}
  reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 2, 0, 0, 2, 0, 0, 1, 3, 1, 1, 3, 1, 1, 2, 2, 2, 2, 2, 2, 2)
  # reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, ["heavy"], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 2, 2, 2, 2, 2, 2, 2)
  print(reco_dt2)
  assert reco_dt2 == ['inter','vae'] 

def test_compute_reco_dt_case_8(service):
  t_traj_mm = {'t_tp': 20, 't_velo': 10, 'oid': 2795, 'did': 367}
  reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, ["dependent"], 5, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1)
  # reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1)
  assert reco_dt2 == ['elec','tpu'] 

def test_compute_reco_dt_case_9(service):
  t_traj_mm = {'t_tp': 30, 't_velo': 35, 'oid': 2795, 'did': 367}
  reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 20, ["heavy"], 5, 0, 0, 0, 0, 0, 0, 5, 1, 1, 1, 5, 5, 5, 3, 5, 3, 5, 1, 3)
  # reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm, 15, [], 5, 0, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3)
  assert reco_dt2 == ['elec','covoit'] 

# reco_dt2, scores, access = service.compute_reco_multi(t_traj_mm = {'t_tim': 15, 't_tp': 30, 't_velo': 30, 'oid': 100, 'did': 100}, 
#                                               tps_traj = 20, 
#                                               constraints = [], #'night'
#                                               fm_dt_voit = 3, 
#                                               fm_dt_moto = 0, 
#                                               fm_dt_tpu = 1, 
#                                               fm_dt_train = 0, 
#                                               fm_dt_velo = 1, 
#                                               fm_dt_march = 0,
#                                               fm_dt_inter = 1,
#                                               a_voit = 4, 
#                                               a_moto = 2, 
#                                               a_tpu = 3, 
#                                               a_train = 3, 
#                                               a_velo = 3, 
#                                               a_marc = 1, 
#                                               i_tmps = 3, 
#                                               i_prix = 3, 
#                                               i_flex = 3, 
#                                               i_conf = 3, 
#                                               i_fiab = 3, 
#                                               i_prof = 3, 
#                                               i_envi = 3)