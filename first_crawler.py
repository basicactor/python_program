# ファイル操作
import glob
import csv

# データ処理・視覚化
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# クローラー関連
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# 解析
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering

# 日本酒ランキングのURL
FOLLOWRANK_URL = "http://www.sakeno.com/followrank/"

# クロール時の待ち時間
WAIT_TIME = 5

# 銘柄マスタの出力先
MEIGARA_MASTER_PATH = ""

# 銘柄評価スコアの出力先ディレクトリ
MEIGARA_SCORE_DIR = ""

# 銘柄コメントの出力先ディレクトリ
MEIGARA_COMMENTS_DIR = ""

# TFIDF スコア算出後の結果出力先
TFIDF_PATH = ""
# クラスタリング結果の結果出力先
CLUSTER_PATH =""