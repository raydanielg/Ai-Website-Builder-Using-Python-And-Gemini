import os
import google.generativeai as genai
from pathlib import Path

def setup_gemini():
    """Sanidi API na uhakikishe model inafanya kazi"""
    try:
        # Weka API key yako hapa au kwa environment variable
        api_key = "AIzaSyC2QQfB6Mc2-YMBYl-Wvn8CF2TuyDVP_WI"  # Badilisha na API key yako halisi
        genai.configure(api_key=api_key)
        
        # Pata model zinazopatikana
        available_models = [m.name for m in genai.list_models() 
                          if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            print("Hakuna model zinazopatikana kwa generateContent")
            return None
            
        # Chagua model ya kawaida (gemini-pro au ya kwanza kwenye orodha)
        model_name = "models/gemini-pro" if "models/gemini-pro" in available_models else available_models[0]
        print(f"Kutumia model: {model_name}")
        return genai.GenerativeModel(model_name)
    except Exception as e:
        print(f"Hitilafu ya usanidi: {e}")
        return None

def create_website(model):
    """Tengeneza tovuti kwa mujibu ya maagizo ya mtumiaji"""
    print("\nJaza maelezo ya tovuti unayotaka:")
    
    maelezo = {
        "madhumuni": input("1. Madhumuni ya tovuti (mfano: biashara, blog, portfolio): "),
        "huduma": input("2. Huduma unazohitaji (mfano: fomu, mauzo, picha): "),
        "lugha": input("3. Lugha ya tovuti (mfano: Swahili, English): "),
        "mtindo": input("4. Mtindo wa tovuti (mfano: kisasa, rangi nyingi, rahisi): "),
    }
    
    maagizo = f"""
    Tengeneza code kamili ya tovuti kwa:
    - Lugha: {maelezo['lugha']}
    - Madhumuni: {maelezo['madhumuni']}
    - Huduma: {maelezo['huduma']}
    - Mtindo: {maelezo['mtindo']}
    
    Toa:
    1. HTML ya msingi
    2. CSS ya mtindo
    3. JavaScript ya msingi (kama inahitajika)
    4. Maelekezo ya ufungaji
    """
    
    try:
        response = model.generate_content(maagizo)
        return response.text
    except Exception as e:
        print(f"Hitilafu wakati wa kutengeneza tovuti: {e}")
        return None

def save_website(content, folder="tovuti_yangu"):
    """Hifadhi faili za tovuti"""
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        with open(f"{folder}/index.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"\nTovuti imehifadhiwa katika folda '{folder}'")
        print(f"Fungua {folder}/index.html kwa browser yako")
    except Exception as e:
        print(f"Hitilafu wakati wa kuhifadhi: {e}")

def main():
    print("\nMradi wa Tengeneza Tovuti kwa Gemini API")
    
    # Sanidi model
    model = setup_gemini()
    if not model:
        print("Imeshindwa kuanzisha model. Hakikisha API key yako ni sahihi.")
        return
    
    # Tengeneza tovuti
    tovuti = create_website(model)
    if not tovuti:
        print("Imeshindwa kutengeneza tovuti")
        return
    
    # Hifadhi tovuti
    save_website(tovuti)
    
    print("\nUmekamilika! Tovuti yako imetengenezwa.")

if __name__ == "__main__":
    main()