import streamlit as st

def run():
    import pandas as pd
    import numpy as np
    import time
    import matplotlib.pyplot as plt

    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.metrics import (
        mean_absolute_error,
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        confusion_matrix
    )

    st.title("☁️ Urban Air Quality – Model Comparison System")

    # ==========================================
    # LOAD DATASET (Cached)
    # ==========================================
    @st.cache_data
    def load_data():
        return pd.read_csv("Air_quality_data.csv")

    df = load_data()

    required_cols = ["PM2.5", "CO", "NH3", "AQI"]
    if not all(c in df.columns for c in required_cols):
        st.error("Dataset must contain PM2.5, CO, NH3, AQI columns")
        st.stop()

    X = df[["PM2.5", "CO", "NH3"]]
    y = df["AQI"]

    # ==========================================
    # TRAIN MODELS ONLY ONCE (Cached)
    # ==========================================
    @st.cache_resource
    def train_models(X, y):

        lr_model = LinearRegression()

        rf_model = RandomForestRegressor(
            n_estimators=150,
            max_depth=10,
            min_samples_split=4,
            random_state=42
        )

        gb_model = GradientBoostingRegressor(
            n_estimators=1000,
            learning_rate=0.02,
            max_depth=6,
            subsample=0.85,
            min_samples_split=3,
            random_state=42
        )

        lr_model.fit(X, y)
        rf_model.fit(X, y)
        gb_model.fit(X, y)

        return lr_model, rf_model, gb_model

    lr_model, rf_model, gb_model = train_models(X, y)

    # ==========================================
    # COMPARE BUTTON
    # ==========================================
    if st.button("🚀 Compare Models"):

        with st.spinner("Running model evaluation..."):
            time.sleep(0.5)

            df["AQI_LR"] = lr_model.predict(X).round().astype(int)
            df["AQI_RF"] = rf_model.predict(X).round().astype(int)
            df["AQI_GB"] = gb_model.predict(X).round().astype(int)

            df["Error_LR"] = abs(df["AQI_LR"] - df["AQI"])
            df["Error_RF"] = abs(df["AQI_RF"] - df["AQI"])
            df["Error_GB"] = abs(df["AQI_GB"] - df["AQI"])

            mae_lr = mean_absolute_error(y, df["AQI_LR"])
            mae_rf = mean_absolute_error(y, df["AQI_RF"])
            mae_gb = mean_absolute_error(y, df["AQI_GB"])

        # ==========================================
        # MAE TABLE
        # ==========================================
        st.subheader("📊 Model Performance (MAE)")

        perf_df = pd.DataFrame({
            "Model": ["Linear Regression", "Random Forest", "Gradient Boosting"],
            "MAE": [mae_lr, mae_rf, mae_gb]
        })

        st.dataframe(perf_df)

        # ==========================================
        # BAR PLOT
        # ==========================================
        st.subheader("📊 MAE Comparison Bar Plot")

        fig_bar, ax_bar = plt.subplots()
        ax_bar.bar(perf_df["Model"], perf_df["MAE"])
        ax_bar.set_title("Mean Absolute Error Comparison")
        ax_bar.set_ylabel("MAE")
        st.pyplot(fig_bar)

        # ==========================================
        # LINE PLOT
        # ==========================================
        st.subheader("📈 Sample-wise Absolute Error (First 50 Records)")

        sample_df = df.head(50)

        fig_line, ax_line = plt.subplots()
        ax_line.plot(sample_df["Error_LR"], label="Linear Regression")
        ax_line.plot(sample_df["Error_RF"], label="Random Forest")
        ax_line.plot(sample_df["Error_GB"], label="Gradient Boosting")

        ax_line.set_title("Absolute Error Comparison")
        ax_line.set_xlabel("Sample Index")
        ax_line.set_ylabel("Absolute Error")
        ax_line.legend()

        st.pyplot(fig_line)

        # ==========================================
        # CLASSIFICATION SECTION (Balanced)
        # ==========================================
        st.markdown("---")
        st.header("📊 Classification Performance (Balanced Classes)")

        # 🔥 Percentile-based thresholds to avoid class imbalance
        low_thresh = np.percentile(df["AQI"], 33)
        mid_thresh = np.percentile(df["AQI"], 66)

        def create_class_label(aqi):
            if aqi <= low_thresh:
                return 0
            elif aqi <= mid_thresh:
                return 1
            else:
                return 2

        actual_class = df["AQI"].apply(create_class_label)
        pred_class_lr = df["AQI_LR"].apply(create_class_label)
        pred_class_rf = df["AQI_RF"].apply(create_class_label)
        pred_class_gb = df["AQI_GB"].apply(create_class_label)

        def evaluate(y_true, y_pred):
            return [
                accuracy_score(y_true, y_pred),
                precision_score(y_true, y_pred, average="macro"),
                recall_score(y_true, y_pred, average="macro"),
                f1_score(y_true, y_pred, average="macro")
            ]

        classification_df = pd.DataFrame({
            "Metric": ["Accuracy", "Precision", "Recall", "F1 Score"],
            "Linear Regression": evaluate(actual_class, pred_class_lr),
            "Random Forest": evaluate(actual_class, pred_class_rf),
            "Gradient Boosting": evaluate(actual_class, pred_class_gb)
        })

        st.dataframe(classification_df)

        # ==========================================
        # CONFUSION MATRIX (Balanced)
        # ==========================================
        st.subheader("📉 Confusion Matrix - Gradient Boosting")

        cm = confusion_matrix(actual_class, pred_class_gb)

        fig_cm, ax_cm = plt.subplots()
        ax_cm.imshow(cm)

        ax_cm.set_title("Gradient Boosting Confusion Matrix")
        ax_cm.set_xlabel("Predicted")
        ax_cm.set_ylabel("Actual")

        for i in range(len(cm)):
            for j in range(len(cm)):
                ax_cm.text(j, i, cm[i, j],
                           ha="center", va="center")

        ax_cm.set_xticks([0, 1, 2])
        ax_cm.set_yticks([0, 1, 2])
        ax_cm.set_xticklabels(["Good", "Moderate", "Unhealthy"])
        ax_cm.set_yticklabels(["Good", "Moderate", "Unhealthy"])

        st.pyplot(fig_cm)

        st.success("Confusion matrix generated ")
