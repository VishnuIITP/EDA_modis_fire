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

 ## Installation

i). **Clone the Repository**
   ```bash
   git clone https://github.com/VishnuIITP/EDA_modis_fire.git
   cd EDA_modis_fire
   ```

ii). **Set Up Python Environment**
   - Install Python 3.9 or higher.
   - (Optional but recommended) Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate   # Linux/Mac
     venv\Scripts\activate      # Windows
     ```

iii). **Install Dependencies**
   - Install required libraries:
     ```bash
     pip install -r requirements.txt
     ```
   - Typical dependencies include:
     - pandas  
     - numpy  
     - matplotlib  
     - seaborn  
     - scikit-learn

iv0. **Verify Installation**
   - Run a quick check:
     ```bash
     python eda.py
     ```
   - If everything is installed correctly, plots and results will be generated in the `results/` folder.

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

1. **Clone the Repository**
   ```bash
   git clone https://github.com/VishnuIITP/EDA_modis_fire.git
   cd EDA_modis_fire

   ```
2. **Set Up Python Environment**
Install Python 3.9 or higher.

(Optional but recommended) Create a virtual environment:
 ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows
```
3. **Install Dependencies**

Use the requirements.txt file to install all required libraries:
```bash
    pip install -r requirements.txt

```
4. **Run the Notebook**

Launch Jupyter Notebook:
```bash
   jupyter notebook eda_modis_fire.ipynb

```

5. **Check Outputs**

Preprocessed dataset will be saved as:
```bash
   cleaned_fire_data.csv

```