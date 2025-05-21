import re
import streamlit as st
import requests
from groq_api import generate_with_groq


# 1) Sayfa Konfigürasyonu
st.set_page_config(page_title="AI İçerik Planlayıcı", layout="centered")

# 2) Arayüz Başlığı
st.title("🧠 AI İçerik Planlayıcı (Groq API)")
st.markdown(
    "Bir konu gir, sana **başlık**, **alt başlıklar**, **anahtar kelimeler** ve **kaynak önerileri** üreten sistem."
)

# 3) Kullanıcıdan konu al
konu = st.text_input("📝 Konun ne olsun?", placeholder="Örn: Yapay Zeka ile Eğitim")

# 4) Butona basıldığında çalışacak akış
if st.button("İçerik Önerisi Üret") and konu:
    with st.spinner("Groq AI içerik önerisi üretiyor..."):
        # Prompt hazırlama
        prompt = (
            f"Aşağıda bir içerik planı örneği var. Tam olarak bu formatta ve Türkçe karakterleri eksiksiz kullanarak, "
            f"{konu} konusu için 4 madde oluştur.\n\n"
            "Örnek:\n"
            "1. İçerik Başlığı: Eğitimde Yapay Zeka Kullanımı\n"
            "2. Alt Başlıklar:\n"
            "   - Öğrenme Analitiği\n"
            "   - Kişiselleştirilmiş Öğrenme\n"
            "3. Anahtar Kelimeler: yapay zeka, eğitim teknolojileri, kişiselleştirme\n"
            "4. Kaynak Önerileri:\n"
            "   - “Artificial Intelligence in Education” (Kitap)\n"
            "   - https://edtech.example.com\n\n"
            "Lütfen yalnızca bu formatta ve Türkçe karakterleri (ç, ğ, ı, İ, ö, ü, ş) doğru kullanarak cevap ver.\n"
            "1. İçerik Başlığı: …\n"
            "2. Alt Başlıklar:\n"
            "   - …\n"
            "3. Anahtar Kelimeler: …\n"
            "4. Kaynak Önerileri:\n"
            "   - …\n"
        )
        try:
            raw_plan = generate_with_groq(prompt).strip()
        except Exception as e:
            st.error(f"Groq API hatası: {e}")
            st.stop()

    # 5) Ham çıktıyı göster (debug amaçlı)
    pattern = re.compile(r"(\d+)\.\s+([^\n]+)(?:\n((?:\s{3,}- .+\n?)*))?")
    matches = pattern.findall(raw_plan)


    # 6) Çıktıdan bölümleri ayır
    plan_dict = {}
    for match in matches:
        num = match[0]
        title = match[1].strip()
        content_block = match[2].strip() if match[2] else ""
        full_content = f"{title}\n{content_block}".strip()
        plan_dict[num] = full_content

    # 7) Bölümleri ekrana yazdır
    st.subheader("📋 İçerik Planı")

    if not plan_dict:
        st.warning("İçerik planı ayrıştırılamadı. Ham çıktıyı kontrol et.")
    else:
        # Başlık
        st.markdown("### 🎯 **İçerik Başlığı**")
        st.success(plan_dict.get("1", "Belirtilmedi"))

        # Alt Başlıklar
        st.markdown("### 🧩 **Alt Başlıklar**")
        alt_basliklar = plan_dict.get("2", "").split("- ")
        for item in alt_basliklar:
            item = item.strip()
            if item:
                st.markdown(f"- {item}")

        # Anahtar Kelimeler
        st.markdown("### 🗝️ **Anahtar Kelimeler**")
        anahtarlar = plan_dict.get("3", "")
        st.markdown(
            f"<div style='background-color:#f0f2f6; padding:12px; border-radius:8px; color:#222222; font-weight:bold;'>"
            f"{anahtarlar}"
            f"</div>",
            unsafe_allow_html=True
        )

        

        # Kaynaklar
        st.markdown("### 📚 **Kaynak Önerileri**")
        kaynaklar = plan_dict.get("4", "").split("- ")
        for kaynak in kaynaklar:
            kaynak = kaynak.strip()
            if kaynak:
                st.markdown(f"- {kaynak}")