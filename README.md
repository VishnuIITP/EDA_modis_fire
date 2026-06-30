# 🔥 EDA on MODIS Fire Dataset (India, 2024)

This repository contains **Exploratory Data Analysis (EDA)** on the MODIS fire dataset for India (2024), sourced from **NASA FIRMS**.  
The goal is to understand fire detection patterns, reliability, and severity using satellite data.

---

## 📂 Files
- **eda_modis_fire.ipynb** → Jupyter Notebook with step‑by‑step EDA  
- **modis_2024_india.csv** → Dataset containing fire hotspot detections  

---

## 🔑 Dataset Overview
- **Source:** NASA FIRMS (MODIS Collection)  
- **Region:** India  
- **Year:** 2024  
- **Variables include:**  
  - Latitude & Longitude → fire location  
  - Brightness → fire pixel intensity  
  - Confidence → reliability of detection (low/nominal/high)  
  - FRP (Fire Radiative Power) → energy released by fire (MW)  
  - Satellite → Aqua or Terra  
  - Day/Night flag → detection time  
  - Acquisition date/time → when fire was observed  

---

## 🎯 Project Purpose
The analysis aims to:
- Inspect dataset structure and quality  
- Visualize fire detection patterns  
- Analyze confidence levels and FRP distribution  
- Compare Aqua vs Terra satellite detections  
- Highlight severe fire events and anomalies  

---

## 🚀 How to Use
1. Clone the repository:
   ```bash
   git clone https://github.com/VishnuIITP/EDA_modis_fire.git
