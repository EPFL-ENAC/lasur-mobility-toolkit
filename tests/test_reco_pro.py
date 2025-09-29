import pytest
from typo_modal.service import TypoModalService, load_data

@pytest.fixture
def service():
  od_mm, orig_dess, dest_dess, can_df = load_data()
  return TypoModalService(od_mm, orig_dess, dest_dess, can_df)

def test_compute_reco_pro_h3(service):
  freq_mod_pro_journeys = [
    {
        "days": 1,
        "mode": "plane",
        "hex_id": "81397ffffffffff"
      },
      {
        "days": 1,
        "mode": "plane",
        "hex_id": "81393ffffffffff"
      },
      {
        "days": 2,
        "mode": "car",
        "hex_id": "821fa7fffffffff"
      },
      {
        "days": 2,
        "mode": "car",
        "hex_id": "821f4ffffffffff"
      },
      {
        "days": 5,
        "mode": "walking",
        "hex_id": "851f9103fffffff"
      },
      {
        "days": 5,
        "mode": "boat",
        "hex_id": "851f8e87fffffff"
      },
      {
        "days": 5,
        "mode": "moto",
        "hex_id": "851f8e87fffffff"
      },
      {
        "days": 6,
        "mode": "car",
        "hex_id": "851f91affffffff"
      },
      {
        "days": 6,
        "mode": "car",
        "hex_id": "851f91b7fffffff"
      },
      {
        "days": 7,
        "mode": "car",
        "hex_id": "851f91abfffffff"
      },
      {
        "days": 7,
        "mode": "car",
        "hex_id": "851f8e87fffffff"
      },
      {
        "days": 7,
        "mode": "car",
        "hex_id": "851f9cdbfffffff"
      },
      {
        "days": 8,
        "mode": "car",
        "hex_id": "851f8343fffffff"
      },
      {
        "days": 8,
        "mode": "car",
        "hex_id": "851f9917fffffff"
      },
      {
        "days": 9,
        "mode": "plane",
        "hex_id": "851f9917fffffff"
      }
    ]

  result = service.compute_reco_pro_h3(scores={"velo":55, "tpu":55, "train":55, "elec":55},
                                       freq_mod_pro_journeys=freq_mod_pro_journeys,
                                       d_lat=46.25, d_lon=6.15)
  assert result == ['train','avoid','train','avoid','walking','boat','elec_moto','bike','train','pub','elec','train','train','elec','elec']

def test_compute_reco_pro_h3_1trip(service):
  result = service.compute_reco_pro_h3(scores={"velo":55, "tpu":55, "train":55, "elec":55},
                                       freq_mod_pro_journeys=[{"days": 2, "mode": "car", "hex_id": "821fa7fffffffff"},],
                                       d_lat=46.25, d_lon=6.15)
  assert result == ["train"]

def test_compute_reco_pro_h3_0trip(service):
  result = service.compute_reco_pro_h3(scores={"velo":50, "tpu":50, "train":50, "elec":50},
                                       freq_mod_pro_journeys=[],
                                       d_lat=46.25, d_lon=6.15)
  assert result == []

def test_compute_reco_pro_local_null(service):
  result = service.compute_reco_pro(
    scores={"velo":50, "tpu":50, "train":50, "elec":50},
    pro_loc=True, pro_reg=True, pro_int=True,
    fm_pro_loc_voit=0, fm_pro_loc_moto=0, fm_pro_loc_tpu=0, fm_pro_loc_train=0, fm_pro_loc_velo=0, fm_pro_loc_marc=0,
    fm_pro_reg_voit=0, fm_pro_reg_moto=0, fm_pro_reg_train=0, fm_pro_reg_avio=0,
    fm_pro_int_voit=0, fm_pro_int_train=0, fm_pro_int_avio=0
  )
  assert result == ("", "", "")

def test_compute_reco_pro_local_velo(service):
  result = service.compute_reco_pro(
    scores={"velo":60, "tpu":40, "train":30, "elec":20},
    pro_loc=True, pro_reg=False, pro_int=False,
    fm_pro_loc_voit=2, fm_pro_loc_moto=2, fm_pro_loc_tpu=2, fm_pro_loc_train=2, fm_pro_loc_velo=2, fm_pro_loc_marc=0,
    fm_pro_reg_voit=0, fm_pro_reg_moto=0, fm_pro_reg_train=0, fm_pro_reg_avio=0,
    fm_pro_int_voit=0, fm_pro_int_train=0, fm_pro_int_avio=0
  )
  assert result == ("velo", "", "")

def test_compute_reco_pro_local_tpu(service):
  result = service.compute_reco_pro(
    scores={"velo":40, "tpu":70, "train":40, "elec":40},
    pro_loc=True, pro_reg=False, pro_int=False,
    fm_pro_loc_voit=2, fm_pro_loc_moto=2, fm_pro_loc_tpu=2, fm_pro_loc_train=2, fm_pro_loc_velo=2, fm_pro_loc_marc=0,
    fm_pro_reg_voit=0, fm_pro_reg_moto=0, fm_pro_reg_train=0, fm_pro_reg_avio=0,
    fm_pro_int_voit=0, fm_pro_int_train=0, fm_pro_int_avio=0
  )
  assert result == ("tpu", "", "")

