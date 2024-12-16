import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load the merged dataset
merged_shipping = pd.read_csv('..\dashboard\merged_shipping.csv')
merged_reviews = pd.read_csv('..\dashboard\merged_reviews.csv')

# --------------- Pertanyaan 1 ---------------
# Hitung waktu pengiriman aktual dan estimasi
merged_shipping['actual_delivery_days'] = (pd.to_datetime(merged_shipping['order_delivered_customer_date']) - pd.to_datetime(merged_shipping['order_purchase_timestamp'])).dt.days
merged_shipping['estimated_delivery_days'] = (pd.to_datetime(merged_shipping['order_estimated_delivery_date']) - pd.to_datetime(merged_shipping['order_purchase_timestamp'])).dt.days

# Hitung selisih antara aktual dan estimasi
merged_shipping['delivery_delay'] = merged_shipping['actual_delivery_days'] - merged_shipping['estimated_delivery_days']

# Plot histogram waktu pengiriman aktual dan estimasi
st.subheader('Distribusi Waktu Pengiriman Aktual dan Estimasi')
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(merged_shipping['actual_delivery_days'], kde=True, color='blue', label='Actual Delivery Days', ax=ax)
sns.histplot(merged_shipping['estimated_delivery_days'], kde=True, color='orange', label='Estimated Delivery Days', ax=ax)
plt.legend()
plt.title('Distribusi Waktu Pengiriman Aktual dan Estimasi')
plt.xlabel('Hari')
plt.ylabel('Frekuensi')
st.pyplot(fig)  # Digunakan untuk menampilkan plot di Streamlit
st.write("Grafik ini menunjukkan distribusi waktu pengiriman aktual dan estimasi. Waktu pengiriman aktual dihitung berdasarkan perbedaan antara tanggal pengiriman yang diterima oleh pelanggan dan tanggal pembelian. Waktu pengiriman estimasi dihitung berdasarkan perbedaan antara tanggal pengiriman yang diperkirakan dan tanggal pembelian.")

# Plot distribusi keterlambatan
st.subheader('Distribusi Keterlambatan Pengiriman')
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(merged_shipping['delivery_delay'], kde=True, color='red', ax=ax)
plt.title('Distribusi Keterlambatan Pengiriman')
plt.xlabel('Hari Keterlambatan')
plt.ylabel('Frekuensi')
st.pyplot(fig)  # Digunakan untuk menampilkan plot di Streamlit
st.write("Grafik ini menggambarkan distribusi keterlambatan pengiriman, yaitu selisih antara waktu pengiriman aktual dan estimasi. Keterlambatan positif menunjukkan pengiriman lebih lama dari estimasi, sedangkan keterlambatan negatif menunjukkan pengiriman lebih cepat dari estimasi.")

# Rata-rata keterlambatan per negara bagian penjual
st.subheader('Rata-Rata Keterlambatan Pengiriman per Negara Bagian')
delay_by_state = merged_shipping.groupby('seller_state')['delivery_delay'].mean().sort_values()

# Visualisasi rata-rata keterlambatan per negara bagian
fig, ax = plt.subplots(figsize=(12, 8))
delay_by_state.plot(kind='bar', color='purple', ax=ax)
plt.title('Rata-Rata Keterlambatan Pengiriman per Negara Bagian')
plt.xlabel('Negara Bagian')
plt.ylabel('Rata-Rata Keterlambatan (Hari)')
plt.xticks(rotation=45)
st.pyplot(fig)  # Digunakan untuk menampilkan plot di Streamlit
st.write("Bar chart ini menunjukkan rata-rata keterlambatan pengiriman berdasarkan negara bagian penjual. Negara bagian dengan rata-rata keterlambatan tinggi mungkin memerlukan perhatian lebih dalam hal pengelolaan logistik.")

# --------------- Pertanyaan 2 ---------------
# Hitung rata-rata skor ulasan per kategori
st.subheader('Rata-Rata Skor Ulasan per Kategori Produk')
avg_review_score = merged_reviews.groupby('product_category_name')['review_score'].mean().sort_values(ascending=False)

# Visualisasi rata-rata skor ulasan per kategori
fig, ax = plt.subplots(figsize=(14, 8))
avg_review_score.plot(kind='bar', color='green', ax=ax)
plt.title('Rata-Rata Skor Ulasan per Kategori Produk')
plt.xlabel('Kategori Produk')
plt.ylabel('Rata-Rata Skor Ulasan')
plt.xticks(rotation=90)
st.pyplot(fig)  # Digunakan untuk menampilkan plot di Streamlit
st.write("Bar chart ini menunjukkan rata-rata skor ulasan per kategori produk. Kategori dengan skor ulasan lebih tinggi menunjukkan kepuasan pelanggan yang lebih baik.")

# Plot boxplot skor ulasan berdasarkan kategori untuk 10 kategori teratas
st.subheader('Distribusi Skor Ulasan pada 10 Kategori Teratas')
top_categories = merged_reviews['product_category_name'].value_counts().head(10).index
fig, ax = plt.subplots(figsize=(12, 8))
sns.boxplot(data=merged_reviews[merged_reviews['product_category_name'].isin(top_categories)], 
            x='product_category_name', y='review_score', palette='Set3', ax=ax)
plt.title('Distribusi Skor Ulasan pada 10 Kategori Teratas')
plt.xlabel('Kategori Produk')
plt.ylabel('Skor Ulasan')
plt.xticks(rotation=45)
st.pyplot(fig)  # Digunakan untuk menampilkan plot di Streamlit
st.write("Boxplot ini menunjukkan distribusi skor ulasan pada 10 kategori produk teratas. Setiap box mewakili kuartil dan rentang skor ulasan, memberikan gambaran tentang variasi ulasan dalam kategori produk.")

# Korelasi atribut produk dengan skor ulasan
st.subheader('Korelasi Atribut Produk dengan Skor Ulasan')
product_attributes = ['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
correlation = merged_reviews[product_attributes + ['review_score']].corr()

# Visualisasi matriks korelasi
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
plt.title('Korelasi Atribut Produk dengan Skor Ulasan')
st.pyplot(fig)  # Digunakan untuk menampilkan plot di Streamlit
st.write("Heatmap ini menunjukkan korelasi antara atribut produk (berat, panjang, tinggi, lebar) dan skor ulasan. Korelasi yang tinggi menunjukkan bahwa atribut tertentu dapat mempengaruhi skor ulasan.")
