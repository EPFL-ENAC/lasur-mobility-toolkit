import pytest
from typo_modal.service import TypoModalService, load_data

# compute_mesu_empl(self, empl, reco_dt2, reco_pro_loc, reco_pro_reg, reco_pro_int)
epfl = { "id_empl": "EPFL",
  "mesures_globa":["Possibilité de télétravailler au domicile"],
  "mesures_tpu":["Prise en charge abo UNIRESO (TPG)"], 
  "mesures_train":["Prise en charge abo CFF (AG) tout ou en partie",
                "Prise en charge abo CFF (1/2 tarif)"],
  "mesures_inter":[],              
  "mesures_velo":["Mise à disposition de vestiaire et douches",
                "Places de stationnement sécurisé vélo",
                "Possibilité de chargement batterie vélo électrique"],
  "mesures_covoit":["Places de stationnement réservées covoiturage"],
  "mesures_elec":["Bornes de chargement véhicule électrique"],
  "mesures_pro_velo":[],
  "mesures_pro_tpu":["Prise en charge abo UNIRESO (TPG)"],
  "mesures_pro_train":["Prise en charge abo CFF (Abonnement Général)"],
  "mesures_pro_elec":[]
}

modus = { "id_empl": "MODU",
  "mesures_globa":["Possibilité de télétravailler au domicile",
                  "Possibilité de travailler dans un tiers-lieu"],
  "mesures_tpu":["Prise en charge abo UNIRESO (TPG)",
                "Prise en charge abo Léman Pass"], 
  "mesures_train":["Prise en charge abo CFF (1/2 tarif plus)"],
  "mesures_inter":["Prise en charge partielle abo P+R",
                "Prise en charge abo vélostation"],              
  "mesures_velo":["Subvention à l'achat d'un vélo / vélo électrique",
                "Possibilité de chargement batterie vélo électrique",
                "Remboursement d'équipement de sécurité et confort vélo"],
  "mesures_covoit":["Prise en charge des trajets en covoiturage",
                  "Mise en relation covoiturage avec collègues au sein de l'entreprise"],
  "mesures_elec":["Prise en charge abo mobility car-sharing"],
  "mesures_pro_velo":["Flotte de vélos électriques d'entreprise à disposition pour déplacements pro"],
  "mesures_pro_tpu":["Prise en charge abo UNIRESO (TPG)"],
  "mesures_pro_train":["Politique de substitution de l'avion par le train"],
  "mesures_pro_elec":["Véhicules électriques à disposition pour déplacements pro"]
}

@pytest.fixture
def service():
  od_mm, orig_dess, dest_dess = load_data()
  return TypoModalService(od_mm, orig_dess, dest_dess)

def test_mesu_empl_case_1(service):
  reco_dt2 = ['train','vae']
  reco_pro_loc = "velo"
  reco_pro_reg = "train"
  reco_pro_int = "train"
  mesure_dt1, mesure_dt2, mesure_pro_loc, mesure_pro_regint = service.compute_mesu_empl(empl = epfl, reco_dt2 = reco_dt2, reco_pro_loc=reco_pro_loc, reco_pro_reg=reco_pro_reg, reco_pro_int=reco_pro_int)
  assert mesure_dt1 == ['Prise en charge abo CFF (AG) tout ou en partie', 'Prise en charge abo CFF (1/2 tarif)'] # FIXME
  assert mesure_dt2 == ["Mise à disposition de vestiaire et douches",
                "Places de stationnement sécurisé vélo",
                "Possibilité de chargement batterie vélo électrique"]
  assert mesure_pro_loc == []
  assert mesure_pro_regint == ["Prise en charge abo CFF (Abonnement Général)"]

def test_compute_mesu_empl_case_2(service):
  reco_dt2 = ['velo','tpu']
  reco_pro_loc = "tpu"
  reco_pro_reg = "train"
  reco_pro_int = "elec"
  mesure_dt1, mesure_dt2, mesure_pro_loc, mesure_pro_regint = service.compute_mesu_empl(empl = modus, reco_dt2 = reco_dt2, reco_pro_loc=reco_pro_loc, reco_pro_reg=reco_pro_reg, reco_pro_int=reco_pro_int)
  assert mesure_dt1 == ["Subvention à l'achat d'un vélo / vélo électrique",
                "Possibilité de chargement batterie vélo électrique",
                "Remboursement d'équipement de sécurité et confort vélo"]
  assert mesure_dt2 == ["Prise en charge abo UNIRESO (TPG)",
                "Prise en charge abo Léman Pass"]
  assert mesure_pro_loc == ["Prise en charge abo UNIRESO (TPG)"]
  assert mesure_pro_regint == ["Politique de substitution de l'avion par le train"]

def test_mesu_empl_case_3(service):
  reco_dt2 = ['covoit','orga']
  reco_pro_loc = "train"
  reco_pro_reg = "elec"
  reco_pro_int = "train"
  mesure_dt1, mesure_dt2, mesure_pro_loc, mesure_pro_regint = service.compute_mesu_empl(empl = epfl, reco_dt2 = reco_dt2, reco_pro_loc=reco_pro_loc, reco_pro_reg=reco_pro_reg, reco_pro_int=reco_pro_int)
  assert mesure_dt1 == ["Places de stationnement réservées covoiturage"]
  assert mesure_dt2 == ["Possibilité de télétravailler au domicile"]
  assert mesure_pro_loc == ["Prise en charge abo CFF (Abonnement Général)"]
  assert mesure_pro_regint == ["Prise en charge abo CFF (Abonnement Général)"]

def test_compute_mesu_empl_case_4(service):
  reco_dt2 = ['inter','elec']
  reco_pro_loc = "elec"
  reco_pro_reg = "elec"
  reco_pro_int = "elec"
  mesure_dt1, mesure_dt2, mesure_pro_loc, mesure_pro_regint = service.compute_mesu_empl(empl = modus, reco_dt2 = reco_dt2, reco_pro_loc=reco_pro_loc, reco_pro_reg=reco_pro_reg, reco_pro_int=reco_pro_int)
  assert mesure_dt1 == ["Prise en charge partielle abo P+R",
                "Prise en charge abo vélostation"] 
  assert mesure_dt2 == ["Prise en charge abo mobility car-sharing"]
  assert mesure_pro_loc == ["Véhicules électriques à disposition pour déplacements pro"]
  assert mesure_pro_regint == ["Véhicules électriques à disposition pour déplacements pro"]