def test_compute_reco_pro_local_train(service):
  result = service.compute_reco_pro(
    scores={"velo":40, "tpu":40, "train":70, "elec":40},
    pro_loc=True, pro_reg=False, pro_int=False,
    fm_pro_loc_voit=2, fm_pro_loc_moto=2, fm_pro_loc_tpu=2, fm_pro_loc_train=2, fm_pro_loc_velo=2, fm_pro_loc_marc=0,
    fm_pro_reg_voit=0, fm_pro_reg_moto=0, fm_pro_reg_train=0, fm_pro_reg_avio=0,
    fm_pro_int_voit=0, fm_pro_int_train=0, fm_pro_int_avio=0
  )
  assert result == ("train", "", "")

def test_compute_reco_pro_local_elec(service):
  result = service.compute_reco_pro(
    scores={"velo":40, "tpu":40, "train":40, "elec":70},
    pro_loc=True, pro_reg=False, pro_int=False,
    fm_pro_loc_voit=2, fm_pro_loc_moto=2, fm_pro_loc_tpu=2, fm_pro_loc_train=2, fm_pro_loc_velo=2, fm_pro_loc_marc=0,
    fm_pro_reg_voit=0, fm_pro_reg_moto=0, fm_pro_reg_train=0, fm_pro_reg_avio=0,
    fm_pro_int_voit=0, fm_pro_int_train=0, fm_pro_int_avio=0
  )
  assert result == ("elec", "", "")

def test_compute_reco_pro_regional_train(service):
  result = service.compute_reco_pro(
    scores={"velo":40, "tpu":40, "train":60, "elec":20},
    pro_loc=False, pro_reg=True, pro_int=False,
    fm_pro_loc_voit=0, fm_pro_loc_moto=0, fm_pro_loc_tpu=0, fm_pro_loc_train=0, fm_pro_loc_velo=0, fm_pro_loc_marc=0,
    fm_pro_reg_voit=1, fm_pro_reg_moto=1, fm_pro_reg_train=1, fm_pro_reg_avio=0,
    fm_pro_int_voit=0, fm_pro_int_train=0, fm_pro_int_avio=0
  )
  assert result == ("", "train", "")

def test_compute_reco_pro_regional_elec(service):
  result = service.compute_reco_pro(
    scores={"velo":40, "tpu":40, "train":20, "elec":60},
    pro_loc=False, pro_reg=True, pro_int=False,
    fm_pro_loc_voit=0, fm_pro_loc_moto=0, fm_pro_loc_tpu=0, fm_pro_loc_train=0, fm_pro_loc_velo=0, fm_pro_loc_marc=0,
    fm_pro_reg_voit=1, fm_pro_reg_moto=1, fm_pro_reg_train=1, fm_pro_reg_avio=0,
    fm_pro_int_voit=0, fm_pro_int_train=0, fm_pro_int_avio=0
  )
  assert result == ("", "elec", "")

def test_compute_reco_pro_international_train(service):
  result = service.compute_reco_pro(
    scores={"velo":40, "tpu":40, "train":60, "elec":20},
    pro_loc=False, pro_reg=False, pro_int=True,
    fm_pro_loc_voit=0, fm_pro_loc_moto=0, fm_pro_loc_tpu=0, fm_pro_loc_train=0, fm_pro_loc_velo=0, fm_pro_loc_marc=0,
    fm_pro_reg_voit=0, fm_pro_reg_moto=0, fm_pro_reg_train=0, fm_pro_reg_avio=0,
    fm_pro_int_voit=1, fm_pro_int_train=1, fm_pro_int_avio=1
  )
  assert result == ("", "", "train")

def test_compute_reco_pro_international_elec(service):
  result = service.compute_reco_pro(
    scores={"velo":40, "tpu":40, "train":20, "elec":60},
    pro_loc=False, pro_reg=False, pro_int=True,
    fm_pro_loc_voit=0, fm_pro_loc_moto=0, fm_pro_loc_tpu=0, fm_pro_loc_train=0, fm_pro_loc_velo=0, fm_pro_loc_marc=0,
    fm_pro_reg_voit=0, fm_pro_reg_moto=0, fm_pro_reg_train=0, fm_pro_reg_avio=0,
    fm_pro_int_voit=1, fm_pro_int_train=1, fm_pro_int_avio=1
  )
  assert result == ("", "", "train")

def test_compute_reco_pro_no_recommendation(service):
  result = service.compute_reco_pro(
    scores={"velo":20, "tpu":20, "train":20, "elec":20},
    pro_loc=True, pro_reg=True, pro_int=True,
    fm_pro_loc_voit=1, fm_pro_loc_moto=1, fm_pro_loc_tpu=1, fm_pro_loc_train=1, fm_pro_loc_velo=1, fm_pro_loc_marc=1,
    fm_pro_reg_voit=1, fm_pro_reg_moto=1, fm_pro_reg_train=1, fm_pro_reg_avio=1,
    fm_pro_int_voit=1, fm_pro_int_train=0, fm_pro_int_avio=1
  )
  assert result == ("", "", "")