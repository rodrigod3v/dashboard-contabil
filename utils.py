import os
import json
import time
import pandas as pd
import streamlit as st

CACHE_DIR = "cache_data"
HISTORY_FILE = "upload_history.json"
OPTIONS_FILE = "options.json"
SETTINGS_FILE = "settings.json"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# --- History Management ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def save_uploaded_file(uploaded_file):
    # Saves file physically
    ext = os.path.splitext(uploaded_file.name)[1]
    if not ext:
        ext = ".csv" if uploaded_file.type == 'text/csv' else ".xlsx"
    
    # Unique name
    filename = f"{int(time.time())}_{uploaded_file.name}"
    file_path = os.path.join(CACHE_DIR, filename)

    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Update history
        history = load_history()
        # Remove duplicates by name (keeping newest)
        history = [h for h in history if h['original_name'] != uploaded_file.name]
        
        # Add to top
        history.insert(0, {
            "path": file_path,
            "original_name": uploaded_file.name,
            "timestamp": time.time()
        })
        
        # Keep only last 3
        if len(history) > 3:
            removed = history.pop()
            if os.path.exists(removed['path']):
                try:
                    os.remove(removed['path'])
                except:
                    pass
        
        save_history(history)
        return file_path
    except Exception as e:
        st.error(f"Erro ao salvar cache: {e}")
        return None

# --- Data Loading ---
def load_data(file_input):
    try:
        if isinstance(file_input, str):
            if file_input.endswith('.csv'):
                df = pd.read_csv(file_input)
            else:
                df = pd.read_excel(file_input)
        else:
            if file_input.name.endswith('.csv'):
                df = pd.read_csv(file_input)
            else:
                df = pd.read_excel(file_input)
        
        # Basic Preprocessing
        # Normalize column names (remove accents)
        rename_map = {
            'Responsável': 'Responsavel',
            'Inconsistências': 'Inconsistencias',
            'Situação': 'Status',
            'Estado': 'Status'
        }
        df.rename(columns=rename_map, inplace=True)

        if 'Dia' in df.columns:
            df['Dia'] = pd.to_datetime(df['Dia'], errors='coerce')
            
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None

# --- Options Management (for Editor) ---
def load_options():
    defaults = {
        "responsavel": [], 
        "inconsistencias": [],
        "status": ['Pendente', 'Resolvido', 'Em Análise', 'Cancelado']
    }
    
    if os.path.exists(OPTIONS_FILE):
        try:
            with open(OPTIONS_FILE, "r") as f:
                data = json.load(f)
                # Merge with defaults ensuring keys exist
                for key, val in defaults.items():
                    if key not in data:
                        data[key] = val
                return data
        except:
            return defaults
    return defaults

def save_options_file(data):
    with open(OPTIONS_FILE, "w") as f:
        json.dump(data, f)

# --- Settings Management ---
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_settings(s_name, s_email):
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"sheet_name": s_name, "email_share": s_email}, f)
