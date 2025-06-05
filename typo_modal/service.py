#import necessary packages
import pandas as pd
import geopandas as gpd
from importlib import resources

def load_data():
  """load precomputed geo data"""
  package_name = 'typo_modal.data'
  file_path = resources.files(package_name) / 'od_mm.parquet'
  with file_path.open('rb') as f:
    od_mm = pd.read_parquet(f)
  file_path = resources.files(package_name) / 'orig_desserte.parquet'
  with file_path.open('rb') as f:
    orig_dess = gpd.read_parquet(f)
  file_path = resources.files(package_name) / 'dest_desserte.parquet'
  with file_path.open('rb') as f:
    dest_dess = gpd.read_parquet(f)
  return od_mm, orig_dess, dest_dess

class TypoModalService:
  
  def __init__(self, od_mm, orig_dess, dest_dess):
    self.od_mm = od_mm
    self.orig_dess = orig_dess
    self.dest_dess = dest_dess
    
  # def filter_nnz_dict(self, pair):
  #   key, value = pair
  #   if value > 0:
  #       return True  # keep pair in the filtered dictionary
  #   else:
  #       return False  # filter pair out of the dictionary
    
  def compute_geo(self, o_lon: float, o_lat: float, d_lon: float, d_lat: float) -> dict:
      """Snaps to nearest origin and destination in OD matrix database.

      Args:
          o_lon (float): Origin longitude
          o_lat (float): Origin latitude
          d_lon (float): Destination longitude
          d_lat (float): Destination latitude

      Returns:
          dict: Origin and destination ids and travel times in tim, tp and velo
      """
      try:
        od_df = pd.DataFrame({"od":['o','d'],"lon":[o_lon,d_lon], "lat":[o_lat,d_lat]})
        od_pt = gpd.GeoDataFrame(od_df, geometry=gpd.points_from_xy(od_df.lon, od_df.lat),crs="4326")
        orig_snap = od_pt.to_crs(2056).sjoin_nearest(self.orig_dess, max_distance = 100000, distance_col = "dist").reset_index().loc[0]
        dest_snap = od_pt.to_crs(2056).sjoin_nearest(self.dest_dess, max_distance = 100000, distance_col = "dist").reset_index().loc[1]
        oid = orig_snap['id_true']
        did = dest_snap['id_true']
        t_traj_mm = self.od_mm.loc[(self.od_mm.orig == oid) & (self.od_mm.dest == did), ['t_tim', 't_tp', 't_velo']].reset_index(drop = True).to_dict(orient='records')[0]
        t_traj_mm['oid'] = int(oid)
        t_traj_mm['did'] = int(did)
        return t_traj_mm
      except:
        # case out of bounds
        return {}   

  def compute_reco_dt(self, t_traj_mm, tps_traj, tx_trav, tx_tele, fm_dt_voit, fm_dt_moto, fm_dt_tpu, fm_dt_train, fm_dt_velo, 
                      a_voit, a_moto, a_tpu, a_train, a_marc, a_velo, i_tmps, i_prix, i_flex, i_conf, i_fiab, i_prof, i_envi):
    """input:frequences modales domicile-travail, attitudes envers modes, importance de differents aspects;
    output: recommandations de mobilite durable pour le deplacement domicile-travail de l'employe.e"""
    sum_importance = i_tmps + i_prix + i_flex + i_conf + i_fiab + i_prof + i_envi
    score_velo = round(20*(i_tmps*1 + i_prix*5 + i_flex*4 + i_conf*1 + i_prof*1 + i_fiab*4 + i_envi*5)/sum_importance)
    score_tpu = round(20*(i_tmps*3 + i_prix*4 + i_flex*2 + i_conf*2 + i_prof*4 + i_fiab*2 + i_envi*4)/sum_importance)
    score_train = round(20*(i_tmps*3 + i_prix*2 + i_flex*2 + i_conf*3 + i_prof*5 + i_fiab*3 + i_envi*3)/sum_importance)
    score_covoit = round(20*(i_tmps*4 + i_prix*3 + i_flex*2 + i_conf*4 + i_prof*4 + i_fiab*2 + i_envi*2)/sum_importance)
    score_elec = round(20*(i_tmps*4 + i_prix*1 + i_flex*5 + i_conf*5 + i_prof*1 + i_fiab*4 + i_envi*1)/sum_importance)
    scores = {'velo':score_velo, 'tpu':score_tpu, 'train':score_train, 'covoit':score_covoit, 'elec':score_elec}
    reco_dt = 'none'

    if a_train >= 3 and score_train>50 and t_traj_mm['t_tp']  <=  2*tps_traj and self.orig_dess.loc[self.orig_dess.id_true == t_traj_mm['oid'], 'train'].values == 1 and self.dest_dess.loc[self.dest_dess.id_true == t_traj_mm['did'], 'train'].values == 1:
      reco_dt = 'train'
    elif a_tpu >= 3 and score_tpu>50 and t_traj_mm['t_tp']  <=  2*tps_traj and self.orig_dess.loc[self.orig_dess.id_true == t_traj_mm['oid'], 'tpu'].values == 1 and self.dest_dess.loc[self.dest_dess.id_true == t_traj_mm['did'], 'tpu'].values == 1:
      reco_dt = 'tpu'
    elif a_marc >= 3 and t_traj_mm['t_velo']  <=  5:
      reco_dt = 'marche'
    elif a_velo >= 3 and score_velo>50 and t_traj_mm['t_velo']  <=  2*tps_traj and t_traj_mm['t_velo']  <=  15:
      reco_dt = 'velo'
    elif a_velo >= 3 and score_velo>50 and t_traj_mm['t_velo']  <=  2*tps_traj and t_traj_mm['t_velo']  <=  40:
      reco_dt = 'vae'
    elif a_train >= 3 and a_voit >= 3 and score_train>50 and self.dest_dess.loc[self.dest_dess.id_true == t_traj_mm['did'], 'train'].values == 1:
      reco_dt = 'inter'
    elif a_voit >= 3 and score_covoit>50:
      reco_dt = 'covoit'
    elif a_voit >= 3 or a_moto >= 3 and score_elec>50:
      reco_dt = 'elec'
    else:
      reco_dt = 'orga'
    
    if fm_dt_voit == 0 and fm_dt_moto == 0 and tx_trav-tx_tele>0:
      if fm_dt_velo/(tx_trav-tx_tele) > 0.5:
        reco_dt = "velo"
      elif fm_dt_tpu/(tx_trav-tx_tele) > 0.5:
        reco_dt = "tpu"
      elif fm_dt_train/(tx_trav-tx_tele) > 0.5:
        reco_dt = "train"
    return reco_dt, scores
  
  def compute_reco_multi(self, t_traj_mm, tps_traj, constraints, fm_dt_voit, fm_dt_moto, fm_dt_tpu, fm_dt_train, fm_dt_velo, fm_dt_march, fm_dt_inter,
                      a_voit, a_moto, a_tpu, a_train, a_velo, a_marc, i_tmps, i_prix, i_flex, i_conf, i_fiab, i_prof, i_envi):
    """input:frequences modales domicile-travail, attitudes envers modes, importance de differents aspects;
    output: recommandations de mobilite durable pour le deplacement domicile-travail de l'employe.e"""
    sum_importance = i_tmps + i_prix + i_flex + i_conf + i_fiab + i_prof + i_envi
    score_marche = 50 + 2*a_marc + 2*fm_dt_march
    score_velo = round(15*(i_tmps*1 + i_prix*5 + i_flex*4 + i_conf*1 + i_prof*1 + i_fiab*4 + i_envi*5)/sum_importance) + 2*a_velo + 2*fm_dt_velo
    score_vae = round(15*(i_tmps*3 + i_prix*3 + i_flex*4 + i_conf*1 + i_prof*1 + i_fiab*4 + i_envi*5)/sum_importance) + a_velo + a_moto + fm_dt_velo + fm_dt_moto
    score_tpu = round(15*(i_tmps*3 + i_prix*4 + i_flex*2 + i_conf*2 + i_prof*4 + i_fiab*2 + i_envi*4)/sum_importance) + 2*a_tpu + 2*fm_dt_tpu
    score_train = round(15*(i_tmps*3 + i_prix*1 + i_flex*2 + i_conf*3 + i_prof*5 + i_fiab*3 + i_envi*4)/sum_importance) + 2*a_train + 2*fm_dt_train
    score_covoit = round(15*(i_tmps*4 + i_prix*3 + i_flex*2 + i_conf*4 + i_prof*4 + i_fiab*2 + i_envi*2)/sum_importance) + 2*a_voit + 2*fm_dt_voit
    score_elec = round(15*(i_tmps*4 + i_prix*1 + i_flex*5 + i_conf*5 + i_prof*1 + i_fiab*4 + i_envi*1)/sum_importance) + 2*a_voit + 2*fm_dt_voit
    score_inter = round(15*(i_tmps*4 + i_prix*2 + i_flex*3 + i_conf*4 + i_prof*3 + i_fiab*3 + i_envi*2)/sum_importance) + a_train + a_voit + fm_dt_train + fm_dt_voit + 2 * fm_dt_inter
    scores = {'marche':score_marche,'velo':score_velo, 'vae':score_vae, 'tpu':score_tpu, 'train':score_train, 'covoit':score_covoit, 'elec':score_elec, 'inter':score_inter}

    can_train = 0
    can_tpu = 0
    can_walk = 0
    can_bike = 0
    can_vae = 0
    can_inter = 0
    can_elec = 0
    can_covoit = 0
    if t_traj_mm['t_tp']  <=  2*tps_traj and self.orig_dess.loc[self.orig_dess.id_true == t_traj_mm['oid'], 'train'].values == 1 and self.dest_dess.loc[self.dest_dess.id_true == t_traj_mm['did'], 'train'].values == 1:
      can_train = 1
    if t_traj_mm['t_tp']  <=  2*tps_traj and self.orig_dess.loc[self.orig_dess.id_true == t_traj_mm['oid'], 'tpu'].values == 1 and self.dest_dess.loc[self.dest_dess.id_true == t_traj_mm['did'], 'tpu'].values == 1:
      can_tpu = 1
    if t_traj_mm['t_velo']  <=  6 and "disabled" not in constraints and "heavy" not in constraints:
      can_walk = 1
    if t_traj_mm['t_velo']  <=  2*tps_traj and t_traj_mm['t_velo']  <=  18 and "disabled" not in constraints and "heavy" not in constraints:
      can_bike = 1
    if t_traj_mm['t_velo']  <=  2*tps_traj and t_traj_mm['t_velo']  <=  60 and "disabled" not in constraints and "heavy" not in constraints:
      can_vae = 1
    if self.orig_dess.loc[self.orig_dess.id_true == t_traj_mm['oid'], 'train'].values == 0 and self.dest_dess.loc[self.dest_dess.id_true == t_traj_mm['did'], 'train'].values == 1:
      can_inter = 1
    if len(constraints)==0 or constraints==["night"]:
      can_elec=0.7
      can_covoit=0.7
    elif constraints==["dependent"] or constraints==["heavy"]:
      can_elec=0.9
      can_covoit=0.7
    elif constraints==["disabled"]:
      can_elec=0.9
      can_covoit=0.9
    else:
      can_elec=1
      can_covoit=1
    access = {'marche':can_walk,'velo':can_bike, 'vae':can_vae, 'tpu':can_tpu, 'train':can_train, 'covoit':can_covoit, 'elec':can_elec, 'inter':can_inter}
    score_access = {'marche':can_walk * score_marche,'velo':can_bike * score_velo,'vae':can_vae * score_vae,'tpu':can_tpu * score_tpu,'train':can_train * score_train,'covoit':can_covoit * score_covoit,'elec':can_elec * score_elec,'inter':can_inter * score_inter}
    reco_multi = sorted(score_access, key=score_access.get, reverse=True)
    reco_dt2 = reco_multi[0:2]
    return reco_dt2, scores, access
  
  def compute_reco_pro(self, scores, pro_loc, pro_reg, pro_int, 
    fm_pro_loc_voit, fm_pro_loc_moto, fm_pro_loc_tpu, fm_pro_loc_train, fm_pro_loc_velo, fm_pro_loc_marc,
    fm_pro_reg_voit, fm_pro_reg_moto, fm_pro_reg_train, fm_pro_reg_avio,
    fm_pro_int_voit, fm_pro_int_train, fm_pro_int_avio):
    # init return values
    reco_pro_loc = ""
    reco_pro_reg = ""
    reco_pro_int = ""
    #deplacements pro portee locale
    if pro_loc:
      fr_pro_loc = fm_pro_loc_voit + fm_pro_loc_moto + fm_pro_loc_tpu + fm_pro_loc_train + fm_pro_loc_velo + fm_pro_loc_marc
      if fr_pro_loc > 0:
        if fm_pro_loc_marc == fr_pro_loc:
          reco_pro_loc = "marche"
        elif scores['velo']>55 or fm_pro_loc_velo/fr_pro_loc >= 0.5:
          reco_pro_loc = "velo"
        elif scores['tpu']>55 or fm_pro_loc_tpu/fr_pro_loc >= 0.5:
          reco_pro_loc = "tpu"
        elif scores['train']>55 or fm_pro_loc_train/fr_pro_loc >= 0.5:
          reco_pro_loc = "train"
        elif scores['elec']>55 or fm_pro_loc_voit/fr_pro_loc >= 0.5:
          reco_pro_loc = "elec"
      #else: 
        #reco_pro_loc = "global"
        # reco_pro_loc_ranked=[item for item in sorted(scores, key=scores.get, reverse=True) if item not in ['covoit','inter','marche']]
        # reco_pro_loc = reco_pro_loc_ranked[0]
    #deplacements pro portee regionale
    if pro_reg:
      fr_pro_reg = fm_pro_reg_voit + fm_pro_reg_moto + fm_pro_reg_train + fm_pro_reg_avio
      if fr_pro_reg > 0:
        if scores['train']>50 or fm_pro_reg_train/fr_pro_reg >= 0.5:
          reco_pro_reg = "train"
        elif scores['elec']>50 or fm_pro_reg_voit/fr_pro_reg >= 0.5:
          reco_pro_reg = "elec"
      #else:
        #reco_pro_reg = "global"
    #deplacements pro portee internationale
    if pro_int:
      if fm_pro_int_voit >= 1:
        if scores['train']>50 or fm_pro_int_train >= 1:
          reco_pro_int = "train"
        elif scores['elec']>50:
          reco_pro_int = "elec"
      if fm_pro_int_avio >= 1:
        if scores['train']>50 or fm_pro_int_train >= 1:
          reco_pro_int = "train"
    return reco_pro_loc, reco_pro_reg, reco_pro_int

  def compute_mesu_empl(self, empl, reco_dt2, reco_pro_loc, reco_pro_reg, reco_pro_int):
    # init return values
    mesure_dt1 = []
    mesure_dt2 = []
    mesure_pro_loc = []
    mesure_pro_regint = []
    if reco_dt2[0] == 'marche':
      mesure_dt1 = []
    elif reco_dt2[0] == 'velo':
      mesure_dt1 = empl['mesures_velo']
    elif reco_dt2[0] == 'vae':
      mesure_dt1 = empl['mesures_velo']
    elif reco_dt2[0] == 'tpu':
      if empl['mesures_tpu'] != []:
        mesure_dt1 = empl['mesures_tpu']
      else:
        mesure_dt1 = empl['mesures_train']
    elif reco_dt2[0] == 'train':
      if empl['mesures_train'] != []:
        mesure_dt1 = empl['mesures_train']
      else:
        mesure_dt1 = empl['mesures_tpu']
    elif reco_dt2[0] == 'inter':
      if empl['mesures_inter'] != []:
        mesure_dt1 = empl['mesures_inter']
      else:
        mesure_dt1 = empl['mesures_train']
    elif reco_dt2[0] == 'covoit':
      mesure_dt1 = empl['mesures_covoit']
    elif reco_dt2[0] == 'elec':
      mesure_dt1 = empl['mesures_elec']
    elif reco_dt2[0] == 'orga':
      mesure_dt1 = empl['mesures_globa']
    else:
      mesure_dt1 = reco_dt2[0]
        
    if reco_dt2[1] == 'marche':
      mesure_dt2 = []
    elif reco_dt2[1] == 'velo':
      mesure_dt2 = empl['mesures_velo']
    elif reco_dt2[1] == 'vae':
      mesure_dt2 = empl['mesures_velo']
    elif reco_dt2[1] == 'tpu':
      if empl['mesures_tpu'] != []:
        mesure_dt2 = empl['mesures_tpu']
      else:
        mesure_dt2 = empl['mesures_train']
    elif reco_dt2[1] == 'train':
      if empl['mesures_train'] != []:
        mesure_dt2 = empl['mesures_train']
      else:
        mesure_dt2 = empl['mesures_tpu']
    elif reco_dt2[1] == 'inter':
      if empl['mesures_inter'] != []:
        mesure_dt2 = empl['mesures_inter']
      else:
        mesure_dt2 = empl['mesures_train']
    elif reco_dt2[1] == 'covoit':
      mesure_dt2 = empl['mesures_covoit']
    elif reco_dt2[1] == 'elec':
      mesure_dt2 = empl['mesures_elec']
    elif reco_dt2[1] == 'orga':
      mesure_dt2 = empl['mesures_globa']
    else:
      mesure_dt2 = reco_dt2[1]
      
    if reco_pro_loc == 'marche':
      mesure_pro_loc = []
    elif reco_pro_loc == 'velo':
      mesure_pro_loc = empl['mesures_pro_velo']
    elif reco_pro_loc == 'tpu':
      if empl['mesures_pro_tpu'] != []:
        mesure_pro_loc = empl['mesures_pro_tpu']
      else:
        mesure_pro_loc = empl['mesures_pro_train']
    elif reco_pro_loc == 'train':
      if empl['mesures_pro_train'] != []:
        mesure_pro_loc = empl['mesures_pro_train']
      else:
        mesure_pro_loc = empl['mesures_pro_tpu']
    elif reco_pro_loc == 'elec':
      mesure_pro_loc = empl['mesures_pro_elec']
    if reco_pro_reg == 'train' or reco_pro_int == 'train':
      mesure_pro_regint = empl['mesures_pro_train']
    elif reco_pro_reg == 'elec' or reco_pro_int == 'elec':
      mesure_pro_regint = empl['mesures_pro_elec']
    return mesure_dt1, mesure_dt2, mesure_pro_loc, mesure_pro_regint

  def display_main_mode(self,fm_dt_voit, fm_dt_moto, fm_dt_tpu, fm_dt_train, fm_dt_velo,fm_dt_march, fm_dt_inter, mesure_dt1, mesure_dt2):
    main_mode=""
    fm={"the car":fm_dt_voit, "the motorbike":fm_dt_moto, "public transport":fm_dt_tpu, "the train":fm_dt_train, "the bicycle":fm_dt_velo,"walking":fm_dt_march,"intermodality":fm_dt_inter}
    main_mode=max(fm, key=fm.get)
    if fm_dt_inter == 1:
      text_a = "At present, you mainly use a combination of modes to get to your workplace."
    else:
      text_a = "At present, you mainly use " + main_mode + " to get to your workplace."
    if main_mode == "the car" or  main_mode == "the motorbike":
      text_b = "Based on the information you have entered, the following modes of transport are recommended for your commuting journey:"
    else:
      text_b = "Your commuting habits are already sustainable. The following alternatives are available to you for your commuting journey:"
    if mesure_dt1 != [] or mesure_dt2 != [] :
      text_c = "To promote sustainable mobility, your employer offers the following measures:"
    else:
      text_c = ""
    return text_a, text_b, text_c