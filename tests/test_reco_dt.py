# import pytest
# from typo_modal.service import TypoModalService, load_data

# # compute_reco_dt(t_traj_mm, tps_traj, tx_trav, tx_tele, fm_dt_voit, fm_dt_moto, fm_dt_tpu, fm_dt_train, fm_dt_velo, 
# #         a_voit, a_moto, a_tpu, a_train, a_marc, a_velo, i_tmps, i_prix, i_flex, i_conf, i_fiab, i_prof, i_envi)

# # @pytest.fixture
# def service():
#   od_mm, orig_dess, dest_dess = load_data()
#   return TypoModalService(od_mm, orig_dess, dest_dess)

# def test_compute_reco_dt_case_1(service):
#   t_traj_mm = {'t_tp': 20, 't_velo': 10, 'oid': 100, 'did': 100}
#   reco_dt, scores = service.compute_reco_dt(t_traj_mm, 15, 5, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 5, 5, 5, 5, 5, 5, 5)
#   assert reco_dt == 'velo' # FIXME
#   # assert scores == {'velo': 100, 'tpu': 60, 'train': 60, 'covoit': 60, 'elec': 60} # FIXME

# def test_compute_reco_dt_case_2(service):
#   t_traj_mm = {'t_tp': 20, 't_velo': 10, 'oid': 100, 'did': 100}
#   reco_dt, scores = service.compute_reco_dt(t_traj_mm, 15, 5, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 1, 1, 1, 1, 1, 1, 1)
#   assert reco_dt == 'train' # FIXME
#   assert scores == {'velo': 20, 'tpu': 20, 'train': 20, 'covoit': 20, 'elec': 20} # FIXME

# def test_compute_reco_dt_case_3(service):
#   t_traj_mm = {'t_tp': 20, 't_velo': 10, 'oid': 100, 'did': 100}
#   reco_dt, scores = service.compute_reco_dt(t_traj_mm, 15, 5, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3)
#   assert reco_dt == 'inter' # FIXME
#   assert scores == {'velo': 60, 'tpu': 60, 'train': 60, 'covoit': 60, 'elec': 60} # FIXME

# def test_compute_reco_dt_case_4(service):
#   t_traj_mm = {'t_tp': 20, 't_velo': 10, 'oid': 100, 'did': 100}
#   reco_dt, scores = service.compute_reco_dt(t_traj_mm, 15, 5, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4)
#   assert reco_dt == 'elec' # FIXME
#   assert scores == {'velo': 80, 'tpu': 80, 'train': 80, 'covoit': 80, 'elec': 80} # FIXME

# def test_compute_reco_dt_case_5(service):
#   t_traj_mm = {'t_tp': 20, 't_velo': 10, 'oid': 100, 'did': 100}
#   reco_dt, scores = service.compute_reco_dt(t_traj_mm, 15, 5, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2)
#   assert reco_dt == 'orga' # FIXME
#   assert scores == {'velo': 50, 'tpu': 50, 'train': 50, 'covoit': 50, 'elec': 50} # FIXME
