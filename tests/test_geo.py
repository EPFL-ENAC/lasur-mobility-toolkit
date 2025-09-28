import pytest
from typo_modal.service import TypoModalService, load_data

@pytest.fixture
def service():
  od_mm, orig_dess, dest_dess, can_df = load_data()
  return TypoModalService(od_mm, orig_dess, dest_dess, can_df)

def test_compute_geo(service):
  result = service.compute_geo(6.19, 46.32, 6.14, 46.21)#6.11, 46.25 #6.22, 46.20, 6.19, 46.32,
  expected = {
    't_tim': 22,
    't_tp': 29,
    't_velo': 44,
    'oid': 2676,
    'did': 281
  }
  assert result == expected

def test_compute_geo_no_match(service):
  result = service.compute_geo(0.0, 0.0, 0.0, 0.0)
  assert result == {}

def test_compute_geo_different_points(service):
  result = service.compute_geo(6.2, 46.3, 6.4, 46.5)
  expected = {
    't_tim': 52,
    't_tp': 59,
    't_velo': 105,
    'oid': 2680,
    'did': 525
  }
  assert result == expected
