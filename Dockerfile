# Python 3.11 slim görüntüsü kullanılarak temel imaj oluştur
FROM python:3.11-slim

# Çalışma dizinini belirle
WORKDIR /app

# Gereksinimler dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamanın tamamını kopyala
COPY . .

# Flask uygulamasını çalıştır
CMD ["flask", "run", "--host=0.0.0.0"]
