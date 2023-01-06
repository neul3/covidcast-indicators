"""Tests for eval_day.py"""
import mock
import pandas as pd
from delphi_utils.flash_eval.eval_day import (flash_eval_lag)
import math

def test_flash_input():
    "Simple test for main flash-eval method with known output."
    mock_logger = mock.Mock()
    input_df = pd.read_csv('flash_ref/test_input.csv', index_col=0, parse_dates=[0], header=0)
    flash_eval_lag(input_df,  [0, math.inf], 1, 'confirmed_incidence_num', mock_logger)
    mock_logger.info.assert_called_once_with('min_anomalies', payload='*2023-01-03 00:00:00* \n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,nh|*nh, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,ca|*ca, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,il|*il, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,va|*va, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,ky|*ky, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,mi|*mi, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,mo|*mo, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,ms|*ms, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,wv|*wv, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,nj|*nj, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,nm|*nm, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,pr|*pr, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,sc|*sc, 0.0*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,tx|*tx, 0.004084609773887673*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,ak|*ak, 0.016338439095550692*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,ks|*ks, 0.016338439095550692*>\n\t<https://ananya-joshi-visapp-vis-523f3g.streamlitapp.com/?params=2023-01_03,2023-01_04,wy|*wy, 0.016338439095550692*>\n', hits=17)