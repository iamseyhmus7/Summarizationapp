from flask import Flask, request, render_template, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("arayüz.html")

# Yerel ve Tokenizer Yolları
model_path = "Summarization_model"
tokenizer_path = "Summarization_tokenizer"

try:
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
except Exception as e:
    raise RuntimeError(f"Model veya Tokenizer yüklenirken bir hata oluştu: {e}")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_text = data.get("text")

        if not input_text:
            return jsonify({'Error': "Bir giriş sağlanmadı"})

        # Metni özetleme işlemleri
        # encode fonksiyon, girdi metnini modelin anlayabileceği bir formata dönüştürür. 
        # Bu dönüşüm, metni sayılardan oluşan bir diziye (token) dönüştürmeyi içerir.
        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)
        # generate fonksiyon, modelin verilen girdilerden bir özet üretmesini sağlar.
        summary_ids = model.generate(inputs, max_length=500, min_length=200, length_penalty=2.0, num_beams=4, early_stopping=True)
        # decode fonksiyon, modelden alınan özet tokenlerini (sayılardan oluşan diziyi) anlamlı metne dönüştürür.
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify({"Summary": summary})
    except Exception as e:
        return jsonify({"Error": str(e)})
    
if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)

