import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime
import requests

import os
from dotenv import load_dotenv

from streamlit_image_coordinates import streamlit_image_coordinates

value = streamlit_image_coordinates("aaa .JPG")

st.write(value)
st.set_page_config(page_title="مركز المراقبة والتحكم  - الرياض", layout="wide")

st.title("🚦 مركز المراقبة والتحكم الرياض ")
st.markdown(f"**التاريخ والوقت:** {datetime.now().strftime('%d/%m/%Y %H:%M')} - الرياض")

# === حالة الطقس الحية ===
st.header("🌤️ حالة الطقس الحية في الرياض")

@st.cache_data(ttl=300)
def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=24.7136&longitude=46.6753&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,weather_code&timezone=Asia/Riyadh"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['current']
        return {
            "درجة الحرارة": data['temperature_2m'],
            "الرطوبة": data['relative_humidity_2m'],
            "سرعة الرياح": data['wind_speed_10m'],
            "هطول الأمطار": data['precipitation'],
            "الوصف": {0: "صافية", 1: "غائم جزئيًا", 61: "أمطار خفيفة", 80: "أمطار غزيرة"}.get(data['weather_code'], "غير معروف")
        }
    return None

weather = get_weather()

if weather:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("درجة الحرارة", f"{weather['درجة الحرارة']} °C")
    col2.metric("الرطوبة", f"{weather['الرطوبة']}%")
    col3.metric("سرعة الرياح", f"{weather['سرعة الرياح']} كم/س")
    col4.metric("هطول الأمطار", f"{weather['هطول الأمطار']} مم")

    st.info(f"**الوصف:** {weather['الوصف']}")

    # تنبيهات طقس
    alerts = []
    if weather['هطول الأمطار'] > 2: alerts.append("🟠 أمطار حالياً - حذر على الطرق")
    if weather['سرعة الرياح'] > 50: alerts.append("🟠 رياح قوية")
    if weather['درجة الحرارة'] > 40: alerts.append("🔥 حرارة شديدة")
    if alerts:
        st.warning("\n".join(alerts))
    else:
        st.success("✅ ظروف طقس آمنة")

# === إحصائيات الكاميرات والشاشات ===
st.header("📊 إحصائيات الأجهزة")
data_pie1 = pd.DataFrame({'حالة': ['متصل', 'غير متصل'], 'نسبة': [94, 6]})
data_pie2 = pd.DataFrame({'حالة': ['متصل', 'غير متصل'], 'نسبة': [86, 14]})
data_pie3 = pd.DataFrame({'حالة': ['متصل', 'غير متصل'], 'نسبة': [557, 14]})

