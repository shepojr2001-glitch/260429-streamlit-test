import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

st.set_page_config(
    page_title="타이타닉 생존확률 예측 앱",
    layout="wide"
)

st.title("타이타닉 생존확률 예측 실습")
st.write("승객 정보를 입력하면 머신러닝 모델이 생존확률을 예측합니다.")


# 1. 데이터 로드

@st.cache_data
def load_data():
    df = sns.load_dataset("titanic")
    return df

raw_df=load_data()

# 2. 데이터 전처리 함수


# "survived" : 생존 여부 (0 = 사망, 1 = 생존)
# ,"pclass" : 티켓 클래스 (1 = 1st, 2 = 2nd, 3 = 3rd)
# ,"sex" : 성
# ,"age" : 나이
# ,"sibsp" : 형제자매/배우자 수
# ,"parch" : 부모자식간
# ,"fare" : 운임료
# ,"embarked" : 승선한 항구 (C = Cherbourg, Q = Queenstown, S = Southampton)
    

def preprocess_data(df):
    df = df[["survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]].copy()
    df["age"] = df["age"].fillna(df["age"].median())
    df["fare"] = df["fare"].fillna(df["fare"].median())
    df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])
    df = pd.get_dummies(df, columns=["sex", "embarked"], drop_first=True)
    return df
df = preprocess_data(raw_df)

# 3. 사이드바

menu=st.sidebar.radio("메뉴 선택"
                          ,["데이터 보기","시각화","모델 학습","생존확률 예측"]
                          )
# -----------------------------
# 4. 데이터 보기
# -----------------------------
if menu == "데이터 보기":
    st.subheader("원본 데이터")
    st.dataframe(raw_df.head(100), use_container_width=True)

    st.subheader("전처리된 데이터")
    st.dataframe(df.head(100), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("전체 승객 수", len(raw_df))
    col2.metric("생존자 수", int(raw_df["survived"].sum()))
    col3.metric("생존율", f"{raw_df['survived'].mean() * 100:.1f}%")

# -----------------------------
# 5. 시각화
# -----------------------------
elif menu == "시각화":
    st.subheader("타이타닉 데이터 시각화")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(
            raw_df,
            x="survived",
            title="생존 여부 분포",
            labels={"survived": "생존 여부"}
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.histogram(
            raw_df,
            x="sex",
            color="survived",
            barmode="group",
            title="성별 생존 분포"
        )
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig3 = px.histogram(
            raw_df,
            x="pclass",
            color="survived",
            barmode="group",
            title="객실 등급별 생존 분포"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = px.histogram(
            raw_df,
            x="age",
            color="survived",
            nbins=30,
            title="나이별 생존 분포"
        )
        st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# 6. 모델 학습
# -----------------------------       
elif menu == "모델 학습":
    st.subheader("머신러닝 모델 학습")

    X = df.drop("survived",axis=1)
    y = df["survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42, 
        stratify = y 
    )

    model_name = st.selectbox(
        "모델 선택",
        ["Logistic Regression", "Random Forest"]
    )

    if model_name == "Logistic Regression":
        model = LogisticRegression(max_iter=1000)
    else:
        model = RandomForestClassifier(n_estimators=100,
                                      random_state=42) 
       
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)        
    
    st.metric("모델 정확도", f"{accuracy * 100:.2f}%")

# -----------------------------
# 6.5. 변수 중요도
# -----------------------------

    st.write("학습 데이터 크기:", X_train.shape)
    st.write("테스트 데이터 크기:", X_test.shape)

    if model_name == "Random Forest":
        importance_df = pd.DataFrame({
            "feature": X.columns,
            "importance": model.feature_importances_
        }).sort_values("importance", ascending=False)

        st.subheader("변수 중요도")
        fig = px.bar(
            importance_df,
            x="feature",
            y="importance",
            title="생존 예측에 영향을 준 변수"
        )
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 7. 생존확률 예측
# -----------------------------
elif menu == "생존확률 예측":
    st.subheader("승객 정보 입력")

    X = df.drop("survived", axis=1)
    y = df["survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

# -----------------------------
# 8. 사용자 입력 UI
# -----------------------------

    col1, col2 = st.columns(2)

    with col1:
        pclass = st.selectbox("객실 등급", [1, 2, 3])
        sex = st.selectbox("성별", ["male", "female"])
        age = st.slider("나이", 0, 80, 30)
        fare = st.slider("요금", 0.0, 600.0, 50.0)

    with col2:
        sibsp = st.slider("형제/배우자 수", 0, 8, 0)
        parch = st.slider("부모/자녀 수", 0, 6, 0)
        embarked = st.selectbox("탑승 항구", ["S", "C", "Q"])

# -----------------------------
# 9. 입력값을 모델용 데이터로 변환
# -----------------------------
    input_data = pd.DataFrame([{
        "pclass": pclass,
        "age": age,
        "sibsp": sibsp,
        "parch": parch,
        "fare": fare,
        "sex_male": 1 if sex == "male" else 0,
        "embarked_Q": 1 if embarked == "Q" else 0,
        "embarked_S": 1 if embarked == "S" else 0
    }])

    input_data = input_data[X.columns]

# -----------------------------
# 10. 생존확률 계산
# -----------------------------
    if st.button("생존확률 계산"):
        survival_prob = model.predict_proba(input_data)[0][1]
        prediction = model.predict(input_data)[0]

        st.metric("예상 생존 확률", f"{survival_prob * 100:.2f}%")

        if prediction == 1:
            st.success("모델 예측 결과: 생존 가능성이 높습니다.")
        else:
            st.error("모델 예측 결과: 생존 가능성이 낮습니다.")

        st.write("입력 데이터")
        st.dataframe(input_data, use_container_width=True)        