col_p1, col_p2, col_p3, col_p4, col_p5, col_p6 = st.columns(6)
with col_p1:
    st.metric("كاميرات جديدة", "557")
    fig1 = px.pie(data_pie1, values='نسبة', names='حالة', hole=0.6, color_discrete_sequence=['blue', 'orange'])
    fig1.update_traces(textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

with col_p2:
    st.metric("شاشات إلكترونية", "96")
    fig2 = px.pie(data_pie2, values='نسبة', names='حالة', hole=0.6, color_discrete_sequence=['blue', 'orange'])
    fig2.update_traces(textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

with col_p3:
    st.metric("لوحات اسكادا ", "63")
    fig2 = px.pie(data_pie3, values='نسبة', names='حالة', hole=0.6, color_discrete_sequence=['blue', 'orange'])
    fig2.update_traces(textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

# === تنبيهات حركة المرور والحوادث ===
st.header("🚗 حالة الازدحام والحوادث")
congestion = 28  # من TomTom حالياً (يمكن أتمتة)
st.metric("مستوى الازدحام", f"{congestion}%")

if congestion > 50:
    st.error("🚨 ازدحام شديد!")
else:
    st.success("✅ حركة مرور سلسة")

st.subheader("🚨 حوادث مرورية حالية")
incidents = []  # لا حوادث اليوم
if incidents:
    st.error(f"تم رصد {len(incidents)} حادث!")
else:
    st.success("✅ لا حوادث مرورية خطيرة حالياً")

# === الخريطة ===
st.header("🗺️ خريطة المراقبة مع رادار الأمطار")
m = folium.Map(location=[24.7136, 46.6753], zoom_start=11)

folium.TileLayer(
    tiles=f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={"e29134605a18dff8e1b9a6ba7c946899"}",
    attr="OpenWeatherMap",
    name="رادار الأمطار",
    overlay=True,
    opacity=0.6
).add_to(m)

folium.LayerControl().add_to(m)
st_folium(m, width=1200, height=600)
st.components.v1.iframe(
    "https://embed.windy.com/embed2.html?lat=24.7&lon=46.6&zoom=6&level=surface&overlay=wind",
    height=600
)
st.components.v1.iframe(
    "https://app.powerbi.com/reportEmbed?reportId=9103dc5e-9f41-48f4-9a7c-a85ae159f691&autoAuth=true&ctid=e4396007-25d4-437c-895d-c317ddb4a259",
    height=600
)
st.components.v1.iframe("https://www.tomtom.com/traffic-index/riyadh-traffic/"

, height=800
)
# ────────────────────────────────────────────────
#               إعداداتك الشخصية
# ────────────────────────────────────────────────
TOMTOM_API_KEY = "j4n4vVb6lgR3Negs76yB8NDXfpa0MJI9"  # غيّرها بمفتاحك الحقيقي

# أمثلة نقاط في الرياض (يمكنك إضافة المزيد)
LOCATIONS = {
    "الملقا → المطار": {"start": "24.8200,46.6300", "end": "24.9570,46.6988"},
    "برج المملكة → طريق الملك فهد شمال": {"start": "24.7119,46.6744", "end": "24.820,46.630"},
    "النسيم → وسط الرياض": {"start": "24.650,46.780", "end": "24.7136,46.6753"},
    "الدائري الشرقي": {"start": "24.650,46.780", "end": "24.750,46.850"},
}

# عتبة التحذير (يمكن تعديلها)
WARNING_DELAY_MIN = 10          # تأخير أكثر من 10 دقائق → تحذير
WARNING_CONGESTION_RATIO = 1.5  # زحام أكثر من 1.5 ضعف السرعة الحرة

st.set_page_config(page_title="حالة المرور في الرياض", layout="wide")

# ────────────────────────────────────────────────
st.title("🛣️ مراقب الازدحام المروري في الرياض (TomTom)")
st.markdown(f"**التاريخ والوقت الحالي**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# تحديث تلقائي (بالمتصفح) كل 5 دقائق — يمكن تعطيله عبر الـ checkbox
AUTO_REFRESH_SEC = 100  # 5 دقائق
if st.checkbox("تفعيل التحديث التلقائي كل 5 دقائق", value=True):
    st.markdown(f'<meta http-equiv="refresh" content="{AUTO_REFRESH_SEC}">', unsafe_allow_html=True)
    st.caption(f"التطبيق سيعيد تحميل الصفحة كل {AUTO_REFRESH_SEC//60} دقيقة.")

# ────────────────────────────────────────────────
# اختيار الطريق
route_name = st.selectbox("اختر الطريق / المسار", list(LOCATIONS.keys()))
points = LOCATIONS[route_name]
start = points["start"]
end   = points["end"]

# جلب البيانات فورًا عند تحميل الصفحة (التحديث اليدوي يعيد تحميل الصفحة)
if st.button("تحديث يدوي", key="refresh"):
    st.experimental_rerun()

with st.spinner("جاري جلب بيانات الزحام من TomTom..."):
    # ───── Routing API مع traffic=true ─────
    departAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    url = (
        f"https://api.tomtom.com/routing/1/calculateRoute/{start}:{end}/json?"
        f"key={TOMTOM_API_KEY}&traffic=true&departAt={departAt}&travelMode=car"
    )

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        route = data["routes"][0]
        summary = route["summary"]

        distance_km = summary["lengthInMeters"] / 1000
        travel_time_min = summary["travelTimeInSeconds"] / 60
        delay_min = summary.get("trafficDelayInSeconds", 0) / 60
        arrival_time = summary["arrivalTime"]
        congestion_ratio = (
            summary["travelTimeInSeconds"] / summary["noTrafficTravelTimeInSeconds"]
            if "noTrafficTravelTimeInSeconds" in summary else 1.0
        )

        # ───── عرض النتائج ─────
        col1, col2, col3 = st.columns(3)
        col1.metric("المسافة", f"{distance_km:.1f} كم")
        col2.metric("الوقت المتوقع", f"{travel_time_min:.0f} دقيقة")
        col3.metric("التأخير بسبب الزحام", f"{delay_min:.0f} دقيقة")

        st.subheader("حالة الزحام")
        st.progress(min(congestion_ratio / 3, 1.0))  # شريط تقدم (max ~3x)

        # تحذير
        if delay_min > WARNING_DELAY_MIN or congestion_ratio > WARNING_CONGESTION_RATIO:
            st.error(f"⚠️ **تحذير زحام شديد!** تأخير {delay_min:.0f} دقيقة (نسبة الزحام {congestion_ratio:.2f}x)")
            st.markdown("ننصح بتجنب هذا الطريق الآن أو البحث عن بديل.")
        else:
            st.success("✅ الطريق سالك نسبيًا، لا تأخير كبير.")

        st.caption(f"وقت الوصول المتوقع: {arrival_time}")

        # ───── عرض الخريطة مع المسار ─────
        st.subheader("الخريطة مع المسار")
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=11, tiles="cartodbpositron")

        # إضافة المسار (من نقاط الـ legs)
        points_list = []
        for leg in route["legs"]:
            for pt in leg["points"]:
                points_list.append((pt["latitude"], pt["longitude"]))

        if points_list:
            folium.PolyLine(points_list, color="blue", weight=6, opacity=0.8).add_to(m)
            folium.Marker(points_list[0], popup="البداية", icon=folium.Icon(color="green")).add_to(m)
            folium.Marker(points_list[-1], popup="النهاية", icon=folium.Icon(color="red")).add_to(m)

        st_folium(m, width=1000, height=500)

    except Exception as e:
        st.error("حدث خطأ عند جلب بيانات الزحام. تأكد من اتصال الإنترنت ومفتاح TomTom.")
        st.exception(e)


st.info("داشبوردأبا الخيل ـ `streamlit run traffic_dashboard.py`")